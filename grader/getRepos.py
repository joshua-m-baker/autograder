#!/usr/bin/env python3

"""
    Initial file to be run to clone repos and deploy test files
"""
import os, sys, re
import spreadsheet
import config
import githubcommands
import shutil

#Defaults to selecting proper assignment folder, but can be replaced with a misspelled folder.
def writeTestCodeToFolder(username, repoPath=config.STUDENT_REPO_PATH, folder=config.ASSIGNMENT_NAME, path_to_template=config.TEMPLATE_PATH):
    studentPath = config.join_path(repoPath.format(username), folder,"gradingTests.py")
    graderPath = os.path.abspath(os.path.dirname(__file__)) # path to the grader dir, not where the script was run

    with open(studentPath, "w+") as tests_file:
        #add the current folder temporarily to python path so stuff here can be imported elsewhere
        tests_file.write("""import sys\nsys.path.insert(0, r"{}")\n""".format(graderPath))
        #add a reference to the template folder so the test cases can be loaded
        tests_file.write("""TEMPLATE_FOLDER=r"{}"\n""".format(config.join_path(graderPath, config.TEMPLATE_FOLDER)))
        tests_file.write("""username='{}'\n""".format(username))
        with open(path_to_template, "r") as template:
            for line in template:
                tests_file.write(line.replace("\\n", os.linesep))

# Use RE defined in config.py
def findMisspelledAssignmentFolder(username, repo_path=config.STUDENT_REPO_PATH, regex=config.typoRE):
    for folder in os.listdir(config.join_path(repo_path.format(username))):
        if re.search(regex, folder):
            return folder
    return ""

def deployScriptForUsernames(usernamesList):
    for student in usernamesList:
        student = student.replace("\n", "")
        try:
            writeTestCodeToFolder(student)

        except Exception as e:
            try:
                #Use a regular expression to look for a misspelled folder
                misspelledFolder = findMisspelledAssignmentFolder(student)
                if misspelledFolder:
                    print("!!!!! Found folder with typo in name. Make sure to take off points for {} !!!!!".format(student))
                    writeTestCodeToFolder(student, folder=misspelledFolder)
                else:
                    print("No folder {} for {}. No tests generated.".format(config.ASSIGNMENT_NAME, student))
            except Exception as e:
                print("No tests generated because of exception: {}".format(e))

def banish_god_forsaken_code(file_path):
    bad_words = ["print(", "os.system", "input("] #comment lines out if they contain these things

    lines = []
    with open(file_path, "r") as student_file:
        for line in student_file.readlines():
            if re.match("^\w", line): #if the line is not indented 
                if any([word in line for word in bad_words]):
                    line = "# {}".format(line)
            lines.append(line)

    with open(file_path, "w") as fixed:
        fixed.writelines(lines)

def makeFolderIfMissing(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

def main():

    makeFolderIfMissing(config.REPOS_FOLDER)
    username_list = spreadsheet.getMyUsernames(config.USERNAME) #TODO prompt on no usernames written
    if not username_list:
        print("No usernames to grade found. Run setup.py if you haven't yet. If you have, the grading list might not have been updated yet.")

    githubcommands.setup_repos(username_list, config.REPO_URL_TEMPLATE, config.REPOS_FOLDER, config.STUDENT_REPO_PATH, config.DUE_DATE)
    deployScriptForUsernames(username_list)
    with open("usernames.txt", "w") as f:
        for name in username_list:
            f.write("{}\n".format(name))
    for name in username_list:
        assignment_path = config.join_path(config.STUDENT_REPO_PATH.format(name), config.ASSIGNMENT_NAME)
        try:
            for p in [f for f in os.listdir(assignment_path) if "py" in config.join_path(assignment_path, f)]:
                pass
                #banish_god_forsaken_code(config.join_path(assignment_path, p))
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
