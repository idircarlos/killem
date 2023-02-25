import time as t

class Skill:
    
    def __init__(self,name,cd):
        self.name = name
        self.cd = cd
        self.current_cd = t.time()
        self.ready = True
        
    def trigger(self):
        if self.ready:
            self.current_cd = t.time()
            self.ready = False
            return True
        return False
        
    def update_cd(self):
        if not self.ready:
            if t.time() - self.current_cd >= self.cd:
                self.ready = True

    def get_cd(self):
        if self.ready:
            return 0
        return self.cd - (t.time() - self.current_cd)
                
        