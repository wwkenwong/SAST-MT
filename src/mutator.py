import re 
import random 
import pkg_resources
import os
import ast 
from comby import Comby
# pip3 install comby
# Tailor made rules 
from comby_rule import matching_rules_list, rule_to_replacer_dict
from utils import * 
import copy 

global USED_VAR_ID
USED_VAR_ID = []

defined_operation = ['+',"-",'%','/','^']

signed_type = {
    'int': [-2147483648, 2147483647],
    'char': [-128, 127],
    'short' : [-32768,32767],
    'long long': [-9223372036854775808, 9223372036854775807],
}

unsigned_type = {
    'unsigned int': [0, 4294967295],
    'unsigned char': [0, 255],
    'unsigned short': [0, 65535],
    'unsigned long long': [0, 18446744073709551615],
}

# Expand 

signed_type['ssize_t'] = signed_type['int']
unsigned_type['size_t'] = unsigned_type['unsigned int']

float_type = ['float', 'double']

NUM_TYPE = list(signed_type.keys()) + list(unsigned_type.keys())

def check_range(x,low,up):
    if up>=x and x>=low:
        return True 
    return False


def ret_varname():
    return "var_"+str(random.randint(0x1fffff,0xffffff))

def gen_dec_stmt(existing_var,init = None):
    '''
    existing_var: list of existing variable
    init: - if None, random to return varaible with init 
          - Otherwise -> True or False 
    return a list with TYPE and the returned statement 
    [TYPE,var,statement]
    '''
    ret_stmt = ""
    tmp_varname = ret_varname()
    test_var_flag = True 
    while test_var_flag:
        if tmp_varname in existing_var:
            tmp_varname = ret_varname()
        else:
            test_var_flag = False 
    if random.random()>0.5:
        type_list = list(unsigned_type.keys())
        type_list += list(signed_type.keys())
        TYPE = random.choice(type_list)
        if TYPE in unsigned_type.keys():
            r = unsigned_type[TYPE]
        else:
            r = signed_type[TYPE]
        NUM = random.randint(r[0],r[1])
    else:
        TYPE = random.choice(float_type)
        NUM = random.random()
        NUM += random.randint(signed_type['int'][0],signed_type['int'][1])
    ret_stmt = TYPE+" "+tmp_varname
    if init is None:
        if random.random()>0.5:
            ret_stmt += " = "+str(NUM)
    elif init == True:
        ret_stmt += " = "+str(NUM)
    ret_stmt += ';'
    return [TYPE,tmp_varname,ret_stmt] 

def guess_a_type(number_str):
    tmp_num = ast.literal_eval(number_str)
    if type(tmp_num) is int :
        type_list = list(unsigned_type.keys())
        if tmp_num < 0:
            type_list += list(signed_type.keys())
        done_flag = False
        while done_flag == False:
            test_type = random.choice(type_list)
            if test_type in unsigned_type.keys():
                res = check_range(tmp_num,unsigned_type[test_type][0],unsigned_type[test_type][1])
            else:
                res = check_range(tmp_num,signed_type[test_type][0],signed_type[test_type][1])
            if res == True:
                done_flag = True
                return test_type
    elif type(tmp_num) is float:
        return random.choice(float_type)


