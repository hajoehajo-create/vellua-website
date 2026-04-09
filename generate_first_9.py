import re
import subprocess
import time

def run():
    print("Starte Batch-Generierung der ersten 9 Artikel...")
    
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Wir suchen nach allen disco-item Links
    # Format: <a href="https://open.spotify.com/album/ID" target="_blank"><img class="disco-item" src="COVER" alt="TITLE" title="TITLE (DATE)"></a>
    pattern = r'<a href="https://open\.spotify\.com/album/([^"]+)"[^>]*>\s*<img class="disco-item" src="([^"]+)" alt="[^"]+" title="([^(]+)\s*\(([^)]+)\)">'
    matches = re.findall(pattern, content)

    # Wir nehmen die neuesten 9 (also die ersten 9 auf der Seite)
    top_9 = matches[:9]
    
    # Wir drehen die Liste um, weil unser Blog-Skript die Kacheln immer "oben" einfügt.
    # So taucht der neueste Artikel (Index 0) als allerletztes ganz oben auf!
    top_9.reverse()

    for item in top_9:
        spotify_id, cover_url, title, date = item
        title = title.strip()
        date = date.strip()
        
        print(f"Generiere: {title} ({date})")
        
        # Aufruf des bestehenden Skripts
        cmd = [
            "python3", "generate_blog.py",
            "--title", title,
            "--date", date,
            "--cover", cover_url,
            "--spotify-id", spotify_id
        ]
        
        process = subprocess.run(cmd, capture_output=True, text=True)
        if process.returncode != 0:
            print(f"Fehler bei {title}:")
            print(process.stderr)
        else:
            print("Erfolgreich!")
            
        # Kurze Pause für die Gemini API (Rate Limits)
        time.sleep(2)

if __name__ == "__main__":
    run()
