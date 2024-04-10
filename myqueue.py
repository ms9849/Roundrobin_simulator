class MyQueue:
    def __init__(self):
        self.queue = []
    
    def push(self, process):
        self.queue.append(process)
    
    def get(self):
        return self.queue.pop(0)

    def empty(self):
        return len(self.queue) == 0