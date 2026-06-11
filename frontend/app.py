import streamlit as st
import requests
import os
from dotenv import load_dotenv
import textwrap

# ─── ENV & CONFIG ───────────────────────────────────────────────────────────────
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'python_engine', '.env')
load_dotenv(dotenv_path, override=True)

STRAPI_URL   = os.getenv("STRAPI_URL", "http://localhost:1337")
API_TOKEN    = os.getenv("STRAPI_API_TOKEN", "")
HEADERS      = {"Authorization": f"Bearer {API_TOKEN}"}

st.set_page_config(
    page_title="Gezin Durun | AI Gezi Rehberi",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── GLOBAL CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* Darker gradient over the image for better text readability */
html, body, .stApp { 
    background-image: linear-gradient(rgba(5, 5, 10, 0.75), rgba(5, 5, 10, 0.9)), url('https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=2560&auto=format&fit=crop') !important; 
    background-size: cover !important; 
    background-attachment: fixed !important; 
    background-position: center !important; 
    color: #f8fafc !important; 
}

p, h1, h2, h3, h4, h5, h6, li, label, div[data-testid="stMarkdownContainer"] { 
    font-family: 'Outfit', sans-serif !important; 
    text-shadow: 0 2px 5px rgba(0,0,0,0.8); 
}

/* ── Hide Streamlit Boilerplate & Sidebar ── */
#MainMenu, footer, .stDeployButton, [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
header { background: transparent !important; }
.block-container { padding: 3rem 2rem !important; max-width: 1500px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.3); border-radius: 3px; }

/* ── Selectbox & Radio overrides ── */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
[data-testid="stRadio"] label { 
    background: rgba(15, 15, 25, 0.6) !important; 
    backdrop-filter: blur(12px) !important; 
    border: 1px solid rgba(255,255,255,0.15) !important; 
    border-radius: 12px !important; 
    color: #f8fafc !important; 
    font-family: 'Outfit', sans-serif !important; 
}
[data-testid="stRadio"] > div { gap: 0.5rem; }

/* ── Container overrides for "Ayarlar" box via CSS Marker ── */
div[data-testid="stElementContainer"]:has(#ayarlar-marker) + div[data-testid="stElementContainer"] > div,
div.element-container:has(#ayarlar-marker) + div.element-container > div {
    background: rgba(15, 15, 25, 0.55) !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5) !important;
    border-radius: 20px !important;
    padding: 1.5rem !important;
}

