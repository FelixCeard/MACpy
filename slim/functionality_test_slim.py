from utils import SLIM
import pandas as pd

if __name__ == '__main__':
    options = {
        "folder_name": "SLIM",
        "max_mem": 1536,
        "preferred_afopt": "internal",
        "internal_mine_to": "memory",
        "fic_path": r"C:\Users\felix\PycharmProjects\MACpy\slim\bin\fic_x64.exe",

    }

    slim = SLIM(options)

    # creation of database
    path_to_dat = r"C:\Users\felix\PycharmProjects\MACpy\slim\test\chess.dat"

    opt = {
        "path_dat": r"C:\Users\felix\PycharmProjects\MACpy\slim\test\chess.dat",
        "easy": "0",
    }

    slim.convert_dat_to_db(opt)

    opt = {
        "path_dat": r"C:\Users\felix\PycharmProjects\MACpy\slim\test\chess.dat",
        "easy": "0",
        "num_threads": 1,
    }
    slim.mine_compression(opt)