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

    matches_elements = soup.find_all(class_="cardEvent ng-star-inserted")

    matches = []

    for match_element in matches_elements:
        match_info = {}

        team_elements = match_element.find_all(class_="scoreboard_contestantLabel")
        if len(team_elements) >= 2:
            match_info["team_home"] = team_elements[0].get_text(strip=True)
            match_info["team_away"] = team_elements[1].get_text(strip=True)

        
        odd_elements = match_element.select(".oddValue.ng-star-inserted")
        if len(odd_elements) >= 3:
            match_info["odd_home"] = odd_elements[0].get_text(strip=True)
            match_info["odd_draw"] = odd_elements[1].get_text(strip=True)
            match_info["odd_away"] = odd_elements[2].get_text(strip=True)


        event_type_element = match_element.find("span", class_="breadcrumb_itemLabel.ng-star-inserted")
        match_info["event_type"] = event_type_element.get_text(strip=True) if event_type_element else ""

        matches.append(match_info)

    return matches



# événement au démarrage du bot
@client.event 
async def on_ready():
    print("Le bot est prêt!!! ")

# événement à la réception d'un message
@client.event
async def on_message(message):
    if message.channel.id == PARIS_CHANNEL_ID and message.content == "/paris":
       await message.channel.send("Les paris du jour : ")
       
    for match_info in get_paris():
        team_home = match_info.get("team_home", "N/A")
        team_away = match_info.get("team_away", "N/A")
        odd_home = match_info.get("odd_home", "N/A")
        odd_draw = match_info.get("odd_draw", "N/A")
        odd_away = match_info.get("odd_away", "N/A")
        event_type = match_info.get("event_type", "N/A")
        
        formatted_message = (
            f"{event_type}\n"
            f"{team_home} Vs {team_away}\n"
            f"Cotes: {team_home} : {odd_home} /  {team_away} : {odd_away} / Match Nul : {odd_away}\n"
            f"\n\n"
        )
        await message.channel.send(formatted_message)

client.run(TOKEN)