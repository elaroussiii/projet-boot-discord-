# bot_config.py
import os
import discord

# Préfixe des commandes (par exemple: !helpme, !reset)
COMMAND_PREFIX = "!"

# Intents (permissions que ton bot demande à Discord)
INTENTS = discord.Intents.default()
INTENTS.message_content = True   # nécessaire pour lire le contenu des messages
INTENTS.members = True           # utile si tu veux gérer les utilisateurs

def get_token():
    """
    Récupère le token depuis la variable d'environnement DISCORD_TOKEN.

    ⚠️ Important : ne mets JAMAIS ton token directement dans le code.
    Mets-le dans une variable d'environnement :
      - Windows PowerShell :   setx DISCORD_TOKEN "ton_token"
      - Git Bash (temporaire): export DISCORD_TOKEN="ton_token"

    Ensuite, redémarre ton terminal pour que la variable soit active.
    """
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError(
            "❌ Le token Discord est manquant. "
            "Définis la variable d'environnement DISCORD_TOKEN."
        )
    return token
