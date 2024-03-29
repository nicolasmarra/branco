from dotenv import load_dotenv
import os
import re
import asyncio
from paris import *
from pronostics import afficher_pronostic

# chargement des variables d'environnement
load_dotenv()

# récupération du token
TOKEN = os.getenv('TOKEN')

# récupération de l'id du channel général
PARIS_CHANNEL_ID = int(os.getenv('PARIS_CHANNEL_ID'))


# configuration des itents Discord
intents = discord.Intents.all()

# création du client Discord
client = discord.Client(intents=intents)

async def supprimer_message(channel):
    await channel.purge()

async def envoyer_messages(channel, messages):
    for message in messages:
        if isinstance(message, discord.Embed):
            await channel.send(embed=message)
        else:
            await channel.send(message)
    await asyncio.sleep(2)

async def envoyer_message(channel, message):
    await channel.send(message)

async def envoyer_paris_du_jour(commande="/paris"):
    channel = client.get_channel(PARIS_CHANNEL_ID)
    #print(commande)
    embed_paris = afficher_paris(commande)
    #print(embed_paris)
    messages = []
    for embed_pari in embed_paris:
        messages.append(embed_pari)
    await envoyer_messages(channel, messages)

async def envoyer_pronostics():
    channel = client.get_channel(PARIS_CHANNEL_ID)
    embed_pronostics = afficher_pronostic()
    messages = []
    for embed_pronostic in embed_pronostics:
        messages.append(embed_pronostic)
    await envoyer_messages(channel, messages)

async def traiter_commandes(message):
    commande = message.content
    commande_divisee = commande.split(" ")

    if message.channel.id == PARIS_CHANNEL_ID and (commande == "/paris" or commande == "/paris-live"):
        await envoyer_paris_du_jour(commande)

    elif message.channel.id == PARIS_CHANNEL_ID and commande_divisee[0] =="/paris":
        if len(commande_divisee) >= 3 and commande_divisee[1] == "-c":

            url = get_url(commande_divisee[2])
            if url is None:
                await envoyer_message(message.channel, "Ce championnat n'existe pas")
            
            else:   
                embed_paris = afficher_paris(commande_divisee[0], url)
                messages = []
                for embed_pari in embed_paris:
                    messages.append(embed_pari)
                await envoyer_messages(message.channel, messages)

        elif len(commande_divisee) >= 3 and commande_divisee[1] == "-e":
            equipe = commande[9:]
            equipe = re.split(r'\s|-', equipe)
            equipe = ' '.join(equipe)[1:]
            embed_equipe = get_paris_equipe(equipe,commande_divisee[0])

            if (embed_equipe is None):
                await envoyer_message(message.channel, "Cette équipe ne joue pas aujourd'hui")
            else: 
                await message.channel.send(embed=embed_equipe)
    
        elif len(commande_divisee) == 3 and commande_divisee[1] == "-d":
            equipe = commande_divisee[2]
            lien_match = get_lien_match(equipe,commande_divisee[0])
            if (lien_match is None):
                await envoyer_message(message.channel, "Cette équipe ne joue pas aujourd'hui")
            else:
                print(lien_match)

    elif message.channel.id == PARIS_CHANNEL_ID and (message.content == "/pronostic" or (len(commande_divisee) == 2 and commande_divisee[0] == "/pronostic" and commande_divisee[1] == "1")):
        
        await envoyer_pronostics()
    
    elif message.channel.id == PARIS_CHANNEL_ID and len(commande_divisee) == 2 and commande_divisee[0] == "/pronostic" and commande_divisee[1] == "2":
        
        embed_pronostics = afficher_pronostic(commande_divisee[1])
        messages = []
        for embed_pronostic in embed_pronostics:
            messages.append(embed_pronostics)
        await envoyer_messages(message.channel, messages)

    elif message.channel.id == PARIS_CHANNEL_ID and message.content == "/help":
        embed_help = discord.Embed(title="**Liste des commandes**", color=0xff0000)
        embed_help.add_field(name="**/paris**", value="Affiche les paris du jour")
        embed_help.add_field(name="**/paris-live**", value="Affiche les paris en live")
        embed_help.add_field(name="**/paris -c <championnat>**", value="Affiche les paris du championnat")
        embed_help.add_field(name="**/paris -e <équipe>**", value="Affiche les paris de l'équipe")
        embed_help.add_field(name="**/pronostic**", value="Affiche les pronostics du jour")
        embed_help.add_field(name="**/pronostic 1**", value="Affiche les pronostics du jour (sportytrader)")
        embed_help.add_field(name="**/pronostic 2**", value="Affiche les pronostics du jour (rue des joueurs)")
        embed_help.add_field(name="**/delete**", value="Supprime les messages du channel")
        await message.channel.send(embed=embed_help)


    elif message.channel.id == PARIS_CHANNEL_ID and message.content == "/delete" and (message.author == "nicolasmarra" or message.author.guild_permissions.administrator):
        await supprimer_message(message.channel)
    
    elif message.channel.id == PARIS_CHANNEL_ID and message.author != client.user: 
        await message.channel.send("Commande inconnue : tapez /help pour afficher la liste des commandes")


# événement au démarrage du bot
@client.event 
async def on_ready():
    print("Le bot est prêt!!! ")

# événement à la réception d'un message
@client.event
async def on_message(message):
    await traiter_commandes(message)

client.run(TOKEN)

