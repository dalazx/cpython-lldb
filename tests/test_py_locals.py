from .conftest import extract_command_output, run_lldb


CODE = u'''\
def fa():
    abs(1)


def fb(spam, *args, eggs=42, **kwargs):
    a = 42
    b = [1, 'hello', u'тест']
    c = ([1], 2, [[3]])
    d = 'test'
    e = {'a': -1, 'b': 0, 'c': 1}

    fa()


def fc():
    fb('foobar', 1, 2, 3, foo=b'spam')


fc()
'''.lstrip()


def test_locals():
    expected = u'''\
a = 42
args = (1, 2, 3)
b = [1, u'hello', u'\\u0442\\u0435\\u0441\\u0442']
c = ([1], 2, [[3]])
d = u'test'
e = {u'a': -1, u'b': 0, u'c': 1}
eggs = 42
kwargs = {u'foo': 'spam'}
spam = u'foobar'
'''

    response = run_lldb(
        code=CODE,
        breakpoint='builtin_abs',
        commands=['py-up', 'py-locals'],
    )
    actual = extract_command_output(response, 'py-locals')

    assert actual == expected


def test_globals():
    response = run_lldb(
        code=CODE,
        breakpoint='builtin_abs',
        commands=['py-up', 'py-up', 'py-up', 'py-locals'],
    )
    actual = extract_command_output(response, 'py-locals')

    actual_keys = set(line.split('=')[0].strip()
                      for line in actual.split('\n') if line)
    expected_keys = set(['__builtins__', '__package__',
                         '__name__', '__doc__', '__file__',
                         'fa', 'fb', 'fc'])
    assert (expected_keys & actual_keys) == expected_keys


def test_no_locals():
    response = run_lldb(
        code=CODE,
        breakpoint='builtin_abs',
        commands=['py-locals'],
    )
    actual = extract_command_output(response, 'py-locals')

    assert actual == u'\n'
