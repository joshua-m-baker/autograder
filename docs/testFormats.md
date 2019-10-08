# yaml format
I've settled on yaml as the best format for both writing tests quickly and providing the range of information needed.
Yaml is a fairly simple markup language that has a lot of similarities to python. The test files will get parsed and converted to python dictionaries. There is some abuse of yaml, and there might be a slightly natural way to do this, but at the same time I think it works well enough

The general format is shown below. For the most part you can just write things how they would be in python. There are a few things to make note of. 
    - Currently to put in multiple values, it has to be in a list surrounded by quotes, i.e. "[1,2,3]". 
    - If you want to input a list as the single parameter, use two sets of brackets: [[1,2,3]] (if the list is one of multiple parameters you don't need to do that). 
    If you want to test multiple objects, put them under class1, class2, etc.

```
fileName:
    functionName:
        
        #The general format is key/value pairs, where the key is the input, and value is the output.

        myInput: myOutput #Generic format of test values
        1: "2" #This test case has an int input and string output.
        "2": 3 #This test case has a string input and an int output.
        [1,2,3]: 1 #One input value, a list
        "[1,2,3]": 1 # Three separate inputs, not a list

        #For multiple inputs, put them in a list surrounded by quotes.
    
    functionTwo:
        type: printOutput
        #to change the type of test, do this, set "type" to what you want. No type defaults to functionOutput
        myInput: |
            This is how you do multi lines.
            A pipe character and 
            indented text

    functionThree:
        type: functionContains
        for:  #no value defaults to True
        while: True
        remove: False
        #Testing that 'functionThree' contains for and while (no output defaults to True for functionContains), and doesn't contain remove
    
    functionThree-1: #if you want to do tests of multiple different types, make another block with the same name, dash some number
        1: 10
    
fileTwo:
    class1: #any number can go here
        init: myClass(1,2)
        #function tests for classes are the same as functions, just inside class
        functionOne:
            1: 1

```

