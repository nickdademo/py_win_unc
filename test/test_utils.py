from unittest import TestCase

from win_unc.internal import utils


never = lambda _: False
always = lambda _: True
is_alpha = lambda x: x.isalpha()


class ListTransformerTestCase(TestCase):
    def assertEqualLists(self, first, second):
        self.assertEqual(list(first), list(second))


class TestDropWhile(ListTransformerTestCase):
    def test_drop_nothing(self):
        self.assertEqualLists(utils.drop_while(never, ''), '')
        self.assertEqualLists(utils.drop_while(never, 'a'), 'a')
        self.assertEqualLists(utils.drop_while(never, 'abc'), 'abc')

    def test_drop_everything(self):
        self.assertEqualLists(utils.drop_while(always, ''), '')
        self.assertEqualLists(utils.drop_while(always, 'a'), '')
        self.assertEqualLists(utils.drop_while(always, 'abc'), '')

    def test_drop_with_predicate(self):
        not_alpha = lambda x: not x.isalpha()
        self.assertEqualLists(utils.drop_while(not_alpha, ''), '')
        self.assertEqualLists(utils.drop_while(not_alpha, 'abc'), 'abc')
        self.assertEqualLists(utils.drop_while(not_alpha, '123abc456'), 'abc456')
        self.assertEqualLists(utils.drop_while(not_alpha, '   abc   '), 'abc   ')
        self.assertEqualLists(utils.drop_while(not_alpha, '   '), '')


class TestTakeWhile(ListTransformerTestCase):
    def test_take_nothing(self):
        self.assertEqualLists(utils.take_while(never, ''), '')
        self.assertEqualLists(utils.take_while(never, 'a'), '')
        self.assertEqualLists(utils.take_while(never, 'abc'), '')

    def test_take_everything(self):
        self.assertEqualLists(utils.take_while(always, ''), '')
        self.assertEqualLists(utils.take_while(always, 'a'), 'a')
        self.assertEqualLists(utils.take_while(always, 'abc'), 'abc')

    def test_take_with_predicate(self):
        self.assertEqualLists(utils.take_while(is_alpha, ''), '')
        self.assertEqualLists(utils.take_while(is_alpha, 'abc'), 'abc')
        self.assertEqualLists(utils.take_while(is_alpha, '123abc456'), '')
        self.assertEqualLists(utils.take_while(is_alpha, '   abc   '), '')
        self.assertEqualLists(utils.take_while(is_alpha, '   '), '')


class TestFirst(TestCase):
    def test_no_match(self):
        self.assertEqual(utils.first(never, ''), None)
        self.assertEqual(utils.first(never, 'abc'), None)

    def test_all_match(self):
        self.assertEqual(utils.first(always, ''), None)
        self.assertEqual(utils.first(always, 'abc'), 'a')

    def test_with_predicate(self):
        self.assertEqual(utils.first(is_alpha, ''), None)
        self.assertEqual(utils.first(is_alpha, 'abc'), 'a')
        self.assertEqual(utils.first(is_alpha, '123abc'), 'a')
        self.assertEqual(utils.first(is_alpha, '   abc'), 'a')


class TestReversedFirst(TestCase):
    def test_no_match(self):
        self.assertEqual(utils.rfirst(never, ''), None)
        self.assertEqual(utils.rfirst(never, 'abc'), None)

    def test_all_match(self):
        self.assertEqual(utils.rfirst(always, ''), None)
        self.assertEqual(utils.rfirst(always, 'abc'), 'c')

    def test_with_predicate(self):
        self.assertEqual(utils.rfirst(is_alpha, ''), None)
        self.assertEqual(utils.rfirst(is_alpha, 'abc'), 'c')
        self.assertEqual(utils.rfirst(is_alpha, 'abc123'), 'c')
        self.assertEqual(utils.rfirst(is_alpha, 'abc   '), 'c')


class TestHigherOrderNot(TestCase):
    def test_not_(self):
        false_ = lambda: False
        true_ = lambda: True
        id_ = lambda x: x

        self.assertEqual(utils.not_(false_)(), True)
        self.assertEqual(utils.not_(id_)(False), True)

        self.assertEqual(utils.not_(true_)(), False)
        self.assertEqual(utils.not_(id_)(True), False)


def raiseSomething(exception):
    raise exception()


class TestCatch(TestCase):
    def assertIsType(self, typeId, b):
        self.assertEqual(typeId, type(b))

    def test_catch(self):
        self.assertIsType(Exception, utils.catch(raiseSomething, Exception))
        self.assertIsType(ValueError, utils.catch(raiseSomething, ValueError))
        self.assertIsType(Exception, utils.catch(self.raiseSomething, Exception))
        self.assertIsType(ValueError, utils.catch(self.raiseSomething, ValueError))

    def raiseSomething(self, exception):
        raise exception()
