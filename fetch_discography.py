import os
import json
import base64
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime

# Load .env manually to avoid dependencies
with open(".env") as f:
    env = dict(line.strip().split("=", 1) for line in f if "=" in line)

CLIENT_ID = env.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = env.get("SPOTIFY_CLIENT_SECRET")

def get_token():
    if not CLIENT_ID or not CLIENT_SECRET:
        print(f"Error: Missing credentials. ID: {bool(CLIENT_ID)}, Secret: {bool(CLIENT_SECRET)}")
        return None
        
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_base64 = base64.b64encode(auth_str.strip().encode()).decode()
    
    print(f"Constructing token request for ID: {CLIENT_ID[:5]}...")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0"
    }
    data = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
    
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req) as f:
            resp_data = json.loads(f.read().decode())
            return resp_data["access_token"]
    except urllib.error.HTTPError as e:
        print(f"Token Request Error: {e.code}")
        print(f"Response Body: {e.read().decode()}")
        raise
    except Exception as e:
        print(f"General Error in get_token: {e}")
        raise

def spotify_request(url, token):
    headers = {"Authorization": f"Bearer {token}", "User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as f:
            return json.loads(f.read().decode())
    except urllib.error.HTTPError as e:
        print(f"API Request Error: {e.code} for {url}")
        print(f"Response Body: {e.read().decode()}")
        raise
    except Exception as e:
        print(f"General Error in spotify_request: {e}")
        raise

def fetch_discography():
    token = get_token()
    
    # Search for artist "vellúa"
    query = urllib.parse.quote("vellúa")
    search_url = f"https://api.spotify.com/v1/search?q={query}&type=artist&limit=1"
    search_results = spotify_request(search_url, token)
    
    if not search_results["artists"]["items"]:
        print("Artist not found.")
        return
    
def fetch_all_releases(artist_id, token):
    all_releases = []
    seen_ids = set()
    
    # Types to fetch
    groups = ["album", "single", "compilation"]
    
    for group in groups:
        url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups={group}"
        while url:
            # We must be careful about the 'limit' parameter again since it was causing 400s
            # If the 'next' URL from Spotify contains a limit, it usually works.
            response = spotify_request(url, token)
            for item in response.get("items", []):
                if item["id"] not in seen_ids:
                    seen_ids.add(item["id"])
                    all_releases.append(item)
            url = response.get("next")
            
    return all_releases

def fetch_discography():
    token = get_token()
    
    # Search for artist "vellúa"
    query = urllib.parse.quote("vellúa")
    search_url = f"https://api.spotify.com/v1/search?q={query}&type=artist&limit=1"
    search_results = spotify_request(search_url, token)
    
    if not search_results["artists"]["items"]:
        print("Artist not found.")
        return
    
    artist_name = search_results["artists"]["items"][0]["name"]
    artist_id = search_results["artists"]["items"][0]["id"]
    print(f"Found Artist: {artist_name} (ID: {artist_id})")
    
    all_items = fetch_all_releases(artist_id, token)
    print(f"Total items found: {len(all_items)}")
    
    discography = []
    
    for item in all_items:
        album_id = item["id"]
        album_url = f"https://api.spotify.com/v1/albums/{album_id}"
        album_details = spotify_request(album_url, token)
        
        release_date = album_details["release_date"]
        try:
            date_obj = datetime.strptime(release_date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%d. %B %Y").replace("January", "Januar").replace("February", "Februar").replace("March", "März").replace("May", "Mai").replace("June", "Juni").replace("July", "Juli").replace("October", "Oktober").replace("December", "Dezember")
        except:
            formatted_date = release_date
            
        image_url = item["images"][0]["url"] if item["images"] else ""
        
        discography.append({
            "title": item["name"],
            "id": album_id,
            "url": item["external_urls"]["spotify"],
            "image": image_url,
            "date": release_date,
            "display_date": formatted_date
        })
    
    # Sort by date descending
    discography.sort(key=lambda x: x["date"], reverse=True)
    
    # Update index.html
    update_index_html(discography)

def update_index_html(discography):
    if not discography:
        return
        
    latest = discography[0]
    
    with open("index.html", "r") as f:
        content = f.read()
    
    # Update Hero Section
    import re
    
    # Update OpenGraph Tags
    content = re.sub(r'(<meta property="og:title" content=")(.*?)(">)', f'\\1{latest["title"]} - vellúa\\3', content)
    content = re.sub(r'(<meta property="og:image" content=")(.*?)(">)', f'\\1{latest["image"]}\\3', content)
    
    # Generic description logic used across both Hero and OG
    new_desc = f"Creating spaces of peace in a loud world. Discover our brand new single '{latest['title']}', connecting ancient acoustic traditions with modern sonic landscapes."
    content = re.sub(r'(<meta property="og:description" content=")(.*?)(">)', f'\\1{new_desc}\\3', content)
    
    # Update Hero Title
    content = re.sub(r'(<h2 class="slide-title">)(.*?)(</h2>)', f'\\1{latest["title"]}\\3', content)
    
    # Update Hero Image (specifically within the hero-image-wrapper to avoid Nav logo)
    image_pattern = re.compile(r'(<div class="hero-image-wrapper">.*?<img src=")(.*?)(".*?\balt=")(.*?)(".*?\bclass="slide-image">)', re.DOTALL)
    content = image_pattern.sub(f'\\1{latest["image"]}\\3{latest["title"]} Cover\\5', content)
    
    # Update Hero Spotify Link
    content = re.sub(r'(<a href=")(.*?)(" target="_blank" class="cta-button">Listen on Spotify</a>)', f'\\1{latest["url"]}\\3', content)
    
    # Update Hero Description
    hero_desc_pattern = re.compile(r'(<p class="hero-desc">)(.*?)(</p>)', re.DOTALL)
    content = hero_desc_pattern.sub(f'\\1{new_desc}\\3', content)

    # Update Discography Grid
    grid_pattern = re.compile(r'(<div class="grid-container fade-in">)(.*?)(</div>)', re.DOTALL)
    
    new_items_html = "\n"
    for item in discography:
        new_items_html += f'                <a href="{item["url"]}" target="_blank"><img class="disco-item" src="{item["image"]}" alt="{item["title"]}" title="{item["title"]} ({item["display_date"]})"></a>\n'
    
    updated_content = grid_pattern.sub(r'\1' + new_items_html + r'            \3', content)
    
    with open("index.html", "w") as f:
        f.write(updated_content)
    
    print("\nSuccessfully updated index.html with Hero Section and Grid.")
    
    # Auto-deploy
    from deploy import deploy as sftp_deploy
    sftp_deploy()

if __name__ == "__main__":
    fetch_discography()
