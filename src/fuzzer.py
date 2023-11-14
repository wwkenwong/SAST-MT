import argparse 
from Fuzz import * 

def get_argument_parser():
    parser = argparse.ArgumentParser(description="SAAS Fuzzing")
    parser.add_argument("-s", "--seed",
                    type=str,
                    required=True,
                    help="File path to the seed file for mutation")
    parser.add_argument('-c', '--cmd', 
                    type=str,
                    required=True,
                    help='The command for building the given seed')
    parser.add_argument("-q", "--QL",
                    type=str,
                    required=True,
                    help="The QL files required for testing")
    parser.add_argument("-hf", "--home_folder",
                    type=str,
                    help="The path to save the output")
    parser.add_argument('-b', '--build_required',
                        nargs='+',  
                        help='space delimited list of path')
    parser.add_argument("-O", "--opt",
                    type=int,
                    help="Compiler optimization level for testing, option 0,1,2,3. By default, we follow the opion of the cmd")
    parser.add_argument("-max_iter", "--max_run",
                    type=int,
                    help="The number of maximal cycle we execute the fuzzer")
    parser.add_argument('-diff_test', '--diff_test',
                        action='store_true',
                        help="Enable testing across supplied compiler OPT level and default OPT level of build cmd")
    # parser.add_argument("-thread", "--thread",
    #                 type=int,
    #                 help="The number of maximal cycle we execute the fuzzer")
    return parser


if __name__ == '__main__':
    seed = '' 
    cmd  =''
    QL   = ''
    ENV_DICT = {}
    home_folder = None 
    build_required = None 
    opt = None 
    # inf loop until we kill 
    max_run = -1 
    parser = get_argument_parser()
    args = parser.parse_args()
    thread = 0
    if args.seed:
        seed = args.seed
        cmd = args.cmd
        QL  = args.QL
        if args.home_folder:
            ENV_DICT['home_folder'] = args.home_folder
        if args.build_required:
            ENV_DICT['build_required'] = args.build_required
        if args.max_run:
            max_run = args.max_run
        if args.opt:
            opt = args.opt
        print("[+] Parsed arg")
        print("[+] Start to fuzz !!")
        fuzz = Fuzz(seed = seed, cmd = cmd, QL = QL, ENV_DICT = ENV_DICT, diff_test= args.diff_test ,opt=opt, max_run = max_run, thread = thread)
        fuzz.run_loop()
    else:
        print("[+] No seed were found")
        exit()




#import multiprocessing 
#pool = multiprocessing.Pool(6)
#ans = pool.map(call_QL, cmd_list)