/* ── Glassmorphism Utility Class ── */
.dark-glass {
    background: rgba(15, 15, 25, 0.55);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    border-radius: 20px;
}
</style>
""".replace('\n', ' '), unsafe_allow_html=True)

# ─── API HELPERS ────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_cities(locale: str = "tr") -> list:
    try:
        r = requests.get(
            f"{STRAPI_URL}/api/cities?locale={locale}&populate=*",
            headers=HEADERS,
            timeout=8
        )
        return r.json().get("data", []) if r.ok else []
    except Exception:
        return []

@st.cache_data(ttl=300)
def fetch_places(city_doc_id: str, locale: str = "tr") -> list:
    try:
        url = (
            f"{STRAPI_URL}/api/places"
            f"?locale={locale}"
            f"&filters[city][documentId][$eq]={city_doc_id}"
            f"&populate=CoverImage"
        )
        r = requests.get(url, headers=HEADERS, timeout=8)
        return r.json().get("data", []) if r.ok else []
    except Exception:
        return []

# ─── COMPONENT RENDERERS ────────────────────────────────────────────────────────

def render_hero():
    html_content = textwrap.dedent("""
    <div class="dark-glass" style="padding: 2.5rem 2rem; margin-bottom: 2rem; position: relative; overflow: hidden;">
        <div style="position: absolute; top: -50px; right: -50px; width: 150px; height: 150px; background: radial-gradient(circle, rgba(99,102,241,0.3) 0%, transparent 70%); border-radius: 50%;"></div>
        <div style="display:flex; align-items:center; gap: 1rem; margin-bottom: 0.5rem;">
            <span style="font-size: 2.5rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));">🧭</span>
            <div>
                <div style="font-size:0.75rem; font-weight:700; letter-spacing:3px; color: #818cf8; text-transform:uppercase;">AI Destekli</div>
                <h1 style="font-size:2.2rem; font-weight:800; background: linear-gradient(135deg, #ffffff, #a5b4fc); -webkit-background-clip:text; -webkit-text-fill-color:transparent; line-height:1.1; margin:0;">
                    Gezin Durun
                </h1>
            </div>
        </div>
        <p style="color: #cbd5e1; font-size:1rem; font-weight:500; line-height:1.6; margin-top: 1rem;">
            Yapay zeka tarafından zenginleştirilmiş içeriklerle dünyanın en güzel destinasyonlarını keşfedin.
        </p>
    </div>
    """)
    st.html(html_content)

def render_city_header(city: dict):
    name    = city.get("Name", "")
    country = city.get("Country", "")
    info    = city.get("ShortInfo", "")
    html_content = textwrap.dedent(f"""
    <div class="dark-glass" style="padding: 2.5rem; margin-bottom: 2rem; display: flex; align-items: flex-start; gap: 1.5rem;">
        <div style="font-size:4rem; flex-shrink:0; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.5));">🏙️</div>
        <div>
            <h2 style="font-size:2.5rem; font-weight:800; color:#ffffff; margin-bottom:0.25rem;">{name}</h2>
            <div style="
                display:inline-block; background: rgba(99,102,241,0.3);
                border:1px solid rgba(99,102,241,0.5); border-radius:20px;
                padding:0.4rem 1.2rem; font-size:0.85rem; font-weight:700;
                color:#ffffff; letter-spacing:1px; text-transform:uppercase; margin-bottom:1.2rem;
            ">{country}</div>
            <p style="color:#f8fafc; font-size:1.1rem; font-weight:400; line-height:1.7;">{info}</p>
        </div>
    </div>
    """)
    st.html(html_content)

def render_place_card(place: dict, idx: int):
    name        = place.get("Name", "Bilinmiyor")
    description = place.get("Description", "Açıklama bulunmuyor.")
    rating      = place.get("Rating")
    cover       = place.get("CoverImage")

    if rating:
        full  = int(rating)
        half  = 1 if (rating - full) >= 0.5 else 0
        empty = 5 - full - half
        stars = "★" * full + ("½" if half else "") + "☆" * empty
        rating_html = f"""
        <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.75rem;">
            <span style="color:#fbbf24; font-size:1.1rem; letter-spacing:2px; text-shadow: 0 0 8px rgba(251,191,36,0.6);">{stars}</span>
            <span style="color:#fbbf24; font-weight:800; font-size:1rem;">{rating}</span>
        </div>"""
    else:
        rating_html = ""

    if cover and cover.get("url"):
        img_url  = f"{STRAPI_URL}{cover['url']}"
        img_html = f'<img src="{img_url}" style="width:100%; height:220px; object-fit:cover; border-radius:14px; margin-bottom:1.2rem; box-shadow: 0 6px 16px rgba(0,0,0,0.4);" />'
    else:
        gradient_colors = [
            ("rgba(99,102,241,0.5)", "rgba(168,85,247,0.4)"),
            ("rgba(236,72,153,0.5)", "rgba(245,158,11,0.4)"),
            ("rgba(16,185,129,0.5)", "rgba(59,130,246,0.4)"),
        ]
        g1, g2   = gradient_colors[idx % len(gradient_colors)]
        img_html = f"""
        <div style="
            width:100%; height:220px; border-radius:14px; margin-bottom:1.2rem;
            background: linear-gradient(135deg, {g1}, {g2});
            display:flex; align-items:center; justify-content:center;
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: inset 0 0 20px rgba(0,0,0,0.3);
        ">
            <span style="font-size:4rem; opacity:0.9; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.5));">🗺️</span>
        </div>"""

    accent_colors = ["#818cf8", "#c084fc", "#f472b6", "#fbbf24", "#34d399", "#60a5fa"]
    accent = accent_colors[idx % len(accent_colors)]

    html_content = textwrap.dedent(f"""
    <div class="dark-glass" style="
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
        position: relative;
    ">
        <div style="
            position:absolute; top:0; left:0; width:6px; height:100%;
            background: linear-gradient(180deg, {accent}, transparent);
            border-radius: 20px 0 0 20px;
        "></div>
        <div style="padding-left:0.5rem;">
            {img_html}
            {rating_html}
            <h3 style="font-size:1.4rem; font-weight:800; color:#ffffff; margin-bottom:0.6rem; line-height:1.3;">{name}</h3>
            <p style="color:#e2e8f0; font-size:1rem; font-weight:400; line-height:1.6; display:-webkit-box; -webkit-line-clamp:4; -webkit-box-orient:vertical; overflow:hidden;">
                {description}
            </p>
        </div>
    </div>
    """)
    st.html(html_content)

# ─── MAIN APP ───────────────────────────────────────────────────────────────────
def main():
    if "locale" not in st.session_state:
        st.session_state.locale = "tr"
    if "city_id" not in st.session_state:
        st.session_state.city_id = None
        
    def deduplicate(city_list):
        d = {}
        for c in city_list:
            if c.get("Name") not in d:
                d[c.get("Name")] = c
        return list(d.values())

    init_cities = deduplicate(fetch_cities("tr"))
    
    # --- AUTO-LOADER LOGIC ---
    if not init_cities:
        import subprocess
        import sys
        import time
        with st.spinner("Sunucu yeni uyandı, veritabanı boş görünüyor. Gezi verileri sizin için otomatik olarak internetten çekiliyor, lütfen 20-30 saniye bekleyin... 🚀"):
            try:
                env = os.environ.copy()
                env["STRAPI_URL"] = STRAPI_URL
                env["STRAPI_API_TOKEN"] = API_TOKEN
                
                script_dir = os.path.join(os.path.dirname(__file__), '..', 'python_engine')
                subprocess.run([sys.executable, "main.py"], cwd=script_dir, env=env, check=True)
                
                # Clear streamlit cache so it fetches the new data
                time.sleep(2)
                fetch_cities.clear()
                fetch_places.clear()
                init_cities = deduplicate(fetch_cities("tr"))
            except Exception as e:
                st.error(f"Otomatik veri yükleme sırasında bir hata oluştu: {e}")
    # -------------------------

    en_cities   = deduplicate(fetch_cities("en"))

    # Layout: Split Screen
    col_left, col_right = st.columns([1, 2.2], gap="large")

    with col_left:
        # 1. Hero
        render_hero()

        # 2. Controls
        st.markdown('<span id="ayarlar-marker"></span>', unsafe_allow_html=True)
        with st.container():
            st.markdown("<h3 style='margin-bottom:1.5rem; margin-top:0; font-size:1.4rem; color:#fff; font-weight:700;'>⚙️ Ayarlar</h3>", unsafe_allow_html=True)
            
            st.markdown("**🌐 Dil / Language**")
            lang_choice = st.radio("", ["🇹🇷 Türkçe", "🇬🇧 English"], label_visibility="collapsed", index=0 if st.session_state.locale=="tr" else 1)
            new_locale = "tr" if "Türkçe" in lang_choice else "en"
            if new_locale != st.session_state.locale:
                st.session_state.locale = new_locale
                st.rerun()

            st.markdown("<br>**🏙️ Şehir Seç**", unsafe_allow_html=True)
            
            current_list = init_cities if new_locale == "tr" else en_cities
            city_map = {c["documentId"]: c.get("Name", "?") for c in current_list}
            doc_ids  = list(city_map.keys())

            if not doc_ids:
                st.warning("Henüz veri yok.")
                selected_city_id = None
            else:
                default_idx = 0
                if st.session_state.city_id in doc_ids:
                    default_idx = doc_ids.index(st.session_state.city_id)
                selected_city_id = st.selectbox("", doc_ids, index=default_idx, format_func=lambda x: city_map[x], label_visibility="collapsed")
                if selected_city_id != st.session_state.city_id:
                    st.session_state.city_id = selected_city_id
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Önbelleği (Cache) Temizle", use_container_width=True):
                fetch_cities.clear()
                fetch_places.clear()
                st.rerun()
                    
        import streamlit.components.v1 as components
        components.html("""
        <script>
            const headings = window.parent.document.querySelectorAll('h3');
            headings.forEach(h => {
                if(h.innerText.includes('Ayarlar')) {
                    const container = h.closest('div[data-testid="stVerticalBlock"]');
                    if(container) {
                        container.style.background = 'rgba(15, 15, 25, 0.55)';
                        container.style.backdropFilter = 'blur(24px)';
                        container.style.WebkitBackdropFilter = 'blur(24px)';
                        container.style.borderRadius = '20px';
                        container.style.border = '1px solid rgba(255, 255, 255, 0.1)';
                        container.style.padding = '1.5rem';
                        container.style.boxShadow = '0 8px 32px 0 rgba(0, 0, 0, 0.5)';
                    }
                }
            });
        </script>
        """, height=0)

        # 3. Info Block
        st.html("""
        <div class="dark-glass" style="padding: 1.5rem; font-size: 0.9rem; font-weight:400; color: #e2e8f0; line-height: 1.7;">
            <div style="color:#818cf8; font-weight:800; margin-bottom:0.8rem; font-size: 1.1rem;">⚡ Nasıl Çalışır?</div>
            Veriler <b style="color:#ffffff;">Strapi CMS</b> üzerinde saklanır.<br>
            Görseller <b style="color:#ffffff;">Pollinations AI</b> ile üretilir.<br>
            Çeviriler <b style="color:#ffffff;">deep-translator</b> kullanır.
        </div>
        """)

    with col_right:
        if not selected_city_id:
            st.html("""
            <div class="dark-glass" style="padding:4rem; text-align:center;">
                <div style="font-size:3.5rem; margin-bottom:1rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));">⚠️</div>
                <h3 style="color:#ffffff; font-weight:800; font-size: 2rem;">Bağlantı Kurulamadı</h3>
                <p style="color:#cbd5e1; font-size:1.1rem;">Lütfen önce backend scriptini (run_all.bat) çalıştırıp veri çekin.</p>
            </div>
            """)
            return

        cities = deduplicate(fetch_cities(new_locale))
        selected_city = next((c for c in cities if c["documentId"] == selected_city_id), None)
        
        if selected_city:
            render_city_header(selected_city)
            
            places = fetch_places(selected_city["documentId"], new_locale)
            
            if not places:
                st.html("""
                <div class="dark-glass" style="padding:4rem; text-align:center;">
                    <div style="font-size:3.5rem; margin-bottom:1rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));">🔍</div>
                    <h3 style="color:#fde68a; font-weight:800; font-size:2rem;">Mekan Bulunamadı</h3>
                </div>
                """)
            else:
                label = "Gezilecek Yerler" if new_locale == "tr" else "Places to Visit"
                st.html(f"""
                <div style="display:flex; align-items:center; gap:1rem; margin-bottom:1.5rem; margin-top: 1rem;">
                    <span style="font-size:2rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));">📍</span>
                    <h2 style="font-size:1.8rem; font-weight:800; color:#ffffff; margin:0; text-shadow: 0 2px 6px rgba(0,0,0,0.6);">{label}</h2>
                    <div style="
                        background:rgba(99,102,241,0.3); border:1px solid rgba(99,102,241,0.5);
                        border-radius:20px; padding:0.3rem 1rem;
                        font-size:0.9rem; font-weight:800; color:#ffffff;
                    ">{len(places)} yer</div>
                </div>
                """)
                
                # 2-column grid
                p_cols = st.columns(2)
                for i, place in enumerate(places):
                    with p_cols[i % 2]:
                        render_place_card(place, i)

if __name__ == "__main__":
    main()
