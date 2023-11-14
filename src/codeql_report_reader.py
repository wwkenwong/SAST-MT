import glob 

# ([0-9a-fA-F]:?){8} REGEX for getting intermediate step's line and file 


def parse_QL_csv(csv_name):
    '''
    Input the csv name, out put a list of buggy lines found 
    Here, we will ignore the dataflow 
    '''
    ret = []
    csv_tmp = open(csv_name).read()
    if len(csv_tmp)>0:
        csv_tmp = csv_tmp.split('\n')
        csv_tmp = [x for x in csv_tmp if len(x)>0]
        for line in csv_tmp:
            # The last 5 items included
            # The line number and the c or cpp 
            # That detected the crash 
            ret.append(line[-5:])
    return ret

# def parse_QL_SARIF():
#     return 

# def check_failure(csv_tocheck):


# csv_results = glob.glob('*.csv')

# TEST_TARGET = []

# for subcsv in csv_results:
#     ret = parse_QL_csv(subcsv)
#     if len(ret)>0:
#         TEST_TARGET.append({'name':subcsv,'bug_site':ret})

'''
>>> len(csv_results)
35559
>>> len(TEST_TARGET)
5189
>>> 5189/35559
0.145926488371439
'''

