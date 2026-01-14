import os
import pandas
import time
import tkinter, tkinter.filedialog

date = time.strftime("%Y-%m-%d")   

base_url = "https://www.theaudiodb.com/api/v1/json/123/" # Base URL with a placeholder API key (Free tier API used)
album_endpoint = "searchalbum.php?s=" # Endpoint for searching albums by artist name
track_endpoint = "track.php?m=" # Endpoint for pulling all tracks on an album by album ID

user_input = input("Please enter an artist's name to continue.\n")
artist_name = user_input.replace(" ", "_") # Replace spaces with underscores for proper URL formatting

album_url = f"{base_url}{album_endpoint}{artist_name}" # Assembles the full URL for album search

dir_path = tkinter.filedialog.askdirectory(title="Select Directory to Save Album Data") # Prompts user to select a directory to save data

pandas.read_json(album_url).to_json(f"{dir_path}\{artist_name}_albumData_{date}.json", orient="records", indent=4) # Saves album data to JSON file

