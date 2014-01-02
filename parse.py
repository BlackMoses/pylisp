'''
Python s-expressions parser and interpreter.
PoC that writing languages is fun.

Written entirely by BlackMoses; blackmoses.org

Very hacky :)
Simplicity over complexity.
'''


class InterpreterError(Exception):
    pass


class TokenizerError(InterpreterError):
    pass


class ParserError(InterpreterError):
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
            if not isinstance(atom, (float, int, str, unicode)):
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
        raise RuntimeError('S-expression is not closed.')

    if tokens[0] != '(':
        raise RuntimeError('S-expression is not opened.')
    return do_parse(tokens[1:])[0]
