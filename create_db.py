import requests
import json
import io
import sys

# my id 76561198047674342


# Main utilities
def request(req):
	return (requests.get(req))

def error_handling(error_code, message=""):

	if message == "":

		error = {
			"0": "Success",
			"404": "This is not currently available on the API.",
			"500": "Server error."
		}

		if error_code not in error:
			message = "Unknown error."
		else:
			message = error[error_code]

	print(f"Error code : {error_code}.\n{message}", file=sys.stderr)
	exit(error_code)




# Random utilities
def print_players_in_game(player_list):
	for profile in player_list:
		print(f"Player name : {profile['name']}, elo : {profile['rating']}")




# Teams utilities
def sort_player_by_team(player_list):
	teams = {1: [], 2: [], 3: [], 4: [], '-': []}
	for player in player_list:
		teams[player['team']].append(player)
	
	return teams

def print_teams(teams):
	for i in range(4):
		if len(teams[i + 1]) != 0:
			print(f"Team {i + 1}")
			for p in teams[i + 1]:
				print(f"{p['name']}, {p['rating']}")
			print("")
	


# Main function
def main():

	resp = request("https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id=4&start=1&count=10000")

	if resp.status_code != 200:
		error_handling(resp.status_code)
	
	f = io.open("teamgame_random.txt", "w", encoding='utf-8')
	
	f.write('Player Username:Profile ID:Stean ID:Player Rating:Player Rank:Games Played:Games Won:Last Match Time\n')

	for player in resp.json()['leaderboard']:
		f.write(f"{player['name']}:{player['profile_id']}:{player['steam_id']}:{player['rating']}:{player['rank']}:{player['games']}:{player['wins']}:{player['last_match_time']}\n")
	f.close()


main()
