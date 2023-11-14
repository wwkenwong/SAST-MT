import re
from Config import * 
from tree_sitter import Language, Parser
from tree_sitter import Node, Parser, Tree, TreeCursor
from collections import namedtuple
from mutator import * 
import random

OP_CODE = {'ELLIPSIS': '("...")', 'RIGHT_ASSIGN': '(">>=")', 'LEFT_ASSIGN': '("<<=")', 
           'ADD_ASSIGN': '("+=")', 'SUB_ASSIGN': '("-=")', 'MUL_ASSIGN': '("*=")', 
           'DIV_ASSIGN': '("/=")', 'MOD_ASSIGN': '("%=")', 'AND_ASSIGN': '("&=")', 
           'XOR_ASSIGN': '("^=")', 'OR_ASSIGN': '("|=")', 'RIGHT_OP': '(">>")', 
           'LEFT_OP': '("<<")', 'INC_OP': '("++")', 'DEC_OP': '("--")', 
           'PTR_OP': '("->")', 'AND_OP': '("&&")', 'OR_OP': '("||")', 'LE_OP': '("<=")', 
           'GE_OP': '(">=")', 'EQ_OP': '("==")', 'NE_OP': '("!=")', 'INST_END': '(";")', 
           'BEGIN': '("{")', 'END': '("}")', 'COMMA': '(",")', 'COLUMN': '(":")', 
           'EQ': '("=")', 'P_OPEN': '("(")', 'P_CLOSE': '(")")', 'B_OPEN': '("[")', 
           'B_CLOSE': '("]")', 'DOT': '(".")', 'AND': '("&")', 'NOT': '("!")', 
           'NEG': '("~")', 'LESS_SIG': '("-")', 'PLUS_SIG': '("+")', 
           'MUL': '("*")', 'DIV': '("/")', 'MOD': '("%")', 'LESS': '("<")', 
           'GREATER': '(">")', 'XOR': '("^")', 'OR': '("|")', 'QUESTION': '("?")'}

OP_CODE_reverse = {}

for key, value in OP_CODE.items():
    OP_CODE_reverse[value] = key

def parse_assignment_expression(code,node):
    '''
    BNF: 
    _assignment_left_expression ::=  ( identifier |  call_expression |  field_expression 
                                    |  pointer_expression |  subscript_expression 
                                    |  parenthesized_expression )
    assignment_expression ::=   (  ( (  _assignment_left_expression )  
                            ( '='  |  '*='  |  '/='  |  '%='  |  '+='  |  '-='  |  '<<='  
                            |  '>>='  |  '&='  |  '^='  |  '|='  )  
                            (  _expression )  )  )
    The left must the use
    Middle determine the operation 
    Right will be operation / wtever 
    '''
    ret = {}
    ret['left']  = node.child_by_field_name('left')
    try:
        ret['OP']    = OP_CODE_reverse[node.children[1].sexp()]
    except:
        # For loop case 
        ret['OP']    = None 
    ret['right'] = node.child_by_field_name('right')
    return ret 

def get_type(cursor, came_up, type_to_get):
    '''
    Using DFS to travere the AST tree
    '''
    ret = None 
    if cursor.node.type == type_to_get:
        return cursor.node
    if not came_up:
        if (cursor.goto_first_child()):
            ret = get_type(cursor, False, type_to_get)
        elif (cursor.goto_next_sibling()):
            ret = get_type(cursor, False, type_to_get)
        elif (cursor.goto_parent()):
            ret = get_type(cursor, True, type_to_get)
    else:
        if (cursor.goto_next_sibling()):
            ret = get_type(cursor, False, type_to_get)
        elif (cursor.goto_parent()):
            ret = get_type(cursor, True, type_to_get)
    return ret


def ret_type_list(node, type_to_get):
    '''
    Driver for collecting the required type Node
    '''
    cursor = node.walk()
    ret_list = []
    while True:
        tmp_node = get_type(cursor, False, type_to_get)
        if tmp_node is not None:
            ret_list.append(tmp_node)
        if (not cursor.goto_next_sibling()):
            break 
    return ret_list

def ret_str(code,node):
    '''
    Return the string version of the node 
    '''
    if node is not None:
        return code[node.start_byte:node.end_byte]
    else:
        return "FAiL3D" 

def ret_is_x(str_stmt,x):
    ctr = 0 
    for z in str_stmt:
        if z == '*':
            ctr += 1
    return ctr 

def dump_identifier(cursor, came_up, fn):
    if len(cursor.node.children) == 0:
        fn.append(cursor.node)
        # print(ret_str(code,cursor.node))
        # print(cursor.node.type)
        # print('-'*10)
    if not came_up:
        if (cursor.goto_first_child()):
            dump_identifier(cursor, False, fn)
        elif (cursor.goto_next_sibling()):
            dump_identifier(cursor, False, fn)
        elif (cursor.goto_parent()):
            dump_identifier(cursor, True, fn)
    else:
        if (cursor.goto_next_sibling()):
            dump_identifier(cursor, False, fn)
        elif (cursor.goto_parent()):
            dump_identifier(cursor, True, fn)

# var_struct(name = ,type = ,name_ptr = ,type_ptr = ,def_ptr = ,use =)
var_struct = namedtuple('var_struct', 'name type name_ptr type_ptr def_ptr \
                                        use POINTER_TYPE REF_TYPE IS_ARRAY ARRAY_SIZE')

'''
name : Name of the variable in string 
type : Type of the variable in string 
name_ptr : The pointer to the name of the ptr in the def site
type_ptr : The pointer to the type of the ptr in the def site
def_ptr : The pointer to statement of the def site
use : A list of list for ptr towards the statement of the use case, sorted by ascending order before use,
      Where [point of use, stmt] 
        - 0 is the exact location for the use of variable
        - 1 is the statement for it happens 
POINTER_TYPE : Naive check if the var is a pointer (we count how many *), 0 for non-pointer type  
REF_TYPE : Check if it is a var of pass-by-reference 
IS_ARRAY : True or False 
ARRAY_SIZE : if IS_ARRAY True, we analysis this 
'''

