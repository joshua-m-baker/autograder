import testRunner
import sys, os

def main():
    print("-"*20)
    print("importTests")
    testRunner.importTests(TEMPLATE_FOLDER)
    print()
    print("-"*20)
    print("import student code")
    testRunner.importStudentCode()
    print()
    print("-"*20)
    print("prepare io")
    testRunner.prepareIO()
    print()
    print("-"*20)
    print("run tests")
    testRunner.runTests()
    print()
    print("-"*20)
    print("results")
    testRunner.showResults()

if __name__ == "__main__":
    main()