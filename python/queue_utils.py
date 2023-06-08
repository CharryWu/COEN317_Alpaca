def job2str(job):
    if job.filename:
        return job.filename
    elif job.id:
        return job.id
    return str(job)

class CircularQueue:
    def __init__(self, capacity) -> None:
        self.capacity = capacity
        self.queue = [None] * capacity
        self.tail = -1
        self.head = 0
        self.size = 0
    
    def get_front(self):
        if self.isEmpty():
            return None
        return self.queue[self.head]

    def enqueue(self, item):
        if self.isFull():
            print("Error: Queue is Full")
            return False
        else:
            self.tail = (self.tail + 1) % self.capacity
            self.queue[self.tail] = item
            self.size += 1
            return True

    def dequeue(self):
        if self.isEmpty():
            print("Error: Queue is Empty")
            return
        else:
            item = self.queue[self.head]
            self.head = (self.head + 1) % self.capacity
            self.size -= 1
            return item

    def isFull(self):
        return self.size == self.capacity

    def isEmpty(self):
        return self.size == 0

    def __str__(self):
        ll = list(map(job2str, self.queue))
        return str(ll)
