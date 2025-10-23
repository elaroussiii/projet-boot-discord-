# test_persistence.py
from features.history_manager import HistoryManager
from features.conversation_manager import ConversationManager
from utils.persistence import save_json, load_json

# Managers
hm = HistoryManager()
cm = ConversationManager()

uid = 111  # faux id utilisateur

# --- Simuler des actions
hm.add_command(uid, "!ping")
hm.add_command(uid, "!help")

cm.start_conversation(uid)               # question root
cm.handle_user_message(uid, "web")       # Q1 front/back
cm.handle_user_message(uid, "back")      # Q2 python/node
cm.handle_user_message(uid, "python")    # feuille (réponse finale)

# --- Sauvegarder
save_json("data/history_data.json", hm.dump_for_save())
save_json("data/conversation_data.json", cm.dump_for_save())
print("💾 Sauvegarde effectuée.")

# --- Recharger dans de nouveaux objets et vérifier
hm2 = HistoryManager()
cm2 = ConversationManager()
hm2.load_from_data(load_json("data/history_data.json"))
cm2.load_from_data(load_json("data/conversation_data.json"))
print("✅ Rechargement effectué.")
print("Historique rechargé:", hm2.get_all_commands(uid))
