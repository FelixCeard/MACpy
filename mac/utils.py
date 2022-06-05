import os
import os.path as path
import subprocess

import pandas as pd


class MAC:

    def __init__(self):

        cwd = os.getcwd()
        dir_name = 'MAC'

        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.jar_path = path.join(self.dir_path, 'MAC.jar').replace('\\', '/')

        if path.isdir(path.join(cwd, dir_name)) is False:
            print('creating dir')
            os.mkdir(path.join(cwd, dir_name))

        self.input_path = path.join(cwd, dir_name, 'temp_input.csv').replace('\\', '/')

        self.path_cp = path.join(cwd, dir_name, 'temp_CP').replace('\\', '/')
        self.path_runtime = path.join(cwd, dir_name, 'temp_runtime').replace('\\', '/')
        self.path_data = path.join(cwd, dir_name, 'temp_data').replace('\\', '/')

        self.sep = ';'

        self.CLUMPS = 30

        self.cp = {}

    def parse_df(self, df):
        df.to_csv(self.input_path, header=False, index=False, sep=self.sep)

    def run(self, df: pd.DataFrame):
        assert len(df.shape) == 2, "Expected a dataframe with n rows and m columns"

        self.parse_df(df)  # save csv

        rows = df.shape[0]
        columns = df.shape[1] - 1  # one predictor

        cmd = f'java -jar {self.jar_path} -FILE_INPUT {self.input_path} -FILE_CP_OUTPUT {self.path_cp} -FILE_RUNTIME_OUTPUT {self.path_runtime} -FILE_DATA_OUTPUT {self.path_data} -NUM_ROWS {rows} -NUM_MEASURE_COLS {columns} -FIELD_DELIMITER {self.sep} -CLUMPS {self.CLUMPS}'
        print('mac is running...')
        r = subprocess.run(cmd, stdout=subprocess.PIPE)
        self.terminal_output = r.stdout.decode('utf-8')
        print('mac has finished:')

        self.parse_response()

        return self.cp

    def parse_response(self):
        with open(self.path_cp, 'r') as file:
            content = ''.join(file.readlines()).split('-------------------------------------\n')

        for i, bin_str in enumerate(content):
            c = bin_str.split('\n')[1:-1]
            self.cp[i] = [float(n) for n in c]
