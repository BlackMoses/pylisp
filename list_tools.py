''' Basic tools for constructing and traversing linkedlists.  '''


def _valid_element(el):
    ''' Validate list item constraints required by language. '''
    if type(el) != tuple or len(el) != 2:
        raise TypeError('List element must always be 2-element tuple!')


def car(lst):
    ''' Return first list element. '''
    _valid_element(lst)
    return lst[0]


def is_valid(lst):
    '''
    Check if given linkedlist is a valid one.
    Valid linkedlists are terminated by None.
    '''
    _valid_element(lst)

    if lst[1] is None:
        return True
    try:
        return is_valid(lst[1])
    except TypeError:
        # Not an iterable
        return False


def cdr(lst):
    _valid_element(lst)
    return lst[1]


def cons(el, lst):
    '''
    Returns list appended to the element.
    Or element prepended to the list.
    (FYI, tuples are immutable)
    :param el - anything
    :param lst - linkedlist or None, passing something else will result
        in creating invalid list
    '''
    return (el, lst)


def nth(n, lst):
    ''' Returns list element number n.  '''
    if lst is None:
        raise IndexError('nth went out of range.')

    _valid_element(lst)
    if n == 0:
        return car(lst)
    else:
        return nth(n - 1, cdr(lst))


def length(lst, start=1):
    ''' Returns list length. '''
    _valid_element(lst)
    if lst[1] is None:
        return start
    else:
        return length(cdr(lst), start=start + 1)
