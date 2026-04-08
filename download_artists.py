import urllib.request
import os

downloads = {
    "Stein-Bull-Hansen.jpg": "https://vellua-music.com/old/wp-content/uploads/2020/05/Stein-Bull-Hansen-600-e1724532286204.jpg",
    "Tatiana-Shishkova.jpg": "https://vellua-music.com/old/wp-content/uploads/2020/05/Tatiana-Shishkova-scaled-e1723749029672.jpg",
    "Roman-Lacrouts.jpg":    "https://vellua-music.com/old/wp-content/uploads/2020/05/Roman-scaled-e1724532144363.jpg",
    "Hamed-Torkaman.jpg":    "https://vellua-music.com/old/wp-content/uploads/2020/05/Hamed-Torkaman.jpg",
    "Carolina-Teruel.jpg":   "https://vellua-music.com/old/wp-content/uploads/2020/05/Carolina-Teruel-scaled-e1724532716970.jpg",
    "Ilia-Mazya.jpg":        "https://vellua-music.com/old/wp-content/uploads/2020/05/Ilia-Mazya-e1724532482674.jpg",
    "Hugo-Lee.jpg":          "https://vellua-music.com/old/wp-content/uploads/2020/05/Hugo-Lee-e1724532388131.jpg"
}

os.makedirs('images', exist_ok=True)

for filename, url in downloads.items():
    print(f"Downloading {filename}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(os.path.join('images', filename), 'wb') as f:
                f.write(response.read())
        print(f"Success: {filename}")
    except Exception as e:
        print(f"Error {filename}: {e}")

