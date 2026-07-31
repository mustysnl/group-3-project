# File handling helpers - remembers which country codes the user has searched before

import os
import json

FAVOURITES_FILE = "favourite_countries.json"


def load_favourites():
    # if the file doesn't exist yet (first run), there's nothing to load
    if not os.path.exists(FAVOURITES_FILE):
        return []
    with open(FAVOURITES_FILE, "r") as f:
        return json.load(f)  # reads the JSON file back into a Python list


def save_favourite(code):
    favourites = load_favourites()
    if code not in favourites:  # avoid saving the same country twice
        favourites.append(code)
        with open(FAVOURITES_FILE, "w") as f:
            json.dump(favourites, f, indent=2)  # writes the list back out as JSON
