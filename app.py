import streamlit as st
import requests
import zipfile
import io
from duckduckgo_search import DDGS
from concurrent.futures import ThreadPoolExecutor

# ==========================================
# 1. CONFIGURATION & INDUSTRIAL THEME
# ==========================================
st.set_page_config(
    page_title="SANGRAH",
    page_icon="🌏",
    layout="wide"
)

st.markdown("""
<style>
    /* GLOBAL RESET */
    .stApp, p, h1, h2, h3, h4, h5, label, span, div, li, button {
        font-family: 'Inter', sans-serif !important;
        color: #ffffff !important;
    }

    /* BACKGROUND: DEEP DATA OCEAN */
    .stApp {
        background: linear-gradient(180deg, #002366 0%, #4169E1 100%);
        background-attachment: fixed;
    }

    /* INPUTS (Glass Style) */
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background-color: rgba(0, 0, 0, 0.4) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
    }
    
    /* BUTTONS (Teal/Cyan Gradient) */
    div.stButton > button {
        background: linear-gradient(90deg, #00C9FF, #92FE9D) !important;
        border: none !important;
        color: #002b36 !important; /* Dark text for contrast */
        font-weight: bold !important;
        border-radius: 8px !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px #00C9FF;
    }

    /* PROGRESS BAR */
    .stProgress > div > div > div > div {
        background-color: #00C9FF;
    }

    /* =========================================
       THE SAMRION 2026 FOOTER (Replica)
       ========================================= */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #004d66; /* Dark Teal matched from image */
        color: #ffffff;
        text-align: center;
        padding: 12px;
        font-size: 10px;
        letter-spacing: 2px;
        text-transform: uppercase;
        z-index: 9999;
        font-weight: 500;
        box-shadow: 0 -4px 10px rgba(0,0,0,0.3);
    }

    /* HIDE DEFAULT JUNK */
    #MainMenu, footer, header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MINING ENGINE (High Volume)
# ==========================================

def download_image(link):
    """Worker function for threads"""
    try:
        # 3 second timeout to skip slow servers immediately
        r = requests.get(link, timeout=3)
        if r.status_code == 200:
            return r.content
    except:
        return None

def mine_data(query, count):
    """The Industrial Mining Logic"""
    
    # 1. SEARCH PHASE
    status_text.write(f"🔍 Initializing Deep Search for '{query}'...")
    results = []
    
    try:
        with DDGS() as ddgs:
            # We fetch slightly more to account for dead links
            search_gen = ddgs.images(
                query, 
                region="wt-wt", 
                safesearch="off", 
                max_results=count + 50 
            )
            # Convert generator to list
            for r in search_gen:
                results.append(r['image'])
                if len(results) >= count + 20: # Buffer
                    break
    except Exception as e:
        st.error(f"Search Network Error: {e}")
        return None

    if not results:
        st.error("No data found. Try a broader term.")
        return None

    # 2. DOWNLOAD PHASE (Massive Parallelism)
    downloaded_images = []
    status_text.write(f"⬇️ Establishing connections to {len(results)} servers...")
    
    prog_bar = st.progress(0)
    
    # 30 Workers for high speed
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = {executor.submit(download_image, url): url for url in results}
        
        completed = 0
        for future in futures:
            data = future.result()
            if data:
                downloaded_images.append(data)
            
            # Update Progress
            completed += 1
            progress = min(completed / len(results), 1.0)
            prog_bar.progress(progress)
            
            # Hard Stop if we hit the limit
            if len(downloaded_images) >= count:
                break

    return downloaded_images[:count]

# ==========================================
# 3. INTERFACE
# ==========================================

st.title("SANGRAH")
st.markdown("### Massive Scale Dataset Collector")
st.markdown("---")

c1, c2, c3 = st.columns([3, 1, 1])

with c1:
    topic = st.text_input("Target Class", placeholder="e.g. Broken Circuit Board")
with c2:
    # UPDATED LIMIT: 50,000
    count = st.number_input("Volume", min_value=10, max_value=50000, value=100, step=50)
with c3:
    st.write("")
    mine_btn = st.button("🚀 INITIATE", use_container_width=True)

# STATUS OUTPUT
status_text = st.empty()

if mine_btn and topic:
    if count > 1000:
        st.warning("⚠️ High Volume Alert: Downloading >1000 images takes time. Please keep this tab open.")
        
    images = mine_data(topic, count)
    
    if images:
        status_text.write("✅ Collection Complete. Compressing Archives...")
        
        # ZIP PROCESS
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            for i, img_data in enumerate(images):
                filename = f"{topic.replace(' ', '_')}_{i+1}.jpg"
                zf.writestr(filename, img_data)
        
        zip_buffer.seek(0)
        
        st.success(f"💎 Successfully Secured {len(images)} Files.")
        
        # PREVIEW
        st.write("### 👁️ Data Sample")
        cols = st.columns(6)
        for i in range(min(6, len(images))):
            cols[i].image(images[i], use_container_width=True)

        # DOWNLOAD
        st.download_button(
            label=f"⬇️ DOWNLOAD DATASET ({len(images)} Files)",
            data=zip_buffer,
            file_name=f"SANGRAH_{topic}.zip",
            mime="application/zip",
            type="primary",
            use_container_width=True
        )
        status_text.empty()

# THE SAMRION 2026 FOOTER (Exact Match)
st.markdown("""
<div class="footer">
    POWERED BY SAMRION INTELLIGENCE &nbsp;|&nbsp; © 2026 SAMRION AI INFRASTRUCTURE &nbsp;|&nbsp; FOUNDER: NITIN RAJ
</div>
""", unsafe_allow_html=True)
