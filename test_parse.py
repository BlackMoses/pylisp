import pytest

from parse import tokenize, parse


@pytest.mark.parametrize('input, expected_result',
    [
        ('', []),

        # Parentheses:
        ('()', ['(', ')']),
        ('(())', ['(', '(', ')', ')']),
        ('(()()())', ['(', '(', ')', '(', ')', '(', ')', ')']),

        # Words:
        (
            'hitler', ['hitler']
        ),
        (
            'let there be rock and roll',
            ['let', 'there', 'be', 'rock', 'and', 'roll']
        ),

        # S-expressions:
        (
            '(make me a tuple)',
            ['(', 'make', 'me', 'a', 'tuple', ')']
        ),
        (
            '(make (me a) tuple)',
            ['(', 'make', '(', 'me', 'a', ')','tuple', ')']
        ),

        # Invalid S-expressions:
        (
            '(make me ( a tuple)',
            ['(', 'make', 'me', '(', 'a', 'tuple', ')']
        ),
        (
            '(make (((((',
            ['(', 'make', '(', '(', '(', '(', '(']
        ),
    ]
)
def test_tokenize(input, expected_result):
    assert expected_result == tokenize(input)


@pytest.mark.parametrize('input, expected_result',
    [
        (['(', ')'], []),
        (['(', '(', ')', ')'], [[]]),
        (['(', 'a', ')'], ['a']),
        (['(', 'a', 'b', ')'], ['a', 'b']),
        (['(', '(', ')', 'a', 'b', ')'], [[], 'a', 'b']),
        (['(', '(', 'a', 'b', ')', 'a', 'b', ')'], [['a', 'b'], 'a', 'b']),
    ],
)
def test_parse(input, expected_result):
    assert expected_result == parse(input)


@pytest.mark.parametrize('input',
    [
        (['(']),
        ([')'], []),
        (['(', ')', ')'], [[]]),
        (['a', ')'], ['a']),
        (['a', 'b', ')'], ['a', 'b']),
        (['(', ')', 'a', 'b', ')'], [[], 'a', 'b']),
        (['(', 'a', 'b', ')', 'a', 'b', ')'], [['a', 'b'], 'a', 'b']),
    ],
)
def test_parse_raises(input):
    with pytest.raises(RuntimeError):
        parse(input)



