import os
import re
import argparse
# import openai  # Wird später entkommentiert, wenn du deinen API Key einfügen möchtest

# ----------------- ZIELGRUPPEN PROFIL & PROMPT -----------------
AUDIENCE_PERSONA = """
TARGET AUDIENCE METRICS (For AI Context):
- Demographics: Adults aged 25-54 (25-34 holds 25%, 35-54 holds 40%). This is a mature audience seeking relaxation, reflection, or cultural depth.
- Gender: 56% Male, 38% Female. Very balanced, maintain a universal, thoughtful tone.
- Geography: Highly international! Top 4: Turkey, USA, Germany, France. The text MUST be in international English.
- Tone: The tone must be worldly, respectful, reflective, and poetic. Avoid slang or overly trendy Gen-Z language. Focus on themes of multicultural connection, stepping out of daily stress, and acoustic sonic journeys.
- Neighborhood: Acoustic World-Fusion, Cinematic, Middle-Eastern/European traditional fusion.
"""

PROMPT_TEMPLATE = f"""
You are the ghostwriter for the global acoustic duo 'vellúa' (Haval & Joe). 
You write comprehensive, SEO-optimized, and GEO-optimized blog articles for their new music releases. 
The core philosophy is creating 'Spaces of Peace' in a loud world.

{AUDIENCE_PERSONA}

TASK:
Write a beautifully engaging, SEO-optimized blog post (approx. 400-600 words) about our new track '{{track_title}}'. 
Output MUST be raw HTML content containing only <p>, <h2>, <h3>, <strong>, <em>, and <ul>/<li> tags. Do not wrap it in a full HTML document.

STRUCTURE TO FOLLOW STRICTLY:
1. Introduction: Hook the reader (keep in mind the 25-54 age range across Turkey, US, Germany, France). Mention the track name in robust bold. Natural SEO keywords (e.g., 'ambient acoustic music', 'world fusion', 'finding peace').
2. The Multicultural Journey (H2): Describe how acoustic sounds naturally cross borders.
3. Your Space of Peace (H2): Address the reader with 'you' and explain how they can use this piece of music to escape the daily rush.
4. Formatting: Keep paragraphs short for readability on mobile.
Do NOT write a concluding signature, we add it automatically.
"""

def generate_blog_content(track_title):
    from dotenv import load_dotenv
    load_dotenv()
    
    import json
    import urllib.request
    gemini_key = os.environ.get("GEMINI_API_KEY")
    
    if not gemini_key:
        print("FEHLER: GEMINI_API_KEY ist nicht in der .env Datei gesetzt!")
        exit(1)
        
    print(f"Versuche KI Text für '{track_title}' mit Gemini (REST) zu generieren...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
    full_prompt = f"System Context: You are a professional music blog writer for vellúa.\n\n{PROMPT_TEMPLATE.replace('{track_title}', track_title)}"
    
    data = {"contents": [{"parts": [{"text": full_prompt}]}]}
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"API Fehler: {e}")
        exit(1)

def create_blog_post_html(track_title, track_date, cover_url, spotify_embed_id):
    # Dateiname automatisch aus Songname generieren: "mein-neuer-song.html"
    filename = re.sub(r'[^a-z0-9]+', '-', track_title.lower()).strip('-') + '.html'
    
    # 1. Text von KI generieren lassen
    html_content = generate_blog_content(track_title)
    
    # 2. Template zusammenbauen
    template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{track_title} | vellúa Blog</title>
    <meta name="description" content="Read about our new release {track_title}. A space of peace in a loud world.">
    <link rel="icon" type="image/png" href="images/favicon.png">
    <link rel="stylesheet" href="style.css?v=1.5">
    <style>
        .blog-detail-section {{ min-height: 100vh; max-width: 800px; margin: 0 auto; padding: 8rem 2rem 4rem; }}
        .back-link {{ display: inline-block; margin-bottom: 2rem; color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; font-weight: 700; transition: color 0.3s, transform 0.3s; }}
        .back-link:hover {{ color: var(--accent); transform: translateX(-5px); }}
        .blog-detail-header {{ text-align: center; margin-bottom: 3rem; }}
        .blog-detail-meta {{ font-size: 0.9rem; color: var(--accent); text-transform: uppercase; letter-spacing: 2px; font-weight: 600; display: block; margin-bottom: 1rem; }}
        .blog-detail-header h1 {{ font-size: 3.5rem; line-height: 1.1; margin-bottom: 2rem; }}
        .blog-hero-image {{ width: 100%; max-width: 500px; margin: 0 auto 4rem; border-radius: 6px; overflow: hidden; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4); aspect-ratio: 1/1; }}
        .blog-hero-image img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
        .blog-body {{ background: rgba(255, 255, 255, 0.03); padding: 3rem 4rem; border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.08); font-size: 1.15rem; line-height: 1.8; color: var(--text-primary); }}
        .blog-body p {{ margin-bottom: 1.8rem; font-weight: 300; }}
        .blog-body p:last-child {{ margin-bottom: 0; }}
        .blog-signature {{ margin-top: 3rem; font-size: 1.1rem; color: var(--text-secondary); line-height: 1.5; border-top: 1px solid rgba(255, 255, 255, 0.1); padding-top: 2rem; text-align: right; font-style: italic; }}
        .blog-signature strong {{ color: var(--text-primary); font-style: normal; font-size: 1.2rem; }}
        .spotify-embed {{ margin: 3rem 0; width: 100%; }}
        @media (max-width: 768px) {{ .blog-detail-header h1 {{ font-size: 2.5rem; }} .blog-body {{ padding: 2rem 1.5rem; font-size: 1.05rem; }} }}
    </style>
