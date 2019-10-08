# General code path
1. setup.py
    - Run once to set grader specific values

2. getRepos.py
    1. Create folder for repos
    2. Pull usernames to be graded from spreadsheet
    2. Clone and checkout repos from usernames list
    3. Write test file to each student folder

2. gradingTests.py
    1. importTests
        - read in yaml test file, note any class tests
        - call loadFunctionDict and put the result in the global test dict with the filename as the key.
        - Track any output from loading the file
    2. loadFunctionDict
        - Pulls out all test cases for a file. Saves the test type, if specified.
        - Values kept as strings for now
    2. import student code
        - Puts each student module object in an imports dictionary.
    3. prepare input and output
        - The input gets evaluated and put into a list (regardless of how many inputs), so it can be unwrapped consistently when the test is run 
        - Has to be saved till now so student classes can be instantiated
    4. run tests
        - Allow each test case to run itself with the appropriate test type and save the result. 
    5. show results
        - Print out the results 

# Internal Test Structure
```
tests = {
    fileName1: {
        functionName1: [<TestCase.TestCase object at 0x10de915c0>, <TestCase.TestCase object at 0x341e989d0>],
        functionName2: [<TestCase.TestCase object at 0x10de915c0>, <TestCase.TestCase object at 0x341e989d0>]
    },
    fileName2: {
        functionName1: [<TestCase.TestCase object at 0x10de915c0>, <TestCase.TestCase object at 0x341e989d0>],
        functionName2: [<TestCase.TestCase object at 0x10de915c0>, <TestCase.TestCase object at 0x341e989d0>]
    }
}

```

# Test result structure
TODO: Implement this structure/ write it to results file
results = {
    fileName1: {
        functionName: [{className, result, score(?)}, {className, result, score(?)} ]
    }
}