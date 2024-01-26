import discord
from bs4 import BeautifulSoup
import requests



def get_pronostic(site):

    url = "https://www.sportytrader.com/pronostics/football/"

    if site == "2":
            url = "https://www.ruedesjoueurs.com/pronostics/foot.html"
        
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    if site == "2":

        pronostics_items = soup.find_all(class_="card vevent")

        pronostics = []
        for pronostic_item in pronostics_items:
            
            pronostic_info = {}
            pronostic_lien = pronostic_item.find("a", class_="full_link url").get("href")
            pronostic_info["lien"] = pronostic_lien

            pronostic_competition = pronostic_item.find('div', class_='head flex').find_all('div')[0].text.strip()
            pronostic_competition_pays = pronostic_item.find('div', class_='head flex').find_all('div')[1].text.strip()
            pronostic_info["competition"] = pronostic_competition
            pronostic_info["competition_pays"] = pronostic_competition_pays

            pronostic_equipe_domicile = pronostic_item.find('div', class_='main_info flex').find_all('p', class_="medium")[0].text.strip()
            pronostic_equipe_exterieur = pronostic_item.find('div', class_='main_info flex').find_all('p', class_="medium")[1].text.strip()
            pronostic_info["equipe_domicile"] = pronostic_equipe_domicile
            pronostic_info["equipe_exterieur"] = pronostic_equipe_exterieur

            pronostic_date_heure = pronostic_item.find('div', class_='main_info flex').find_all('abbr', class_="round dtstart")[0].text.strip()
            pronostic_match_date = pronostic_date_heure.split("  ")[0]
            pronostic_match_heure = pronostic_date_heure.split("  ")[1]
            pronostic_info["match_date"] = pronostic_match_date
            pronostic_info["match_heure"] = pronostic_match_heure

            pronostic_titre = pronostic_item.find('div', class_='pronostic').find_all('p')[0].text.strip()
            pronostic_suggestion = pronostic_item.find('div', class_='pronostic').find_all('p')[1].text.strip()
            pronostic_suggestion_cote = pronostic_item.find('div', class_='offres flex stretch').find('a', class_="rounded active classactive").find('span',class_="large").text.strip()
            pronostic_info["titre"] = pronostic_titre
            pronostic_info["suggestion"] = pronostic_suggestion
            pronostic_info["suggestion_cote"] = pronostic_suggestion_cote

            pronostics.append(pronostic_info)

        return pronostics
    else:

        pronostics_items = soup.find_all(class_="h-card-prono")

        pronostics = []
        for pronostic_item in pronostics_items:
            
            pronostic_info = {}

            pronostic_date_heure = pronostic_item.find('p', class_='text-center text-xs mt-2 dark:text-white').text.strip()
            pronostic_info["date_heure"] = pronostic_date_heure
            
            pronostic_pays_competition = pronostic_item.find('p', class_='text-center dark:text-white').text.strip()
            pronostic_pays = pronostic_pays_competition.split("\n")[0]
            pronostic_competition = pronostic_pays_competition.split("\n")[1]      
            pronostic_info["competition_pays"] = pronostic_pays
            pronostic_info["competition"] = pronostic_competition

            pronostic_details_match = pronostic_item.find('a',class_="relative flex flex-col w-full mx-auto mt-2 clickandstop")
            
            pronostic_lien = pronostic_details_match.get("href")
            pronostic_info["lien"] = pronostic_lien

            pronostic_equipe_domicile = pronostic_details_match.find_all('span',class_="font-semibold text-center flex min-h-[45px] dark:text-white")[0].text.strip()
            pronostic_equipe_exterieur = pronostic_details_match.find_all('span',class_="font-semibold text-center flex min-h-[45px] dark:text-white")[1].text.strip()
            pronostic_info["equipe_domicile"] = pronostic_equipe_domicile
            pronostic_info["equipe_exterieur"] = pronostic_equipe_exterieur

            pronostic_details_pari = pronostic_item.find('div',class_="bg-gray-100 h-28 mt-3 p-4 rounded-md path-prono")

            pronostic_titre = pronostic_details_pari.find('p', class_="text-center").text.strip()
            pronostic_suggestion = pronostic_details_pari.find('p', class_="text-center font-semibold").text.strip()
            pronostic_info["titre"] = pronostic_titre
            pronostic_info["suggestion"] = pronostic_suggestion

            pronostic_suggestion_cote = pronostic_item.find('bet-now')['odd']
            pronostic_info["suggestion_cote"] = pronostic_suggestion_cote

            pronostics.append(pronostic_info)
           

        return pronostics

def afficher_pronostic(site="1"):
    embed_pronostics_list = []

    for pronostic_info in get_pronostic(site):
        equipe_domicile = pronostic_info.get("equipe_domicile")
        equipe_exterieur = pronostic_info.get("equipe_exterieur")
        competition = pronostic_info.get("competition")
        competition_pays = pronostic_info.get("competition_pays")
        if site == "2":
            match_date = pronostic_info.get("match_date")
            match_heure = pronostic_info.get("match_heure")
        else: 
            date_heure = pronostic_info.get("date_heure")

        titre = pronostic_info.get("titre")
        suggestion = pronostic_info.get("suggestion")
        suggestion_cote = pronostic_info.get("suggestion_cote")
        #lien = pronostic_info.get("lien")

        message_pronositc = (
            f"**{titre}**:\n"
            f"{suggestion} : {suggestion_cote}\n"
        )

        if site == "2":
            embed_pronostic = discord.Embed(title=f"**{competition} - {competition_pays} : le {match_date} à {match_heure}**\n", color=0x0000ff)
        else :
                embed_pronostic = discord.Embed(title=f"**{competition} - {competition_pays} : {date_heure}**\n", color=0x0000ff)
            
        embed_pronostic.add_field(name=f"**{equipe_domicile} vs {equipe_exterieur}**", value=message_pronositc)

        embed_pronostics_list.append(embed_pronostic)
        
    return embed_pronostics_list

