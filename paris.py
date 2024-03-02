import discord
import requests
from bs4 import BeautifulSoup
import json
import re

def get_url(competition):
    with open("assets/competition_url.json", "r") as fichier_json:
        competition_url = json.load(fichier_json)


    return competition_url.get(competition, None)    

def get_flag_evenement(evenement):
    with open("assets/competition_flags.json", "r") as fichier_json:
        competition_flags = json.load(fichier_json)

    
    competition = evenement.split("•")[0].strip()
    return competition_flags.get(competition, "")

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

            
        odds = pari_item.find(class_='market_odds')

        cotes = odds.find_all('span', class_=lambda x: x and x.startswith('btn_label ng-tns'))
        
        if len(cotes) >= 3:
                pari_info["cote_domicile"] = cotes[0].get_text(strip=True)
                pari_info["cote_match_nul"] = cotes[1].get_text(strip=True)
                pari_info["cote_exterieur"] = cotes[2].get_text(strip=True)
                
        else:
            continue
        
        
        pourcentages = odds.find_all("div", class_="progressBar_fill")

        if len(pourcentages) >= 3:
            
            pari_info["pourcentage_domicile"] = re.search(r"width: (\d+)%", pourcentages[0]['style']).group(1)
            pari_info["pourcentage_match_nul"] = re.search(r"width: (\d+)%", pourcentages[1]['style']).group(1)
            pari_info["pourcentage_exterieur"] = re.search(r"width: (\d+)%", pourcentages[2]['style']).group(1)    
           

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
        pourcentage_domicile = pari_info.get("pourcentage_domicile")
        pourcentage_match_nul = pari_info.get("pourcentage_match_nul")
        pourcentage_exterieur = pari_info.get("pourcentage_exterieur")        

        if commande == "/paris-live":
            score_equipe_domicile = pari_info.get("score_equipe_domicile")
            score_equipe_exterieur = pari_info.get("score_equipe_exterieur")
        
        flag_evenement = get_flag_evenement(type_evenement)
        paris_info = None
        if commande == "/paris":
            embed_paris = discord.Embed(title=f"**⚽{flag_evenement} {type_evenement} - {evenement_heure}\n{equipe_domicile} vs {equipe_exterieur}**\n", color=0xff0000)
            paris_info = (
            
            f"🏠{equipe_domicile} : {cote_domicile} ({pourcentage_domicile}%)\n"
            f"🚌 {equipe_exterieur} : {cote_exterieur} ({pourcentage_exterieur}%)\n"
            f"Nul : {cote_match_nul} ({pourcentage_match_nul}%)\n"
        )

        elif commande == "/paris-live":
            embed_paris = discord.Embed(title=f"**🏆 {type_evenement} - {evenement_heure}\n{equipe_domicile} {score_equipe_domicile} - {score_equipe_exterieur} {equipe_exterieur}**\n", color=0xff0000)
            paris_info = (
            
            f"🏠{equipe_domicile} : {cote_domicile}\n"
            f"🚌 {equipe_exterieur} : {cote_exterieur}\n"
            f"Nul : {cote_match_nul}\n"
            )

        embed_paris.add_field(name=f"**-------------------------------------------------**", value=f"```yaml\n{paris_info}\n```")
        
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
        pourcentage_domicile = pari_info.get("pourcentage_domicile")
        pourcentage_match_nul = pari_info.get("pourcentage_match_nul")
        pourcentage_exterieur = pari_info.get("pourcentage_exterieur")        
        
        
        equipe = str(equipe).lower()
        if str(equipe_domicile).lower() == equipe or str(equipe_exterieur).lower() == equipe:

            if commande == "/paris-live":
                score_equipe_domicile = pari_info.get("score_equipe_domicile")
                score_equipe_exterieur = pari_info.get("score_equipe_exterieur")

            flag_evenement = get_flag_evenement(type_evenement)
            paris_info = None
            if commande == "/paris":
                embed_paris = discord.Embed(title=f"**⚽{flag_evenement} {type_evenement} - {evenement_heure}\n{equipe_domicile} vs {equipe_exterieur}**\n", color=0xff0000)
                paris_info = (
                
                f"🏠{equipe_domicile} : {cote_domicile} ({pourcentage_domicile}%)\n"
                f"🚌 {equipe_exterieur} : {cote_exterieur} ({pourcentage_exterieur}%)\n"
                f"Nul : {cote_match_nul} ({pourcentage_match_nul}%)\n"
            )

            elif commande == "/paris-live":
                embed_paris = discord.Embed(title=f"**🏆 {type_evenement} - {evenement_heure}\n{equipe_domicile} {score_equipe_domicile} - {score_equipe_exterieur} {equipe_exterieur}**\n", color=0xff0000)
                paris_info = (
                
                f"🏠{equipe_domicile} : {cote_domicile}\n"
                f"🚌 {equipe_exterieur} : {cote_exterieur}\n"
                f"Nul : {cote_match_nul}\n"
                )

            embed_paris.add_field(name=f"**----------------------------------------------------------**", value=f"```yaml\n{paris_info}\n```")


            return embed_paris

