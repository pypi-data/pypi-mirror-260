import shutil
import os
import subprocess
import logging
import datetime
from git_user import GitUser

logger = logging.getLogger(__name__)

class GitException(Exception):
    "Raised when there is a git issue"
    pass

class GitRepo:
    def __init__(self,
                 url,
                 repo_dir,
                 user: GitUser = None,
                 branch = "master",
                 pull_replace_remote=True,
                 pull_replace_local=False):
        
        self.url = url
        self.repo_dir = repo_dir
        self.user: GitUser = user
        self.base_url = url
        self.branch = branch
        self.currently_committed = False
        self.pull_replace_local = pull_replace_local
        self.pull_replace_remote = pull_replace_remote

        if pull_replace_local == pull_replace_remote:
            raise ValueError("pull_replace_local AND pull_replace_remote cannot be set to the same value")

# private
    
    def _repo_exists(self):
        return os.path.exists(self.repo_dir)
    
    def _inject_credentials(self) -> str:
        return f'{self.url[:8]}{self.user.username}:{self.user.access_token}@{self.url[8:]}'


    def _run_git_cmd(self, cmd, exception_msg="") -> str:
        if type(cmd) is str:
            cmd = [cmd]
        cmd_start = ["git", "--git-dir", os.path.join(self.repo_dir, ".git"), "--work-tree", self.repo_dir]
        cmd_start.extend(cmd)
        run = subprocess.run(cmd_start, capture_output=True)
        if run.returncode != 0:
            if exception_msg == "":
                exception_msg = " ".join(cmd_start)
            logging.error(f"Got an error from a git command, info: \nreturn code: {run.returncode} \nstd_out: {run.stdout.decode()}")
            raise GitException(f"Code: {run.returncode}. Something went wrong when trying to execute git command: {exception_msg}\n{run.stdout.decode()}\n{run.stderr.decode()}")
        return run.stdout.decode()

    def _get_changed_contents(self):
        changed_files = [os.path.join(self.repo_dir, file) for file in self.get_file_changes(["M"])]
        changed_files_contents = []
        for file in changed_files:
            with open(file, "r") as f: changed_files_contents.append(f.read())
        return changed_files_contents, changed_files
    
    def _write_changed_contents(self, changed_files, changed_files_contents):
        for index, file in enumerate(changed_files):
            with open(file, "w") as f: f.write(changed_files_contents[index])

    def _update_repo(self):
        try:
            self._run_git_cmd("pull", exception_msg="pull")
        except GitException as e:
            if "Your local changes to the following files would be overwritten by merge" in str(e):
                print()
                if self.pull_replace_local:
                    self._stage_files()
                    self._run_git_cmd(["stash"])
                elif self.pull_replace_remote:
                    changed_files_contents, changed_files = self._get_changed_contents()
                    self._stage_files()
                    self._run_git_cmd(["stash"])
                    self._run_git_cmd(["pull"])
                    self._write_changed_contents(changed_files, changed_files_contents)
            else:
                logger.error("Looks like you commited changes before re-pulling, why?")
                raise e


    def _inject_credentials(self) -> str:
        return f'{self.url[:8]}{self.user.username}:{self.user.access_token}@{self.url[8:]}'

    def _first_pull(self):
        repo_with_credentials = self._inject_credentials()
        cmd = f"git clone --branch {self.branch} {repo_with_credentials} {self.repo_dir}"
        subprocess.call(cmd, shell=True)

    def _push(self) -> bool:
        self._run_git_cmd(["push"])
        return True
    
    # if files is empty it will stage all
    def _stage_files(self, files=[]):
        if type(files) is str:
            files = [files]
        args = ["-A"]
        if files:
            args = files
        cmd = ["add"]
        cmd.extend(args)
        self._run_git_cmd(cmd)


    def _commit(self, message="", allow_push_fix=False):
        if not message:
            current_date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            message = f"ceotr auto-commit: {current_date_str}"
        if len(message) > 50:
            logger.warning("git commit message too long, please keep it under 50 characters")
        commit_std = self._run_git_cmd(["commit","-m",message[:50]], exception_msg="commit")
        if "nothing to commit" in commit_std:
            logger.warning("Nothing to commit, working tree clean")
            return False
        elif "nothing added to commit but untracked files" in commit_std:
            logger.warning("untracked files found, try adding them first")
        else:
            return True

    def _pull(self):
        msg = self._update_repo()
        print(msg)

