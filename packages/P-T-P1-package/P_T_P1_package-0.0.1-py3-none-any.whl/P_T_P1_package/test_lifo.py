import unittest
import lifo
class test_lifo(unittest.TestCase):
    import numpy as np
    def test_push(self):
        q = lifo.Stack(1)
        l = lifo.Stack(30)
        self.assertEqual(q.push(3), True)
        self.assertEqual(q.push(1), False) #checks we can't go over limit
        self.assertFalse(q.size() == 0) #checks we've actually added
        l.push(3)
        l.push(0)
        l.push(-3)
        l.push(2)
        l.push(-2)
        self.np.testing.assert_array_equal(l.check(), self.np.array([3., 0., -3., 2., -2.])) #Checks that we're really adding
    
    def test_pop_and_pops(self): #easiest to test both at once
        p = lifo.Stack(5)
        p.push(42)
        p.push(43)
        p.push(41)
        self.assertEqual(p.pop(), 41) #removing 1 element
        self.np.testing.assert_array_equal(p.pops(2), self.np.array([43., 42.])) #removing multiple elements
        p.push(42)
        p.push(45)
        p.push(47)
        self.np.testing.assert_array_equal(p.pops(1000), self.np.array([47., 45., 42.])) #removing all elements
        p.push(42)
        p.push(40)
        self.np.testing.assert_array_equal(p.pops(2), self.np.array([40., 42.])) #removing exactly all elements
        p.push(1)
        p.push(2)
        self.np.testing.assert_array_equal(p.pops(0), self.np.array([2., 1.])) #removing 0 elements
        p.pop()
        p.pop()
        self.np.testing.assert_array_equal(p.pops(4), self.np.array([])) #removing multiple from an empty set
        self.assertEqual(p.pop(), None) #removing 1 from an empty set
     

if __name__ == '__main__': #'good god what is this' 'I dunno but it doesn't work without it'
    unittest.main()
    
