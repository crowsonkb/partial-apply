import unittest

from partial_apply import Empty, PartialFn, PartialMethod


def fn(*args, **kwargs):
    return args, kwargs


class Args(object):
    @staticmethod
    def method(*args, **kwargs):
        return args, kwargs

obj = Args()


class TestPartialFn(unittest.TestCase):
    def test_zero(self):
        p = PartialFn(fn)
        self.assertEqual(p(), fn())

    def test_positional(self):
        p = PartialFn(fn, 1, 2)
        self.assertEqual(p(3, 4), fn(1, 2, 3, 4))

    def test_placeholder(self):
        p = PartialFn(fn, Empty, 2)
        self.assertEqual(p(1, 3), fn(1, 2, 3))

    def test_placeholder_fail(self):
        p = PartialFn(fn, Empty, 2)
        with self.assertRaises(TypeError):
            p()

    def test_keyword(self):
        p = PartialFn(fn, a=1, b=2)
        self.assertEqual(p(a=3, c=3), fn(a=3, b=2, c=3))

    def test_repr(self):
        p = PartialFn(fn, Empty, 1, a='thing')
        self.assertEqual(repr(p),
                         "PartialFn({!r}, Empty, 1, a='thing')".format(fn))


class TestPartialMethod(unittest.TestCase):
    def test_zero(self):
        p = PartialMethod('method')
        self.assertEqual(p(obj), fn())

    def test_no_obj_supplied(self):
        p = PartialMethod('method')
        with self.assertRaises(TypeError):
            p()

    def test_positional(self):
        p = PartialMethod('method', 1, 2)
        self.assertEqual(p(obj, 3, 4), fn(1, 2, 3, 4))

    def test_placeholder(self):
        p = PartialMethod('method', Empty, 2)
        self.assertEqual(p(obj, 1, 3), fn(1, 2, 3))

    def test_placeholder_fail(self):
        p = PartialMethod('method', Empty, 2)
        with self.assertRaises(TypeError):
            p(obj)

    def test_keyword(self):
        p = PartialMethod('method', a=1, b=2)
        self.assertEqual(p(obj, a=3, c=3), fn(a=3, b=2, c=3))

    def test_repr(self):
        p = PartialMethod('method', Empty, 1, a='thing')
        self.assertEqual(repr(p),
                         "PartialMethod('method', Empty, 1, a='thing')")


if __name__ == '__main__':
    unittest.main()