# public
        
    def init(self, overwrite: bool) -> None:
        '''
            Create or update the repo.
                Params:
                    overwrite: overwrite the current repo with a fresh clone.
        '''
        if overwrite and self._repo_exists():
            try:
                shutil.rmtree(self.repo_dir)
            except:
                print("WARN: Could not delete repo when trying to init")
        if not self._repo_exists():
            os.makedirs(self.repo_dir, exist_ok=True)

        else:
            current_branch = self._run_git_cmd(["branch", "--show-current"])
            if current_branch != self.branch:
                self.change_branch(self.branch)
            self._update_repo()
            return
        
        self._first_pull()
        self._run_git_cmd(["config","--local","user.name",self.user.username])
        self._run_git_cmd(["config","--local","user.email",self.user.email])

    def change_branch(self, branch: str) -> None:
        '''
            Change the branch.
                Params:
                    branch: the name of the branch to checkout to, needs to exist.
        '''

        try:
            self._run_git_cmd(["checkout", branch], exception_msg="changing branch")
        except Exception as e:
            if "did not match any file(s)" in str(e):
                raise GitException(f"Error: Cannot checkout to '{branch}'. Branch does not exist")
        self._update_repo()

    def get_file_changes(self, filter=[], clean_output=True) -> list: #DOESN'T WORK IF THE DIR HAS SPACES NEED FIX
        '''
            Get untracked file changes on the repo:
                Params:
                    clean_output: True - only return the file names. False - Return the character code with the file name
                    filter[]: A list of characters representing the files state
                Returns:
                    A list of filenames for untracked changes

                Character codes from the git manual:
                            X          Y     Meaning
                -------------------------------------------------
                    [AMD]   not updated
                M        [ MTD]  updated in index
                T        [ MTD]  type changed in index
                A        [ MTD]  added to index
                D                deleted from index
                R        [ MTD]  renamed in index
                C        [ MTD]  copied in index
                [MTARC]          index and work tree matches
                [ MTARC]    M    work tree changed since index
                [ MTARC]    T    type changed in work tree since index
                [ MTARC]    D    deleted in work tree
                        R    renamed in work tree
                        C    copied in work tree
                -------------------------------------------------
                D           D    unmerged, both deleted
                A           U    unmerged, added by us
                U           D    unmerged, deleted by them
                U           A    unmerged, added by them
                D           U    unmerged, deleted by us
                A           A    unmerged, both added
                U           U    unmerged, both modified
                -------------------------------------------------
                ?           ?    untracked
                !           !    ignored
                -------------------------------------------------

            Please use in a list, ex:   ["A", "D"]
                                        ["A"]
        '''
        status = self._run_git_cmd(["status", "--porcelain", "--untracked-files=all"])
        files: list = status.split("\n")[:-1] #emptyline at the end, last index is blank
        if files:
            if filter:
                files = [file for file in files if True in [True for substr in filter if substr in file]]
            if clean_output:
                files = [file.split(" ")[-1] for file in files]
        
        return files
    

    def save_and_upload(self, files: list = [], commit_message="") -> None:
        '''
            Stage, commit, and push changed files to the remote git repo.
                Params:
                    files: optional, a list of filenames to stage, if there are any filenames in this list, 
                            it will only stage those files to be commited and pushed.
                    commit_message: optional, the commit message.
        '''
        self._update_repo()
        if self.get_file_changes():
            self._stage_files(files=files)
            self._commit(commit_message)
            self._push()
        else:
            logger.info("No changed files")
    
