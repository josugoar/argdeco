import types


class Test_1:
    pass


class Test_2:
    pass


def test(*args, **kwargs):
    print(args, kwargs)


test_1 = Test_1()
test_2 = Test_2()
test = types.MethodType(test, test_1)
test = types.MethodType(test, test_2)
test()
