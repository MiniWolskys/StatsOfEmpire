import requests
import sys

# my id 76561198047674342

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
	exit(error)

def print_players_in_game(player_list):
	for profile in player_list:
		print(f"Player name : {profile['name']}, elo : {profile['rating']}")

def main():

	resp = request("https://aoe2.net/api/player/lastmatch?game=aoe2de&steam_id=76561198047674342")

	if resp.status_code != 200:
		error_handling(resp.status_code)

	print_players_in_game(resp.json()["last_match"]["players"])

main()
