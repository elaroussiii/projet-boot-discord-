# test_conversation_manager.py
# Test du système de conversation (ConversationManager)

from features.conversation_manager import ConversationManager

cm = ConversationManager()
uid = 42  # identifiant utilisateur simulé

# Lancement de la conversation
print("---- START ----")
print(cm.start_conversation(uid))              # Question root (choix python / web / musique)

# On choisit Python
print("\n-- Réponse: python --")
print(cm.handle_user_message(uid, "python"))   # Question débutant ? (oui/non)

# On répond oui (débutant)
print("\n-- Réponse: oui --")
print(cm.handle_user_message(uid, "oui"))      # Feuille : conseils débutant

# On reset
print("\n-- Commande: reset --")
print(cm.handle_user_message(uid, "reset"))    # Retour au root

# On teste speak about
print("\n-- Commande: speak about web --")
print(cm.handle_user_message(uid, "speak about web"))   # devrait dire oui

# On part sur Web
print("\n-- Réponse: web --")
print(cm.handle_user_message(uid, "web"))      # Q1 Front ou Back

# On répond back
print("\n-- Réponse: back --")
print(cm.handle_user_message(uid, "back"))     # Q2 Python ou Node

# On répond Python
print("\n-- Réponse: python --")
print(cm.handle_user_message(uid, "python"))   # Feuille: back Python
