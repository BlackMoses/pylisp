'''
Python s-expressions parser and interpreter.
PoC that writing languages is fun.

Written entirely by BlackMoses; blackmoses.org

Very hacky :)
Simplicity over complexity.


For now using Python's lists as native type. Maybe I'll migrate to already
implemented linkedlists.
'''

ATOMS = (float, int, str, unicode)

# Built-in functions:
def a():
    print 'I am a and have just been called'
    return 'a'

def b(*args):
    print 'I am b and have just been called with args: %s' % repr(args)

BUILT_INS = {
    'a': a,
    'b': b
}


class LanguageError(Exception):
    pass


class TokenizerError(LanguageError):
    pass


class ParserError(LanguageError):
    pass


class InterpreterError(LanguageError):
    pass


def tokenize(code):
    '''
    Convert s-expr string to a list of tokens.
    :param code: whitespace-separated ASCII s-expr (string)

    returns list of strings
    '''
    EOF = None  # Indicates end of file.
    # Indicates the index where current word starts. None if the cursor is not
    # over a word. (List to hack Python not having truely lexical scope):
    word_start_index = [None]
    len_plus_eof = len(code) + 1  # Length of the code plus pseudo-EOF.
    tokens = []

    def append_word_if_word():
        if word_start_index[0] is not None:
            token = code[word_start_index[0]:index]
            # Validate the token:
            # Valid types are Python's float, int, str, unicode. Those types
            # are managed by Python's runtime.
            atom = eval(repr(token), {})
            if not isinstance(atom, ATOMS):
                raise TokenizerError(
                    'Token %s is %s. Must be float, int, str or unicode.' %
                    (token, type(token)))
            tokens.append(token)
            word_start_index[0] = None

    for index in range(len_plus_eof):
        char = code[index] if index + 1 < len_plus_eof else EOF

        if char in [' ', '\t', EOF]:  # Whitespace
            append_word_if_word()
        elif char == '(' or char == ')':  # Parenthesis
            append_word_if_word()
            tokens.append(char)
        else:  # Symbol or literal
            if word_start_index[0] is None:
                # We're at the beginning of a word. Mark it:
                word_start_index[0] = index

    return tokens


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
        raise ParserError('S-expression is not closed.')

    if tokens[0] != '(':
        raise ParserError('S-expression is not opened.')
    return do_parse(tokens[1:])[0]


def interpret(i_list):
    ''' Recursively evaluate lists. '''
    # First element is the function name.
    # The rest are args.
    i_globals = BUILT_INS  # Currently code supports only globals.
    # Turing-completeness shall be guaranteed by built-in functions.

    try:
        fn_name = i_list[0]
        fn = i_globals[fn_name]
    except IndexError:
        raise InterpreterError('Empty list call')
    except KeyError:
        raise InterpreterError('Attempted to call unexisting function.')

    args = []
    for el in i_list[1:]:
        if isinstance(el, ATOMS):
            args.append(el)
        elif isinstance(el, list):
            args.append(interpret(el))
        else:
            raise RuntimeError('Incompatible type in interpret: %s. '
                        'Should never happen.' % type(el))

    return fn(*args)

def run(code):
    try:
        tokens = tokenize(code)
        parsed = parse(tokens)
        print interpret(parsed)
        return 0
    except LanguageError as err:
        print repr(err)
        return -1


def main():
    import io, sys
    try:
        code = io.open(sys.argv[1]).read()
    except IndexError:
        print 'File name required.'
        return -2
    except IOError:
        print 'Cannot open file: \'%s\'.' % sys.argv[1]
    return run(code)


if __name__ == '__main__':
    main()
