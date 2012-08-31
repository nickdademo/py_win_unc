from unittest import main, TestCase

from win_unc.internal import parsing


never = lambda _: False
always = lambda _: True
is_alpha = lambda x: x.isalpha()


class ListTransformerTestCase(TestCase):
    def assertEqualList(self, first, second):
        self.assertEqual(list(first), list(second))


class TestDropWhile(ListTransformerTestCase):
    def test_drop_nothing(self):
        self.assertEqualList(parsing.drop_while(never, ''), '')
        self.assertEqualList(parsing.drop_while(never, 'a'), 'a')
        self.assertEqualList(parsing.drop_while(never, 'abc'), 'abc')

    def test_drop_everything(self):
        self.assertEqualList(parsing.drop_while(always, ''), '')
        self.assertEqualList(parsing.drop_while(always, 'a'), '')
        self.assertEqualList(parsing.drop_while(always, 'abc'), '')

    def test_drop_with_predicate(self):
        not_alpha = lambda x: not x.isalpha()
        self.assertEqualList(parsing.drop_while(not_alpha, ''), '')
        self.assertEqualList(parsing.drop_while(not_alpha, 'abc'), 'abc')
        self.assertEqualList(parsing.drop_while(not_alpha, '123abc456'), 'abc456')
        self.assertEqualList(parsing.drop_while(not_alpha, '   abc   '), 'abc   ')
        self.assertEqualList(parsing.drop_while(not_alpha, '   '), '')


class TestTakeWhile(ListTransformerTestCase):
    def test_take_nothing(self):
        self.assertEqualList(parsing.take_while(never, ''), '')
        self.assertEqualList(parsing.take_while(never, 'a'), '')
        self.assertEqualList(parsing.take_while(never, 'abc'), '')

    def test_take_everything(self):
        self.assertEqualList(parsing.take_while(always, ''), '')
        self.assertEqualList(parsing.take_while(always, 'a'), 'a')
        self.assertEqualList(parsing.take_while(always, 'abc'), 'abc')

    def test_take_with_predicate(self):
        self.assertEqualList(parsing.take_while(is_alpha, ''), '')
        self.assertEqualList(parsing.take_while(is_alpha, 'abc'), 'abc')
        self.assertEqualList(parsing.take_while(is_alpha, '123abc456'), '')
        self.assertEqualList(parsing.take_while(is_alpha, '   abc   '), '')
        self.assertEqualList(parsing.take_while(is_alpha, '   '), '')


class TestFirst(TestCase):
    def test_no_match(self):
        self.assertEqual(parsing.first(never, ''), None)
        self.assertEqual(parsing.first(never, 'abc'), None)

    def test_all_match(self):
        self.assertEqual(parsing.first(always, ''), None)
        self.assertEqual(parsing.first(always, 'abc'), 'a')

    def test_with_predicate(self):
        self.assertEqual(parsing.first(is_alpha, ''), None)
        self.assertEqual(parsing.first(is_alpha, 'abc'), 'a')
        self.assertEqual(parsing.first(is_alpha, '123abc'), 'a')
        self.assertEqual(parsing.first(is_alpha, '   abc'), 'a')


class TestReversedFirst(TestCase):
    def test_no_match(self):
        self.assertEqual(parsing.rfirst(never, ''), None)
        self.assertEqual(parsing.rfirst(never, 'abc'), None)

    def test_all_match(self):
        self.assertEqual(parsing.rfirst(always, ''), None)
        self.assertEqual(parsing.rfirst(always, 'abc'), 'c')

    def test_with_predicate(self):
        self.assertEqual(parsing.rfirst(is_alpha, ''), None)
        self.assertEqual(parsing.rfirst(is_alpha, 'abc'), 'c')
        self.assertEqual(parsing.rfirst(is_alpha, 'abc123'), 'c')
        self.assertEqual(parsing.rfirst(is_alpha, 'abc   '), 'c')


class TestHigherOrderNot(TestCase):
    def test_not_(self):
        false_ = lambda: False
        true_ = lambda: True
        id_ = lambda x: x

        self.assertEqual(parsing.not_(false_)(), True)
        self.assertEqual(parsing.not_(id_)(False), True)

        self.assertEqual(parsing.not_(true_)(), False)
        self.assertEqual(parsing.not_(id_)(True), False)


if __name__ == '__main__':
    main()
