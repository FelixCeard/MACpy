import os
import os.path as path
import subprocess
import glob


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
        self.xpsdir = xpsdir

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

    def convert_dat_to_db(self, opt, for_classification=False):
        head, tail = os.path.split(opt["path_dat"])

        easy = "0" if "easy" not in opt else opt["easy"]
        data_dir = head.replace("\\", "/") + "/"
        file_name = ".".join(tail.split(".")[:-1])

        self.data_dir = data_dir
        self.db_name = file_name

        config = f"""taskclass = datatrans
command = convertdb
takeItEasy = {easy}
dataDir = {data_dir}
dbName = {file_name}
dbInEncoding = fimi
dbInExt = dat
dbOutExt = db
dbOutEncoding = fic
dbOutTranslateFw = true
dbOutOrderInTrans = true
dbOutBinned = false
EndConfig
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

        if for_classification:
            path_db = os.path.join(head, file_name+".db")
            with open(path_db, 'r') as file:
                content = file.readlines()
            if "cl" not in opt:
                raise AssertionError("cl need to be specified in the opt as \"cl: [0, 1]\" for example")
            content.insert(2, "cl: "+" ".join(opt["cl"]) + "\n")
            with open(path_db, 'w') as file:
                file.write("".join(content))

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

        # usg or gain
        estimation_strategy = "usg" if "estimation_strategy" not in opt else opt["estimation_strategy"]

        config = f"""taskclass = compress_ng
command = compress
takeItEasy = {easy}
numThreads = {numThreads} 
dataDir = {data_dir}
datatype = {datatype}
iscName = {file_name}-all-{min_sup}d
pruneStrategy = {pruneStrategy}
algo = slimMJ-cccoverpartial-usg
estStrategy = {estimation_strategy}
thresholdBits = 0
maxTime = {maxTime}
reportSup = 50
reportCnd = 0
reportAcc = 0
iscIfMined = zap
iscStoreType = isc
iscChunkType = isc
writeLogFile = no
writeCTLogFile = no
writeReportFile = no
writeProgressToDisk = yes
EndConfig
"""

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

    def mine_classification(self, opt):
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

        config = f"""taskClass = classify
command = classifycompress
takeItEasy = {easy}
dataDir = {data_dir}
iscName = {file_name}-all-1d
seed = 0

## Classification
# Class definition (define which items to regard as class labels; multi-class transactions not allowed!)
# (Only required when class definition is not given in the original database; option overrides any definition given there)
#classDefinition = 9 14 22

## Preferred datatype ( uint16 | bai32 | bm128 (default) )
# Refer to compress.conf for more info on this
#datatype = bm128

## Parallel or not
# Set the number of threads that Slimmer may use
numThreads = 1 

## ---------- 'Expert' settings :) --------- ##

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

# max time in hours, 0=ignore
maxTime = 0
##############################################################################

# Report after every [reportsup] support change in the candidate list
reportSup = 10
# Report at least every reportcnd number of candidates (0 = ignore)
reportCnd = 0

## Pruning
# On-the-fly / online  (nop = no pruning, pop = post-pruning, pep = post estimation pruning, prunes only if estimated gain > 0 bits)
pruneStrategy = pep

## Cross-validation (usually 10-fold CV)
# Number of folds ([2,*] or 1 for training = test)
numFolds = 10

# Perform all code table matching schemes (currently meaning: both absolute && relative CT matching)
allMatchings = 1

## CT matching (only relevant if allMatchings == 0)
# Try to match codetables relative to max.sup (set to 0 to use absolute matching by reportSup)
classifyPercentage = 0

iscIfMined = zap
iscStoreType = isc
iscChunkType = isc
writeLogFile = no
writeCTLogFile = no
writeReportFile = no
writeProgressToDisk = yes

EndConfig
"""

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
