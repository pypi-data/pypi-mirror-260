import unittest
import fifo
class test_fifo(unittest.TestCase):
    import numpy as np
    def test_insert(self):
        q = fifo.FIFO(1)
        l = fifo.FIFO(30)
        self.assertEqual(q.insert(3), True)
        self.assertEqual(q.insert(1), False) #checks we can't go over limit
        self.assertFalse(q.size() == 0) #checks we've actually added
        l.insert(3)
        l.insert(0)
        l.insert(-3)
        l.insert(4)
        self.np.testing.assert_array_equal(l.check(), self.np.array([4., -3., 0., 3.])) #checks array adding is correct

    def test_get_and_gets(self):
        p = fifo.FIFO(5)
        p.insert(42)
        p.insert(43)
        p.insert(41)
        self.assertEqual(p.get(), 42) #removing 1 element
        self.np.testing.assert_array_equal(p.gets(2), self.np.array([41., 43.])) #removing multiple elements - query as to why these arrays must match the order of the lifo arrays, but that's what the readme file says, so...
        p.insert(42)
        p.insert(45)
        p.insert(47)
        self.np.testing.assert_array_equal(p.gets(1000), self.np.array([47., 45., 42.])) #removing all elements
        p.insert(42)
        p.insert(40)
        self.np.testing.assert_array_equal(p.gets(2), self.np.array([40., 42.])) #removing exactly all elements
        p.insert(1)
        p.insert(2)
        self.np.testing.assert_array_equal(p.gets(0), self.np.array([2., 1.])) #removing 0 elements
        p.get()
        p.get()
        self.np.testing.assert_array_equal(p.gets(4), self.np.array([])) #removing multiple from an empty set
        self.assertEqual(p.get(), None) #removing 1 from an empty set
if __name__ == '__main__':
    unittest.main()


