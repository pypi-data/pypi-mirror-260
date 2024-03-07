import test_lifo
import unittest
from unittest import main
class Stack:
    import numpy as np """in retrospect, I regret putting this inside the class (the number of 'self.s' was ridiculous) but 
                            we've really passed the point of no return on that one, and it's more of a cosmetic thing, anyway"""
    def __init__(self, max_val):
        if max_val <= 0:
            raise("Max size too low")
        else:
            self.state = self.np.array([])
            self.max_val = max_val
    def push(self, add):
        if self.size() >= self.max_val:
            return False
        else:
            self.state = self.np.append(self.state, add) #no reason to complicate it more than this, it is basically just functioning as a list of numbers at this point
            return True

    def pop(self):
        if self.size() == 0:
            return None
        else:
            popped = self.state[-1]
            self.state = self.state[:-1]
            return popped #works almost identically to FIFO's get() method

    def pops(self, delete_num):
        if self.size() <= delete_num and delete_num != 0:
            poppeds = self.np.flip(self.state) #kind of dishonest to do this, but it accomplishes the same goal nonetheless, i.e. it presents the elements in a logical way to the user
            self.state = self.np.delete(self.state, range(self.size())) """deletes everything up to where we want to cut off-- this took quite a bit of work to reason through"""
            return poppeds
        elif delete_num == 0:
            return self.np.flip(self.state)
        else:
            poppeds = self.state[self.size() - delete_num:-1] #these both look worse than they really are; they just take the number we want to remove and subtract it away, basically
            self.state = self.np.delete(self.state, range((self.size() - delete_num, self.size()))) """pure magic-- o.k. not really-- it operates on the same principle as fifo:
                                                                                                        store the values to remove, store the values to keep"""
            return poppeds

    def size(self):
        return self.state.size

    def check(self):
        return self.state #For debugging

    def test_stack(): #'why does this work?' 'the docs said so'
        if main(module = 'test_lifo', exit = False):
            return True
        else:
            return False