def ret_rebuilt_rules(rule_dict):
    '''
    0. Detect how many symbols
    1. regen variable 
    2. replace 
    3. return 
    '''
    global USED_VAR_ID
    regex = r"(.?\n)*?^(.*?)(\-\-|\+\+|\[|\.|\*=|\/=|\%=|\+=|\-=|\<\<=|\>\>=|\&=|\^=|\|=|:|=|;)"
    checker = []
    var_dict = {}
    var_type = {}
    rule_dict_local = copy.copy(rule_dict)
    matches = re.finditer(regex, rule_dict_local['rule'], re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            if groupNum == 2:
                checker.append(match.group(groupNum))
    for ixx in range(0,len(checker)):
        tmp_line = checker[ixx].split(' ')
        tmp_line = [x for x in tmp_line if len(x)>0]
        checker[ixx] = " ".join(tmp_line)
        checker[ixx] = checker[ixx].replace("for(","")
    checker = list(set(checker))
    checker = [x for x in checker if len(checker)]
    regex_for_regen = r"<%%var.*%%>"
    for xxx in checker:
        ret = re.findall(regex_for_regen,xxx)
        if len(ret)==1:
            type_str = xxx.replace(ret[0],'').replace(" ",'')
            if len(type_str)>0:
                # If is a ptr, let say int *var, 
                # type_str -> int* 
                if ret[0] not in var_dict.keys():
                    tmp_varname = ret_varname()
                    test_var_flag = True 
                    while test_var_flag:
                        if tmp_varname in USED_VAR_ID:
                            tmp_varname = ret_varname()
                        else:
                            test_var_flag = False 
                    var_dict[ret[0]] = tmp_varname
                    var_type[ret[0]] = type_str
                    USED_VAR_ID.append(tmp_varname)
    for var in var_dict.keys():
        rule_dict_local['rule'] = rule_dict_local['rule'].replace(var,var_dict[var])
    for var in var_type.keys():
        rule_dict_local['var_declar'].append({'type' : var_type[var] , 'name':var_dict[var] })
    return rule_dict_local 

# Code adpoted from universalmutator 
def parseRules(ruleFiles, comby=False):
    rulesText = []
    for ruleFile in ruleFiles:
        if ".rules" not in ruleFile:
            ruleFile += ".rules"
        try:
            if comby:
                rulePath = os.path.join('comby', ruleFile)
            else:
                rulePath = os.path.join('static', ruleFile)
            #with pkg_resources.resource_stream('universalmutator', rulePath) as builtInRule:
            path = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(path, rulePath),'rb') as builtInRule:
                builtInRule = builtInRule.readlines()
                for line in builtInRule:
                    line = line.decode()
                    rulesText.append((line, "builtin:" + ruleFile))
        except BaseException:
            print("FAILED TO FIND RULE", ruleFile, "AS BUILT-IN...")
            try:
                with open(ruleFile, 'rb') as file:
                    file = file.readlines()
                    for l in file:
                        l = l.decode()
                        rulesText.append((l, ruleFile))
            except BaseException:
                print("COULD NOT FIND RULE FILE", ruleFile + "!  SKIPPING...")
    rules = []
    ignoreRules = []
    skipRules = []
    ruleLineNo = 0
    for (r, ruleSource) in rulesText:
        ruleLineNo += 1
        if r == "\n":
            continue
        if " ==> " not in r:
            if " ==>" in r:
                s = r.split(" ==>")
            else:
                if r[0] == "#":  # Don't warn about comments
                    continue
                print("*" * 60)
                print("WARNING:")
                print("RULE:", r, "FROM", ruleSource)
                print("DOES NOT MATCH EXPECTED FORMAT, AND SO WAS IGNORED")
                print("*" * 60)
                continue  # Allow blank lines and comments, just ignore lines without a transformation
        else:
            s = r.split(" ==> ")
        
        if comby:
            lhs = s[0]
            lhs = lhs.rstrip() # Trailing whitespace in rule file will be treated significantly unless stripped, so strip it. If matching trailing whitespace is desired, then regex holes should be used.
        else:
            try:
                lhs = re.compile(s[0])
            except BaseException:
                print("*" * 60)
                print("FAILED TO COMPILE RULE:", r, "FROM", ruleSource)
                print("*" * 60)
                continue
        if (len(s[1]) > 0) and (s[1][-1] == "\n"):
            rhs = s[1][:-1]
        else:
            rhs = s[1]
        if rhs == "DO_NOT_MUTATE":
            ignoreRules.append(lhs)
        elif rhs == "SKIP_MUTATING_REST":
            skipRules.append(lhs)
        else:
            rules.append(((lhs, rhs), (r, ruleSource + ":" + str(ruleLineNo))))
    return (rules, ignoreRules, skipRules)

print("[+] Parsing the rules")
# Here, we assume we are dealing with c or cpp 
#ruleFiles = ['c_like.rules','c.rules','cpp.rules','universal.rules','equivalent.rules']
ruleFiles = ['equivalent.rules']
(rules, ignoreRules, skipRules) = parseRules(ruleFiles)
if len(rules)==0:
    print("[+] Rule parsing has error")
    exit()
