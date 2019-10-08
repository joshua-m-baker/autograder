"""
    Holds functions for bulk repo cloning and checkout
"""
import subprocess
import os
import io
import contextlib
import shutil

def setup_repos(username_list, repo_url_template, repos_dir, repo_path_template, due_date):
    printBuffer = io.StringIO()
    with contextlib.redirect_stdout(printBuffer): #suppress cloning print statements
        for name in username_list:
            dest = repo_path_template.format(name)
            clone_repo(name, repo_url_template, repos_dir, dest)
            checkout_repo(dest, due_date)
            print()
    fix_student_spelling_errors(repos_dir)

def clone_repo(username, repo_url_template, repos_dir, target_directory):
    # Don't reclone existing repos
    try:
        if not os.path.exists(target_directory):
            command = "git clone " + repo_url_template.format(username)
            proc = subprocess.Popen(command, cwd=repos_dir, shell=True, stdout=subprocess.DEVNULL)
            proc.wait() # This loses the async benefits, but ensures the repo is cloned before checking it out
    except Exception as e:
        print("Exception: {}".format(e))

def checkout_repo(path, date):
    try:
        cmd1 = 'git rev-list -n 1 --before="{0}" master'.format(date) # Credit to Larry Gates for the checkout command
        out, err = subprocess.Popen(cmd1, cwd=path, shell=True, stdout=subprocess.PIPE).communicate()
        commit_hash = out.decode("utf-8").rstrip() #windows returns this as a byte string for some godforsaken reason
        command = "git checkout -f {}".format(commit_hash) # Credit to Larry Gates for the checkout command

        return subprocess.Popen(command, cwd=path, shell=True, stdout=subprocess.PIPE).wait()
    except Exception as e:
        print("Exception: {}".format(e))

# Renames any folders in the target directory with spaces in their name to have no spaces
def fix_student_spelling_errors(repos_dir):
    #bad_repos = set() #prevent duplicates from being added, since os.walk might see the same folder more than once
    folders_to_move = set() #prevent duplicates from being added, since os.walk might see the same folder more than once
    for root, dirnames, _ in os.walk(repos_dir):
        for d in dirnames:
            if " " in d and not os.path.exists(root+"/"+d.replace(" ", "")): #make sure there isn't already a correct folder
                folders_to_move.add(root+"/"+d)
    if folders_to_move:
        print()
        print("!!! The following folders had spaces in them. I've removed the spaces, but makes sure to take off points for any misspelled assignment folders. !!!")
        print()
    for path in folders_to_move:
        dest = path.replace(" ", "")
        shutil.move(path, dest)
        #bad_repos.add(path.split("/")[2].split("-")[2])
        print(" - {}".format(path))

        with open(dest+"/"+"mispelling.txt", "w+") as f:
            f.write("This student spelled their assignment folder wrong. Make sure to take off points")
    print()

