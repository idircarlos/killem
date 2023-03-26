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
        
    def choice(self,list):
        return rd.choice(list)
    
    def random_of_ranges(self,ranges):
        num1 = rd.uniform(ranges[0][0],ranges[0][1])
        num2 = rd.uniform(ranges[1][0],ranges[1][1])
        return rd.choice([num1, num2])