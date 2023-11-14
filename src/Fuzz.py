import os 
import subprocess 
import shutil
import threading
import queue
import time 
import random 
from utils import * 
import codeql_report_reader
from codeql_runner import * 
from Config import * 
import mutator
import copy 
from tree_sitter_utils import * 

# The time for logger to write fuzzing stat  
LOGGER_TIME = 60 

# 1 hour fuzzing limit 
FUZZING_TIME = 60* 60 #60

# lock = threading.Lock()

class Fuzz():
    '''
    Our fuzzing routine will be per corpus-QL pair based 
    Hence, we will have a seed + cmd for building it
    Variable declaration: 
    seed : path or name of the seed file 
    cmd  : command for building it 
    QL   : The query file required to evade 
    iteration : number of iteration fuzzed 
    testcase queue : the queue for the testing corpus 
    Mutatnt Queue : the queue for the mutatnt generated 
    anskey: Original ans of the query ,where we only consider the number of entry so far 
    max_run: number of corpus to test 
    opt  : int -O0 -O1 -O2 -O3
    ENV_DICT {
        home_folder -> str 
        build_required -> []
    }
    diff_test : If true, we will use supplied OPT level (opt) vs default level of the make cmd supplied
    '''
    def __init__(self, seed, cmd, QL, ENV_DICT ,diff_test,opt = None ,max_run = -1, thread = 0):
        # For target built from multiple source file
        # We set the seed file for mutation here
        # And we only change it 
        self.seed  = seed
        # File name of the seed
        self.src_name = self.seed.split("/")[-1]
        # We shouldn't assume the CMD is related to the seed 
        self.cmd   = cmd
        self.QL = QL
        self.iteration = 0
        # Some query required to be called by run mode 
        # Due to lack of header 
        self.bqrs_flag = False

        ##########################################
        '''
        Here were data strucutre related to mutation
        We increaement self.mutation_time
        when we generate corpus 
        '''
        self.mutation_time = 0 
        # {Paren: , Current: }
        self.testcase = []
        self.mutatnt = queue.Queue()
        # The list for storing corpus which mutated once or more 
        self.mutated = []
        # The list to save corpus which triggered an exception 
        self.crashed = []
        self.success_exec = 0
        self.thread = thread
        # {code: , gen:, crashed}
        self.cur_parent = None 
        # If the corpus polluted 
        # we escape
        self.polluted_ctr = 0
        # Counter used to stop 
        self.same = 0 
        self._last_mutated = 0
        # Ctr for state reset 
        self.last_crash = 0
        self.last_reset = 0
        ##########################################

        # Currently we only implement checks by number
        # of bug hit, as we only checking by subquery 
        # We should implement by checking the line  
        self.anskey = None 
        self.max_run = max_run 
        # Compiler opt level 
        self.opt = opt 
        # The location for putting the trash , eg the db generated 
        self.trash_id = random.randint(10000,999999999)
        call_clang_format_inplace(self.seed)

        if "home_folder" in ENV_DICT.keys():
            self.home_folder = ENV_DICT["home_folder"]
        else:
            self.home_folder = os.getcwd() + "/"
        # The path will be {CPP_NAME}_{QL_NAME}
        self.home_folder += self.seed.split("/")[-1].replace(".cpp","").replace(".c","").replace(".h","") +"_"+self.QL.split("/")[-1].replace(".ql","")+'/'
        if opt is not None:
            self.home_folder = self.home_folder[:-1]+"_O"+str(opt)+"/"
        
        if opt is not None and diff_test == False :
            '''
            For the case if are testing QL in opt situation
            '''
            if self.cmd.startswith('gcc'):
                self.cmd = self.cmd.replace('gcc','gcc -O'+str(opt))
            elif self.cmd.startswith('g++'):
                self.cmd = self.cmd.replace('g++','g++ -O'+str(opt))
            else:
                print("[+] Unknown compiler opt flag")
                print("[+] Using default (-O0)")

        # 0.1 build a folder for it 
        open_path(self.home_folder)

        self.corpus_folder = self.home_folder+"queue/"
        self.crash_folder = self.home_folder+"failure/"
        self.testing_folder = self.home_folder+"testbench/"
        
        self.normal_log = self.home_folder+'status.log'
        self.event_log = self.home_folder+'event.log'
        self.more_tag = 0 
        self.less_tag = 0 
        self.gen = 0
        self.valid_gen = 0 
        self.thread_list = []
        # 0.2 build the folder for initial profiling 
        open_path(self.home_folder+"initial_profiling/")
        '''
        Now, we config the extra files needed to for building it 
        We do it by copy it from the build essential dict 
        '''
        if "build_required" in ENV_DICT.keys():
            for file in ENV_DICT['build_required']:
                shutil.copy(file, self.home_folder+"initial_profiling/")

        shutil.copy(self.seed, self.home_folder+"initial_profiling/")
        # Next we make a copy as the testbench 
        shutil.copytree(self.home_folder+"initial_profiling/",self.testing_folder)
        if self.thread>0:
            for thread_id in range(1,self.thread):
                tmp_folder = self.home_folder+"testbench_"+str(thread_id)+"/"
                self.thread_list.append(tmp_folder)
                shutil.copytree(self.home_folder+"initial_profiling/",tmp_folder)

        # We snapshot a copy of the 
        # 0.4 build the error case folder  
        # The crash collector 
        open_path(self.crash_folder)
        # 0.5 The corpus queue 
        open_path(self.corpus_folder)
        print("[+] Finished folder initialization")
        # 1. Perform profiling by running query once 
        self.get_anskey()
        print("[+] Finished profiling")
        self.mutatnt.put(self.seed)
        test_case_struct = {'Parent': {'codepath' : None, 'generation': 0}, 
                            'Current': {'codepath' : self.seed, 'generation': 0}}
        # Append twice 
        self.testcase.append(test_case_struct)
        self.testcase.append(test_case_struct)

        if opt is not None and diff_test:
            '''
            For the case of testing across compilet opt lv 
            '''
            if self.cmd.startswith('gcc'):
                self.cmd = self.cmd.replace('gcc','gcc -O'+str(opt))
            elif self.cmd.startswith('g++'):
                self.cmd = self.cmd.replace('g++','g++ -O'+str(opt))
            else:
                print("[+] Unknown compiler opt flag")
                print("[+] Using default (-O0)")
        
        # add the logging path 
        self.st_time = time.time()
        fs = open(self.event_log,'a+')
        fs.write(str(self.st_time)+' FUZZING START\n')
        fs.close()
        self.logger()

    def logger(self):
        # time,crash,more,less,iteration,generation,valid
        fs = open(self.normal_log,'a+')
        line  = str(time.time())+','
        line += str(len(self.crashed))+','
        line += str(self.more_tag)+','
        line += str(self.less_tag)+','
        line += str(self.iteration)+','
        line += str(len(self.mutated))+','
        line += str(self.valid_gen)+','
        line += str(self.gen)+'\n'
        # line += str()+','
        fs.write(line)
        fs.close()
        if len(self.mutated) == self._last_mutated:
            self.same += 1 
        else:
            self.same = 0
            self._last_mutated = self.mutated
        if self.same>10:
            fs = open('/root/ctr_bug.log','a+')
            fail_log = "{} {} {}".format(self.seed,self.cmd,self.QL)
            fs.write(fail_log+"\n")
            fs.close()
            os._exit(1)
        if time.time()-self.st_time < FUZZING_TIME: 
            threading.Timer(LOGGER_TIME, self.logger).start()
        else:
            os._exit(1)


    def get_anskey(self):
        '''
        1. Execute the query with original setup 
        2. Record the result of execution (If its in initialize state)
        3. Return the record 
        '''
        os.chdir(self.home_folder+"initial_profiling/")
        code_build = os.system(self.cmd)
        if code_build!=0:
            log = open(self.home_folder+'init_build_fail.log','a+')
            log.write(self.cmd+'\n')
            log.close()
            # We will handle by exit as it failed 
            exit()
        foldername = self.home_folder+"DB/"
        open_path(foldername)
        CSV_PATH   = self.home_folder+"result.csv"
        db_cmd = gen_db(foldername,self.cmd)
        build_db_ok = os.system(db_cmd)
        if build_db_ok == 0:
            exec_cmd = run_query(CSV_PATH,foldername,self.QL)
            query_status = os.system(exec_cmd)
            if query_status !=0:
                if run_bqrs(CSV_PATH,foldername,self.QL):
                    '''
                    Test for the bqrs mode
                    Update the ans if its ok 
                    '''
                    self.bqrs_flag = True
                    ret = codeql_report_reader.parse_QL_csv(CSV_PATH)
                    self.success_exec += 1
                    if self.anskey == None:
                        self.anskey = len(ret)
                    return ret 
                else:
                    log = open(self.home_folder+'failure_query.log','a+')
                    log.write(exec_cmd+'\n')
                    log.close()
                    # We will handle by exit as it failed 
                    exit()
            else:
                ret = codeql_report_reader.parse_QL_csv(CSV_PATH)
                self.success_exec += 1
                if self.anskey == None:
                    self.anskey = len(ret)
                return ret 
        else:
            log = open(self.home_folder+'/DB_fail_build.log','a+')
            log.write(self.cmd+'\n')
            log.close()
            exit()


    def executor(self,thread_id = None ):
        # Go to the test path  
        cur_test_folder = self.testing_folder
        if thread_id is not None and thread_id != 0:
            if cur_test_folder.endswith("/"):
                cur_test_folder = cur_test_folder[:-1]+"_"+str(thread_id)+"/"
            else:
                cur_test_folder = cur_test_folder+"_"+str(thread_id)+"/"
        os.chdir(cur_test_folder)
        # Remove the old logs, old exe, old src code 
        try:
            os.remove(cur_test_folder+'/*.csv')
            os.remove(cur_test_folder+'/*.out')
            os.remove(cur_test_folder+'/'+self.src_name)
        except:
            pass 
        # Remove db 
        try:
            shutil.rmtree(cur_test_folder+"DB/", ignore_errors=True)
        except:
            pass 
        # Got the path of the case 
        test_case_struct_tmp = self.testcase.pop() 
        case_path = test_case_struct_tmp['Current']['codepath']
        parent_path = test_case_struct_tmp['Parent']['codepath']
        if parent_path == None:
            parent_path = case_path
        # Move to the testing location
        shutil.copy(case_path,cur_test_folder+'/'+self.src_name)
        # Compilation test 
        compiltation_status = os.system(self.cmd)
        if compiltation_status == 0:
            self.polluted_ctr = 0
            # A generation must compile successfully 
            self.valid_gen = max(self.valid_gen,self.cur_parent['generation']+1)
            # Next we check if the result is differet 
            foldername = cur_test_folder+"DB/"
            CSV_PATH   = cur_test_folder+"result.csv"
            db_cmd = gen_db(foldername,self.cmd)
            build_db_ok = os.system(db_cmd)
            if build_db_ok == 0:
                if self.bqrs_flag:
                    query_status = run_bqrs(CSV_PATH,foldername,self.QL)
                    query_status = int(query_status)
                else:
                    exec_cmd = run_query(CSV_PATH,foldername,self.QL)
                    query_status = os.system(exec_cmd)
                if query_status !=0:
                    crash_folder_name   = self.crash_folder+'/QUERY_FAILURE_'+str(random.randint(10000,999999999))+"_gen_"
                    crash_folder_name  += str(test_case_struct_tmp['Current']['generation'])+"_"+str(self.gen)+"_"+str(self.valid_gen)+"_"
                    crash_folder_name  += self.src_name.split('.')[0]+"/"
                    tmp_ext = self.src_name.split('.')[1]
                    open_path(crash_folder_name)
                    shutil.copy(parent_path,crash_folder_name+'parent.'+tmp_ext)
                    shutil.copy(case_path,crash_folder_name+'child.'+tmp_ext)
                    #shutil.copy(case_path,self.crash_folder+'/QUERY_FAILURE_'+str(random.randint(10000,999999999))+"_"+self.src_name)
                else:
                    ret = codeql_report_reader.parse_QL_csv(CSV_PATH)
                    if self.anskey != len(ret):
                        FAIL_TAG = "less_"
                        if len(ret)>self.anskey:
                            FAIL_TAG = "more_"
                            self.more_tag += 1
                        else:
                            self.less_tag += 1
                        # Open a folder 
                        # Copy the parent to it 
                        # We move to our crash collector 
                        crash_folder_name   = self.crash_folder+'/ANALYSIS_FAILURE_'+FAIL_TAG+str(random.randint(10000,999999999))+"_gen_"
                        crash_folder_name  += str(test_case_struct_tmp['Current']['generation'])+"_"+str(self.gen)+"_"+str(self.valid_gen)+"_"
                        crash_folder_name  += self.src_name.split('.')[0]+"/"
                        tmp_ext = self.src_name.split('.')[1]
                        open_path(crash_folder_name)
                        shutil.copy(parent_path,crash_folder_name+'parent.'+tmp_ext)
                        shutil.copy(case_path,crash_folder_name+'child.'+tmp_ext)
                        shutil.copy(CSV_PATH,crash_folder_name+'child_result.csv')
                        shutil.copy(self.home_folder+"result.csv",crash_folder_name+'original_result.csv')
                        #shutil.copy(case_path,self.crash_folder+'/ANALYSIS_FAILURE_'+FAIL_TAG+str(random.randint(10000,999999999))+"_"+self.src_name)
                        # Updated the crashed counter 
                        self.crashed.append(case_path)
                        fs = open(self.event_log,'a+')
                        fs.write("\n"+str(time.time())+'We hit a {} case'.format(FAIL_TAG[:-1]))
                        fs.close()
                        self.last_crash = self.iteration
                    else:
                        # We should seperate the set between bugs and normal
                        # Else we will keep hitting the same bug 
                        # if valid, add to self.mutatnt 
                        self.mutatnt.put(case_path)
                        # as record 
                        self.mutated.append(case_path)
                        # Return to the stack 
                        self.testcase.append(test_case_struct_tmp)
                        self.iteration += 1 
            else:
                # We move to our crash collector 
                crash_folder_name   = self.crash_folder+'/DB_BUILD_FAILURE_'+str(random.randint(10000,999999999))+"_gen_"
                crash_folder_name  += str(test_case_struct_tmp['Current']['generation'])+"_"+str(self.gen)+"_"+str(self.valid_gen)+"_"
                crash_folder_name  += self.src_name.split('.')[0]+"/"
                tmp_ext = self.src_name.split('.')[1]
                open_path(crash_folder_name)
                shutil.copy(parent_path,crash_folder_name+'parent.'+tmp_ext)
                shutil.copy(case_path,crash_folder_name+'child.'+tmp_ext)
        else:
            # else, we delete the case 
            self.polluted_ctr += 1 
            os.remove(case_path)


    def run_loop(self):
        '''
        Do the fuzzing pipeline:
        1. Get the corpus
        2. Get the mutator 
        3. Test side effect 
            - Comby 
            - Universalmutator
        4. Process the query 
        5. Triage 
        '''
        time_now = time.time()
        while time_now-self.st_time < FUZZING_TIME: 
            self.case_generator()
            self.executor()
            self.cur_parent = None 
            time_now = time.time()
            resetted = False
            if self.polluted_ctr > 10:
                resetted = True 
            elif self.last_crash == 0 and self.iteration-self.last_reset > 10 and resetted == False:
                # No bug found 
                # Reset once in every 10 iteration 
                resetted = True
            elif random.random()>0.5 and self.iteration-self.last_crash > 10 and resetted == False:
                # have crash but last crash is more than 10 rounds 
                resetted = True
            elif random.random()>0.2 and self.iteration-self.last_reset > 10 and resetted == False:
                # random state reset  
                resetted = True            
            if resetted:
                test_case_struct = {'Parent': {'codepath' : None, 'generation': 0}, 
                                    'Current': {'codepath' : self.seed, 'generation': 0}}
                self.testcase.append(test_case_struct)
                self.polluted_ctr = 0 
                self.last_reset = self.iteration

        fs = open(self.event_log,'a+')
        fs.write(str(time_now)+' Fuzzing end\n')
        fs.close()
        return 

    # gen, update , shuffle 
    def call_universalmutator(self):
        '''
        1. Get a file 
        2. Call the mutator 
        3. Return a list and enqueue 
        '''
        test_case_struct_tmp = self.testcase.pop()
        casepath = test_case_struct_tmp['Current']['codepath']
        self.cur_parent = test_case_struct_tmp['Current']
        extension =  casepath.split(".")[-1]
        ret = mutator.wrap_universalmutator(casepath, self.corpus_folder,extension)
        self.testcase.append(test_case_struct_tmp)
        return ret

    def call_comby(self):
        test_case_struct_tmp = self.testcase.pop()
        casepath = test_case_struct_tmp['Current']['codepath']
        self.cur_parent = test_case_struct_tmp['Current']
        # Pure comby take in str source code 
        # No parsing is needed 
        source = open(casepath).read()
        extension =  casepath.split(".")[-1]
        ret = mutator.comby_driver(source,self.corpus_folder,extension)
        self.testcase.append(test_case_struct_tmp)
        return ret

    def call_treesitter_utils(self):
        test_case_struct_tmp = self.testcase.pop()
        casepath = test_case_struct_tmp['Current']['codepath']
        self.cur_parent = test_case_struct_tmp['Current']
        # Pure comby take in str source code 
        # No parsing is needed 
        source = open(casepath).read()
        extension =  casepath.split(".")[-1]
        # Randomly gen do how many time mutation 
        num = 1
        test = Program(source)
        test.analysis()
        ret = []
        for i in range(0,num):
            tmp_test = copy.copy(test)
            mutation_code_path = tmp_test.mutation_pipeline(self.corpus_folder,extension)
            if len(mutation_code_path)>0:
                ret.append(mutation_code_path)
            del tmp_test
        self.testcase.append(test_case_struct_tmp)
        return ret

    def case_generator(self):
        # We first get a method of mutation 
        # We assume its possible that we can't generate a new mutant 
        ret = []
        mutate_done = False 
        blank_ctr = 0
        # We setup a flag for generating UM 
        # This can ensure we can generate corpus 
        # For next round after we don't have 
        # Sufficient mutation available 
        next_rd_gen_UM = False 
        while not mutate_done and blank_ctr<10:
            if len(self.testcase)>0:
                if (random.random()>0.7 and self.iteration >1) or (next_rd_gen_UM==True):
                    ret = self.call_universalmutator()
                    next_rd_gen_UM = False 
                elif (random.random()>0.5):
                    ret = self.call_comby()
                else:
                    try:
                        ret = self.call_treesitter_utils()
                    except:
                        ret = []
                if len(ret)>0:
                    mutate_done = True 
                else:
                    blank_ctr += 1 
            else:
                test_case_struct = {'Parent': {'codepath' : None, 'generation': 0}, 
                            'Current': {'codepath' : self.seed, 'generation': 0}}
                self.testcase.append(test_case_struct)
                blank_ctr += 1  
                next_rd_gen_UM = True 
    
        if not mutate_done and blank_ctr>10:
            print("[+] It sounds like we exhausted all the mutation????")
            fs = open(self.event_log,'a+')
            fs.write(str(self.st_time)+' EARLIER STOPPED DUE TO LACK OF MUTATION STRATEGY\n')
            fs.close()
            exit()
        # enqueue the list 
        for case_gen in ret:
            # Normalize the corpus for next round's mutation 
            call_clang_format_inplace(case_gen)
            test_case_struct = {'Parent': {'codepath' : self.cur_parent['codepath'], 'generation': self.cur_parent['generation']}, 
                            'Current': {'codepath' : case_gen, 'generation': self.cur_parent['generation']+1}}
            self.testcase.append(test_case_struct)
        self.gen = max(self.gen,self.cur_parent['generation']+1)

