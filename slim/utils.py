import os
import os.path as path
import subprocess
import glob

import pandas as pd


class SLIM:

    def __init__(self, conf):
        cwd = os.getcwd()

        if conf is None:
            raise AssertionError("Please provide a valid config file. An example can be found on github.")

        dir_name = 'SLIM' if "folder_name" not in conf else conf["folder_name"]
        fic_path = conf['fic_path']

        # create required folders
        os.makedirs(path.join(cwd, dir_name), exist_ok=True)
        os.makedirs(path.join(cwd, dir_name, "data"), exist_ok=True)
        os.makedirs(path.join(cwd, dir_name, "xps"), exist_ok=True)
        basedir = os.path.join(cwd, dir_name + "/").replace("\\", "/")
        datadir = os.path.join(cwd, dir_name, "data/").replace("\\", "/")
        xpsdir = os.path.join(cwd, dir_name, "xps/").replace("\\", "/")

        # save to object
        self.db_name = ""
        self.data_dir = ""
        self.cwd = cwd
        self.fic_path = fic_path
        self.dir_name = dir_name

        # create config file
        max_mem = 1536 if "max_mem" not in conf else conf["max_mem"]
        preferredAfopt = "internal" if "preferred_afopt" not in conf else conf["preferred_afopt"]
        internalmineto = "memory" if "internal_mine_to" not in conf else conf["internal_mine_to"]

        config = f"""maxmemusage = {max_mem}
preferredAfopt = {preferredAfopt}
internalmineto = {internalmineto}
basedir = {basedir}
datadir = {datadir}
xpsdir = {xpsdir}
"""
        head, tail = os.path.split(fic_path)
        with open(os.path.join(head, "fic.user.conf"), "w") as file:
            file.write(config)

    def convert_dat_to_db(self, opt):
        head, tail = os.path.split(opt["path_dat"])

        easy = "0" if "easy" not in opt else opt["easy"]
        data_dir = head.replace("\\", "/") + "/"
        file_name = ".".join(tail.split(".")[:-1])

        self.data_dir = data_dir
        self.db_name = file_name

        config = f"""### Convert database configuration file ###
    
taskclass = datatrans
# Command
command = convertdb
# TakeItEasy(tm)
takeItEasy = {easy}

# Full data path; don't forget to end with a (back)slash. Read from datadir.conf if empty.
dataDir = {data_dir}

## Base database filename
dbName = {file_name}

## Input database
# Encoding ( fimi | fic )
dbInEncoding = fimi
# Extension (search for [dbName].[dbInExt])
dbInExt = dat

## Output database
# Extension
dbOutExt = db
# Encoding ( fic )
dbOutEncoding = fic
# 'Translate forward' (convert item numbers to default fic numbering)
dbOutTranslateFw = true
# Order the items ascending on number (as they should be)
dbOutOrderInTrans = true
# Create a 'binned' database, meaning that all equal transactions are 'merged' into one transaction with a multiplier
# This works well for databases with many 'double' transactions, speeding up the cover process
dbOutBinned = false

# Use the alphabet (and translation) as defined in the following FIC db file. 
# (Use this to ensure that you always get the same alphabet when using a subset of a particular db.)
#useAlphabetFrom = chess

EndConfig

Your comments here.

"""
        # save the config
        conf_file_path = os.path.join(self.cwd, self.dir_name, "convertdb.conf").replace("\\", "/")
        with open(conf_file_path, "w") as file:
            file.write(config)

        # run conversion
        cmd = fr'{self.fic_path} {conf_file_path}'

        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True)
        p.communicate(input=b"\n")
        print("")


    def mine_compression(self, opt):
        easy = "0" if "easy" not in opt else opt["easy"]
        numThreads = 1 if "num_threads" not in opt else opt["num_threads"]

        if self.db_name == "" or self.data_dir == "":
            # todo raise Error
            raise EOFError()

        data_dir = self.data_dir
        file_name = self.db_name

        datatype = "bm128" if "data_type" not in opt else opt["data_type"]
        pruneStrategy = "pep" if "prune_strategy" not in opt else opt["prune_strategy"]

        maxTime = 0 if "max_time" not in opt else opt["max_time"]
        min_sup = 1 if "min_sup" not in opt else opt["min_sup"]

        config = f"""### (Regular) compression configuration file ###

# Class : the task you want to perform : compress_ng
taskclass = compress_ng

# Command compress
command = compress

# TakeItEasy(tm) -- ( 0 | 1 ) If enabled, process runs with low priority.
takeItEasy = {easy}

## Parallel or not
# Set the number of threads that Slimmer may use
numThreads = {numThreads} 

# Full data path; don't forget to end with a (back)slash. Read from datadir.conf if empty.
dataDir = {data_dir}

# Preferred datatype ( uint16 | bai32 | bm128 (default) )
# Always keep to default value (bm128) when the number of different items is <= 128.
# If the number of different items ('alphabet size') is > 128:
#	Dense data --> choose bai32
#	Sparse data --> choose uint16
#	(You may do some small tests to find out what gives the best result for you
#	with respect to both the required computational power and memory space.)
datatype = {datatype}

#Input database/frequent itemset collection to be used as candidates
# iscName = (database Name - candidate type - minimum support + candidate set order)
#iscName = connect-all-2500d
#iscName = ionosphere-all-100d
iscName = {file_name}-all-{min_sup}d
#iris -> database name
#all -> Candidate type determined by ( all | cls | closed )
#1d -> 1 = minimum support, d =  Candidate set order determined by [ a (supp desc, length asc, lex) | d (like a, but length desc) | z | aq | as ... see the code ]

## Compression settings 
## Pruning
# On-the-fly / online  (nop = no pruning, pop = post-pruning, pep = post estimation pruning, prunes only if estimated gain > 0 bits)
pruneStrategy = {pruneStrategy}

### You probably don't want to change anything of the following (possibly except for reportSup)

## Compression settings
# Algorithm name
###############################################################################
# Krimp
#algo = krimp-coverpartial
###############################################################################
###############################################################################
# Slimmer
algo = slimMJ-cccoverpartial-usg

# estimation strategy ( usg | gain ) (usg = estimate candidate quality based on usage count, gain = estimate candidate quality based on actual gain)
estStrategy = gain

## Threshold bits for early stopping compression ( 0 = ignore)
thresholdBits = 0

## maximum time you want algorithm to run (in hours), 0=ignore
maxTime = {maxTime}
##############################################################################

# Report every reportsup support difference (0 = ignore, only on start and end)
reportSup = 50

# Report at least every reportcnd number of candidates (0 = ignore)
reportCnd = 0

# Report at least on every accepted candidate ( bool, 0/1 )
reportAcc = 0

## Storage settings
## What to do when the ISCfile had to be mined? ( zap | store )
# Store means it'll be written /data/candidates and be reused if the same experiment is started
iscIfMined = zap

# The file format to store the ISCFile in ( isc | bisc )
iscStoreType = isc
# The file format to store the temporary ISCFiles in ( isc | bisc )
iscChunkType = isc

# write log file?
writeLogFile = no

# write CTLog file?
writeCTLogFile = no

# write report file?
writeReportFile = no

# write progress to disk? (write code tables and/or stats)
writeProgressToDisk = yes

EndConfig

Your comments here."""

        # save the config
        conf_file_path = os.path.join(self.cwd, "SLIM", "compress.conf").replace("\\", "/")
        with open(conf_file_path, "w") as file:
            file.write(config)

        cmd = fr'{self.fic_path} {conf_file_path}'
        print("")

        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True)
        p.communicate(input=b"\n")

        list_of_files = glob.glob(os.path.join(self.cwd, "SLIM", "xps", "compress_ng") + '/*')
        latest_file = max(list_of_files, key=os.path.getctime)
        print("")
        print("#" * 50, "saving path", "#" * 50, )
        print(latest_file)
        print("#" * 113)