</head>
<body>
    <div class="bg-container">
        <div class="shape shape-1"></div><div class="shape shape-2"></div>
        <div class="shape shape-3"></div><div class="shape shape-4"></div>
    </div>
    <nav class="glass-nav">
        <div class="nav-content">
            <a href="index.html" class="logo"><img src="images/vellua-white-big.png" alt="vellúa logo" decoding="async"></a>
            <ul class="nav-links">
                <li><a href="index.html#home">Home</a></li>
                <li><a href="index.html#discography">Discography</a></li>
                <li><a href="featured-artists.html">Artists</a></li>
                <li><a href="index.html#about">About</a></li>
                <li><a href="index.html#contact">Contact</a></li>
                <li><a href="blog.html" style="color: #cbd5e1;">Blog</a></li>
            </ul>
        </div>
    </nav>
    <!-- Mobile Menu Overlay -->
    <div class="mobile-menu-overlay" id="mobileMenu" role="dialog" aria-label="Mobile navigation">
        
        <a href="index.html#home" class="mobile-nav-link">Home</a>
        <a href="index.html#discography" class="mobile-nav-link">Discography</a>
        <a href="featured-artists.html" class="mobile-nav-link">Artists</a>
        <a href="index.html#about" class="mobile-nav-link">About</a>
        <a href="index.html#contact" class="mobile-nav-link">Contact</a>
        <a href="blog.html" class="mobile-nav-link" style="color: var(--accent);">Blog</a>
    </div>
    <main class="content-wrapper">
        <section class="blog-detail-section fade-in">
            <a href="blog.html" class="back-link">← Back to Overview</a>
            <div class="blog-detail-header">
                <span class="blog-detail-meta">{track_date} • New Release</span>
                <h1>{track_title}</h1>
            </div>
            <div class="blog-hero-image">
                <img src="{cover_url}" alt="{track_title} Cover">
            </div>
            <div class="blog-body">
                {html_content}
                
                <div class="spotify-embed">
                    <div class="spotify-consent-placeholder" data-spotify-src="https://open.spotify.com/embed/album/{spotify_embed_id}?utm_source=generator" onclick="window.loadSpotifyIframe(this)"><svg viewBox="0 0 24 24"><path d="M12 0C5.372 0 0 5.372 0 12s5.372 12 12 12 12-5.372 12-12S18.628 0 12 0zm5.503 17.31c-.22.36-.683.473-1.043.252-2.82-1.722-6.368-2.112-10.55-1.157-.412.093-.822-.164-.916-.576-.094-.412.163-.822.576-.916 4.6-.328 8.514.1 11.674 2.04.36.222.473.684.252 1.044zm1.47-3.262c-.276.45-.86.595-1.31.32-3.228-1.984-8.15-2.56-11.967-1.402-.507.153-1.04-.135-1.194-.642-.153-.51.135-1.043.642-1.196 4.368-1.324 9.774-.672 13.51 1.628.45.276.595.86.32 1.31zm.126-3.41c-3.872-2.3-10.264-2.512-13.97-1.387-.593.18-1.223-.155-1.403-.748-.18-.593.155-1.223.748-1.403 4.267-1.296 11.322-1.037 15.79 1.615.534.317.71 1 .39 1.536z"/></svg> Click to load Spotify Player</div>
                </div>

                <p class="blog-signature">
                    Warm regards,<br>
                    <strong>Haval & Joe</strong><br>
                    vellúa
                </p>
            </div>
        </section>
    </main>

    <script>
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) entry.target.classList.add('visible');
            }});
        }}, {{ threshold: 0.1 }});
        document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

        // Mobile menu toggle
        const hamburger = document.getElementById('hamburger');
        const mobileMenu = document.getElementById('mobileMenu');
        

        function toggleMenu(open) {
            hamburger.classList.toggle('open', open);
            mobileMenu.classList.toggle('open', open);
            document.body.style.overflow = open ? 'hidden' : '';
        }

        hamburger.addEventListener('click', () => {
            const isOpen = mobileMenu.classList.contains('open');
            toggleMenu(!isOpen);
        });

        

        document.querySelectorAll('.mobile-nav-link').forEach(link => {
            link.addEventListener('click', () => toggleMenu(false));
        });
    </script>
    <script src="consent.js"></script>
