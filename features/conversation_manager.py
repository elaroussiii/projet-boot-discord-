# features/conversation_manager.py
# Système de discussion/questionnaire basé sur un arbre (binaire ou non)
# - Commandes prévues : "reset", "speak about X"
# - Stocke l'état par utilisateur via HashTable (structure manuelle)
#
# Intégration prévue côté bot :
#   - !helpme           -> start_conversation(user_id) puis envoyer le message retourné
#   - pendant la conv   -> handle_user_message(user_id, msg) et envoyer la réponse
#   - !reset            -> reset(user_id)
#   - !speak about X    -> speak_about(topic)

from structures.hashtable import HashTable

class TreeNode:
    """
    Nœud d'arbre de conversation.
    - question: str | None  -> Question à poser si ce n'est pas une feuille
    - options: dict[str, TreeNode] | None -> transitions par option (non-binaire autorisé)
    - result: str | None -> Réponse finale si feuille
    - key: str | None -> identifiant de sujet (sert pour 'speak about X')
    """
    def __init__(self, question=None, options=None, result=None, key=None):
        self.question = question
        self.options = options or {}
        self.result = result
        self.key = key

    def is_leaf(self):
        return self.result is not None and not self.options


class ConversationManager:
    """
    Gère un questionnaire multi-sujets :
      - Root demande le sujet (ex: python / web / musique)
      - Chaque sujet a son sous-arbre de questions
      - L'état courant de chaque user_id est stocké dans une HashTable
    """
    def __init__(self):
        # table: user_id -> {"node": TreeNode, "path": [str]}
        self._state = HashTable()
        # construit l'arbre de conversation et l'index des sujets
        self.root, self._topics = self._build_conversation_tree()

        # Quelques synonymes usuels pour options fréquentes
        self._synonyms = {
            "oui": "oui", "yes": "oui", "y": "oui",
            "non": "non", "no": "non", "n": "non",
            "front": "front", "frontend": "front",
            "back": "back", "backend": "back",
            "django": "django", "flask": "flask",
            "scripts": "scripts", "script": "scripts",
            "node": "node", "nodejs": "node",
            "instrument": "instrument", "guitare": "instrument", "piano": "instrument",
            "mao": "mao", "beat": "mao", "prod": "mao",
            "python": "python", "web": "web", "musique": "musique", "music": "musique",
        }

    # -----------------------------
    # Construction des arbres
    # -----------------------------
    def _build_python_subtree(self):
        # Q1: Débutant ?
        q1 = TreeNode(
            question="Tu es débutant en Python ? (oui / non)",
            options={}
        )
        # Feuille pour débutant
        leaf_debutant = TreeNode(
            result=("Je te conseille de commencer par :\n"
                    "- variables, types, conditions, boucles\n"
                    "- fonctions et modules\n"
                    "- petits scripts (calculatrice, mini-jeux)\n"
                    "👉 Ressources: docs.python.org, w3schools/python")
        )
        # Q2 si non-débutant
        q2 = TreeNode(
            question="Tu préfères faire des frameworks web ou des scripts ? (django / flask / scripts)",
            options={}
        )
        leaf_django = TreeNode(
            result=("🚀 Django : structure MVC, ORM intégré, admin auto.\n"
                    "Étapes: créer projet, app, modèles, vues, templates.\n"
                    "👉 Ressources: docs.djangoproject.com")
        )
        leaf_flask = TreeNode(
            result=("🧪 Flask : micro-framework flexible.\n"
                    "Étapes: routes, templates Jinja, extensions (SQLAlchemy, WTForms).\n"
                    "👉 Ressources: flask.palletsprojects.com")
        )
        leaf_scripts = TreeNode(
            result=("🛠️ Scripts : CLI, automatisation, parsing (argparse), requests.\n"
                    "Idées: batch rename, web-scraping, cron.\n"
                    "👉 Ressources: Real Python, Hitchhiker’s Guide")
        )

        q2.options = {
            "django": leaf_django,
            "flask": leaf_flask,
            "scripts": leaf_scripts,
        }
        q1.options = {
            "oui": leaf_debutant,
            "non": q2,
        }
        return q1

    def _build_web_subtree(self):
        q1 = TreeNode(
            question="Tu veux faire du Front ou du Back ? (front / back)",
            options={}
        )
        leaf_front = TreeNode(
            result=("🎨 Front-end : HTML + CSS + JS.\n"
                    "Étapes: sémantique HTML, Flex/Grid, DOM, fetch API.\n"
                    "Frameworks: React/Vue/Svelte.\n"
                    "👉 Ressources: MDN Web Docs, Frontend Mentor")
        )
        q2_back = TreeNode(
            question="Back : plutôt Python ou Node ? (python / node)",
            options={}
        )
        leaf_back_py = TreeNode(
            result=("🐍 Back Python : FastAPI/Flask/Django REST.\n"
                    "Concepts: API REST, ORM, auth, déploiement (uvicorn, docker).")
        )
        leaf_back_node = TreeNode(
            result=("🟢 Back Node : Express/Nest.\n"
                    "Concepts: middleware, routing, JWT, Prisma/TypeORM, PM2.")
        )
        q2_back.options = {
            "python": leaf_back_py,
            "node": leaf_back_node,
        }
        q1.options = {
            "front": leaf_front,
            "back": q2_back,
        }
        return q1

    def _build_music_subtree(self):
        q1 = TreeNode(
            question="Tu veux parler Instrument ou MAO ? (instrument / mao)",
            options={}
        )
        leaf_instr = TreeNode(
            result=("🎸 Instrument : routine, gammes, accords, métronome, ear training.\n"
                    "Outils: JustinGuitar / PianoLessons / Yousician.")
        )
        leaf_mao = TreeNode(
            result=("🎚️ MAO : choix du DAW (FL, Ableton, Reaper), VST, structure (intro/couplet/refrain), mix de base.\n"
                    "Ressources: YouTube - ‘In The Mix’, ‘ADSR’.")
        )
        q1.options = {
            "instrument": leaf_instr,
            "mao": leaf_mao,
        }
        return q1

    def _build_conversation_tree(self):
        # root propose les sujets
        python_sub = self._build_python_subtree()
        web_sub = self._build_web_subtree()
        music_sub = self._build_music_subtree()

        root = TreeNode(
            question=("De quoi veux-tu parler ? (python / web / musique)\n"
                      "👉 Tu peux aussi taper 'reset' pour recommencer."),
            options={
                "python": python_sub,
                "web": web_sub,
                "musique": music_sub,
            }
        )
        topics = {"python", "web", "musique"}
        return root, topics

    # -----------------------------
    # Gestion d'état utilisateur
    # -----------------------------
    def _ensure_state(self, user_id):
        st = self._state.get(user_id)
        if st is None:
            st = {"node": None, "path": []}
            self._state.set(user_id, st)
        return st

    def reset(self, user_id):
        st = self._ensure_state(user_id)
        st["node"] = None
        st["path"] = []
        return "🔄 Conversation réinitialisée. " + self.start_conversation(user_id)

    def start_conversation(self, user_id):
        st = self._ensure_state(user_id)
        st["node"] = self.root
        st["path"] = []
        return self.root.question

    def get_current_question(self, user_id):
        st = self._ensure_state(user_id)
        node = st["node"]
        if node is None:
            return None
        if node.is_leaf():
            return None
        return node.question

    # -----------------------------
    # Commande 'speak about X'
    # -----------------------------
    def speak_about(self, topic: str):
        t = (topic or "").strip().lower()
        return t in self._topics

    def supported_topics(self):
        return sorted(list(self._topics))

    # -----------------------------
    # Logique principale de réponse
    # -----------------------------
    def handle_user_message(self, user_id, message: str):
        """
        Traite un message utilisateur pendant la conversation.
        - Gère 'reset'
        - Gère 'speak about X'
        - Sinon, tente de prendre une option de l'arbre courant
        Retourne un texte prêt à être envoyé.
        """
        msg = (message or "").strip()
        if not msg:
            return "📝 Donne-moi une réponse ou une option."

        low = msg.lower()

        # Commandes globales
        if low == "reset":
            return self.reset(user_id)

        if low.startswith("speak about"):
            topic = low.replace("speak about", "", 1).strip()
            if not topic:
                return f"🎯 Tu peux demander : speak about <sujet>. Sujets possibles : {', '.join(self.supported_topics())}"
            return ("✅ Oui, je parle de ce sujet." if self.speak_about(topic)
                    else "❌ Désolé, je ne traite pas ce sujet.")

        # État courant
        st = self._ensure_state(user_id)
        node = st["node"]

        # Si pas encore démarré, démarre
        if node is None:
            return self.start_conversation(user_id)

        # Si feuille -> on a déjà donné une réponse finale, proposer restart
        if node.is_leaf():
            return ("✅ " + node.result +
                    "\n\nSi tu veux recommencer : tape **reset**.")

        # Normaliser l'option
        opt = self._normalize_option(low)

        # Tenter le matching sur les options existantes
        if opt in node.options:
            next_node = node.options[opt]
            st["path"].append(opt)
            st["node"] = next_node

            if next_node.is_leaf():
                # Réponse finale
                return "✅ " + next_node.result + "\n\nTape **reset** pour recommencer."
            else:
                # Nouvelle question
                return next_node.question

        # Si pas trouvé, suggérer les options disponibles
        suggestions = ", ".join(node.options.keys())
        return f"❓ Je n’ai pas compris. Choisis parmi : {suggestions}"

    # -----------------------------
    # Helpers
    # -----------------------------
    def _normalize_option(self, s: str) -> str:
        return self._synonyms.get(s.strip().lower(), s.strip().lower())

    # Dump/load pour persistance ultérieure (bonus 5)
    def dump_for_save(self):
        out = {}
        for uid in self._state.keys():
            st = self._state.get(uid) or {}
            # On ne peut pas sérialiser des nœuds : on sauvegarde juste le chemin et on repartira de root au reload.
            out[str(uid)] = {
                "path": st.get("path", [])
            }
        return out

    def load_from_data(self, data):
        for k, st in (data or {}).items():
            try:
                uid = int(k)
            except ValueError:
                uid = k
            # On reconstruit l'état en rejouant le path depuis root
            node = self.root
            path = []
            for step in st.get("path", []):
                step_norm = self._normalize_option(step)
                if node and not node.is_leaf() and step_norm in node.options:
                    node = node.options[step_norm]
                    path.append(step_norm)
                else:
                    node = self.root
                    path = []
                    break
            self._state.set(uid, {"node": node, "path": path})