else:
    print("[+] Rule parsing done :)")


def mutants(source, ruleFiles=["universal.rules"], mutateTestCode=False, mutateBoth=False,
            ignorePatterns=None, ignoreStringOnly=False, fuzzing=False,maximal_mutant = 1 ):
    #print("MUTATING WITH RULES:", ", ".join(ruleFiles))
    #(rules, ignoreRules, skipRules) = parseRules(ruleFiles)
    if ignorePatterns is not None:
        for p in ignorePatterns:
            try:
                lhs = re.compile(p)
            except BaseException:
                print("*" * 60)
                print("FAILED TO COMPILE IGNORE PATTERN:", p)
                print("*" * 60)
                continue
            ignoreRules.append(lhs)
    mutants = []
    produced = {}
    lineno = 0
    stringSkipped = 0
    inTestCode = False
    if fuzzing:
        # Pick a random target line, ignore others
        if len(source) == 0:
            return []
        targetLine = random.randrange(1, len(source) + 1)
    for l in source:
        lineno += 1
        if fuzzing and (lineno != targetLine):
            continue
        if inTestCode:
            if "@END_TEST_CODE" in l:
                inTestCode = False
            if (not mutateTestCode) and (not mutateBoth):
                continue
        else:
            if "@BEGIN_TEST_CODE" in l:
                inTestCode = True
                continue
            if mutateTestCode and (not mutateBoth):
                continue
        skipLine = False
        for lhs in ignoreRules:
            if lhs.search(l):
                skipLine = True
                break
        if skipLine:
            continue
        abandon = False
        for ((lhs, rhs), ruleUsed) in rules:
            skipPos = len(l)
            for skipRule in skipRules:
                skipp = skipRule.search(l, 0)
                if skipp and (skipp.start() < skipPos):
                    skipPos = skipp.start()
            pos = 0
            p = lhs.search(l, pos)
            while p and (pos < skipPos):
                pos = p.start() + 1
                try:
                    mutant = l[:p.start()] + lhs.sub(rhs, l[p.start():], count=1)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print("WARNING: Applying mutation raised an exception:", e)
                    print("Abandoning mutation of line", lineno)
                    abandon = True
                    break
                if mutant[-1] != "\n":
                    mutant += "\n"
                skipDueToString = False
                if ignoreStringOnly:
                    noStringsOrig = ""
                    inString = False
                    slen = 0
                    for spos in range(0, len(l)):
                        if not inString:
                            noStringsOrig += l[spos]
                            if l[spos] == '"':
                                inString = True
                                slen = 0
                        else:
                            slen += 1
                            if l[spos] == '"':
                                noStringsOrig += str(slen > 2)
                                noStringsOrig += l[spos]
                                inString = False
                    noStringsMutant = ""
                    inString = False
                    slen = 0
                    for spos in range(0, len(mutant)):
                        if not inString:
                            noStringsMutant += mutant[spos]
                            if mutant[spos] == '"':
                                inString = True
                                slen = 0
                        else:
                            slen += 1
                            if mutant[spos] == '"':
                                noStringsMutant += str(slen > 2)
                                noStringsMutant += mutant[spos]
                                inString = False
                    if noStringsOrig == noStringsMutant:
                        skipDueToString = True
                        stringSkipped += 1
                if (mutant != l) and ((lineno, mutant) not in produced) and (not skipDueToString):
                    mutants.append((lineno, mutant, ruleUsed))
                    if len(mutants) == maximal_mutant:
                        return mutants
                    produced[(lineno, mutant)] = True
                p = lhs.search(l, pos)
            if abandon:
                break
    if stringSkipped > 0:
        print("SKIPPED", stringSkipped, "MUTANTS ONLY CHANGING STRING LITERALS")
    return mutants

def makeMutant(source, mutant, path):
    lineModified = mutant[0]
    newCode = mutant[1]
    with open(path, 'w') as file:
        lineno = 0
        for l in source:
            lineno += 1
            if lineno != lineModified:
                file.write(l)
            else:
                file.write(newCode)