class Function():
    def __init__(self, tree_ptr,code_str):
        '''
        tree ptr is the cursor from tree sitter 
        '''
        self.function_blk_ptr = tree_ptr
        self.code  = code_str
        # The dict for argument passed into the function 
        # Map to var_struct
        self.arg = {}
        # The dict for variable def-use in the function 
        # Map to var_struct
        self.var = {}
        # Dict to possible a call for global function 
        self.possible_global = {}
        # Item to be inserted with location 
        # Like will be stored as a dict???
        self.to_be_inserted = []
        # Function to stmt list 
        self.stmt_list = []
        # Function called dict
        self.function_called = []
        # Location of numeric 
        self.number_literal = []
        # Function called name str to stmt 
        self.function_called_to_stmt = {}
        # Function type as pointer 
        self.function_type_ptr = None
        # Function type as string 
        self.function_type_str = None
        # Function name as pointer 
        self.function_name_ptr = None
        # Function name as string 
        self.function_name_str = None
        # Trigger analysis 
        self.function_analysis()

    def function_analysis(self):
        '''
        1. Analysis the imported arg 
            - Imported arg shd added to def part,  
        '''
        self.basic_analysis()
    
    def basic_analysis(self):
        '''
        Analysis basic infomration for a function
        Expected not to be updated once analysis has done 
        Parse the arg of the function 
        '''
        # Function type as pointer and string
        self.function_type_ptr = self.function_blk_ptr.child_by_field_name('type')
        self.function_type_str = ret_str(self.code,self.function_type_ptr)

        # Get the function dec
        function_dec  = self.function_blk_ptr.child_by_field_name('declarator')

        # Function name as pointer and string
        self.function_name_ptr = function_dec.child_by_field_name('declarator')
        self.function_name_str = ret_str(self.code,self.function_name_ptr)
        
        func_parm  = function_dec.child_by_field_name('parameters')
        parm_list = ret_type_list(func_parm, 'parameter_declaration')
        if len(parm_list)>0:
            for idx in range(0,len(parm_list)):
                type_ptr = parm_list[idx].child_by_field_name('type')
                name_ptr = parm_list[idx].child_by_field_name('declarator')
                type_str = ret_str(self.code,type_ptr)
                # As the * and & will be on the declarator side, for mapping
                # We will need strip away 
                name_str = ret_str(self.code,name_ptr)
                name_str__for_key = name_str.replace('*','').replace('&','')
                var_tmp = var_struct(name = name_str__for_key,
                                     type = type_str,
                                     name_ptr = name_ptr,
                                     type_ptr = type_ptr,
                                     def_ptr = parm_list[idx],
                                     use = [],
                                     POINTER_TYPE = len(re.findall('\*',name_str)),
                                     REF_TYPE = len(re.findall('\&',name_str)),
                                     IS_ARRAY = False,
                                     ARRAY_SIZE = None, 
                                     )
                self.arg[name_str__for_key] = var_tmp
                self.var[name_str__for_key] = var_tmp
        # Function name as pointer and string

        # Get the ptr of declaration 
        function_stmt = self.function_blk_ptr.child_by_field_name('body')
        # Generate def 
        def_list = ret_type_list(function_stmt, 'declaration')
        if len(def_list)>0:
            for i in range(0,len(def_list)):
                self.stmt_list.append(def_list[i])
                line_type = None 
                # 0 We get all the identifier
                identifier_var = ret_type_list(def_list[i],'identifier')
                # Check if any function is being called 
                func_called = ret_type_list(def_list[i],'call_expression')
                for func in func_called:
                    if func.child_count > 0:
                        func_name_str = ret_str(self.code,func.children[0])
                        self.function_called.append(func_name_str)
                        # Function called name str to stmt 
                        if func_name_str not in self.function_called_to_stmt.keys():
                            self.function_called_to_stmt[func_name_str] = []
                        self.function_called_to_stmt[func_name_str].append(func)
                #type_list_tmp = ret_type_list(def_list[i],'primitive_type')
                # From grammar, only 1 type can be found 
                if len(identifier_var) >0 :
                    # 1 Got the earliest identifier 
                    tmp_identifier = None 
                    tmp_identifier_st_byte = 9999999999999 
                    for n in identifier_var:
                        if tmp_identifier_st_byte > n.start_byte:
                            tmp_identifier = n 
                            tmp_identifier_st_byte = n.start_byte 
                    # 2. Got the type 
                    layer_tmp = 0 
                    type_fail = False 
                    while tmp_identifier.prev_sibling == None and type_fail == False:
                        layer_tmp += 1 
                        if layer_tmp == 3:
                            type_fail = True 
                        tmp_identifier = tmp_identifier.parent
                    line_type = tmp_identifier.prev_sibling
                    print(ret_str(self.code,line_type))
                    ptr_level = 0
                    if ret_str(self.code,line_type)[0] == "*":
                        # Do a full dump to obtain the pointer type 
                        tmp_type_check_list = []
                        cursor = def_list[i].walk()
                        dump_identifier(cursor, False, tmp_type_check_list)
                        # Get the index of the pointer in the dumped identifier 
                        ptr_level = 1 
                        index_ptr = tmp_type_check_list.index(line_type)
                        type_parse_flag = False
                        tmp_type = None 
                        while not type_parse_flag:
                            if index_ptr - 1 >=0:
                                index_ptr -= 1 
                                line_type = tmp_type_check_list[index_ptr]
                                if ret_str(self.code,line_type)[0] == "*" :
                                    ptr_level += 1 
                                elif ret_str(self.code,line_type)[0] == ")" or  ret_str(self.code,line_type)[0] == "(" or ret_str(self.code,line_type)[-1] == "(":
                                    pass 
                                else:
                                    type_parse_flag = True 
                            else:
                                # We use the previous result as the type 
                                type_parse_flag = True 
                        print("[+] Fixed pointer type "+ret_str(self.code,line_type))
                    # Variable appears in the bracket will be a use, rather than def 
                    object_init = False 
                    object_init_use_st_byte = None 
                    object_init_use_end_byte = None 
                    use_of_var = []
                    for n in identifier_var:
                        # The case of xxx(a,b,c)
                        if n not in use_of_var:
                            # Creating the defintition 
                            type_ptr = line_type
                            type_str = ret_str(self.code,line_type)
                            name_ptr = n
                            name_str = ret_str(self.code,name_ptr)
                            name_str__for_key = name_str.replace('*','').replace('&','')
                            IS_ARRAY = False
                            ARRAY_SIZE = None
                            print('[+] Doing '+ret_str(self.code,n))
                            if len(ret_str(self.code,n.next_sibling)) > 0:
                                if ret_str(self.code,n.next_sibling) == '[':
                                    IS_ARRAY = True 
                                    # check if it is a size OR only an init 
                                    if ret_str(self.code,n.next_sibling.next_sibling) == ']':
                                        if ret_str(self.code,n.next_sibling.next_sibling.parent.next_sibling) != '=':
                                            print(ret_str(self.code,n)+" is an Array declaration")
                                        else:
                                            print(ret_str(self.code,n)+" is an Array init with "+ret_str(self.code,n.next_sibling.next_sibling.parent.next_sibling.next_sibling))
                                    elif n.next_sibling.next_sibling.type == 'number_literal':
                                        if ret_str(self.code,n.next_sibling.next_sibling.next_sibling) == ']':
                                            if ret_str(self.code,n.next_sibling.next_sibling.next_sibling.parent.next_sibling) != '=':
                                                print(ret_str(self.code,n)+" is an Array declaration with size "+ret_str(self.code,n.next_sibling.next_sibling))
                                                ARRAY_SIZE = n.next_sibling.next_sibling
                                            else:
                                                print(ret_str(self.code,n)+" is an Array with size "+ret_str(self.code,n.next_sibling.next_sibling)+" and init with "+ret_str(self.code,n.next_sibling.next_sibling.parent.next_sibling.next_sibling))
                                                print('The identifier presents: '+str(ret_type_list(n.next_sibling.next_sibling.parent.next_sibling.next_sibling, 'identifier')))
                                                ARRAY_SIZE = n.next_sibling.next_sibling
                                        else:
                                            print(ret_str(self.code,n)+" is an Array with size: "+ret_str(self.code,n.next_sibling.next_sibling))
                                elif ret_str(self.code,n.next_sibling) == ',':
                                    print(ret_str(self.code,n)+" is an variable init")
                                elif ret_str(self.code,n.next_sibling) == '=':
                                    print(ret_str(self.code,n)+" is an variable assigned with "+ret_str(self.code,n.next_sibling.next_sibling))
                                    if n.next_sibling.next_sibling.type == 'number_literal':
                                        self.number_literal.append(n.next_sibling.next_sibling)
                                elif ret_str(self.code,n.next_sibling)[0] == '(' or ret_str(self.code,n.next_sibling)[0] == '{' :
                                    # Case for vector OR Object creation with def varoable 
                                    var_dumped_tmp = ret_type_list(n.next_sibling,'identifier')
                                    for n_tmp in var_dumped_tmp:
                                        use_of_var.append(n_tmp)
                                        # print("Used var -> "+ret_str(self.code,n_tmp))
                                var_tmp = var_struct(name = name_str__for_key,
                                                type = type_str,
                                                name_ptr = name_ptr,
                                                type_ptr = type_ptr,
                                                def_ptr = def_list[i], # We point it to the line 
                                                use = [],
                                                POINTER_TYPE = ptr_level,
                                                REF_TYPE = len(re.findall('\&',name_str)),
                                                IS_ARRAY = IS_ARRAY,
                                                ARRAY_SIZE = ARRAY_SIZE, 
                                                )
                                if name_str__for_key not in self.var.keys():
                                    # We only update the first existance 
                                    self.var[name_str__for_key] = var_tmp
                                else:
                                    self.var[name_str__for_key].use.append([n,def_list[i]])
                            else:
                                print("[+] Weird variable ")
        # Get the use 
        exp_list = ret_type_list(function_stmt, 'expression_statement')
        for i in range(0,len(exp_list)):
            self.stmt_list.append(exp_list[i])
            func_called = ret_type_list(exp_list[i],'call_expression')
            for func in func_called:
                if func.child_count > 0:
                    func_name_str = ret_str(self.code,func.children[0])
                    self.function_called.append(func_name_str)
                    # Function called name str to stmt 
                    if func_name_str not in self.function_called_to_stmt.keys():
                        self.function_called_to_stmt[func_name_str] = []
                    self.function_called_to_stmt[func_name_str].append(func)
            if exp_list[i].children[0].type != 'assignment_expression':
                identifier_var = ret_type_list(exp_list[i],'identifier')
                for ident in identifier_var:
                    # detect if next is a "("
                    # It implies its a function call 
                    check_next = ret_str(self.code,ident.next_sibling)
                    if not check_next.startswith('('):
                        print("Use: "+ret_str(self.code,ident))
                        var_str = ret_str(self.code,ident)
                        if var_str in self.var.keys():
                            self.var[var_str].use.append([ident,exp_list[i]])
                        elif var_str in self.arg.keys():
                            self.arg[var_str].use.append([ident,exp_list[i]])
                        else:
                            if var_str not in self.possible_global.keys():
                                var_tmp = var_struct(name = var_str,
                                                type = None,
                                                name_ptr = ident,
                                                type_ptr = None,
                                                def_ptr = None, 
                                                use = [],
                                                POINTER_TYPE = None,
                                                REF_TYPE = 0,
                                                IS_ARRAY = False,
                                                ARRAY_SIZE = None, 
                                                )
                                self.possible_global[var_str] = var_tmp
                            # If we can't find the variable, maybe it is a global varaible 
                            self.possible_global[var_str].use.append([ident,exp_list[i]])
            else:
                ret = parse_assignment_expression(self.code,exp_list[i].children[0])
                tmp_stmt = []
                for key in ret.keys():
                    if key == 'right' or key == 'left':
                        if ret[key].type == 'identifier':
                            # Link to the use 
                            var_str = ret_str(self.code,ret[key])
                            if var_str in self.var.keys():
                                self.var[var_str].use.append([ret[key],exp_list[i]])
                            elif var_str in self.arg.keys():
                                self.arg[var_str].use.append([ret[key],exp_list[i]])
                            else:
                                if var_str not in self.possible_global.keys():
                                    var_tmp = var_struct(name = var_str,
                                                    type = None,
                                                    name_ptr = ret[key],
                                                    type_ptr = None,
                                                    def_ptr = None, 
                                                    use = [],
                                                    POINTER_TYPE = None,
                                                    REF_TYPE = 0,
                                                    IS_ARRAY = False,
                                                    ARRAY_SIZE = None, 
                                                    )
                                    self.possible_global[var_str] = var_tmp
                                # If we can't find the variable, maybe it is a global varaible 
                                self.possible_global[var_str].use.append([ret[key],exp_list[i]])
                        elif ret[key].type == 'number_literal':
                            # Link to num 
                            self.number_literal.append(ret[key])
                        else:
                            tmp_check_list = []
                            cursor = ret[key].walk()
                            dump_identifier(cursor, False, tmp_check_list)
                            tmp_stmt.append(tmp_check_list)
                # Parsing 
                if len(tmp_stmt)>0:
                    for st in tmp_stmt:
                        for token in st:
                            if token.type == 'identifier':
                                check_next = ret_str(self.code,token.next_sibling)
                                if not check_next.startswith('('):
                                    var_str = ret_str(self.code,token)
                                    if var_str in self.var.keys():
                                        self.var[var_str].use.append([token,exp_list[i]])
                                    elif var_str in self.arg.keys():
                                        self.arg[var_str].use.append([token,exp_list[i]])
                                    else:
                                        if var_str not in self.possible_global.keys():
                                            var_tmp = var_struct(name = var_str,
                                                            type = None,
                                                            name_ptr = token,
                                                            type_ptr = None,
                                                            def_ptr = None, 
                                                            use = [],
                                                            POINTER_TYPE = None,
                                                            REF_TYPE = 0,
                                                            IS_ARRAY = False,
                                                            ARRAY_SIZE = None, 
                                                            )
                                            self.possible_global[var_str] = var_tmp
                                        # If we can't find the variable, maybe it is a global varaible 
                                        self.possible_global[var_str].use.append([token,exp_list[i]])
                            elif token.type == 'number_literal':
                                check_prev = ret_str(self.code,token.prev_sibling)
                                if not check_prev.startswith('['):
                                    self.number_literal.append(token)
                #print("dumped assignment_expression "+str(ret))


