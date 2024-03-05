import random

class randomer():
    def __init__(self):
        self.start = 0
        self.end = 100
        self.showProgress = False


    def random_integer(self,start = 0,end = 100):
        if self.showProgress:
            print("Generating Random Integer. Please Wait...")
        return int(random.randint(start,end))
    
    def random_all(self):
        if self.showProgress:
            print("Generating Random All-Type Numbe. Please Wait...")
        return random.random()