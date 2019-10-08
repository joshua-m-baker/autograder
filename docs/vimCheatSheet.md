I find vim to be a powerful tool when editing the grading report TEX files. With only a few commands you can quickly navigate to any part of the document. 


Move to the next spot where a grade should be filled in
```
    /\d*\/\d\d # Search (/) for 0 or more digits (\d*) followed by a forward slash (\/), followed by two digits (\d\d)
    n   # move to next match
    N   # go to previous match
```

Move to the comments section (from number spot):
    }

Move to the final total
    Gn