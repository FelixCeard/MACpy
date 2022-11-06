# MACpy
## Description
This is a wrapper for Multivariate Maximal Correlation Analysis (MAC) by Nguyen, H-V, Müller, E, Vreeken, J & Böhm, K.

The original code ([https://eda.mmci.uni-saarland.de/prj/mac/](https://eda.mmci.uni-saarland.de/prj/mac/)) is in java. 

## Install
1. make sure to have java installed and in your path variables.
2. Clone the repository and run `python setup.py install`.

Tested on windows 10, python 3.9 and java 17.0.3

## Run
You can use the library directly in your code:
```python
import pandas as pd
from mac import MAC

# init MAC
mac = MAC()

# format your data into a pandas dataframe
df = pd.DataFrame(...)

mac.CLUMPS = 5  # default is 30

# run mac on your dataframe
bins = mac.run(df)

# The returned bins have the following structure
# bins[column_id] = [bin_upper_value_0, bin_upper_value_1, bin_upper_value_2]

# paths
mac.path_cp  # file which contains the bins
mac.path_runtime  # file which contains the runtime informations
mac.path_data  # file which contains the output data of MAC

# if the terminal output is wished
print(mac.terminal_output) 
```

When runing the code, a new directory appears in your working directory containing the outputs of MAC:
```
Workind Directory
├── file.py  # where execute your code
├── MAC  
│   ├── temp_CP         
│   ├── temp_data
│   ├── temp_runtime
│   ├── temp_input.csv
```

## Slim
A wrapper for SLIM is also included. For it please **download** and **extract** from https://eda.mmci.uni-saarland.de/prj/slim/ in the slim folder. The resulting structure should resemble sth. like:
```
Workind Directory
├── README.md 
├── mac  
├── slim  
│   ├── bin         
│   ├── data
│   ├── docs
│   ├── trunk
│   ├── xps
│   ├── __init__.py
│   ├── utils.py
```

Additionally, similar to MAC, a folder is being created in the working directory.
**Note that compression results will be in this folder.** 

## Code example
```python
from slim import SLIM

# <Generate and Save your data to a dat file (example files are in the slim folder)>

slim = SLIM({
    "folder_name": "SLIM",
    "max_mem": 1536,
    "preferred_afopt": "internal",
    "internal_mine_to": "memory",
    "fic_path": r"C:\Users\felix\PycharmProjects\MACpy\slim\bin\fic_x64.exe",
})

slim.convert_dat_to_db({
    "path_dat": r"C:\Users\felix\PycharmProjects\MACpy\slim\test\chess.dat",
    "easy": "0",
})

slim.mine_compression({
    "path_dat": r"C:\Users\felix\PycharmProjects\MACpy\slim\test\chess.dat",
    "easy": "0",
    "num_threads": 1,
    "data_type": "bm128",
    "prune_strategy": "pep",
    "max_time": 0,
    "min_sup": 1
})
```

If you see sth. along
```python
################################################## saving path ##################################################
C:\Users\felix\PycharmProjects\MACpy\slim\SLIM\xps\compress_ng\chess-all-1d-slimMJ-n-cccpu-pep-20221106193627
#################################################################################################################
```

then the compression worked
