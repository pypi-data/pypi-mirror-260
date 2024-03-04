from example_python_package import foo_bar


def test_bar():
    assert foo_bar.bar() == 'bar'

def test_foo():
    assert foo_bar.foo() == 'foo'
