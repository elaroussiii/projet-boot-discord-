# structures/hashtable.py
# Implémentation simple d'une table de hachage avec chaînage

class HashTable:
    def __init__(self, size=256):
        # On crée une liste de buckets (chaque bucket est une liste)
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def _hash(self, key):
        """Calcule l'indice du bucket pour une clé donnée"""
        if isinstance(key, int):
            h = key
        else:
            h = 0
            for ch in str(key):
                h = (h * 31 + ord(ch)) & 0xFFFFFFFF
        return h % self.size

    def set(self, key, value):
        """Ajoute ou met à jour une valeur associée à une clé"""
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def get(self, key):
        """Récupère une valeur associée à une clé (ou None si absente)"""
        index = self._hash(key)
        bucket = self.buckets[index]
        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key):
        """Supprime une clé de la table"""
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return True
        return False

    def keys(self):
        """Retourne la liste de toutes les clés dans la table"""
        all_keys = []
        for bucket in self.buckets:
            for k, _ in bucket:
                all_keys.append(k)
        return all_keys

    def __repr__(self):
        """Affichage lisible pour debug"""
        pairs = []
        for bucket in self.buckets:
            for k, v in bucket:
                pairs.append(f"{k}: {v}")
        return "{" + ", ".join(pairs) + "}"
