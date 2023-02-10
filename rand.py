import random as rd
import time

class Rand:
    def __init__(self):
        self.seed = time.time()
        
    def randint(self,a,b):
        n = rd.randint(a,b)
        self.update_seed()
        return n
    
    def update_seed(self):
        self.seed = time.time()/99 % 9999
        