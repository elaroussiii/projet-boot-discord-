# structures/queue.py
# File (Queue) basée sur une liste chaînée simple — O(1) enqueue/dequeue

class _QNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def enqueue(self, item):
        node = _QNode(item)
        if not self._head:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            return None
        val = self._head.value
        self._head = self._head.next
        if not self._head:
            self._tail = None
        self._size -= 1
        return val

    def peek(self):
        return self._head.value if self._head else None

    def is_empty(self):
        return self._size == 0

    def __len__(self):
        return self._size

    # utilitaires pratiques
    def to_list(self):
        out = []
        cur = self._head
        while cur:
            out.append(cur.value)
            cur = cur.next
        return out

    def position_of(self, item):
        idx = 1
        cur = self._head
        while cur:
            if cur.value == item:
                return idx
            idx += 1
            cur = cur.next
        return -1
