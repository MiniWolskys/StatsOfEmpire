from boto3 import resource
from boto3.dynamodb.conditions import Key
import requests
import json
import pymysql

def request(req):
    return requests.get(req)

def add_to_player_list(leaderboard, first_part, player_list):
    ret = 10000
    pos = 1

    while (ret == 10000):
        players = request(f"https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id={leaderboard}&start={pos}&count=10000").json()
        ret = int(players['count'])
        pos += ret
        for player in players["leaderboard"]:
            if player['clan'] is None:
                player['clan'] = "None"
            if player["profile_id"] in player_list:
                player_list[player["profile_id"]].update({"Id":player['profile_id'], "Name":player['name'], "Steam_Id":player['steam_id'], "Clan":player['clan'], f"{first_part}_Rating":player['rating'], f"{first_part}_Rank":player['rank'], f"{first_part}_Games_Played":player['games'], f"{first_part}_Games_Won":player['wins'], f"{first_part}_Last_Seen":player['last_match_time']})
            else:
                player_list[player["profile_id"]] = {"Id":player['profile_id'], "Name":player['name'], "Steam_Id":player['steam_id'], "Clan":player['clan'], f"{first_part}_Rating":player['rating'], f"{first_part}_Rank":player['rank'], f"{first_part}_Games_Played":player['games'], f"{first_part}_Games_Won":player['wins'], f"{first_part}_Last_Seen":player['last_match_time']}

    return player_list, pos

def get_player_list():
    player_list = {}

    player_list, pos = add_to_player_list(4, "Random_Team", player_list)
    print(f"Retrieved {pos} players from Team Random pool")
    player_list, pos = add_to_player_list(3, "Random", player_list)
    print(f"Retrieved {pos} players from 1v1 Random pool")
    player_list, pos = add_to_player_list(1, "Deathmatch", player_list)
    print(f"Retrieved {pos} players from 1v1 Deathmatch pool")
    player_list, pos = add_to_player_list(2, "Deathmatch_Team", player_list)
    print(f"Retrieved {pos} players from Team Deathmatch pool")
    player_list, pos = add_to_player_list(0, "Unranked", player_list)
    print(f"Retrieved {pos} players from Unranked pool")

    return player_list

def main():
    keys = ["Id", "Name", "Steam_Id", "Clan", "Random_Team_Rating", "Random_Team_Rank", "Random_Team_Games_Played", "Random_Team_Games_Won", "Random_Team_Last_Seen", "Random_Rating", "Random_Rank", "Random_Games_Played", "Random_Games_Won", "Random_Last_Seen", "Deathmatch_Rating", "Deathmatch_Rank", "Deathmatch_Games_Played", "Deathmatch_Games_Won", "Deathmatch_Last_Seen", "Deathmatch_Team_Rating", "Deathmatch_Team_Rank", "Deathmatch_Team_Games_Played", "Deathmatch_Team_Games_Won", "Deathmatch_Team_Last_Seen", "Unranked_Rating", "Unranked_Rank", "Unranked_Games_Played", "Unranked_Games_Won", "Unranked_Last_Seen"]
    players_list = get_player_list()
    print(f"{len(players_list)} retrieved in total.")
    table = "Player_List"
    connection = pymysql.connect(host="testdatabase.csbinovyql8d.eu-west-2.rds.amazonaws.com", user="admin", password="password", db="Player_Base_Information")
    cursor = connection.cursor()
    i = 0
    size = len(players_list)
    for Id in players_list:
        qmarks = ', '.join(['%s'] * len(players_list[Id].keys()))
        query = f"""INSERT INTO {table} ({', '.join(players_list[Id].keys())}) VALUES ({qmarks})"""
        cursor.execute(query, list(players_list[Id].values()))
        print(f"{i*100/size}%", end="\r")
        i += 1
    connection.commit()
    print("100%")

main()
