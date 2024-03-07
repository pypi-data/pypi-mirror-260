import unittest
import oq
class test_oq(unittest.TestCase):
    import numpy as np
    def test_push(self):
        q = oq.OQ(1)
        l = oq.OQ(9)
        self.assertEqual(q.insert(3), True)
        self.assertEqual(q.insert(1), False) #checks we can't go over limit
        self.assertFalse(q.size() == 0) #checks we've actually added
        l.insert(41)
        l.insert(30)
        l.insert(-3)
        l.insert(0)
        l.insert(0)
        l.insert(45)
        l.insert(41)
        self.np.testing.assert_array_equal(l.check(), self.np.array([-3, 0, 0, 30, 41, 41, 45])) #checks everything ends up ordered from a relatively long example with 0s, negatives, repeats, etc.

    def test_pop_and_push(self):
        p = oq.OQ(5)
        p.insert(42)
        p.insert(43)
        p.insert(41)
        self.assertEqual(p.get(), 41) #removing 1 element
        self.np.testing.assert_array_equal(p.gets(2), self.np.array([42., 43.])) #removing multiple elements
        p.insert(42)
        p.insert(45)
        p.insert(47)
        self.np.testing.assert_array_equal(p.gets(1000), self.np.array([42., 45., 47.])) #removing all elements
        p.insert(42)
        p.insert(40)
        self.np.testing.assert_array_equal(p.gets(2), self.np.array([40., 42.])) #removing exactly all elements
        p.insert(1)
        p.insert(2)
        self.np.testing.assert_array_equal(p.gets(0), self.np.array([1., 2.])) #removing 0 elements
        p.get()
        p.get()
        self.np.testing.assert_array_equal(p.gets(4), self.np.array([])) #removing multiple from an empty set
        self.assertEqual(p.get(), None) #removing 1 from an empty set

if __name__ == '__main__':
    unittest.main()

