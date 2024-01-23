import discord 
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup

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

def get_paris():
    url = "https://www.betclic.fr/football-s1"

    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, "html.parser")

    paris_items = soup.find_all(class_="cardEvent ng-star-inserted")

    paris = []

    for pari_item in paris_items:
        pari_info = {}

        equipes_infos = pari_item.find_all(class_="scoreboard_contestantLabel")
        if len(equipes_infos) >= 2:
            pari_info["equipe_domicile"] = equipes_infos[0].get_text(strip=True)
            pari_info["equipe_exterieur"] = equipes_infos[1].get_text(strip=True)
        else: 
            continue

        
        cotes_infos = pari_item.select(".oddValue.ng-star-inserted")
        if len(cotes_infos) >= 3:
            pari_info["cote_domicile"] = cotes_infos[0].get_text(strip=True)
            pari_info["cote_match_nul"] = cotes_infos[1].get_text(strip=True)
            pari_info["cote_exterieur"] = cotes_infos[2].get_text(strip=True)
        else:
            continue

        evenement_infos = pari_item.find_all("span", class_="breadcrumb_itemLabel ng-star-inserted")
        type_evenement = " ".join(element.get_text(strip=True) for element in evenement_infos if element and element.get_text(strip=True))
        pari_info["type_evenement"] = type_evenement

        evenement_heure = pari_item.find("div", class_="event_infoTime ng-star-inserted")
        pari_info["evenement_heure"] = evenement_heure.get_text(strip=True)
        
        paris.append(pari_info)

    return paris



# événement au démarrage du bot
@client.event 
async def on_ready():
    print("Le bot est prêt!!! ")

# événement à la réception d'un message
@client.event
async def on_message(message):
    if message.channel.id == PARIS_CHANNEL_ID and message.content == "/paris":

        for pari_info in get_paris():
            equipe_domicile = pari_info.get("equipe_domicile", "N/A")
            equipe_exterieur = pari_info.get("equipe_exterieur", "N/A")
            cote_domicile = pari_info.get("cote_domicile", "N/A")
            cote_match_nul = pari_info.get("cote_match_nul", "N/A")
            cote_exterieur = pari_info.get("cote_exterieur", "N/A")
            type_evenement = pari_info.get("type_evenement", "N/A")
            evenement_heure = pari_info.get("evenement_heure", "N/A")

            message_paris = (
                f"Cotes: {equipe_domicile} : {cote_domicile} /  {equipe_exterieur} : {cote_exterieur} / Match Nul : {cote_match_nul}\n"
                )
            embed_paris = discord.Embed(title=f"**{type_evenement} - {evenement_heure}**\n", color=0xff0000)
            embed_paris.add_field(name=f"**{equipe_domicile} vs {equipe_exterieur}**", value=message_paris)
            await message.channel.send(embed=embed_paris)


    if message.content == "/delete" and (message.author == "nicolasmarra" or message.author.guild_permissions.administrator):
        await message.channel.purge()
        
client.run(TOKEN)