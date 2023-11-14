import os 
import re 

operator_list = ['+' , '-' , '*' , '/' , '%' , '^' , '&' , '|' , '~' , 
                 '!' , '=' , '<' , '>' , '+=' , '-=' , '*=' , '/=' , '%=' , 
                 '^=' , '&=' , '|=' , '<<' , '>>' , '>>=' , '<<=' , '==' , 
                 '!=' , '<=' , '>=' , '&&' , '||' , ',']

def open_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def all_file_under_path(rootFolderPath):
    ret = []
    for root, dirs, files in os.walk(rootFolderPath):
        for filename in files:
            ret.append(os.path.join(root, filename))
    return ret 

# If we have clang-format, we call by this
# for inplace removal 
# clang-format -style=LLVM -i main.cpp
def call_clang_format_inplace(codename):
    cmd = 'clang-format -style=LLVM -i '+codename
    os.system(cmd)

# if clang-format not found, we use the following code 

def comment_remover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " " # note: a space and not an empty string
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)

def call_regex_format_inplace(codename):
    src_code = open(codename).read()
    src_code = comment_remover(src_code)
    src_code = re.sub('\s+;',';', src_code)
    src_code = re.sub('\s+:',':', src_code)
    for op in operator_list:
        src_code = re.sub('\s+'+op+'\s+',' '+op+' ', src_code)
    fs = open(codename,'w')
    fs.write(src_code)
    fs.close()


