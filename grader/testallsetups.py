import setup
import githubcommands
import config
import spreadsheet
import subprocess   
import os
import csv

def main():

    setup.makeFolderIfMissing(config.REPOS_FOLDER)
    username_list = spreadsheet.getAllUsernames() #TODO prompt on no usernames written
    #githubcommands.setup_repos(username_list, config.REPO_URL_TEMPLATE, config.REPOS_FOLDER, config.STUDENT_REPO_PATH, config.DUE_DATE)

    with open("results.csv", "w") as res:
        writer = csv.writer(res, delimiter=",")
        writer.writerow(["username", "gitignore", "noCodeFolder", "assignment0", "helloworld", "syntax"])
        for name in username_list:
            base_path = config.join_path(config.STUDENT_REPO_PATH.format(name))
            a0path = config.join_path(base_path, "Assignment0")
            helloWorldRuns = False

            gitignoreExists = os.path.isfile(config.join_path(base_path, ".gitignore"))
            noCode = not os.path.isdir(config.join_path(base_path, ".vscode"))
            ass0Exists = os.path.isdir(a0path)
            helloWorldExists = os.path.isfile(config.join_path(a0path, "helloworld.py"))
            if helloWorldExists:
                try:
                    proc = subprocess.Popen("python3 helloworld.py", cwd=a0path, shell=True, stdout=subprocess.DEVNULL)
                    proc.wait()
                    helloWorldRuns = True
                except Exception as e:
                    pass    

            writer.writerow([name, gitignoreExists, noCode, ass0Exists, helloWorldExists, helloWorldRuns])

if __name__ == "__main__":
    main()