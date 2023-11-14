'''
We hardcode all the env Parm here 
'''

##################################################################
# CodeQL configuration 

TAG = "GCJ"

CODEQL_EXECUTABLE = "/root/codeql/codeql"
JULIET_PATH = "/root/C/testcases/"

# Path should ended with / 
RECORD_PATH = "/root/{}_csv_record/".format(TAG)
DB_PATH = "/root/{}_generated_DB/".format(TAG)
LOG_PATH = "/root/{}_log/".format(TAG)
CODEQL_LIB_PATH = "/root/codeql-codeql-cli-v2.8.1/"
LANG = "cpp"
RAM_SIZE = 8000
THREAD = 4
OUTPUT_FORMAT = '\"csv\"'

##################################################################
# list of header files  

INCLUDE = ['cstdint','cstdlib','stdio.h','string.h','algorithm']
# API import needed
# Here we will need a full path until ";" 
# for a successful match 
API = ['void *calloc(size_t nitems, size_t size);']
LOCAITON_TO_TREE_SITTER = {
    'cpp' : '/root/build/my-languages.so', 
    'c' : '/root/build/my-languages.so', 
    'javascript' : '/root/build/my-languages.so', 
}

REWRITE_TAG = [
    "GLOBAL_HERE",
    "FUNC_HERE",
    "EXP_HERE",
]