def afficher_paris_cote(cote, type, commande, url="https://www.betclic.fr/football-s1"):
    embed_paris_list = []
    for pari_info in get_paris(commande, url):
        equipe_domicile = pari_info.get("equipe_domicile")
        equipe_exterieur = pari_info.get("equipe_exterieur")
        cote_domicile = pari_info.get("cote_domicile")
        cote_match_nul = pari_info.get("cote_match_nul")
        cote_exterieur = pari_info.get("cote_exterieur")
        type_evenement = pari_info.get("type_evenement")
        evenement_heure = pari_info.get("evenement_heure")
        pourcentage_domicile = pari_info.get("pourcentage_domicile")
        pourcentage_match_nul = pari_info.get("pourcentage_match_nul")
        pourcentage_exterieur = pari_info.get("pourcentage_exterieur")

        if (type == 1 and cote_domicile >= cote) or (type == 2 and cote_match_nul >= cote) or (type == 3 and cote_exterieur >= cote) is False:
            continue 


        if commande == "/paris-live":
            score_equipe_domicile = pari_info.get("score_equipe_domicile")
            score_equipe_exterieur = pari_info.get("score_equipe_exterieur")

        
            flag_evenement = get_flag_evenement(type_evenement)
            paris_info = None
            if commande == "/paris":
                embed_paris = discord.Embed(title=f"**⚽{flag_evenement} {type_evenement} - {evenement_heure}\n{equipe_domicile} vs {equipe_exterieur}**\n", color=0xff0000)
                paris_info = (
                
                f"🏠{equipe_domicile} : {cote_domicile} ({pourcentage_domicile}%)\n"
                f"🚌 {equipe_exterieur} : {cote_exterieur} ({pourcentage_exterieur}%)\n"
                f"Nul : {cote_match_nul} ({pourcentage_match_nul}%)\n"
            )

            elif commande == "/paris-live":
                embed_paris = discord.Embed(title=f"**🏆 {type_evenement} - {evenement_heure}\n{equipe_domicile} {score_equipe_domicile} - {score_equipe_exterieur} {equipe_exterieur}**\n", color=0xff0000)
                paris_info = (
                
                f"🏠{equipe_domicile} : {cote_domicile}\n"
                f"🚌 {equipe_exterieur} : {cote_exterieur}\n"
                f"Nul : {cote_match_nul}\n"
                )

            embed_paris.add_field(name=f"**----------------------------------------------------------**", value=f"```yaml\n{paris_info}\n```")


        embed_paris_list.append(embed_paris)
    
    return embed_paris_list


    
def get_lien_match(equipe,commande, url="https://www.betclic.fr/football-s1"):
    for pari_info in get_paris(commande, url):
        equipe_domicile = pari_info.get("equipe_domicile")
        equipe_exterieur = pari_info.get("equipe_exterieur")
        evenement_lien = pari_info.get("evenement_lien")

        if(equipe_domicile == equipe or equipe_exterieur == equipe):
            return evenement_lien

    return None



