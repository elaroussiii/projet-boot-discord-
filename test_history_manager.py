# test_history_manager.py
# Test du système d'historique (HistoryManager)

from features.history_manager import HistoryManager

# Création du gestionnaire d'historique
history = HistoryManager()

# Exemple d'identifiant utilisateur (simule un id Discord)
user_id = 123456789

# On ajoute quelques commandes dans l'historique
history.add_command(user_id, "!ping")
history.add_command(user_id, "!help")
history.add_command(user_id, "!play song")

# On affiche toutes les commandes
print("🧾 Historique complet :", history.get_all_commands(user_id))

# On affiche la dernière commande
print("🕐 Dernière commande :", history.get_last_command(user_id))

# On teste l'export formaté
print("\\n📄 Historique formaté :")
print(history.export_history_text(user_id))

# On vide l'historique
history.clear_history(user_id)
print("\\n🗑️ Après suppression :", history.get_all_commands(user_id))

