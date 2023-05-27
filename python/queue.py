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

    def enqueue(self, item):
        if self.size == self.capacity:
            print("Error: Queue is Full")
            return False
        else:
            self.tail = (self.tail + 1) % self.capacity
            self.queue[self.tail] = item
            self.size += 1
            return True

    def dequeue(self):
        item = None
        if self.size == 0:
            print("Error: Queue is Empty")
            return
        else:
            item = self.queue[self.head]
            self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return item

    def __str__(self):
        ll = list(map(job2str, self.queue))
        return str(ll)
