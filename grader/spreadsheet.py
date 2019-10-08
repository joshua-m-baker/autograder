import config
import xlrd

def getAllUsernames():
    usernames = []
    with open("allusernamesF19.txt") as names:
        for name in names:
            usernames.append(name.rstrip())
    return usernames

def getMyUsernames(graderName):
    wb = xlrd.open_workbook(config.GRADING_SPREADSHEET) 
    sheet = wb.sheet_by_index(0) 
    usernameColumn = 1 
    assignmentColumn = -1
    usernameList = []
    for col_index in range(sheet.ncols):
        cell = sheet.cell(0, col_index).value
        if cell == "Assignment{}".format(config.ASSIGNMENT_NUMBER):
            assignmentColumn = col_index
            break
    
    foundGrader = False
    for row in range(sheet.nrows):
        cell = sheet.cell(row, assignmentColumn).value
        if cell == graderName or (cell == '' and foundGrader):
            foundGrader = True
            usernameList.append(sheet.cell(row, usernameColumn).value)
        else:
            foundGrader = False

    return usernameList
