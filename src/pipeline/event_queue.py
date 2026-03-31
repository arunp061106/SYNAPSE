from collections import deque

class EventQueue:

    def __init__(self, batch_size=5):
        self.queue = deque()
        self.batch_size = batch_size

    def push(self, event):
        self.queue.append(event)

    def is_ready(self):
        return len(self.queue) >= self.batch_size

    def get_batch(self):
        batch = []
        while self.queue and len(batch) < self.batch_size:
            batch.append(self.queue.popleft())
        return batch