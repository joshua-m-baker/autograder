import yaml

ASSIGNMENT_NUMBER = 4
DEADLINE_DICT = {0:"2019-10-31 23:00", 1:"2019-9-11 23:00", 2:"2019-9-18 23:00", 3:"2019-9-25 23:00", 4:"2019-10-02 23:00"}

def join_path(*args):
    return "/".join(map(str, args))

DUE_DATE = DEADLINE_DICT[ASSIGNMENT_NUMBER]
REPOS_FOLDER = "./repos" #Where student repos will be cloned to. Don't change
STUDENT_REPO_PATH = join_path(REPOS_FOLDER,"C200-Assignments-{}")
ASSIGNMENT_NAME = "Assignment{}".format(ASSIGNMENT_NUMBER)
TEMPLATE_PATH = "template.py"
TEMPLATE_FOLDER = join_path("AssignmentTemplates", ASSIGNMENT_NAME + ".yaml")

GRADING_SPREADSHEET = "MasterListAssignments.xlsx"

typoRE = "[asignmet\s]+{}\s?".format(ASSIGNMENT_NUMBER)


with open("config.yaml") as c:
    data = yaml.safe_load(c)

    USERNAME = data["username"]
    REPO_URL_TEMPLATE = "https://github.iu.edu/CSCI-C200-Fall-2019/C200-Assignments-{}.git"

    if data["clonetype"] == 'ssh':
        REPO_URL_TEMPLATE = "git@github.iu.edu:CSCI-C200-Fall-2019/C200-Assignments-{}.git"
