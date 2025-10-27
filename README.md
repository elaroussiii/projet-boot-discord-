# Projet Bot Discord B2 — projet-boot-discord

Bot Discord pédagogique qui démontre l’usage de **structures de données codées à la main** (liste chaînée, file/queue, arbre, hashtable), la **persistance** JSON et un **système de verrou** (lock) pour protéger l’intégrité de l’historique.

## ✨ Fonctionnalités :
- Historique des commandes par utilisateur (LinkedList + HashTable)
- Voir toutes les commandes / vider l’historique
- Système de discussion guidée (Arbre non binaire) : `!helpme`, `reset`, `speak about X` (`!speak X`)
- Persistance des données sur disque (JSON) : `!save`
- Protection d’intégrité via **lock** (Queue) : `!lockhistory`, `!unlockhistory`
- Bonus : `!stats` (compte des commandes), `!export` (fichier .txt de l’historique)

## 🎮 Mode d’emploi :

### Historique :
- `!history` → affiche ton historique de commandes
- `!clearhistory` → vide ton historique

### Conversation (arbre de questions) :
- `!helpme` → démarre une conversation guidée
- (réponds simplement aux questions sans `!`)
- `!reset` → réinitialise la conversation en cours
- `!speak <sujet>` → vérifie si le bot traite un sujet (ex: `!speak python`)

### Persistance :
- `!save` → sauvegarde l’état actuel (historique + conversations) dans des fichiers JSON

### Lock (intégrité) :
- `!lockhistory` → réserve l’accès exclusif à l’historique
- `!unlockhistory` → libère le lock ou le transfère à l’utilisateur suivant

### Bonus :
- `!stats` → affiche combien de commandes tu as utilisées
- `!export` → exporte ton historique dans un fichier texte et l’envoie
