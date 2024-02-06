import requests

api_key = "502d35cafb294f65b1b8e6a70f68eedd"
base_url = "https://www.bungie.net/Platform/"

headers = {
    "X-API-Key": api_key,
    "Content-Type": "application/json",
}

def get_numeric_id(display_name, display_name_code, membership_type):
    # Define the request body
    request_body = {
        "displayName": display_name,
        "displayNameCode": display_name_code,
    }

    # Get the numeric ID of a player by their display name and display name code
    response = requests.post(base_url + f"Destiny2/SearchDestinyPlayerByBungieName/{membership_type}/", json=request_body, headers=headers)

    if response.status_code == 200:
        search_data = response.json()
        if search_data["ErrorCode"] == 1:
            # Assuming the first result is the correct player
            numeric_id = search_data["Response"][0]["membershipId"]
            # print(f"Numeric ID for {display_name}: {numeric_id}")
            return numeric_id
        else:
            print(f"Error: {search_data['ErrorCode']}, Message: {search_data['Message']}")
    else:
        print(f"Error: {response.status_code}")

def get_membership_id(numeric_id):
    # Get the numeric ID of a player by their display name and display name code
    response = requests.get(base_url + f"User/GetBungieAccount/{numeric_id}/254/", headers=headers)

    if response.status_code == 200:
        membership_id = response.json()['Response']['bungieNetUser']['membershipId']
        # print(f"Membership ID for {numeric_id}: {membership_id}")
        return membership_id
    else:
        print(f"Error: {response.status_code}")

def get_stats():
    # Get the list of all vendors in Destiny 2
    username = input("Enter your username followed by a # and your 4 digit code: ")
    username, code = username.split("#")
    id = get_numeric_id(username, code, "All")
    membership_id = get_membership_id(id)
    # this asked for membership type not id u dunce
    response = requests.get(base_url + f"Destiny2/3/Account/{id}/Stats/", headers=headers)

    if response.status_code == 200:
        trending_data = response.json()["Response"]["mergedAllCharacters"]["merged"]["allTime"]["secondsPlayed"]["basic"]["value"]
        trending_data = round(trending_data / 60 / 60)
        print(f"{trending_data} hours played")

    else:
        print(f"Error: {response.status_code}")



if __name__ == "__main__":
    # Example usage: Find the numeric ID for a player named "examplePlayer" on Xbox (platform 1)
    # get_numeric_id("Apples#7377", 3)
    get_stats()

    
