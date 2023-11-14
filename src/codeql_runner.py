import os 
import subprocess 
import glob 
import json 
import multiprocessing
from ql_mapping import CodeQL_CWE_TO_TEST_CASE,CodeQL_CWE_TO_QL,\
            MSFT_CHECKING,MSFT_MUST_FIX,MS_MUST_FIX_ISSUE_TO_QUERY,\
            CODEQL,JULIET,CWE_DETECT,JULIET_TO_CHECK
import codeql_report_reader 
from utils import * 
from Config import * 


# Gen folder
# open_path(RECORD_PATH)
# open_path(DB_PATH)
# open_path(LOG_PATH)


def gen_juliet_path(JULIET_PATH):
    ok_dict = {}
    tmp = glob.glob(JULIET_PATH+'*')
    for sss in tmp:
        cwe_key = sss.replace(JULIET_PATH,"").split('_')[0]
        cwe_key = cwe_key.replace("CWE","CWE-")
        if len(cwe_key)<7:
            cwe_key = cwe_key.replace("CWE-","CWE-0")
        if cwe_key in JULIET_TO_CHECK:
            if cwe_key not in ok_dict.keys():
                ok_dict[cwe_key] = []
            ret = all_file_under_path(sss)
            for path in ret:
                if path.endswith('Makefile'):
                    ok_dict[cwe_key].append(path.replace('/Makefile',''))
    return ok_dict


def gen_db(foldername,build_cmd):
    db_create_db  = CODEQL_EXECUTABLE+" database create {} --language="
    db_create_db += LANG + " --command=\"{}\""
    db_create_db  = db_create_db.format(foldername,build_cmd)
    return db_create_db

def run_query(CSV,DB_FOLDER,QL_file):
    '''
    The csv and db folder were in absolute path 
    '''
    query  = CODEQL_EXECUTABLE+" database analyze --ram="+str(RAM_SIZE)
    query += " --threads="+str(THREAD)+" --format="+OUTPUT_FORMAT
    query += " --output=\"{}\" {} \"{}\""
    query  = query.format(CSV,DB_FOLDER,QL_file)
    return query

def run_bqrs(CSV,DB_FOLDER,QL_file):
    '''
    The csv and db folder were in absolute path 
    Step 1. Call query run and create bqrs 
    Step 2. Parse the bqrs and transfer to csv
    Return true or false for the fuzzer to output error or continue 
    '''
    query  = CODEQL_EXECUTABLE+" query run --ram="+str(RAM_SIZE)
    query += " --threads="+str(THREAD)
    query += " --output=\"{}\" --database={} -- \"{}\""
    query  = query.format(CSV+".bqrs",DB_FOLDER,QL_file)
    query_run_status = os.system(query)
    if query_run_status == 0:
        # https://codeql.github.com/docs/codeql-cli/manual/bqrs-decode/
        # 0. Parse the metadata 
        # /testing/yarpgen/build/testing/codeql/codeql bqrs info --format=json -- "/root/fuzzer/static-framework-survey/automation-framework/dataflow-testsdataflow-consistency/xxxx.bqrs" 
        info_cmd  = CODEQL_EXECUTABLE + " bqrs info "
        info_cmd += " --format=json -- "
        info_cmd += CSV+".bqrs"
        res = os.popen(info_cmd).read()
        item = json.loads(res)
        item = item['result-sets']
        tocheck = []
        for x in item:
            if x['rows']>0:
                tocheck.append(x['name'])
        csv_snapshot = []
        for sub_row in tocheck:
            # 1. Run 
            query  = CODEQL_EXECUTABLE+" bqrs decode "
            query += " --output=\"{}\" --result-set={} --format=csv --no-titles -- \"{}\""
            query  = query.format(CSV,sub_row,CSV+".bqrs")
            tmp_fs = open(CSV).read().split("\n")
            tmp_fs = [x for x in tmp_fs if len(x)>0]
            csv_snapshot += tmp_fs
        fs = open(CSV,'w')
        fs.write("\n".join(csv_snapshot))
        fs.close()
        return True
    else:
        return False


def juliet_harness(CASE_PATH,list_of_query):
    os.chdir(CASE_PATH)
    os.system("make individuals > "+CASE_PATH+"/test.log")
    fs = open(CASE_PATH+"/test.log").read()
    fs = fs.split('\n')
    cmd_parsed = []
    for z in fs:
        if len(z)>0:
            # /usr/bin/gcc -c -I ../../../testcasesupport ../../../testcasesupport/io.c -o io.o
            # /usr/bin/gcc -c -I ../../../testcasesupport ../../../testcasesupport/std_thread.c -o std_thread.o
            if z.endswith('io.c -o io.o') or z.endswith('std_thread.c -o std_thread.o'):
                pass 
            else:
                cmd_parsed.append(z)
    for cmd in cmd_parsed:
        if len(cmd)>0:
            try:
                BIN_NAME = cmd.split('.out')[0].split(' ')[-1]
                foldername = DB_PATH+'/'+BIN_NAME
                db_cmd = gen_db(foldername,cmd)
                build_db_ok = os.system(db_cmd)
                if build_db_ok == 0:
                    for QL_file in list_of_query:
                        query_name = QL_file.split("/")[-1].replace('.ql','')
                        QL_file = CODEQL_LIB_PATH + QL_file
                        CSV_PATH = RECORD_PATH +  BIN_NAME + "_" +query_name + '.csv'
                        exec_cmd = run_query(CSV_PATH,foldername,QL_file)
                        query_status = os.system(exec_cmd)
                        if query_status !=0:
                            log = open(LOG_PATH+'/failure_query.log','a+')
                            log.write(exec_cmd+'\n')
                            log.close()
                else:
                    log = open(LOG_PATH+'/fail_build.log','a+')
                    log.write(cmd+'\n')
                    log.close()
            except:
                print('[+] Failed ')
                log = open(LOG_PATH+'/wtf.log','a+')
                log.write(cmd+'\n')
                log.close()

def fuzzing_wrapper(a,b):
    return 

def call_FUZZ(cmd_list):
    fuzzing_wrapper(cmd_list[0],cmd_list[1])

def call_QL(cmd_list):
    juliet_harness(cmd_list[0],cmd_list[1])

