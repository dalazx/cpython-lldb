from .conftest import run_lldb


CODE = u'''
SOME_CONST = u'тест'


def fa():
    abs(1)
    return 1


def fb():
    1 + 1
    fa()


def fc():
    fb()


fc()
'''.lstrip()


def test_up_down(lldb):
    expected = u'''\
  File "test.py", line 11, in fb
    fa()
  File "test.py", line 15, in fc
    fb()
  File "test.py", line 18, in <module>
    fc()
  File "test.py", line 15, in fc
    fb()
  File "test.py", line 11, in fb
    fa()
  File "test.py", line 15, in fc
    fb()
'''.rstrip()
    response = run_lldb(
        lldb,
        code=CODE,
        breakpoint='builtin_abs',
        commands=['py-up', 'py-up', 'py-up', 'py-down', 'py-down', 'py-up'],
    )
    actual = u''.join(response).rstrip()

    assert actual == expected


def test_newest_frame(lldb):
    expected = u'*** Newest frame'
    response = run_lldb(
        lldb,
        code=CODE,
        breakpoint='builtin_abs',
        commands=['py-down'],
    )
    actual = u''.join(response).rstrip()

    assert actual == expected


def test_oldest_frame(lldb):
    expected = u'''\
  File "test.py", line 11, in fb
    fa()
  File "test.py", line 15, in fc
    fb()
  File "test.py", line 18, in <module>
    fc()
*** Oldest frame
'''.rstrip()
    response = run_lldb(
        lldb,
        code=CODE,
        breakpoint='builtin_abs',
        commands=['py-up'] * 4,
    )
    actual = u''.join(response).rstrip()

    assert actual == expected