def wrap_universalmutator(source, path,extension = "cpp"):
    ret = []
    '''
    Universal mutator expect the input as a list 
    Return atmost 5 mutated samples 
    '''
    source_list = []
    with open(source, 'r') as file:
        for l in file:
            source_list.append(l)
    # if mutant_list is blank, we return blank list 
    mutatnt_list = mutants(source_list)
    # As UM will generate toooo much cpp
    # We will cut down some here
    if len(mutatnt_list) > 5: # 100 
        # mutatnt_list = random.sample(mutatnt_list, int(0.3*len(mutatnt_list)))
        mutatnt_list = random.sample(mutatnt_list, 5)
    # mutants.append((lineno, mutant, ruleUsed))
    for mutant in mutatnt_list:
        path_to_save = path + str(random.randint(0x1ffffff,0x7ffffff)) + "."+extension
        makeMutant(source_list, mutant, path_to_save)
        ret.append(path_to_save)
    return ret 


def makeMutantComby(source, mutant, path = None):
    '''
    adopted from universal mutator 
    source -> source code joined 
    '''
    sourceBeforeFragment = source[:mutant[0][0]]
    sourceAfterFragment = source[mutant[0][1]:]
    mutantSource = sourceBeforeFragment + mutant[1] + sourceAfterFragment
    if path is not None:
        with open(path, 'w') as file:
            file.write(mutantSource)
    return mutantSource


def all_comby_rewrite_mutation(source,matching_rules,replacing_rules,folder,extension = "cpp"):
    '''
    Replace all matched 
    With a single transformation
    return a list of path for generated new corpus 
    '''
    ret = []
    comby = Comby()
    test = list(comby.matches(source, matching_rules))
    if len(test)>0:
        source_new = comby.rewrite(source, matching_rules, replacing_rules)
        path = folder + str(random.randint(0x1ffffff,0x7ffffff)) + "."+extension
        fs = open(path,'w')
        fs.write(source_new)
        fs.close()
        ret.append(path)
    return ret 


def individual_comby_mutation(source,matching_rules,replacing_rules,folder,extension = "cpp",rand=False,maximal_mutant = 1):
    '''
    Apply rules to individual rules 
    if rand to True, we random pick some mutation 
    It return a list of path for generated new corpus 
    else we will return blank list 
    '''
    ret = []
    comby = Comby()
    test = list(comby.matches(source, matching_rules))
    if len(test)>0:
        mutants = []
        for match in test:
            environment = dict()
            for entry in match.environment:
                environment[entry] = match.environment.get(entry).fragment
            mutant = comby.substitute(replacing_rules, environment)
            substitutionRange = (match.location.start.offset, match.location.stop.offset)
            lineRange = (match.location.start.line, match.location.stop.line)
            mutants.append((substitutionRange, mutant,lineRange))
        for mutant in mutants:
            path = folder + str(random.randint(0x1ffffff,0x7ffffff)) + "."+extension
            makeMutantComby(source, mutant, path)
            ret.append(path)
            if len(ret) == maximal_mutant:
                return ret 
    return ret 

def comby_driver(source,savepath,extension = "cpp"):
    '''
    source -> str input for the seed going to mutate
    savepath -> str path that pointed to the folder for saving the corpus 
    '''
    comby = Comby()
    # The matching rule that failed 
    failed = []
    # 1. We do a pre-test first 
    # And pass the rule for mutation 
    matched = False
    failed_ctr = 0
    matching_rules = ""
    while not matched and len(matching_rules_list)!=len(failed):
        # Randomly got a matching_rules
        tmp_flag = False
        matching_rules = random.choice(matching_rules_list)	 
        test = list(comby.matches(source, matching_rules))
        if len(test)>0: 
            matched = True 
        else:
            failed.append(matching_rules)
            failed_ctr += 1 
            if failed_ctr > 5:
                # If failed, we return a blank list 
                return []
    replacing_rules_dict = random.choice(rule_to_replacer_dict[matching_rules])
    replacing_rules = ret_rebuilt_rules(replacing_rules_dict)
    ret = individual_comby_mutation(source,matching_rules,replacing_rules['rule'],savepath,extension)
    return ret 
