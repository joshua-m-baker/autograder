This is an automatic grading program built for an intro to programming class. Although there are many auto-grading programs available, this one was built specifically for the class. This program is part of a larger, private repository, but this code specifically was authored by me. 

# Requirements
    - Git (Git bash for Windows)
    - Python
    - Pip

# Initial setup
You should only have to do this once
- Clone the grading repo with preferred method
- Cd to autograder/grader
- Install dependencies in requirements.txt with pip
    - `pip3 install -r requirements.txt`
    - `python3 -m pip install -r requirements.txt`
    - `py -m pip install -r requirements.txt`
    - Or however you run pip on your system
- Run ```setup.py``` and choose the corresponding values
    - You also can just edit config.yaml directly, then run ```setup.py``` to ensure everything is good

# Grading
(This description assumes you are in `autograder/grader`)
- Command line
    - Run `getRepos.py`
        - This will clone the repos you need to grade into the ./repos folder
        - Your repos are pulled based on the DUE_DATE variable in `config.py` and the corresponding row in the grading spreadsheet (eventually. For now it just pulls some test ones)
    - To test someone's code, just cd to repos/C200-Assignments-username/Assignment# and run gradingTests.py
        - The output will tell you about any issues running the Student's code, and the final results will be at the bottom 
- GUI
    - TBD

# Abilities
Currently, all the tests are function based. The following test types currently exist:

- functionOutput
    - Check the output of a function against expected output. Multiple different equality checks happen
        - Soon to allow defining custom equality functions in the test file
- printOutput
    - Check what a student's function prints against expected output. Currently is only an exact match, but some fuzziness could easily be implemented.
- functionContains:
    - Check if a function does or does not contain a certain string. 
        - For example, this can be used to insure a function does contain a required loop type, or does not contain builtin functions.
- classes:
    - Student classes can be instantiated with custom constructors, and then any of the above can be used to test functions inside the class
- onImport:
    - Check if stuff is printed when the file is imported. 
    
As an additional note, almost any python- interpretable thing can be passed in as input or output, so things like lambda functions and numpy arrays can be used for input/ output.

More in depth on the test file formats [here](docs/testFormats.md)

# Structure
Wrote up some stuff in [this doc](docs/architecture.md)

# Sample Output
```
--------------------
importTests

--------------------
import student code
Error importing: correlation
[Errno 2] No such file or directory: 'Assignment11/acme_zyx.txt'

--------------------
prepare io

--------------------
run tests
Module correlation wasn't imported

--------------------
results

Testing file: haversine
  Testing function: hd
    Test Case: Passed

    Test Case: Passed


Testing file: lineclass
  Testing function: get_line
    Test Case: Passed

  Testing function: __mul__
    Test Case: Passed

    Test Case: Passed


Testing file: weird
  Testing function: g
    Test Case: Passed

    Test Case: Passed


Testing file: matrix
  Testing function: mm
    Test Case: Passed

  Testing function: tp
    Test Case: Passed

  Testing function: add_m
    Test Case: Failed - Exception
    -> Test failed for value: [np.array([[1,2,4],[3,4,3]]), np.array([[1,2,4],[3,4,3]])]
    -> Exception: - Function failed to run: index 10 is out of bounds for axis 0 with size 3

Testing file: correlation
  The test case was loaded but the function wasn't imported from the student's code.
```

# TODOs
- Specify point value per test
- Only test file open in gui
- Repo validator 
- Import packages in test file
- Include imports needed for test case values at top of test runner
- Command line arguments to control stuff:
    - Verbose/ short output for running tests
    - Run tests for only one file
    - Force re- clone
- Provide context for why test wasn't run in printResults
    - failed importing etc 
---
- ~~Autogenerate smallusernames.txt from the excel file directly to avoid errors where people copy the wrong column~~
- ~~Add custom equality checks~~ 
- ~~Clean up cloning script~~
- ~~Test case type for contents of function~~
    - ~~include/ exclude: loop type, recursive call, etc~~
- ~~Clean up class test in testClass~~
- ~~Check if the repos folder exists, if not then create it on setup~~
- ~~Add ability to toggle off cloning/ checking out repos wi    th command line argument~~
- ~~Some sort of teardown to get rid of the student repos after you're done, and possibly include Sub's csv script~~
- ~~Bring in some sort of testing framework to keep everything working smoothly~~
- ~~Have tests with multiple inputs~~
- ~~Have test cases for classes~~
- ~~Allow tests to have classes as input~~
- ~~Write test cases in different format~~
    - ~~yaml~~
    - ~~Make every input set a list so it can just be unwrapped for the function call~~
- ~~Add the ability to set different test types (find a good way to specify in template file):~~
    - ~~Check function result (default)~~
    - ~~Check printed text (with input?)~~
