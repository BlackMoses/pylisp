'''
Python s-expressions parser and interpreter.
PoC that writing languages is fun.

Written entirely by BlackMoses; blackmoses.org

Very hacky :)
Simplicity over complexity.
'''


def tokenize(code):
    '''
    Convert s-expr string to a list of tokens.
    :param code: whitespace-separated ASCII s-expr (string)

    returns list of strings
    '''
    # Generalize the input
    code = code.replace('(', ' ( ').replace(')', ' ) ')
    return code.split()

def parse(tokens):
    '''
    Parse list of string tokens containing variables, literals
    and syntax ('(' and ')').
    Produce output of nested lists.
    '''
    def do_parse(tokens):
        output = []
        index = 0
        while index < len(tokens):
            if tokens[index] == '(':
                element, delta = do_parse(tokens[index + 1:])
                output.append(element)
                index += delta
            elif tokens[index] == ')':
                return output, index + 1
            else:
                output.append(tokens[index])
            index += 1
        raise RuntimeError('S-expression is not closed.')

    if tokens[0] != '(':
        raise RuntimeError('S-expression is not opened.')
    return do_parse(tokens[1:])[0]

