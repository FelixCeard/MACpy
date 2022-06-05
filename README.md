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
