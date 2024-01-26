from dotenv import load_dotenv
import os
import re
from paris import *
from pronostics import get_pronostic, afficher_pronostic

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

async def envoyer_message(channel, message):
    await channel.send(message)

async def traiter_commandes(message):
    commande = message.content
    commande_divisee = commande.split(" ")
    if message.channel.id == PARIS_CHANNEL_ID and (commande == "/paris" or commande == "/paris-live"):

        embed_paris = afficher_paris(commande)
        for embed_pari in embed_paris:
            await message.channel.send(embed=embed_pari)

    elif message.channel.id == PARIS_CHANNEL_ID and commande_divisee[0] =="/paris":
        if len(commande_divisee) >= 3 and commande_divisee[1] == "-c":

            url = get_url(commande_divisee[2])
            if url is None:
                await envoyer_message(message.channel, "Ce championnat n'existe pas")
            else:   
                embed_paris = afficher_paris(commande_divisee[0], url)
                for embed_pari in embed_paris:
                    await message.channel.send(embed=embed_pari)

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

    elif message.channel.id == PARIS_CHANNEL_ID and message.content == "/pronostic":
        embed_pronostics = afficher_pronostic()
        for embed_pronostic in embed_pronostics:
            await message.channel.send(embed=embed_pronostic)

    
    elif message.channel.id == PARIS_CHANNEL_ID and message.content == "/help":
        embed_help = discord.Embed(title="**Liste des commandes**", color=0xff0000)
        embed_help.add_field(name="**/paris**", value="Affiche les paris du jour")
        embed_help.add_field(name="**/paris-live**", value="Affiche les paris en live")
        await message.channel.send(embed=embed_help)

            

    elif message.content == "/delete" and (message.author == "nicolasmarra" or message.author.guild_permissions.administrator):
        await message.channel.purge()
        


# événement au démarrage du bot
@client.event 
async def on_ready():
    print("Le bot est prêt!!! ")

# événement à la réception d'un message
@client.event
async def on_message(message):
    await traiter_commandes(message)

client.run(TOKEN)