class Program():
    def __init__(self, code_str,lang = "cpp"):
        lang_set = None 
        if lang in LOCAITON_TO_TREE_SITTER.keys():
            lang_set = Language(LOCAITON_TO_TREE_SITTER[lang], lang)
        else:
            print("Language pack is missing ")
            exit()
        self.parser = Parser()
        self.parser.set_language(lang_set)
        self.code  = code_str
        self.codetree = self.parse(code_str)
        # variable analyzed 
        self.var = []
        # For cpp, we use Function to handle here 
        # Generated variable
        self.generated_var = []
        # Stored the type of the var 
        # self.var_to_type = {}
        # The fragment or snippet for modification 
        # {'coord' : (2,1), 'code' : "" , "replace" : True}
        self.modified_fragment = []
        # List of function available 
        self.function = {}
        # List of Global variable 
        self.global_stmt = []
        # List of defintion 
        self.def_stmt = []
        # List to TAGGED -> [TAG,CODE] 
        self.TAGGED = []

        self.analysis()
        self.mutator_pass = [ 
            self.mutator_local_def_to_global,
            self.mutator_dec_to_global,
            self.mutator_return_const_with_function,
            self.mutator_return_var_with_function,
        ]

    def parse(self,code_str):
        '''
        Parse code in the form of string
        To the tree sitter structure 
        '''
        tree = self.parser.parse(bytes(code_str,"utf8"))
        return tree 

    def commit(self):
        '''
        0. Load the code changes from modified_fragment
        1. Apply the change 
        2. Reparse it
        '''
        # sort 
        new_code_str = ""
        # movable
        st_pt = 0 
        end_pt = len(self.code)
        # hardcoded
        old_end = len(self.code)
        # {'coord' : (2,1), 'code' : "" , "replace" : True}
        # coord -> The old code needed to replace 
        # code -> new content 
        self.modified_fragment = sorted(self.modified_fragment, key=lambda x: x['coord'][0])
        for fragment in self.modified_fragment:
            # append 
            if fragment['replace'] == False:
                # if fragment['coord'][0] equals to 0, it will become -1 
                end_pt = max(0,fragment['coord'][0] )
                new_code_str += self.code[st_pt:end_pt] + fragment['code']
                st_pt = fragment['coord'][1]
        new_code_str += self.code[st_pt:old_end]
        self.modified_fragment = []
        self.code = new_code_str
        self.codetree = self.parse(self.code)

    def commit_by_tag(self,tag,code_to_add):
        '''
        Given a tag, replace the tag with the code
        tag examples:  
        GLOBAL_HERE
        FUNC_HERE
        '''
        if "//" not in tag:
            tag = "//" + tag
        self.code = self.code.replace(tag,code_to_add+"\n"+tag+'\n')
        self.codetree = self.parse(self.code)

    def commit_by_tag_batch(self):
        # [TAG,CODE] 
        for item in self.TAGGED:
            self.commit_by_tag(item[0],item[1])
        self.TAGGED = []

    def analysis(self):
        '''
        Success analysis will return True, else will give a false
        Then let the caller to stop 
        0. call gen_import_tag 
        '''
        if self.gen_import_tag():
            self.commit()
        if not self.gen_function_list():
            return False
        self.global_variable_analysis()
        return True 

    def gen_import_tag(self):
        '''
        0. Check if certain import exist, if not, got the location to place the import 
           and place an import tag <IMPORT>
        1. Return a true if we need fix the import 
        '''
        IMPORT_STR = "\n"
        ST_POINT = -99999
        EDITED = False
        for lib in INCLUDE:
            if lib not in self.code:
                EDITED = True 
                IMPORT_STR += "#include <"+str(lib)+">\n"
        for api in API:
            if api not in self.code:
                EDITED = True 
                IMPORT_STR += str(api)+"\n"
        # Enable global insertion 
        for tag in REWRITE_TAG:
            if tag not in self.code:
                EDITED = True 
                if "//" not in tag:
                    tag = "//"+tag
                IMPORT_STR += "\n"+tag+"\n\n"
        if EDITED:
            '''
            0. Get the location of last spot
                We have 2 case 
                If not, simply set last location to 0  
            1. append the last location to the self.modified_fragment
            '''
            include_list = []
            try:
                # Will trigger maximal recursion if no header 
                include_list = ret_type_list(self.codetree, 'preproc_include')
            except:
                pass 
            if len(include_list)>0:
                ST_POINT = include_list[-1].end_byte
            else:
                ST_POINT = 0 
            self.modified_fragment.append({'coord' : (ST_POINT,ST_POINT), 'code' : IMPORT_STR+"\n" , "replace" : False})
            return True 
        return False 

    def gen_function_list(self):
        func_list = ret_type_list(self.codetree, 'function_definition')
        if len(func_list) == 0:
            return False 
        else:
            min_func_st = 99999999999
            self.var = []
            self.def_stmt = []
            for fp in func_list:
                min_func_st = min(min_func_st,fp.start_byte)
                fp_tmp = Function(fp,self.code)
                # Use string to point it to function pointer 
                self.function[fp_tmp.function_name_str] = fp_tmp
                # Update the list of variable
                for varname in fp_tmp.var.keys():
                    self.var.append(varname)
                    self.def_stmt.append(fp_tmp.var[varname].def_ptr)
            return True 
    
    def global_variable_analysis(self):
        def_list = ret_type_list(self.codetree, 'declaration')
        func_bound_list = []
        self.global_stmt = []
        for func_name in self.function.keys():
            func_bound_list.append((self.function[func_name].function_blk_ptr.start_byte,self.function[func_name].function_blk_ptr.end_byte))
        for stmt in def_list:
            if stmt not in self.def_stmt:
                # We just assume global variable will declear like 
                # TYPE var mannaer
                # We skipped the function and constructor case
                # Not in (  and not within range of function 
                if "(" not in ret_str(self.code,stmt):
                    bounded = False
                    for r in func_bound_list:
                        if stmt.start_byte > r[0] and r[1] > stmt.start_byte:
                            bounded = True 
                            break 
                    if bounded == False:
                        self.global_stmt.append(stmt)
                    # Extract the statement ???
    
    def save_to_file(self,path):
        fs = open(path,'w')
        fs.write(self.code)
        fs.close()

    def mutation_pipeline(self,folder,extension = "cpp"):
        go = random.randint(1,6)
        if   go == 1:
            ret = self.mutator_local_def_to_global()
        elif go == 2:
            ret = self.mutator_dec_to_global()
        elif go == 3:
            ret = self.mutator_single_for_loop()
        elif go == 4:
            ret = self.mutator_return_var_with_max_min()
        elif go == 5:
            ret = self.mutator_return_number_with_max_min()
        else:
            ret = self.mutator_local_redefine()
        if ret:
            print("TREE-SITTER Mutation works")
            path = folder + str(random.randint(0x1ffffff,0x7ffffff)) + "."+extension
            self.save_to_file(path)
        else:
            path= ""
        return path


    def random_obtain_defined_function(self):
        if len(list(self.function.keys()))>0:
            func_name_tmp = random.choice(list(self.function.keys()))
            return func_name_tmp
        else:
            return -1 

    def mutator_array_and_arg_predicate(self):
        # Get an arg OR array constant 
        # Suck to a int unsat predicate 
        return True
    
    def mutator_gen_predicate(self,func_name_tmp = None,ran_var_name_tmp = None):
        done_var = False 
        fail_cnt = 0 
        PREPARED = False
        if func_name_tmp is not None:
            PREPARED = True 
        while done_var == False:
            if func_name_tmp is None:
                name_tmp = self.random_obtain_defined_function()
                if name_tmp != -1:
                    func_name_tmp = name_tmp
            if ran_var_name_tmp is None and func_name_tmp is not None :
                if len(list(self.function[func_name_tmp].var.keys()))>0:
                    ran_var_name_tmp = random.choice(list(self.function[func_name_tmp].var.keys()))
                    # check if it got a use 
                    if ran_var_name_tmp is not None:
                        if len(self.function[func_name_tmp].var[ran_var_name_tmp].use)>0:
                            use_site = random.choice(self.function[func_name_tmp].var[ran_var_name_tmp].use)
                else:
                    fail_cnt += 1 
                    if not PREPARED:
                        func_name_tmp = None 
                    ran_var_name_tmp = None 
                    if fail_cnt > 10:
                        return False 

    def mutator_single_for_loop(self,func_name_tmp = None,ran_var_name_tmp = None):
        done_var = False 
        fail_cnt = 0 
        PREPARED = False
        if func_name_tmp is not None:
            PREPARED = True 
        while done_var == False:
            if func_name_tmp is None:
                name_tmp = self.random_obtain_defined_function()
                if name_tmp != -1:
                    func_name_tmp = name_tmp
            if ran_var_name_tmp is None and func_name_tmp is not None :
                if len(list(self.function[func_name_tmp].var.keys()))>0:
                    ran_var_name_tmp = random.choice(list(self.function[func_name_tmp].var.keys()))
                    # check if it got a use 
                    if ran_var_name_tmp is not None:
                        if len(self.function[func_name_tmp].var[ran_var_name_tmp].use)>0:
                            use_site = random.choice(self.function[func_name_tmp].var[ran_var_name_tmp].use)
                else:
                    fail_cnt += 1 
                    if not PREPARED:
                        func_name_tmp = None 
                    ran_var_name_tmp = None 
                    if fail_cnt > 10:
                        return False 
            elif ran_var_name_tmp is not None and func_name_tmp is not None :
                if ran_var_name_tmp is not None:
                    if len(list(self.function[func_name_tmp].var[ran_var_name_tmp].use))>0:
                        use_site_tmp = random.choice(self.function[func_name_tmp].var[ran_var_name_tmp].use)
                        print(ret_str(self.code,use_site_tmp[1]))
                        ret = parse_assignment_expression(self.code,use_site_tmp[1].children[0])
                        print(ret)
                        if use_site_tmp[0] != ret['left']:
                            done_var = True 
                            use_site = use_site_tmp
                        else:
                            fail_cnt += 1 
                            if not PREPARED:
                                func_name_tmp = None 
                            ran_var_name_tmp = None 
                            if fail_cnt > 10:
                                return False 
                    else:
                        fail_cnt += 1 
                        if not PREPARED:
                            func_name_tmp = None 
                        ran_var_name_tmp = None 
                        if fail_cnt > 10:
                            return False 
                else:
                    fail_cnt += 1
                    if not PREPARED:   
                        func_name_tmp = None 
                    ran_var_name_tmp = None 
                    if fail_cnt > 10:
                        return False 
            else:
                fail_cnt += 1 
                if not PREPARED:
                    func_name_tmp = None 
                ran_var_name_tmp = None 
                if fail_cnt > 10:
                    return False 
        loop_ctr = ret_varname() 
        for_str  = "for (int " 
        for_str += loop_ctr +" = 0 ; "+loop_ctr+"<1;" + loop_ctr+"++){\n"
        for_str += ret_str(self.code,use_site[1])
        if not for_str.endswith(';'):
            for_str+";"
        for_str += "}"
        ST_POINT = use_site[1].start_byte
        ED_POINT = use_site[1].end_byte
        self.modified_fragment.append({'coord' : (ST_POINT,ED_POINT), 'code' : for_str , "replace" : False})
        self.commit()
        return True

    def mutator_return_var_with_max_min(self,func_name_tmp = None,ran_var_name_tmp = None):
        done_var = False 
        fail_cnt = 0 
        PREPARED = False
        if func_name_tmp is not None:
            PREPARED = True 
        while done_var == False:
            if func_name_tmp is None:
                name_tmp = self.random_obtain_defined_function()
                if name_tmp != -1:
                    func_name_tmp = name_tmp
            if ran_var_name_tmp is None and func_name_tmp is not None :
                if len(list(self.function[func_name_tmp].var.keys()))>0:
                    ran_var_name_tmp = random.choice(list(self.function[func_name_tmp].var.keys()))
                    # check if it got a use 
                    if ran_var_name_tmp is not None:
                        if len(self.function[func_name_tmp].var[ran_var_name_tmp].use)>0:
                            use_site_tmp = random.choice(self.function[func_name_tmp].var[ran_var_name_tmp].use)
                            print(ret_str(self.code,use_site_tmp[1]))
                            ret = parse_assignment_expression(self.code,use_site_tmp[1].children[0])
                            print(ret)
                            if use_site_tmp[0] != ret['left']:
                                done_var = True 
                                use_site = use_site_tmp
                            else:
                                fail_cnt += 1 
                                if not PREPARED:
                                    func_name_tmp = None 
                                ran_var_name_tmp = None 
                                if fail_cnt > 10:
                                    return False 
                else:
                    fail_cnt += 1 
                    if not PREPARED:
                        func_name_tmp = None 
                    ran_var_name_tmp = None 
                    if fail_cnt > 10:
                        return False 
            elif ran_var_name_tmp is not None and func_name_tmp is not None :
                if ran_var_name_tmp is not None:
                    if len(list(self.function[func_name_tmp].var[ran_var_name_tmp].use))>0:
                        use_site_tmp = random.choice(self.function[func_name_tmp].var[ran_var_name_tmp].use)
                        print(ret_str(self.code,use_site_tmp[1]))
                        ret = parse_assignment_expression(self.code,use_site_tmp[1].children[0])
                        print(ret)
                        if use_site_tmp[0] != ret['left']:
                            done_var = True 
                            use_site = use_site_tmp
                        else:
                            fail_cnt += 1 
                            if not PREPARED:
                                func_name_tmp = None 
                            ran_var_name_tmp = None 
                            if fail_cnt > 10:
                                return False 
                    else:
                        fail_cnt += 1 
                        if not PREPARED:
                            func_name_tmp = None 
                        ran_var_name_tmp = None 
                        if fail_cnt > 10:
                            return False 
                else:
                    fail_cnt += 1
                    if not PREPARED:   
                        func_name_tmp = None 
                    ran_var_name_tmp = None 
                    if fail_cnt > 10:
                        return False 
            else:
                fail_cnt += 1 
                if not PREPARED:
                    func_name_tmp = None 
                ran_var_name_tmp = None 
                if fail_cnt > 10:
                    return False 
        TYPE_TMP = self.function[func_name_tmp].var[ran_var_name_tmp].type
        if TYPE_TMP not in signed_type.keys() and TYPE_TMP not in unsigned_type.keys():
            return False
        PTR_LEVEL_TMP = self.function[func_name_tmp].var[ran_var_name_tmp].POINTER_TYPE
        if PTR_LEVEL_TMP >0:
            return False 
        type_bound_list = []
        if random.random()>0.5:
            var_str = ret_varname()
            dec_line = TYPE_TMP+" "
            if random.random()>0.5:
                dec_line += "&"
            dec_line += var_str +" = "+ret_str(self.code,use_site[0]) + " ;\n"
            ST_POINT = use_site[1].start_byte - 1
            ED_POINT = use_site[1].start_byte - 1
            self.modified_fragment.append({'coord' : (ST_POINT,ED_POINT), 'code' : dec_line , "replace" : False})
        else:
            var_str = ret_str(self.code,use_site[0])
        if TYPE_TMP in signed_type.keys():
            type_bound_list = signed_type[TYPE_TMP]
        else:
            type_bound_list = unsigned_type[TYPE_TMP]
        if random.random()>0.5:
            func = "std::min({},{})".format(var_str,str(type_bound_list[1]))
        else:
            func = "std::max({},{})".format(var_str,str(type_bound_list[0]))
        ST_POINT = use_site[0].start_byte
        ED_POINT = use_site[0].end_byte
        self.modified_fragment.append({'coord' : (ST_POINT,ED_POINT), 'code' : func , "replace" : False})
        self.commit()
        return True

    def mutator_return_number_with_max_min(self,func_name_tmp = None):
        done_var = False
        fail_cnt = 0 
        while done_var == False:
            if func_name_tmp is None:
                name_tmp = self.random_obtain_defined_function()
                if name_tmp != -1:
                    if len(self.function[name_tmp].number_literal)>0:
                        func_name_tmp = name_tmp
                        done_var = True 
                    else:
                        fail_cnt += 1 
                        if fail_cnt > 10:
                            return False 
                else:
                    fail_cnt += 1 
                    if fail_cnt > 10:
                        return False 
            else:
                done_var = True 
        num_ptr = random.choice(self.function[func_name_tmp].number_literal)
        num_str = ret_str(self.code,num_ptr)
        type_str = guess_a_type(num_str)
        type_bound_list = []
        if type_str in signed_type.keys():
            type_bound_list = signed_type[type_str]
        else:
            type_bound_list = unsigned_type[type_str]
        if random.random()>0.5:
            func = "std::min({},{})".format(num_str,str(type_bound_list[1]))
        else:
            func = "std::max({},{})".format(num_str,str(type_bound_list[0]))
        ST_POINT = num_ptr.start_byte
        ED_POINT = num_ptr.end_byte
        self.modified_fragment.append({'coord' : (ST_POINT,ED_POINT), 'code' : " "+func , "replace" : False})
        self.commit()
        return True  

    def mutator_dec_to_global(self,commit = True):
        '''
        commit -> if set to false, we will defer to commit action 
        Create dec to global scope and call it 
        ret -> [TYPE,tmp_varname,ret_stmt] 
        '''
        ret = gen_dec_stmt(self.var+self.generated_var)
        self.generated_var.append(ret[1])
        if commit:
            self.commit()
            self.commit_by_tag('GLOBAL_HERE',ret[2])
        else:
            self.TAGGED.append(['GLOBAL_HERE',ret[2]])
            return ret 
        return True 


    def mutator_local_def_to_global(self, func_name_tmp = None ,ran_var_name_tmp = None,commit = True):
        '''
        func_name_tmp
        ran_var_name_tmp
        commit: If it set to false, we defer the commit steps 
        BUG : char *smallbuffer, *bigbuffer; -> pick one get two 
        '''
        done_var = False 
        fail_cnt = 0
        PREPARED = False
        if func_name_tmp is not None:
            PREPARED = True 
        while done_var == False:
            if func_name_tmp is None:
                name_tmp = self.random_obtain_defined_function()
                if name_tmp != -1:
                    func_name_tmp = name_tmp
            if ran_var_name_tmp is None and func_name_tmp is not None :
                if len(list(self.function[func_name_tmp].var.keys()))>0:
                    ran_var_name_tmp = random.choice(list(self.function[func_name_tmp].var.keys()))
                if ran_var_name_tmp is not None:
                    done_var = True 
                else:
                    fail_cnt += 1 
                    if not PREPARED:
                        func_name_tmp = None 
                    ran_var_name_tmp = None 
                    if fail_cnt > 10:
                        return False 
            else:
                fail_cnt += 1 
                if not PREPARED:
                    func_name_tmp = None 
                ran_var_name_tmp = None 
                if fail_cnt > 10:
                    return False 
        var_in_def_line = ret_type_list(self.function[func_name_tmp].var[ran_var_name_tmp].def_ptr,'identifier')
        line_to_global = None 
        if len(var_in_def_line) == 1:
            # Copy the line 
            line_to_global = ret_str(self.code,self.function[func_name_tmp].var[ran_var_name_tmp].def_ptr)
            if not line_to_global.endswith(";"):
                line_to_global += ";"
            ST_POINT = self.function[func_name_tmp].var[ran_var_name_tmp].def_ptr.start_byte
            ED_POINT = self.function[func_name_tmp].var[ran_var_name_tmp].def_ptr.end_byte
            self.modified_fragment.append({'coord' : (ST_POINT,ED_POINT), 'code' : "" , "replace" : False})
        else:
            def_ptr = self.function[func_name_tmp].var[ran_var_name_tmp].name_ptr
            def_done = False
            while not def_done:
                if def_ptr is not None:
                    tmp = ret_str(self.code,def_ptr.parent)
                    if tmp.endswith(";") or tmp.endswith(","):
                        def_done = True 
                    else:
                        def_ptr = def_ptr.parent
                else:
                    return False
            TYPE_TMP = self.function[func_name_tmp].var[ran_var_name_tmp].type
            PTR_LEVEL_TMP = self.function[func_name_tmp].var[ran_var_name_tmp].POINTER_TYPE
            VAR_TMP = ret_str(self.code,def_ptr)
            line_to_global =  TYPE_TMP+" "+ "*"*PTR_LEVEL_TMP+VAR_TMP+';'
            ST_POINT = def_ptr.start_byte
            ED_POINT = def_ptr.end_byte
            line_test = ret_str(self.code,self.function[func_name_tmp].var[ran_var_name_tmp].def_ptr)
            append_flag = False 
            forward_template = ""
            for zzzz in range(1,10):
                line_test_tmp = line_test.replace(VAR_TMP+" "*zzzz+";",'')
                if not line_test_tmp.endswith(';'):
                    forward_template = VAR_TMP+" "*zzzz+";"
                    append_flag = True 
                    break
            if(append_flag == False):
                # For removing the comma 
                ED_POINT += 1
            else:
                # We need to fix the backward comma 
                OFFSET = 0
                print(forward_template)
                for zzzz in range(0,10):
                    line_test_tmp = line_test.replace(','+' '*zzzz+forward_template,'')
                    if not line_test_tmp.endswith(';'):
                        OFFSET = zzzz
                        break
                ST_POINT -= OFFSET
            self.modified_fragment.append({'coord' : (ST_POINT,ED_POINT), 'code' : "" , "replace" : False})
        if commit:
            self.commit()
            self.commit_by_tag('GLOBAL_HERE',line_to_global)
        else:
            self.TAGGED.append(['GLOBAL_HERE',line_to_global])
        return True 

    def mutator_local_redefine(self,func_name_tmp = None,ran_var_name_tmp = None):
        done_var = False 
        fail_cnt = 0 
        PREPARED = False
        if func_name_tmp is not None:
            PREPARED = True 
        while done_var == False:
            if func_name_tmp is None:
                name_tmp = self.random_obtain_defined_function()
                if name_tmp != -1:
                    func_name_tmp = name_tmp
            if ran_var_name_tmp is None and func_name_tmp is not None :
                if len(list(self.function[func_name_tmp].var.keys()))>0:
                    ran_var_name_tmp = random.choice(list(self.function[func_name_tmp].var.keys()))
                    # check if it got a use 
                    if ran_var_name_tmp is not None:
                        if len(self.function[func_name_tmp].var[ran_var_name_tmp].use)>0:
                            use_site_tmp = random.choice(self.function[func_name_tmp].var[ran_var_name_tmp].use)
                            print(ret_str(self.code,use_site_tmp[1]))
                            ret = parse_assignment_expression(self.code,use_site_tmp[1].children[0])
                            print(ret)
                            if use_site_tmp[0] != ret['left']:
                                done_var = True 
                                use_site = use_site_tmp
                            else:
                                fail_cnt += 1 
                                if not PREPARED:
                                    func_name_tmp = None 
                                ran_var_name_tmp = None 
                                if fail_cnt > 10:
                                    return False 
                else:
                    fail_cnt += 1 
                    if not PREPARED:
                        func_name_tmp = None 
                    ran_var_name_tmp = None 
                    if fail_cnt > 10:
                        return False 
            elif ran_var_name_tmp is not None and func_name_tmp is not None :
                if ran_var_name_tmp is not None:
                    if len(list(self.function[func_name_tmp].var[ran_var_name_tmp].use))>0:
                        use_site_tmp = random.choice(self.function[func_name_tmp].var[ran_var_name_tmp].use)
                        print(ret_str(self.code,use_site_tmp[1]))
                        ret = parse_assignment_expression(self.code,use_site_tmp[1].children[0])
                        print(ret)
                        if use_site_tmp[0] != ret['left']:
                            done_var = True 
                            use_site = use_site_tmp
                        else:
                            fail_cnt += 1 
                            if not PREPARED:
                                func_name_tmp = None 
                            ran_var_name_tmp = None 
                            if fail_cnt > 10:
                                return False 
                    else:
                        fail_cnt += 1 
                        if not PREPARED:
                            func_name_tmp = None 
                        ran_var_name_tmp = None 
                        if fail_cnt > 10:
                            return False 
                else:
                    fail_cnt += 1
                    if not PREPARED:   
                        func_name_tmp = None 
                    ran_var_name_tmp = None 
                    if fail_cnt > 10:
                        return False 
            else:
                fail_cnt += 1 
                if not PREPARED:
                    func_name_tmp = None 
                ran_var_name_tmp = None 
                if fail_cnt > 10:
                    return False 
        TYPE_TMP = self.function[func_name_tmp].var[ran_var_name_tmp].type
        PTR_LEVEL_TMP = self.function[func_name_tmp].var[ran_var_name_tmp].POINTER_TYPE
        var_str = ret_varname()
        ref_var_str = ret_varname()
        gen_ref = False 
        redef_str  = TYPE_TMP+"*"*PTR_LEVEL_TMP+" "
        redef_str += var_str +" = "+ret_str(self.code,use_site[0]) + " ;\n"  
        ref_ref_flag = False
        if random.random()>0.5:
            if random.random()>0.5:
                gen_ref = True 
                redef_str  = TYPE_TMP+"*"*PTR_LEVEL_TMP+" &"
                redef_str += ref_var_str +" = "+ret_str(self.code,use_site[0]) + " ;\n"  
            else:
                ref_ref_flag = True
                redef_str  = TYPE_TMP+"*"*PTR_LEVEL_TMP+" &"
                redef_str += var_str +" = "+ret_str(self.code,use_site[0]) + " ;\n"  
                redef_str += TYPE_TMP+"*"*PTR_LEVEL_TMP+" &"
                if random.random()>0.5:
                    redef_str += ref_var_str +" = "+var_str + " ;\n"  
                else:
                    redef_str += ref_var_str +" = "+ret_str(self.code,use_site[0]) + " ;\n"  
        ST_POINT = use_site[1].start_byte - 1
        ED_POINT = use_site[1].start_byte - 1
        for pt in self.function[func_name_tmp].var[ran_var_name_tmp].use:
            if pt[0].start_byte > ST_POINT:
                if gen_ref:
                    if random.random()>0.5:
                        self.modified_fragment.append({'coord' : (pt[0].start_byte,pt[0].end_byte), 'code' : ref_var_str , "replace" : False})
                elif ref_ref_flag:
                    op = [var_str,ref_var_str,ret_str(self.code,use_site[0])]
                    var_tmp = random.choice(op)
                    self.modified_fragment.append({'coord' : (pt[0].start_byte,pt[0].end_byte), 'code' : var_tmp , "replace" : False})
                else:
                    self.modified_fragment.append({'coord' : (pt[0].start_byte,pt[0].end_byte), 'code' : var_str , "replace" : False})
        self.modified_fragment.append({'coord' : (ST_POINT,ED_POINT), 'code' : redef_str , "replace" : False})
        self.commit()
        return True


