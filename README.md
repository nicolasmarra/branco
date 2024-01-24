# Branco

Branco est un bot Discord conçu pour fournir des informations sur les paris sportifs. Le bot peut récupérer les cotes pour les matchs en direct (/paris-live) ou les prochains matchs (/paris).

## Installation

1. Installez les dépendances nécessaires à l'aide de la commande suivante :
   ```
   pip install -r requirements.txt
   ```

2. Créez un fichier `.env` à la racine du projet avec les informations suivantes :
   ```
   TOKEN=VOTRE_TOKEN_DISCORD
   PARIS_CHANNEL_ID=ID_DE_VOTRE_CANAL_GENERAL
   ```

3. Exécutez le script Python pour lancer le bot :
   ```
   python3 branco.py
   ```

## Commandes

- `/paris` : affiche les prochains matchs avec leurs cotes.
- `/paris-live` : affiche les cotes des matchs en direct.
- `/delete` : supprime les messages dans le canal (accessible uniquement par l'utilisateur "nicolasmarra" ou les administrateurs du serveur).

**Note :** Assurez-vous que le bot a les autorisations nécessaires pour lire et envoyer des messages dans le canal spécifié.

## TODO

- [x] Afficher les informations sur les matchs du jour et les matchs en live.
- [x] Afficher les inforlations des matchs d'un championnat spécifique.
- [ ] Afficher les classements des équipes avec des détails tels que le face à face, les derniers matchs des équipes, les stats sur les buts encaissés et marqués, et la composition probable.
- [ ] Afficher les pronostics d'un certain match, le pronostic complet avec tous les détails du match, et le pronostic simplifié.

## Auteur

Ce bot a été développé par Nicolas MARRA (nicolasmarra12@gmail.com).
