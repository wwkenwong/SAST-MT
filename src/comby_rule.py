# modify the return
return_int = 'return :[1];'
return_int_rewrite = [ 
{'rule':'''
int ret = :[1] + 1 - 1; 
ret = ret<<2;
return ret/4;
''' , 'var_declar' : []}
]

# int e = d++;
int_var_eq_plusplus = 'int :[2] = :[1]++;'

int_var_eq_plusplus_rewrite = [ 
{'rule':'''
int <%%var-regen_1%%> = :[1];
int :[2] = 100;
:[2] += :[1];
:[2] -= 99;
''' , 
'var_declar' : []},
{'rule':'''
int :[2] = :[1]++;
int *<%%var-regen_1%%> = &:[2];
int *<%%var-regen_2%%> = &:[2];
int *<%%var-regen_3%%> = &:[2];
int *<%%var-regen_4%%> = &:[2];
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
int :[2];
while(:[2] = :[1]){
    :[2]++;
    break;
}
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},

]

# int ++ 
int_plusplus = ':[1]++;'
int_plusplus_rewrite = [
{'rule':'''
int <%%var-regen_1%%> = :[1];
<%%var-regen_1%%> = <%%var-regen_1%%> + 2;
int <%%var-regen_2%%> = <%%var-regen_1%%>;
<%%var-regen_2%%> -= 1;
:[1] = <%%var-regen_2%%>; 
''' , 
'var_declar' : []},

{'rule':'''
int <%%var-regen_1%%> = :[1];
<%%var-regen_1%%>++;
:[1] = <%%var-regen_1%%>;
''' , 'var_declar' : [] },

{'rule':'''
int <%%var-regen_2%%> = 1;
int <%%var-regen_1%%> = 100;
<%%var-regen_1%%> += :[1];
if(<%%var-regen_1%%> > :[1]){
    <%%var-regen_2%%> += :[1];
    <%%var-regen_1%%> -= 99;
    :[1] = <%%var-regen_1%%>;
    printf("a%d\n", <%%var-regen_2%%>);
} else{
    :[1] = :[1] + 1;
}
''' , 'var_declar' : []},
{'rule':'''
:[1] = :[1]|1;
''' , 'var_declar' : []},
{'rule':'''
int <%%var-regen_1%%> = :[1];
:[1] = :[1]|1;
:[1] = :[1] > <%%var-regen_1%%> ? :[1] : :[1]++;
''' , 'var_declar' : []},
{'rule':'''
while(:[1]++){
    break;
}
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
while(:[1]+=1){
    break;
}
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
while(:[1]--){
    :[1]++;
    :[1]++;
    break;
}
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
]

# int --
int_minusminus = ':[1]--;'
int_minusminus_rewrite = [
{'rule':'''
int <%%var-regen_1%%> = :[1];
<%%var-regen_1%%> = <%%var-regen_1%%> - 2;
int <%%var-regen_2%%> = <%%var-regen_1%%>;
<%%var-regen_2%%> += 1;
:[1] = <%%var-regen_2%%>; 
''' , 
'var_declar' : []},

{'rule':'''
int <%%var-regen_1%%> = :[1];
<%%var-regen_1%%>--;
:[1] = <%%var-regen_1%%>;
''' , 'var_declar' : [] },

{'rule':'''
int <%%var-regen_2%%> = 1;
int <%%var-regen_1%%> = 100;
<%%var-regen_1%%> += :[1];
if(<%%var-regen_1%%> > :[1]){
    <%%var-regen_2%%> += :[1];
    <%%var-regen_1%%> -= 101;
    :[1] = <%%var-regen_1%%>;
    printf("a%d\n", <%%var-regen_2%%>);
} else{
    :[1] = :[1] - 1;
}
''' , 'var_declar' : []},
{'rule':'''
:[1] -= 1;
''' , 'var_declar' : []},
{'rule':'''
while(:[1]--){
    break;
}
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
while(:[1]-=1){
    break;
}
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
while(:[1]++){
    :[1]--;
    :[1]--;
    break;
}
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},

]

three_int = 'int :[1], :[2], :[3];'
three_int_rewrite = [ 
{'rule':
'''
int :[1], :[2], :[3];
:[1] = 1;
:[2] = 2147483647;
:[3] = -2147483647 - 1;
//<CODE_BRICK>
if (:[1]%139-:[2]%99-:[3]%190 >= 571642825){
    abort();
}
:[3] = 0;
:[2] = 0;
:[1] = 0;
'''
, 'var_declar' : []},
]

int_var_eq = 'int :[1] = :[2];'
# ptr 
int_var_eq_rewrite = [
{'rule':'''
int :[1] = :[2];
:[1] -= 100; 
int <%%var-regen_1%%> = :[2];
int *<%%var-regen_2%%> = &:[1];
int *<%%var-regen_3%%> = &:[1];
int *<%%var-regen_4%%> = <%%var-regen_2%%>;
int *<%%var-regen_5%%> = <%%var-regen_3%%>;

if ((*<%%var-regen_2%%>-*<%%var-regen_3%%>)*(*<%%var-regen_4%%>-*<%%var-regen_5%%>) >0){
    abort();
}
<%%var-regen_2%%> = NULL;
:[1] = <%%var-regen_1%%>; 
''' , 'var_declar' : []},
{'rule':'''
int :[1] = (:[2]-1)|1;
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
int :[1] = (:[2]-1)|1;
:[1] = :[1] == :[2] ? :[1] : :[1]+1;
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
int :[1] = (:[2]-1)|1;
:[1] = :[1] != :[2] ? :[1]+1 : :[1];
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
int :[1] = (:[2]-1)|1;
:[1] = :[1] == :[2] ? :[1] : :[2];
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
int :[1] = (:[2]-1)|1;
:[1] = :[1] != :[2] ? :[2] : :[1];
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
int :[1];
while(:[1] = :[2]){
    break;
}
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
int :[1] = 1337;
int <%%var-regen_1%%> = :[2] - 1;
if(:[1] != <%%var-regen_1%%>){
    :[1] = :[2];
}else{
    :[1] += 1; 
    <%%var-regen_1%%> += 1;
    printf("a%d\n", <%%var-regen_1%%>);
}
''' , 'var_declar' : [{'type' : "" , 'name': ""}]}
]

# char *p1;
char_ptr = "char *:[1];"

char_ptr_rewrite = [
{'rule':'''
char *:[1];
char **<%%var-regen_1%%> = &:[1];
char **<%%var-regen_2%%> = &:[1];
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
]

# char *p1 = buffer;
char_ptr_eq = "char *:[1] = :[2];"

char_ptr_eq_rewrite = [
{'rule':'''
char *<%%var-regen_1%%> = :[2];
char *<%%var-regen_2%%> = :[2];
char *<%%var-regen_3%%> = :[2];
char *<%%var-regen_4%%> = :[2];
char *:[1] = :[2];
*<%%var-regen_3%%> = 0;
*<%%var-regen_4%%>+1 = 0;
if (*<%%var-regen_1%%>!=*<%%var-regen_2%%>){
    abort();
}
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
char *:[1];
char **<%%var-regen_1%%> = &:[1];
char **<%%var-regen_2%%> = &:[1];
char **<%%var-regen_3%%> = &:[1];
*:[1] = :[2];
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},

]

# char buffer[128];
char_array = "char :[1][:[2]];" # OK 

char_array_rewrite = [
{'rule':'''
char :[1][:[2]];
char *<%%var-regen_1%%> = :[1];
char *<%%var-regen_2%%> = :[1];
char *<%%var-regen_3%%> = :[1];
char *<%%var-regen_4%%> = :[1];
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},

]

# int intBuffer[100];
int_array = "int :[1][:[2]];" # OK 

int_array_rewrite = [
{'rule':'''
int :[1][:[2]];
int *<%%var-regen_1%%> = :[1];
int *<%%var-regen_2%%> = :[1];
int *<%%var-regen_3%%> = :[1];
int *<%%var-regen_4%%> = :[1];
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
]

# int i;
int_var = "int :[1];" # OK 

int_var_rewrite = [ 
{'rule':'''
int :[1];
int *<%%var-regen_1%%> = &:[1];
int *<%%var-regen_2%%> = &:[1];
int *<%%var-regen_3%%> = &:[1];
int *<%%var-regen_4%%> = &:[1];
*<%%var-regen_1%%> = 1; 
if (*<%%var-regen_1%%>+*<%%var-regen_2%%>+*<%%var-regen_3%%>+*<%%var-regen_4%%> == 4){
    *<%%var-regen_1%%> = *<%%var-regen_2%%>^*<%%var-regen_3%%>; 
}
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
]


# int a = b + c;
int_plus = ":[1] = :[2] + :[3];" # OK 
int_plus_with_type = "int :[1] = :[2] + :[3];" # OK 
int_plus_rewrite = [ 
{'rule':'''
int <%%var-regen_1%%> = :[2];
int <%%var-regen_2%%> = :[3];
:[1] = <%%var-regen_1%%> + <%%var-regen_2%%>;
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
int &<%%var-regen_1%%> = :[2];
int &<%%var-regen_2%%> = :[3];
:[1] = <%%var-regen_1%%> + <%%var-regen_2%%>;
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
int &<%%var-regen_1%%> = :[2];
int &<%%var-regen_2%%> = :[3];
:[1] = :[2] + <%%var-regen_2%%>;
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
]


int_minus = ":[1] = :[2] - :[3];" # OK 
int_minus_with_type = "int :[1] = :[2] - :[3];" # OK 
int_minus_rewrite = [ 
{'rule':'''
int <%%var-regen_1%%> = :[2];
int <%%var-regen_2%%> = :[3];
:[1] = <%%var-regen_1%%> - <%%var-regen_2%%>;
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
int &<%%var-regen_1%%> = :[2];
int &<%%var-regen_2%%> = :[3];
:[1] = <%%var-regen_1%%> - <%%var-regen_2%%>;
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
int &<%%var-regen_1%%> = :[2];
int &<%%var-regen_2%%> = :[3];
:[1] = :[2] - <%%var-regen_2%%>;
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
]


int_multi = ":[1] = :[2] * :[3];" # OK 
int_multi_with_type = "int :[1] = :[2] * :[3];" # OK 
int_multi_rewrite = [ 
{'rule':'''
int <%%var-regen_1%%> = :[2];
int <%%var-regen_2%%> = :[3];
:[1] = <%%var-regen_1%%> * <%%var-regen_2%%>;
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
int &<%%var-regen_1%%> = :[2];
int &<%%var-regen_2%%> = :[3];
:[1] = <%%var-regen_1%%> * <%%var-regen_2%%>;
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
int &<%%var-regen_1%%> = :[2];
int &<%%var-regen_2%%> = :[3];
:[1] = :[2] * <%%var-regen_2%%>;
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
]


int_div = ":[1] = :[2] / :[3];" # OK 
int_div_with_type = "int :[1] = :[2] / :[3];" # OK 
int_div_rewrite = [ 
{'rule':'''
int <%%var-regen_1%%> = :[2];
int <%%var-regen_2%%> = :[3];
:[1] = <%%var-regen_1%%> / <%%var-regen_2%%>;
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
int &<%%var-regen_1%%> = :[2];
int &<%%var-regen_2%%> = :[3];
:[1] = <%%var-regen_1%%> / <%%var-regen_2%%>;
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
int &<%%var-regen_1%%> = :[2];
int &<%%var-regen_2%%> = :[3];
:[1] = :[2] / <%%var-regen_2%%>;
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
]

int_mod = ":[1] = :[2] % :[3];" # OK 
int_mod_with_type = "int :[1] = :[2] % :[3];" # OK 
int_mod_rewrite = [ 
{'rule':'''
int <%%var-regen_1%%> = :[2];
int <%%var-regen_2%%> = :[3];
:[1] = <%%var-regen_1%%> % <%%var-regen_2%%>;
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
int &<%%var-regen_1%%> = :[2];
int &<%%var-regen_2%%> = :[3];
:[1] = <%%var-regen_1%%> % <%%var-regen_2%%>;
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
{'rule':'''
int &<%%var-regen_1%%> = :[2];
int &<%%var-regen_2%%> = :[3];
:[1] = :[2] % <%%var-regen_2%%>;
''' , 'var_declar' : [{'type' : "" , 'name': ""}]},
]


# string var only 
matching_rules_list = [ 
int_plusplus,
int_minusminus,
three_int,
int_var_eq_plusplus,
return_int,
char_ptr_eq,
char_array,
int_array,
int_var,
int_var_eq,
char_ptr,
int_plus,
int_plus_with_type,
int_minus,
int_minus_with_type,
int_multi,
int_multi_with_type,
int_div,
int_div_with_type,
int_mod,
int_mod_with_type,
] 

# String to replacing template 
rule_to_replacer_dict = {
int_plusplus : int_plusplus_rewrite,
int_minusminus : int_minusminus_rewrite ,
three_int : int_minusminus_rewrite,
int_var_eq_plusplus : int_var_eq_plusplus_rewrite,
return_int : return_int_rewrite,
char_ptr_eq : char_ptr_eq_rewrite,
char_array : char_array_rewrite,
int_array : int_array_rewrite,
int_var : int_var_rewrite,
int_var_eq : int_var_eq_rewrite,
char_ptr : char_ptr_rewrite,
int_plus : int_plus_rewrite,
int_plus_with_type : int_plus_rewrite,
int_minus : int_minus_rewrite ,
int_minus_with_type : int_minus_rewrite,
int_multi : int_multi_rewrite,
int_multi_with_type : int_multi_rewrite,
int_div : int_div_rewrite,
int_div_with_type : int_div_rewrite,
int_mod : int_mod_rewrite,
int_mod_with_type : int_mod_rewrite,
}