</body>
</html>
"""
    # HTML speichern
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(template)
    print(f"✅ Blog-Artikel generiert: {filename}")
    
    # 3. Blog-Übersichtsseite aktualisieren
    update_blog_index(track_title, track_date, cover_url, filename)
    
    # 4. Sitemap aktualisieren
    update_sitemap(filename)

def update_sitemap(filename):
    from datetime import date
    sitemap_path = os.path.join(os.path.dirname(__file__), 'sitemap.xml')
    if not os.path.exists(sitemap_path):
        return
    
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_url = f"https://vellua-music.com/{filename}"
    
    # Nicht doppelt einfügen
    if new_url in content:
        print(f"ℹ️  Sitemap enthält bereits: {filename}")
        return
    
    today = date.today().isoformat()
    new_entry = f"""   <url>
      <loc>{new_url}</loc>
      <lastmod>{today}</lastmod>
      <changefreq>monthly</changefreq>
      <priority>0.7</priority>
   </url>
</urlset>"""
    
    content = content.replace('</urlset>', new_entry)
    
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Sitemap aktualisiert: {new_url}")
    
def get_new_card(track_title, track_date, cover_url, filename):
    return f"""
            <a href="{filename}" class="blog-card fade-in">
                <img class="blog-img" src="{cover_url}" alt="{track_title} Cover">
                <div class="blog-content">
                    <span class="blog-meta">{track_date} • New Release</span>
                    <h2 class="blog-title">{track_title}</h2>
                    <p class="blog-excerpt">Discover the acoustic journey behind our new song. A space of peace in a loud world.</p>
                    <span class="blog-readmore">Read full story →</span>
                </div>
            </a>"""

def update_blog_index(track_title, track_date, cover_url, filename):
    index_path = os.path.join(os.path.dirname(__file__), 'blog.html')
    if not os.path.exists(index_path):
        return
        
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    new_card = get_new_card(track_title, track_date, cover_url, filename)
            
    content = content.replace('<div class="blog-grid">', f'<div class="blog-grid">{new_card}', 1)
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Blog-Übersicht (blog.html) erfolgreich aktualisiert!")
    
    update_index_preview(new_card)

def update_index_preview(new_card):
    import re
    index_path = os.path.join(os.path.dirname(__file__), 'index.html')
    if not os.path.exists(index_path): return
    with open(index_path, 'r', encoding='utf-8') as f: content = f.read()
    
    grid_match = re.search(r'(<div class="blog-grid" id="index-blog-grid"[^>]*>)(.*?)(</div>\s*<div style="text-align: center;">)', content, re.DOTALL)
    if not grid_match: return
    
    cards = re.findall(r'<a href="[^"]+".*?</a>', grid_match.group(2), re.DOTALL)
    cards.insert(0, new_card)
    cards = cards[:3]  # Only keep the newest 3
    
    new_inner = "\n                " + "\n                ".join(cards) + "\n            "
    new_content = content[:grid_match.start()] + grid_match.group(1) + new_inner + grid_match.group(3) + content[grid_match.end():]
    
    with open(index_path, 'w', encoding='utf-8') as f: f.write(new_content)
    print("✅ Startseite (index.html) Blog Preview mit Top 3 Artikel aktualisiert!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a blog post for a new Vellúa release.')
    parser.add_argument('--title', default='Echoes Of Time', help='Song Title')
    parser.add_argument('--date', default='15. May 2026', help='Release Date')
    parser.add_argument('--cover', default='https://i.scdn.co/image/ab67616d0000b273f290cab5b3115fbe69cf0f7e', help='Spotify Image URL')
    parser.add_argument('--spotify-id', default='3D4yYorqh6vee5xRwL0CWo', help='Spotify Album ID')
    args = parser.parse_args()

    create_blog_post_html(args.title, args.date, args.cover, args.spotify_id)
