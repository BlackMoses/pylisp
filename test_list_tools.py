import pytest

from list_tools import *


def test_cons():
    assert cons('a', 'b') == ('a', 'b')
    assert cons('a', ()) == ('a', ())


def test_is_valid():
    with pytest.raises(TypeError):
        is_valid(())

    with pytest.raises(TypeError):
        is_valid((1,))

    assert is_valid(('a', 'b')) is False
    assert is_valid(('a', ('b', ('c', 'd')))) is False
    assert is_valid(('a', None)) is True
    assert is_valid(('a', ('b', ('c', None)))) is True


def test_car():
    with pytest.raises(TypeError):
        car(())

    with pytest.raises(TypeError):
        car((1,))

    assert car((1, None)) == 1
    assert car(('a', ('b', ('c', None)))) == 'a'


def test_cdr():
    assert cdr((1, None)) is None
    assert cdr((1, (2, None))) == (2, None)

    assert cdr((1, 2)) == 2


def test_nth():
    assert nth(0, ('a', ('b', ('c', None)))) == 'a'
    assert nth(1, ('a', ('b', ('c', None)))) == 'b'
    assert nth(2, ('a', ('b', ('c', None)))) == 'c'

    with pytest.raises(IndexError):
        nth(1, (1, None))

    with pytest.raises(TypeError):
        nth(1, (2, 3))


def test_length():
    assert length((1, None)) == 1
    assert length((1, (2, None))) == 2
    assert length((1, (2, (3, None)))) == 3
