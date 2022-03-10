# 定长队列
class MyQueue:
    """模拟队列"""
    def __init__(self,maxlength):
        self.items = []
        self.maxlength = maxlength

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def add(self,item):  # 外部接口
        self.enqueue(item)
        if self.size() > self.maxlength:
            self.dequeue()

    def print(self):  # 外部接口
        print(f"{self.items},size:{self.size()}")

    def exist(self,item):
        # 加进来的是tuple就能直接in
        return item in self.items
