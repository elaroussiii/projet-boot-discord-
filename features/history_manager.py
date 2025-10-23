# features/history_manager.py
# Gère l'historique des commandes de chaque utilisateur
# Utilise les structures manuelles : HashTable + LinkedList

from structures.linked_list import LinkedList
from structures.hashtable import HashTable

class HistoryManager:
    def __init__(self):
        # hashtable : key = user_id (int ou str), value = LinkedList instance
        self._table = HashTable()

    def _get_or_create_list(self, user_id):
        """Récupère ou crée une liste chaînée pour l'utilisateur."""
        lst = self._table.get(user_id)
        if lst is None:
            lst = LinkedList()
            self._table.set(user_id, lst)
        return lst

    def add_command(self, user_id, command_str):
        """Ajoute une commande à l'historique d'un utilisateur."""
        lst = self._get_or_create_list(user_id)
        lst.append(command_str)

    def get_last_command(self, user_id):
        """Retourne la dernière commande de l'utilisateur (ou None)."""
        lst = self._table.get(user_id)
        if lst is None:
            return None
        return lst.get_last()

    def get_all_commands(self, user_id):
        """Retourne la liste (Python list) de toutes les commandes de l'utilisateur."""
        lst = self._table.get(user_id)
        if lst is None:
            return []
        return lst.get_all()

    def clear_history(self, user_id):
        """Vide l'historique d'un utilisateur."""
        lst = self._table.get(user_id)
        if lst:
            lst.clear()

    def delete_user_history(self, user_id):
        """Supprime complètement l'entrée de la table pour cet utilisateur."""
        self._table.delete(user_id)

    def export_history_text(self, user_id):
        """Retourne l'historique sous forme de texte (utile pour un export)."""
        cmds = self.get_all_commands(user_id)
        if not cmds:
            return ""
        lines = [f"{i+1}. {c}" for i, c in enumerate(cmds)]
        return "\n".join(lines)

    # Sauvegarde/chargement (pour plus tard)
    def dump_for_save(self):
        """Transforme les données en dictionnaire serialisable pour sauvegarde."""
        out = {}
        for key in self._table.keys():
            ll = self._table.get(key)
            out[str(key)] = ll.get_all() if ll else []
        return out

    def load_from_data(self, data_dict):
        """Recharge les données sauvegardées."""
        for k, cmds in data_dict.items():
            try:
                user_id = int(k)
            except ValueError:
                user_id = k
            ll = LinkedList()
            for c in cmds:
                ll.append(c)
            self._table.set(user_id, ll)
