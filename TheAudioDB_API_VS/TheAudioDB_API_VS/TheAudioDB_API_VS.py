import requests
import time
import tkinter, tkinter.filedialog
import json
from pathlib import Path

def check_if_file_exists(file_path):
    if Path(file_path).is_file():
        return True
    if Path(file_path).is_dir():
        return True
    else:
        return False

date = time.strftime("%Y-%m-%d")   

base_url = "https://www.theaudiodb.com/api/v1/json/123/" # Base URL with a placeholder API key (Free tier API used)
album_endpoint = "searchalbum.php?s=" # Endpoint for searching albums by artist name
track_endpoint = "track.php?m=" # Endpoint for pulling all tracks on an album by album ID

while 1==1:

    user_input = input("Please enter an artist's name to continue.\n")
    artist_name = user_input.replace(" ", "_") # Replace spaces with underscores for proper URL formatting
    dir_path = tkinter.filedialog.askdirectory(title="Select Directory to Save Album Data") # Prompts user to select a directory to save data
    if check_if_file_exists(f"{dir_path}\{artist_name}") == False:
        artist_path = Path(f"{dir_path}\{artist_name}")
        artist_path.mkdir(parents=True, exist_ok=True)

### Album Data Retrieval ###
    if check_if_file_exists(f"{dir_path}\{artist_name}\{artist_name}_albumData_{date}.json") == False: # Check if file already exists before making request from API

        album_url = f"{base_url}{album_endpoint}{artist_name}" # Assembles the full URL for album search
        response = requests.get(album_url)

        if response.status_code == 200:
            data = response.json()
            try:
                first_value = data["album"][0]["idAlbum"] # Attempt to check that at least one album exists for the artist requested
                file_name = f"{dir_path}\{artist_name}\{artist_name}_albumData_{date}.json"
                with open(file_name, "w", encoding = "utf-8") as file:
                    json.dump(data, file, indent=4) # Saves album data to JSON file
                break # Artist data has been saved, exit loop
            except:
                print("Artist not found. Please check spelling and try again.\n")
        else:
            print("Failed to connect. Please try again later")
    
    else:
        print("Album data file already exists in the selected directory. Skipping request...\n")

### Track Data Retrieval ###
album_count = len(list(data["album"])) # Counts the number of albums that are listed for the artist

for i in range(album_count): # Collects all album IDs for the artist
    album_id = data["album"][int(i)]["idAlbum"] # Gets the album ID for the current album in the loop
    track_url = f"{base_url}{track_endpoint}{album_id}" # Assembles the full URL for track search by album ID
    track_response = requests.get(track_url)

    if track_response.status_code == 200:

        track_data = track_response.json()
        try:
            first_value = track_data["track"][0]["idTrack"] # Attempt to check that at least one track exists for the artist requested
        except:
            print(f"Could not find track data for '{album_id}'. Skipping...\n")
            break # Exit loop if no track data found

        file_name = f"{dir_path}\{artist_name}\{artist_name}_{album_id}_trackData_{date}.json"
        with open(file_name, "w", encoding = "utf-8") as file:
            json.dump(track_data, file, indent=4) # Saves track data to JSON file


    else:
        print(f"Could not find track data for '{album_id}'. Skipping...\n")
