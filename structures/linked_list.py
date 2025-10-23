# structures/linked_list.py
# Implémentation d'une liste chaînée simple pour stocker les commandes d'un utilisateur

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, value):
        """Ajoute un élément à la fin de la liste chaînée"""
        node = Node(value)
        if not self.head:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.length += 1

    def get_all(self):
        """Retourne tous les éléments sous forme de liste Python"""
        values = []
        current = self.head
        while current:
            values.append(current.value)
            current = current.next
        return values

    def get_last(self):
        """Retourne le dernier élément ajouté"""
        return self.tail.value if self.tail else None

    def clear(self):
        """Vide complètement la liste"""
        self.head = None
        self.tail = None
        self.length = 0

    def __len__(self):
        return self.length

    def __repr__(self):
        return " -> ".join(self.get_all()) if self.head else "Empty LinkedList"
