class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    
    
    def move(self,vector):
        self.x += vector.h
        self.y += vector.v
    
    

class Vector:
    def __init__(self, h, v):
        pass # replace these passes with your code!
      
    def add(self, otherVector):
        pass
      
    def divide(self, scalar):
        if scalar != 0:
            pass
