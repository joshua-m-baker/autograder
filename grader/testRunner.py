import re
from os import listdir
from testcase import TestCase
from testcase import Status
from testcase import funcType
import sys, os, importlib, inspect, math, io, re
import yaml
from types import ModuleType
import contextlib

# Common imports for homework stuff
import numpy as np
import matplotlib

tests = {}
imports = {}
import_outputs = {}
filesToTest = []
classesToTest = []

def importTests(testFilePath):
    with open(testFilePath) as testFile:

        data = yaml.load(testFile, Loader=yaml.Loader)
        
        for fileName, objects in data.items():
            classTest = False
            #Unnest the functions from the class marker
            for k in objects.keys():
                nCLass = re.match(r'class\d', k)
                if fileName not in tests:
                    tests[fileName] = {}
                if nCLass:
                    classTest = True
                    loadFunctionDict(tests[fileName], objects[nCLass[0]], classTest)
                    filesToTest.append(fileName)
                else:
                    loadFunctionDict(tests[fileName], objects, classTest)
                    filesToTest.append(fileName)
                    break
    
def loadFunctionDict(target_dict, importedDict, isClassTest=False):
    '''
        Takes in a dictionary of the imported test values, mostly strings. Returns a dictionary of test class objects
    ''' 
    #testDict = {}
    classInit = ""
    if "init" in importedDict.keys():
        # If the test type is special, capture it then remove it so what's left is just test cases
        classInit = importedDict["init"]
        del importedDict["init"]

    for functionName, function in importedDict.items():
        functionName = functionName.split("-")[0] # hack to allow different test types 
        testType = ""
        if functionName not in target_dict:
            target_dict[functionName] = []

        if "type" in function.keys():
            # If the test type is special, capture it then remove it so what's left is just test cases
            testType = function["type"]
            del function["type"]

        for testInput, testOutput in function.items():
            t = TestCase(functionName, str(testInput), str(testOutput), isClassTest, classInit, testType)
            target_dict[functionName].append(t)

    #return testDict

# attempts to import said modules
def importStudentCode():
    errorMessages = []
    original_stdin = sys.stdin
    for import_name in filesToTest:
        printBuffer = io.StringIO()
        with contextlib.redirect_stdout(printBuffer): #supress any outputs while loading, but save them for later if needed
            sys.stdin = io.StringIO("") # this will cause input to hit an EOF error, which stops importing the file and gets caught by the importer
            try: 
                imports[import_name] = importlib.import_module(import_name)
            except Exception as e: 
                errorMessages.append({import_name: e})
                # TODO maybe put None or the exception in the imports dict so it can be added to the didn't run message
        #output = printBuffer.getvalue()
        import_outputs[import_name] = last_print(printBuffer.getvalue())

    for error in errorMessages:
        key = next(iter(error)) #we know there's only one key pair, so grab that. https://stackoverflow.com/questions/30362391/how-do-you-find-the-first-key-in-a-dictionary/39292086
        print("Error importing:", key)
        print(error[key])  
    sys.stdin = original_stdin

def last_print(buffer):
    return buffer.split("$")[-1].rstrip()

def prepareIO():
    for testFile, functionList in tests.items():
        try:
            studentModule = imports[testFile] 
        except:
            print("Module {} wasn't imported".format(testFile))
            continue

        for functionName, testList in functionList.items():
            for test in testList:

                if test.isClassTest:
                    test.studentObj = loadClass(test.classInitString)
                    if test.studentObj == None:
                        test.message = "Failed on initializing student class"
                        print("Failed initializing class: {}".format(test.classInitString))
                        continue
                        
                
                test.inputList = prepareIOString(test.inputString, True) 
                if type(test.inputList) != list:
                    test.message = "Failed on preparing input"
                    print("Failed initializing input: {}".format(test.inputString))
                
                test.expectedOutput = prepareIOString(test.outputString)
                
def runTests(): 

    for testFile, functionList in tests.items():
        try:
            studentModule = imports[testFile] 
        except:
            print("Module {} wasn't imported".format(testFile))
            continue

        for functionName, testList in functionList.items():
            for test in testList:
                if test.isClassTest:
                    try:
                        #studentClass = getattr(studentModule, type(test.studentObj).__name__)

                        functionToTest = getattr(test.studentObj, test.testName)

                        test.runTest(functionToTest)
                    except Exception as e:
                        print("Exception: " + str(e))   

                else:
                    try:
                        if(test.testName == "onImport"): #TODO improve this
                            test.runImportTest(import_outputs[testFile])
                        else:
                            functionToTest = getattr(studentModule, test.testName)
                            test.runTest(functionToTest)
                    except Exception as e:
                        print("Exception: " + str(e))
    return tests

def prepareIOString(ioString, isInput = False):
    '''
        Takes in the input string and turns it into python objects. 
        If it's for input, it returns a list of the inputs, even if there is only one item (or zero)
        For output it just returns the value
    '''
    op = None
    try:
        op = eval(ioString)
    except Exception as e:
        c = loadClass(ioString)
        op = c if c else ioString
    if isInput:
        if type(op) != list:
            op = [op]
    return op

def loadClass(classInitString):

    for name, module in imports.items():
        try:
            # https://mail.python.org/pipermail/python-list/2002-December/142208.html
            return eval(classInitString, module.__dict__)
        except Exception:
            continue
    return None
   
def show_illegal_function_usage():
    print("illegal function usage results")
    for sFile, functions in tests.items():
        print("Testing file: " + sFile)
        try:
            studentFile = imports[sFile] #ie not present in student's code
        except:
            print("  The test case was loaded but the function wasn't imported from the student's code.")
            print("\n")
            continue
        for function, testList in functions.items():
            results = []
            print("  Testing function: " + function)
            for case in testList:
                if case.testType == funcType.functionContains and case.status == Status.failed:
                    print(case.getResultMessage())

def showResults():
    show_illegal_function_usage()
    print("*"*20)
    print("\n")
    for sFile, functions in tests.items():

        print("Testing file: " + sFile)
        try:
            studentFile = imports[sFile] #ie not present in student's code
        except:
            print("  The test case was loaded but the function wasn't imported from the student's code.")
            print("\n")
            continue
        for function, testList in functions.items():
            results = []
            print("  Testing function: " + function)
            for case in testList:
                if case.testType != funcType.functionContains:
                    results.append(case.status)
                #print(case.getResultMessage())
            print("    Score: {}/{}".format(results.count(Status.passed), len(results)))
        print()
    x = input("Press any key to show all details for failed cases... ")
    print()
    print("-"*20)
    print()
    showFullResults()

def showFullResults():
    for sFile, functions in tests.items():
        #if not any([True for x in functions.items() for f,l in x for test in l if test.status == Status.failed ]):
        #    continue
        #print("Testing file: " + sFile)
        try:
            studentFile = imports[sFile] #ie not present in student's code
        except:
            print("  The test case was loaded but student's file ({}) wasn't imported.".format(sFile))
            print("\n")
            continue
        if any([True for l in functions.values() for case in l if case.status != Status.passed ]):
            print("Testing file: " + sFile)
        for function, testList in functions.items():
            if any([True for case in testList if case.status != Status.passed]):
                print("  Testing function: " + function)
            for case in testList:
                #results.append(case.status)
                if case.status != Status.passed:
                    print(case.getResultMessage())
            #print("    Score: {}/{}".format(results.count(Status.passed), len(results)))
        print()

    
