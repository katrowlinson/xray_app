import xraylib

def validate_int(*s):
    for i in s:
        try: 
            int(i)
            return True
        except ValueError:
            return False

def validate_float(*s):
    for i in s:
        try: 
            float(i)
            return True
        except ValueError:
            return False
                
def validate_str(*s):
    for i in s:
        try: 
            str(i)
            return True
        except ValueError:
            return False
            
def validate_int_or_str(*s):
    for i in s:
        try:
            int(i)
            return True
        except ValueError:
            try:
                str(i)
                return True
            except ValueError:
                return False
                
#------------------------------------------------------------------------------------------------
def make_tup(_dict):
    tup = [(k, k) for k, v in _dict.items()]
    return tup
    
def check_xraylib_key(key):
    if key in xraylib.__dict__.keys():
        return True
    else:
        return False

def calc_output(function, *values):
    xrl_function = getattr(xraylib, function)
    lst = []
    for value in values:
        if validate_int(value) == True and float(value) == int(value):
            lst.append(int(value))
        elif validate_float(value) == True:
            lst.append(float(value))  
        elif check_xraylib_key(str(value)) == True:
            value = getattr(xraylib, value)
            lst.append(value) 
        elif xraylib.SymbolToAtomicNumber(value) != 0:
            lst.append(xraylib.SymbolToAtomicNumber(value))
        else:
            lst.append(value)     
    print(lst)        
    try:
        output = float(xrl_function(*lst))
        return output
    except:
        try:
            xrl_function = getattr(xraylib, function + '_CP')
            output = float(xrl_function(*lst))
            return output
        except:
            output = 'Error'
            return output

def code_example(tple, function, *variables):
    languages = [x[0] for x in tple]
    labels = [x[1] for x in tple]
    examples = []
    for label in labels:
        if label == 'C/C++/Objective-C':
            support = '#include <xraylib.h>'
        elif label == 'Fortran 2003/2008':
            support = 'use :: xraylib'
        elif label == 'Perl':
            support = 'use xraylib.pm;'
        elif label == 'IDL':
            support = '@xraylib'
        elif label == 'Python':
            support = 'import xraylib'
        elif label == 'Java':
            support = 'import com.github.tschoonj.xraylib.*;'
        elif label == 'C#/.NET':
            support = 'using Science;'
        elif label == 'Lua':
            support = 'require("xraylib")'
        elif label == 'Ruby':
            support = 'require \'xraylib\''
        elif label == 'PHP':
            support = 'include("xraylib.php");'
        string = 'Enable support for xraylib in ' + str(label) + ' using: ' + str(support)
        examples.append(string)
    
    for language in languages:
        #ADD DIVS/ID SO CSS CAN WORK
        lst = []
        if language == 'c++':
            for variable in variables:
                if validate_int(variable) == True:
                    lst.append(variable)
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('SymbolToAtomicNumber("' + variable + '")')
            _input = ', '.join(lst)
            example = str(function) + '(' + _input + ')'
        
        elif language == 'fortran':
            for variable in variables:
                if validate_int(variable) == True:
                    lst.append(variable)
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('symboltoatomicnumber(\'' + variable + '\')')
                elif check_xraylib_key(str(variable)) == True:
                    lst.append('$xraylib::' + variable.lower())
            _input = ', '.join(lst)
            example = str(function).lower() + '(' + _input + ')'
        
        elif language == 'perl':
            for variable in variables:
                if validate_int(variable) == True:
                    lst.append(variable)
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('xraylib::SymbolToAtomicNumber("' + variable + '")')
                elif check_xraylib_key(str(variable)) == True:
                    lst.append('$xraylib::' + variable)
            _input = ', '.join(lst)
            example = 'xraylib::' + str(function) + '(' + _input + ')'
        
        elif language == 'idl':
            lst = []
            for variable in variables:
                if validate_int(variable) == True or check_xraylib_key(str(variable)) == True:
                    lst.append(variable)
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('SYMBOLTOATOMICNUMBER(\'' + variable + '\')')
            _input = ', '.join(lst)
            example = str(function).upper() + '(' + _input + ')'
        
        elif language == 'py':
            for variable in variables:
                if validate_int(variable) == True:
                    lst.append(variable)
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('xraylib.SymbolToAtomicNumber("' + variable + '")')
                elif check_xraylib_key(str(variable)) == True:
                    lst.append('xraylib.' + variable)
            _input = ', '.join(lst)
            example = 'xraylib.' + str(function) + '(' + _input + ')'
        
        elif language == 'java':
            for variable in variables:
                if validate_int(variable) == True:
                    lst.append(variable)
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('Xraylib.SymbolToAtomicNumber("' + variable + '")')
                elif check_xraylib_key(str(variable)) == True:
                    lst.append('Xraylib.' + variable)
            _input = ', '.join(lst)
            example = 'Xraylib.' + str(function) + '(' + _input + ')'
        
        elif language == 'c#':
            for variable in variables:
                if validate_int(variable) == True:
                    lst.append(variable)
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('Xraylib.SymbolToAtomicNumber("' + variable + '")')
                elif check_xraylib_key(str(variable)) == True:
                    lst.append('Xraylib.' + variable)
            _input = ', '.join(lst)
            example = 'Xraylib.' + str(function) + '(' + _input + ')'
        
        elif language == 'lua':
            for variable in variables:
                if validate_int(variable) == True:
                    lst.append(variable)
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('xraylib.SymbolToAtomicNumber("' + variable + '")')
                elif check_xraylib_key(str(variable)) == True:
                    lst.append('xraylib.' + variable)
            _input = ', '.join(lst)
            example = 'xraylib.' + str(function) + '(' + _input + ')'
        
        elif language == 'ruby':
            for variable in variables:
                if validate_int(variable) == True:
                    lst.append(variable)
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('Xraylib.SymbolToAtomicNumber("' + variable + '")')
                elif check_xraylib_key(str(variable)) == True:
                    lst.append('Xraylib::' + variable)
            _input = ', '.join(lst)
            example = 'Xraylib.' + str(function) + '(' + _input + ')'
        
        elif language == 'php': 
            for variable in variables:
                if validate_int(variable) == True or check_xraylib_key(str(variable)) == True:
                    lst.append(variable)
                elif xraylib.SymbolToAtomicNumber(variable) != 0:
                    lst.append('SymbolToAtomicNumber("' + variable + '")')
            _input = ', '.join(lst)
            example = str(function) + '(' + _input + ')'
        examples.append(example)
    examples = '<br>'.join(examples)  
    return examples        