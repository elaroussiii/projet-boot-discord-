# main.py
import discord
from discord.ext import commands
from bot_config import COMMAND_PREFIX, INTENTS, get_token

from features.history_manager import HistoryManager
from features.conversation_manager import ConversationManager
from utils.persistence import save_json, load_json
from utils.lock_system import LockSystem

# -------------------------------------
# Initialisation du bot et des gestionnaires
# -------------------------------------
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=INTENTS)

history = HistoryManager()
conversation = ConversationManager()
locksys = LockSystem()

# -------------------------------------
# Événements
# -------------------------------------
@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

    # Chargement des données si présentes
    hist_data = load_json("data/history_data.json")
    conv_data = load_json("data/conversation_data.json")

    try:
        history.load_from_data(hist_data)
    except Exception as e:
        print("⚠️ Erreur chargement historique:", e)

    try:
        conversation.load_from_data(conv_data)
    except Exception as e:
        print("⚠️ Erreur chargement conversation:", e)

    print("💾 Données chargées (si présentes).")

# -------------------------------------
# Commandes liées à l’historique
# -------------------------------------
@bot.command(name="history")
async def history_cmd(ctx):
    # Check lock
    holder, _ = locksys.status("history")
    if holder is not None and holder != ctx.author.id:
        await ctx.send("⛔ L'historique est verrouillé par un autre utilisateur. Tape `!lockhistory` pour entrer en file d'attente.")
        return

    cmds = history.get_all_commands(ctx.author.id)
    if not cmds:
        await ctx.send("ℹ️ Ton historique est vide.")
    else:
        await ctx.send(f"🧾 Ton historique : {cmds}")

@bot.command()
async def clearhistory(ctx):
    # Check lock
    holder, _ = locksys.status("history")
    if holder is not None and holder != ctx.author.id:
        await ctx.send("⛔ L'historique est verrouillé par un autre utilisateur. Tape `!lockhistory` pour entrer en file d'attente.")
        return

    history.clear_history(ctx.author.id)
    await ctx.send("🗑️ Historique vidé.")

# -------------------------------------
# Commandes liées à la conversation
# -------------------------------------
@bot.command(name="helpme")
async def helpme_cmd(ctx):
    """Démarre une conversation/questionnaire."""
    msg = conversation.start_conversation(ctx.author.id)
    await ctx.send(msg)

@bot.command(name="reset")
async def reset_cmd(ctx):
    """Réinitialise la conversation."""
    msg = conversation.reset(ctx.author.id)
    await ctx.send(msg)

@bot.command(name="speak")
async def speak_cmd(ctx, *, topic: str = None):
    """Vérifie si un sujet est supporté."""
    if not topic:
        await ctx.send(f"🎯 Sujets possibles : {', '.join(conversation.supported_topics())}")
        return
    if conversation.speak_about(topic):
        await ctx.send("✅ Oui, je parle de ce sujet.")
    else:
        await ctx.send("❌ Désolé, ce sujet n'est pas traité.")

# -------------------------------------
# Sauvegarde (persistance)
# -------------------------------------
@bot.command()
async def save(ctx):
    """Sauvegarde les données sur disque."""
    try:
        save_json("data/history_data.json", history.dump_for_save())
        save_json("data/conversation_data.json", conversation.dump_for_save())
        await ctx.send("💾 Données sauvegardées.")
    except Exception as e:
        await ctx.send(f"❌ Erreur sauvegarde: {e}")

# -------------------------------------
# Commandes de lock (intégrité)
# -------------------------------------
@bot.command()
async def lockhistory(ctx):
    """Demander l'accès exclusif à l'historique."""
    status, pos = locksys.acquire("history", ctx.author.id)
    if status == "acquired":
        await ctx.send("🔒 Tu as maintenant le lock sur l'historique. Tu es le seul à y accéder.")
    elif status == "already":
        await ctx.send("ℹ️ Tu possèdes déjà le lock sur l'historique.")
    else:  # queued
        await ctx.send(f"⏳ Lock déjà pris. Tu es en file d'attente (position {pos}).")

@bot.command()
async def unlockhistory(ctx):
    """Relâcher l'accès exclusif à l'historique."""
    ok, info, next_id = locksys.release("history", ctx.author.id)
    if not ok and info == "not_holder":
        await ctx.send("❌ Tu ne possèdes pas le lock, impossible de le relâcher.")
    elif ok and info == "released":
        await ctx.send("✅ Lock libéré. L'historique est maintenant libre.")
    elif ok and info == "transferred":
        await ctx.send(f"✅ Lock transféré automatiquement à l'utilisateur suivant (ID: {next_id}).")

# -------------------------------------
# Stats (bonus)
# -------------------------------------
@bot.command()
async def stats(ctx):
    """Affiche des statistiques sur ton historique."""
    # Check lock (lecture soumise au lock pour rester cohérent)
    holder, _ = locksys.status("history")
    if holder is not None and holder != ctx.author.id:
        await ctx.send("⛔ L'historique est verrouillé par un autre utilisateur. Tape `!lockhistory` pour entrer en file d'attente.")
        return

    cmds = history.get_all_commands(ctx.author.id)
    if not cmds:
        await ctx.send("ℹ️ Tu n'as encore utilisé aucune commande.")
    else:
        await ctx.send(f"📊 Tu as utilisé **{len(cmds)}** commandes au total depuis le début.")

# -------------------------------------
# Export (bonus)
# -------------------------------------
@bot.command()
async def export(ctx):
    """Exporte ton historique dans un fichier texte et l'envoie."""
    # Check lock (lecture soumise au lock pour rester cohérent)
    holder, _ = locksys.status("history")
    if holder is not None and holder != ctx.author.id:
        await ctx.send("⛔ L'historique est verrouillé par un autre utilisateur. Tape `!lockhistory` pour entrer en file d'attente.")
        return

    cmds = history.get_all_commands(ctx.author.id)
    if not cmds:
        await ctx.send("ℹ️ Ton historique est vide, rien à exporter.")
        return

    filename = f"history_{ctx.author.id}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        for i, cmd in enumerate(cmds, start=1):
            f.write(f"{i}. {cmd}\n")

    await ctx.send(file=discord.File(filename))


# -------------------------------------
# Listener global (messages) - corrigé anti-doublons
# -------------------------------------
@bot.listen("on_message")
async def log_and_converse(message):
    # Ignore les bots (dont toi-même)
    if message.author.bot:
        return

    user_id = message.author.id
    content = message.content.strip()

    # 1) Commandes (préfixe) : on LOG l'historique puis on STOP.
    if content.startswith(COMMAND_PREFIX):
        holder, _ = locksys.status("history")
        # Autoriser l'écriture si pas de lock ou si c'est le détenteur actuel
        if holder is None or holder == user_id:
            history.add_command(user_id, content)

        # Très important :
        # NE PAS APPELER bot.process_commands ici.
        # Avec @bot.listen, discord.py gère déjà les commandes tout seul.
        # On sort pour éviter d'enchaîner la logique "conversation" et/ou doubler la commande.
        return

    # 2) Messages SANS préfixe : gestion de la conversation active
    st = conversation._state.get(user_id)
    if st and st.get("node") is not None:
        reply = conversation.handle_user_message(user_id, content)
        if reply:
            await message.channel.send(reply)
# -------------------------------------

if __name__ == "__main__":
    token = get_token()
    bot.run(token)
