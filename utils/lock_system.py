# utils/lock_system.py
# Système de verrouillage par ressource (ex: "history") avec file d'attente
from structures.queue import Queue
from structures.hashtable import HashTable

class _Lock:
    def __init__(self):
        self.holder = None       # user_id courant
        self.queue = Queue()     # file d'attente des user_id

class LockSystem:
    def __init__(self):
        # ressource(string) -> _Lock
        self._locks = HashTable()

    def _get_or_create(self, resource: str) -> _Lock:
        lk = self._locks.get(resource)
        if lk is None:
            lk = _Lock()
            self._locks.set(resource, lk)
        return lk

    def status(self, resource: str):
        """Retourne (holder, queue_list)."""
        lk = self._get_or_create(resource)
        return lk.holder, lk.queue.to_list()

    def acquire(self, resource: str, user_id: int):
        """
        Retourne (status, position)
        status ∈ {"acquired","already","queued"}
        position = 0 si acquired/already, sinon position dans la file (1 = tête)
        """
        lk = self._get_or_create(resource)
        if lk.holder is None:
            lk.holder = user_id
            return "acquired", 0
        if lk.holder == user_id:
            return "already", 0

        # déjà dans la queue ?
        pos = lk.queue.position_of(user_id)
        if pos == -1:
            lk.queue.enqueue(user_id)
            pos = len(lk.queue)
        return "queued", pos

    def release(self, resource: str, user_id: int):
        """
        Libère le lock si user_id est le holder.
        Retourne (ok, info, next_id)
        info ∈ {"not_holder","released","transferred"}
        """
        lk = self._get_or_create(resource)
        if lk.holder != user_id:
            return False, "not_holder", None

        if lk.queue.is_empty():
            lk.holder = None
            return True, "released", None
        next_id = lk.queue.dequeue()
        lk.holder = next_id
        return True, "transferred", next_id
