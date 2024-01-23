import discord 
from dotenv import load_dotenv
import os

# chargement des variables d'environnement
load_dotenv()

# récupération du token
TOKEN = os.getenv('TOKEN')

# configuration des itents Discord
default_intents = discord.Intents.default()
default_intents.all()

# création du client Discord
client = discord.Client(intents=default_intents)

# événement au démarrage du bot
@client.event 
async def on_ready():
    print("Le bot est prêt!!! ")

# événement à la réception d'un message
@client.event
async def on_message(message):
    pass



client.run(TOKEN)