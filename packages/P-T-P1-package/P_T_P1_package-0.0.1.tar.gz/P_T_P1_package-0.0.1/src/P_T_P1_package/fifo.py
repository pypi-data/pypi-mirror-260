import test_fifo
import unittest
from unittest import main
class FIFO:
    import numpy as np
    def __init__(self, max_size): #the whole magic methods thing has kind of been bothering me... it is unclear how they work
        if max_size <= 0:
            raise("Max too small") #a negative or zero max would be somewhat self-defeating, so it should not be allowed
        else:
            self.state = self.np.array([])
            self.max_size = max_size

    def insert(self, add):
        if (self.size()) < self.max_size: #we insert at the begining, mostly to make taking out the elements easier
            self.state = self.np.insert(self.state, 0, add) #the revelaton of self.state= took around half for me to figure out...
            return True
        else:
            return False #only two options here since the array is either too big or it isn't

    def get(self):
        if self.size() == 0:
            return None
        elif self.size() > 0:
            removed = self.state[-1]
            self.state = self.state[:-1]
            return removed """since it's first in, first out, we just remove the last element...
                                which is really the oldest element since we have been adding elements to the begining of the array.
                                This is perhaps a touch confusing, but it made sense to me at the time (and it works!)"""
        else:
            print("How did we get here?") #had already programmed the last one as elif to make what was happening more clear and kept this around just for fun

    def gets(self, num_rem):
        self.num_rem = num_rem
        if self.num_rem >= self.size() and self.num_rem != 0: #easiest to take care of this first: it's just clearing the array
            removed = self.state
            self.state = self.np.delete(self.state, range(self.size()))
            return removed
        elif self.num_rem < 0: #logically impossible
            raise("index too small")
        elif self.num_rem == 0:
            return self.state
        else:
            removed = self.state[num_rem - 1:]
            self.state = self.state[:num_rem - 1] #just takes up to the index of all the numbers we want to get rid of
            return removed
   
    def size(self):
        return self.state.size

    def check(self): #probably violates Chekov's gun (Chekov's function?)
        return self.state #For debugging, became permanent when I wrote the tests

    def test_fifo():
        if main(module = 'test_fifo', exit = False): #I don't really understand this, but the docs said to do it, and it works, so I'm just going with it
            return True
        else:
            return False

