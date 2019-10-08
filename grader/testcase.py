import inspect
import os, io, ast, re
import numpy 
import contextlib #Used for testing print statements

class Status:
    """
    Test case statuses
    """
    notRan = "Not Ran"
    passed = "Passed"
    failed = "Failed"
    exception = "Failed - Exception"

class funcType:
    """
    Supported function types
    """
    functionOutput = "functionOutput"
    printOutput = "printOutput"
    functionContains = "functionContains"

class TestCase:
    
    messageIndent = " "*4

    def __init__(self, name, inputString, outputString, isClassTest, classInit, testType=funcType.functionOutput):
        self.testName = name
        self.testType = funcType.functionOutput if testType=="" else testType
        self.inputString = inputString
        self.outputString = outputString
        self.isClassTest = isClassTest
        self.classInitString = classInit

        self.inputList = []
        self.expectedOutput = None
        self.studentFunction = lambda:None
        self.studentObj = None

        self.actualOutput = None
        self.status = Status.notRan
        self.message = ""

    def __str__(self):
        return "Test Class: {{ {}.{}: {}, {} }}".format(self.classInitString if self.isClassTest else "", self.testName, self.inputList, self.expectedOutput)
    
    def __repr__(self):
        return "Test Class: {{ {}.{}: {}, {} }}".format(self.classInitString if self.isClassTest else "", self.testName, self.inputList, self.expectedOutput)

    def assertNumbersAreEqualOld(self, expectedNumber, studentNumber, precision=2):
        return round(expectedNumber, precision) == round(studentNumber, precision)

    def assertNumbersAreEqual(self, expectedNumber, studentNumber, tau=.0001):
        return abs(expectedNumber - studentNumber) < tau

    def assertLinesAreEqual(self, expectedLine, studentLine):
        expectedDict = re.search("{.*}", expectedLine)
        actualDict = re.search("{.*}", studentLine)
        if expectedDict and actualDict:
            expectedDict = ast.literal_eval(expectedDict.group(0))
            actualDict = ast.literal_eval(actualDict.group(0))
            if expectedDict == actualDict:
                return True
            else:
                return False
        else:
            if expectedLine != studentLine:
                return False
        return True

    # Returns the formatted message string
    #TODO push this as refactoring
    def getResultMessage(self):
        if self.status == Status.passed:
            return "{}Test Case: {}".format(self.messageIndent, self.status)
        elif self.status == Status.notRan:
            return "{}Test Case: {}".format(self.messageIndent, self.status)
        elif self.status == Status.exception:
            result = "{}Test Case: {}\n".format(self.messageIndent, self.status)
            result += "{}-> Test failed for value: {}\n".format(self.messageIndent, self.inputString)
            result += "{}-> Exception: {}".format(self.messageIndent, self.message)
            return result
        else:
            if self.testType == funcType.functionOutput:
                result =  "{}Test Case: {}\n".format(self.messageIndent, self.status)
                result += "{}-> Test failed for value: {}\n".format(self.messageIndent, self.inputString)
                result += "{}-> Actual value: \n{}\n Expected value: \n{}\n".format(self.messageIndent, self.actualOutput, self.expectedOutput)
                return result

            elif self.testType == funcType.printOutput:
                result =  "{}Test Case: {}\n".format(self.messageIndent, self.status)
                result += "{}  -> Test failed for value: {}\n".format(self.messageIndent, self.inputString)
                result += "{}  -> Should have printed: {}\n".format(self.messageIndent, self.expectedOutput)
                result += "{}  -> It actually printed: {}".format(self.messageIndent, self.actualOutput)
                return result

            elif self.testType == funcType.functionContains:
                result = "{}Test Case: {}\n".format(self.messageIndent, self.status)
                result += "{}  {}".format(self.messageIndent, self.message)
                return result

    def runImportTest(self, outputList):
        if (self.expectedOutput in outputList):
            self.status = Status.passed
        else:
            self.status = Status.failed
            self.actualOutput = outputList

    def runTest(self, studentFunction):
        self.studentFunction = studentFunction
        if self.testType == "functionOutput":
            self.__testFunctionOutput()
        elif self.testType == "functionContains":
            self.__testFunctionContains()
        elif self.testType == "printOutput":
            self.__testPrintOutput()
        return self.status
    
    def __testFunctionOutput(self, customEq=None):
        eqList = [lambda x,y: x==y, self.assertNumbersAreEqualOld, numpy.allclose]
        if customEq:
            eqList.append(customEq)
        try: 
            self.actualOutput = self.studentFunction(*self.inputList)
            for equalityTest in eqList:
                try:
                    if equalityTest(self.expectedOutput, self.actualOutput):
                        self.status = Status.passed
                        self.message = ""
                        return
                except:
                    continue

            self.status = Status.failed
            self.message = "- Function didn't have correct output"
        except Exception as e: 
            self.status = Status.exception
            self.message = "- Function failed to run: {}".format(e)

    def __testFunctionContains(self):
        if self.expectedOutput == None:
            self.expectedOutput = True
        raw_source = inspect.getsource(self.studentFunction)
        #strip off function definition
        raw_source = raw_source.split('\n')[1:]
        source = ','.join(raw_source)

        #test if input is in source, and if that equality equals 'expectedOutput'

        present = self.inputString in source

        if present == self.expectedOutput:
            self.status = Status.passed
            self.message = ""
        else: 
            self.status = Status.failed
            if self.expectedOutput:
                self.message = "- Function doesn't contain {}".format(self.inputString)
            else:
                self.message = "- Function contains {} and it shouldn't".format(self.inputString)
    
    def __testPrintOutput(self):
        printBuffer = io.StringIO()
        with contextlib.redirect_stdout(printBuffer):
            try: 
                self.actualOutput = self.studentFunction(*self.inputList)            
            except Exception as e: 
                self.status = Status.exception
                self.message = "- Function failed to run: {}".format(e)
                return
            
        output = printBuffer.getvalue()

        # Clean the strings of empty strings and extra spaces
        studentOutput = [line for line in map(lambda x : x.strip(), output.split(os.linesep)) if line != ""]
        testOutput = [line for line in map(lambda x : x.strip(), self.expectedOutput.split(os.linesep)) if line != ""]

        exactOutput = True
        for test, student in zip(testOutput, studentOutput):
            # If a dictionary is printed out, capture it so we can evaluate it
            if not self.assertLinesAreEqual(test, student):
                self.expectedOutput = test
                self.actualOutput = student
                self.status = Status.failed
                self.message = "- Function didn't have correct output"
                break
        if self.status != Status.failed:
                self.status = Status.passed
                self.message = ""
