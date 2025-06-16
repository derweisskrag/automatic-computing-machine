# Analysis

## Overview

This part of our codebase contains the actual datascience analyze. It is the place where we utilize our package. You do not use `importlib.util` to import your function. 
There are reasons for that: 

- You create functions, test them and then we can deploy if everything is ready.
- Then we go here and use those functions to fulfill the task assigned to us.

However, if you want, you can. Why not? However, I would use `main.ipynb` in the root and imported the CSV path
using our available methods. From root, you can simply 

```python
from tomodachi_core.tomodachi.utils import check_timestamp
from tomodachi_core.config_development.config import CSV_PATH
```

Or if you work with different data, say, processed one, then we would have to use "SAVE_TO_CSV" variable. This is because it will pinpoint 
the exact location of the `processed csv file`. 

## SPRINT-1

For more information, please read docs/tasks/README.md. According to the SPRINT-1.ipynb, we had to implement preprocessing of the given `CSV` file:

- check dates (according to Python & Pandas as they differ in the datetime data type: datetime64[ns] vs datetime)
- removes na values and using the `fillna`, replacing the `na` values the median of the column data
- remove duplicates
- check the types 
- save the preprocessed file

## SPRINT-2