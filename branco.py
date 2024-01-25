import discord 
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import json

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


def get_url(competition):
    with open("competition_url.json", "r") as fichier_json:
        competition_url = json.load(fichier_json)


    return competition_url.get(competition, None)    

def get_paris(commande, url):
    
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    paris_items = None 

    if commande == "/paris":
        paris_items = soup.find_all(class_=["cardEvent ng-star-inserted","cardEvent is-superLive ng-star-inserted"])
    elif commande == "/paris-live":
        paris_items = soup.find_all(class_="cardEvent is-live ng-star-inserted")
    
    #print(len(paris_items))

    paris = []

    for pari_item in paris_items:
        pari_info = {}

        evenement_lien = pari_item['href']
        pari_info["evenement_lien"] = evenement_lien


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
        

        if commande == "/paris-live":
            score_equipe_domicile = pari_item.find("span", class_="scoreboard_score scoreboard_score-1 ng-star-inserted").get_text(strip=True)
            score_equipe_exterieur = pari_item.find("span", class_="scoreboard_score scoreboard_score-2 ng-star-inserted").get_text(strip=True)
            pari_info["score_equipe_domicile"] = score_equipe_domicile
            pari_info["score_equipe_exterieur"] = score_equipe_exterieur

        paris.append(pari_info)

    return paris


def afficher_paris(commande, url="https://www.betclic.fr/football-s1"):
    embed_paris_list = []
    for pari_info in get_paris(commande, url):
        equipe_domicile = pari_info.get("equipe_domicile")
        equipe_exterieur = pari_info.get("equipe_exterieur")
        cote_domicile = pari_info.get("cote_domicile")
        cote_match_nul = pari_info.get("cote_match_nul")
        cote_exterieur = pari_info.get("cote_exterieur")
        type_evenement = pari_info.get("type_evenement")
        evenement_heure = pari_info.get("evenement_heure")

        if commande == "/paris-live":
            score_equipe_domicile = pari_info.get("score_equipe_domicile")
            score_equipe_exterieur = pari_info.get("score_equipe_exterieur")

        message_paris = (
            f"Cotes: {equipe_domicile} : {cote_domicile} /  {equipe_exterieur} : {cote_exterieur} / Match Nul : {cote_match_nul}\n"
            )
        

        embed_paris = discord.Embed(title=f"**{type_evenement} - {evenement_heure}**\n", color=0xff0000)
        
        if commande == "/paris":
            embed_paris.add_field(name=f"**{equipe_domicile} vs {equipe_exterieur}**", value=message_paris)
        elif commande == "/paris-live":
            embed_paris.add_field(name=f"**{equipe_domicile} {score_equipe_domicile} - {score_equipe_exterieur} {equipe_exterieur}**", value=message_paris)

        embed_paris_list.append(embed_paris)
    
    return embed_paris_list


def get_paris_equipe(equipe,commande, url="https://www.betclic.fr/football-s1"):
    for pari_info in get_paris(commande, url):
        equipe_domicile = pari_info.get("equipe_domicile")
        equipe_exterieur = pari_info.get("equipe_exterieur")
        cote_domicile = pari_info.get("cote_domicile")
        cote_match_nul = pari_info.get("cote_match_nul")
        cote_exterieur = pari_info.get("cote_exterieur")
        type_evenement = pari_info.get("type_evenement")
        evenement_heure = pari_info.get("evenement_heure")
        
        if equipe_domicile == equipe or equipe_exterieur == equipe:

            if commande == "/paris-live":
                score_equipe_domicile = pari_info.get("score_equipe_domicile")
                score_equipe_exterieur = pari_info.get("score_equipe_exterieur")

            message_paris = (
                f"Cotes: {equipe_domicile} : {cote_domicile} /  {equipe_exterieur} : {cote_exterieur} / Match Nul : {cote_match_nul}\n"
            )
        

            embed_paris = discord.Embed(title=f"**{type_evenement} - {evenement_heure}**\n", color=0xff0000)
        
            if commande == "/paris":
                embed_paris.add_field(name=f"**{equipe_domicile} vs {equipe_exterieur}**", value=message_paris)
            elif commande == "/paris-live":
                embed_paris.add_field(name=f"**{equipe_domicile} {score_equipe_domicile} - {score_equipe_exterieur} {equipe_exterieur}**", value=message_paris)

            return embed_paris
    
def get_lien_match(commande, url,equipe):
    for pari_info in get_paris(commande, url):
        equipe_domicile = pari_info.get("equipe_domicile")
        equipe_exterieur = pari_info.get("equipe_exterieur")
        evenement_lien = pari_info.get("evenement_lien")

        if(equipe_domicile == equipe or equipe_exterieur == equipe):
            return evenement_lien

    return None

def afficher_paris_match(url):

    return None

# événement au démarrage du bot
@client.event 
async def on_ready():
    print("Le bot est prêt!!! ")

# événement à la réception d'un message
@client.event
async def on_message(message):
    commande = message.content
    commande_divisee = commande.split(" ")
    if message.channel.id == PARIS_CHANNEL_ID and (commande == "/paris" or commande == "/paris-live"):

        embed_paris = afficher_paris(commande)
        for embed_pari in embed_paris:
            await message.channel.send(embed=embed_pari)

    elif message.channel.id == PARIS_CHANNEL_ID and commande_divisee[0] =="/paris":
        if len(commande_divisee) == 3 and commande_divisee[1] == "-c":

            url = get_url(commande_divisee[2])
            if url is None:
                await message.channel.send("Ce championnat n'existe pas")
            else:   
                embed_paris = afficher_paris(commande_divisee[0], url)
                for embed_pari in embed_paris:
                    await message.channel.send(embed=embed_pari)
        
        elif len(commande_divisee) == 3 and commande_divisee[1] == "-e":
            equipe = commande_divisee[2]
            embed_equipe = get_paris_equipe(equipe,commande_divisee[0])

            if (embed_equipe is None):
                await message.channel.send("Cette équipe ne joue pas aujourd'hui")
            else: 
                await message.channel.send(embed=embed_equipe)
    


    elif message.channel.id == PARIS_CHANNEL_ID and message.content == "/help":
        embed_help = discord.Embed(title="**Liste des commandes**", color=0xff0000)
        embed_help.add_field(name="**/paris**", value="Affiche les paris du jour")
        embed_help.add_field(name="**/paris-live**", value="Affiche les paris en live")
        await message.channel.send(embed=embed_help)

    if message.content == "/delete" and (message.author == "nicolasmarra" or message.author.guild_permissions.administrator):
        await message.channel.purge()
        
client.run(TOKEN)