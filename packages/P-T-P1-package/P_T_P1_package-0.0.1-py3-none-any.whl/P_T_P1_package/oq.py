import test_oq
import unittest
from unittest import main
class OQ:
    import numpy as np
    def __init__(self, max_size):
        if max_size <= 0:
            raise("Max too small")
        else:
            self.state = self.np.array([])
            self.max_size = max_size #not exactly sure why this is neccessary, but here we are

    def insert(self, add):
        if self.size() < self.max_size:
            if self.size() == 0 or add > self.state[-1]: """if the array is empty or the number is larger than the last element in the array,
                                                            we can just append it to the end. This assumes, of course, that the list is already sorted"""
                self.state = self.np.append(self.state, add)
                return True
            else:"""otherwise we end up having to find the correct place ourselves. There are probably more efficient ways to do this, 
                    but 'look at each element and see which is bigger than our add' seemed the easiest option"""
                size_for_loop = self.size()
                for i in range(size_for_loop):
                    if add < self.state[i]:
                        location = i #this variable is kind of pointless but it's 9:00 PM and I don't want to mess wwith this anymore
                        self.state = self.np.insert(self.state, location, add)
                        return True #I'm kind of shocked this works, actually ("it's not elves, exactly")
        else:
            return False

    def get(self):
        if self.size() > 0:
            remove = self.state[0] #this is maybe a little dumb, but it works!
            self.state = self.state[1:] #we simply cut twice and save each bit
            return remove
        else:
            return None
    
    def gets(self, num_rem):
        if num_rem > self.size():
            remove = self.state[:]
            self.state = self.np.delete(self.state, range(self.size())) #removes all the elements
            return remove
        elif num_rem < 0:
            raise("index to small")
        elif num_rem == 0:
            return self.state #nothing needs to be removed
        else:
            remove = self.state[: num_rem]
            self.state = self.state[num_rem:]
            return remove #removes the first 'num_rem' elements
            
#This next function strikes me as kind of pointless, but it had to happen, I guess
    def size(self):
        return self.state.size

    def check(self):
        return self.state #For debugging

    def test_ordered():
        if main(module = 'test_oq', exit = False): #terrible to program, and kind of pointless, as far as I'm concerned
            return True
        else:
            return False

