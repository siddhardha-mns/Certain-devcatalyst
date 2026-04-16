import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import json
import os
import hashlib
import base64
from pathlib import Path
import random

# ─── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="AWS Cloud Clubs Mecs – Certificate Generator",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Logo helper ────────────────────────────────────────────────
LOGO_PATH = str(Path(__file__).parent / "assets" / "logo_beige.png")

def get_base64_image(image_path: str) -> str:
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_b64 = get_base64_image(LOGO_PATH)

# ─── Cream/Red Theme CSS ───────────────────────────
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    :root {{
        --space-dark: #03030b;
        --space-mid: #0a0a20;
        --beige-text: #F5F5DC;
        --gold-accent: #D4AF37;
        --gold-glow: rgba(212, 175, 55, 0.4);
    }}

    /* ── ANIMATIONS ── */
    @keyframes float1 {{
        0% {{ transform: translate(0, 0) scale(1); opacity: 0.3; }}
        33% {{ transform: translate(30px, -50px) scale(1.1); opacity: 0.5; }}
        66% {{ transform: translate(-20px, 20px) scale(0.9); opacity: 0.4; }}
        100% {{ transform: translate(0, 0) scale(1); opacity: 0.3; }}
    }}
    @keyframes float2 {{
        0% {{ transform: translate(0, 0) scale(1); opacity: 0.2; }}
        50% {{ transform: translate(-40px, -30px) scale(1.2); opacity: 0.4; }}
        100% {{ transform: translate(0, 0) scale(1); opacity: 0.2; }}
    }}
    @keyframes twinkling {{
        0% {{ opacity: 0.2; }}
        50% {{ opacity: 0.8; }}
        100% {{ opacity: 0.2; }}
    }}

    /* ── DYNAMIC BACKGROUND ── */
    @keyframes galaxyDrift {{
        from {{ background-position: 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0; }}
        to {{ background-position: -2000px 2000px, -800px 800px, -800px 800px, -800px 800px, -800px 800px, -800px 800px, -300px 300px, -300px 300px, -300px 300px, -300px 300px, -300px 300px, 0 0, 0 0; }}
    }}

    html, body, [data-testid="stAppViewContainer"] {{
        background-color: var(--space-dark) !important;
        background-image: 
            /* Cosmic Galaxy Band (Layer 0, flows fast) */
            linear-gradient(45deg, transparent 35%, rgba(212, 175, 55, 0.05) 45%, rgba(245, 245, 220, 0.03) 50%, transparent 65%),
            /* Fast Stardust (Layer 1) */
            radial-gradient(1.5px 1.5px at 20px 30px, var(--beige-text) 100%, transparent),
            radial-gradient(2px 2px at 150px 250px, rgba(212, 175, 55, 0.9) 100%, transparent),
            radial-gradient(1px 1px at 300px 80px, rgba(245, 245, 220, 0.8) 100%, transparent),
            radial-gradient(2px 2px at 80px 320px, var(--beige-text) 100%, transparent),
            radial-gradient(1.5px 1.5px at 350px 150px, rgba(212, 175, 55, 0.7) 100%, transparent),
            /* Slow Dense Stardust (Layer 2) */
            radial-gradient(1px 1px at 50px 50px, rgba(245, 245, 220, 0.6) 100%, transparent),
            radial-gradient(0.5px 0.5px at 120px 80px, rgba(212, 175, 55, 0.5) 100%, transparent),
            radial-gradient(1px 1px at 200px 220px, rgba(245, 245, 220, 0.4) 100%, transparent),
            radial-gradient(0.5px 0.5px at 280px 110px, rgba(212, 175, 55, 0.6) 100%, transparent),
            radial-gradient(1px 1px at 80px 180px, rgba(245, 245, 220, 0.5) 100%, transparent),
            /* Static Soft Galaxy Glows */
            radial-gradient(circle at 15% 50%, rgba(212, 175, 55, 0.06), transparent 30%),
            radial-gradient(circle at 85% 30%, rgba(212, 175, 55, 0.09), transparent 30%);
        background-size: 2000px 2000px, 400px 400px, 400px 400px, 400px 400px, 400px 400px, 400px 400px, 200px 200px, 200px 200px, 200px 200px, 200px 200px, 200px 200px, 100% 100%, 100% 100%;
        background-repeat: repeat, repeat, repeat, repeat, repeat, repeat, repeat, repeat, repeat, repeat, repeat, no-repeat, no-repeat;
        animation: galaxyDrift 150s linear infinite;
        color: var(--beige-text) !important;
        font-family: 'Inter', sans-serif !important;
        overflow-x: hidden;
    }}
    
    /* Golden Galaxy Floating Elements */
    [data-testid="stAppViewContainer"]::before,
    [data-testid="stAppViewContainer"]::after {{
        content: '';
        position: fixed;
        width: 600px;
        height: 600px;
        border-radius: 50%;
        pointer-events: none;
        z-index: 0;
        filter: blur(80px);
    }}
    [data-testid="stAppViewContainer"]::before {{
        background: radial-gradient(circle, rgba(212, 175, 55, 0.15) 0%, transparent 60%);
        top: -100px;
        left: -100px;
        animation: float1 20s infinite ease-in-out;
    }}
    [data-testid="stAppViewContainer"]::after {{
        background: radial-gradient(circle, rgba(138, 43, 226, 0.1) 0%, rgba(212, 175, 55, 0.1) 40%, transparent 70%);
        bottom: -150px;
        right: -100px;
        animation: float2 25s infinite ease-in-out;
    }}

    /* ── GLOBAL TEXT VISIBILITY ── */
    .stMarkdown, .stText, p, span, li {{
        color: var(--beige-text) !important;
        font-weight: 400 !important;
        position: relative;
        z-index: 1;
    }}

    label, h1, h2, h3, h4, h5, h6 {{
        color: var(--gold-accent) !important;
        font-weight: 800 !important;
        position: relative;
        z-index: 1;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.2);
    }}

    /* Global Headings */
    h1, h2, h3, h4, h5, h6 {{
        background: none !important;
        -webkit-text-fill-color: var(--gold-accent) !important;
        margin-bottom: 0.5rem !important;
    }}

    /* Special Heading 1 (Large Title) */
    h1 {{
        font-size: 2.5rem !important;
        border-bottom: 1px solid rgba(212, 175, 55, 0.3) !important;
        padding-bottom: 0.5rem !important;
        color: var(--beige-text) !important;
        -webkit-text-fill-color: var(--beige-text) !important;
    }}

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {{
        background: rgba(5, 5, 16, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(212, 175, 55, 0.2);
    }}
    [data-testid="stSidebar"] div[role="radiogroup"] label p, 
    [data-testid="stSidebar"] label {{
        color: var(--beige-text) !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }}
    div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child > div {{
        background-color: var(--gold-accent) !important;
    }}

    /* Alerts and Notifications */
    .stAlert p, .stAlert div, [data-testid="stNotificationContent"], .stAlert span {{
        color: var(--beige-text) !important;
        font-weight: 400 !important;
    }}
    .stAlert strong, .stAlert b {{
        color: var(--gold-accent) !important;
        font-weight: 800 !important;
    }}

    /* Input Labels and Text */
    .stTextInput label, .stTextArea label, .stNumberInput label, .stSelectbox label, [data-testid="stWidgetLabel"] p {{
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        color: var(--gold-accent) !important;
    }}
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {{
        background: rgba(10, 10, 32, 0.6) !important;
        border: 1px solid rgba(212, 175, 55, 0.4) !important;
        border-radius: 10px !important;
        color: var(--beige-text) !important;
        font-weight: 600 !important;
        backdrop-filter: blur(5px);
    }}
    .stTextInput > div > div > input::placeholder {{
        color: rgba(245, 245, 220, 0.4) !important;
    }}
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: var(--gold-accent) !important;
        box-shadow: 0 0 10px var(--gold-glow) !important;
    }}

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {{ width: 10px; }}
    ::-webkit-scrollbar-track {{ background: var(--space-dark); }}
    ::-webkit-scrollbar-thumb {{ background: rgba(212, 175, 55, 0.5); border-radius: 5px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: var(--gold-accent); }}

    hr {{ border-color: rgba(212, 175, 55, 0.2) !important; }}

    .footer {{
        text-align: center;
        padding: 3rem 0 1.5rem;
        color: var(--beige-text) !important;
        font-weight: 400 !important;
        font-size: 0.9rem !important;
        border-top: 1px solid rgba(212, 175, 55, 0.2);
        margin-top: 2rem;
        position: relative;
        z-index: 1;
    }}
    .footer .heart {{
        color: var(--gold-accent) !important; 
        font-size: 1.2rem;
        animation: twinkling 2s infinite ease-in-out;
    }}

    /* ── Buttons ── */
    .stButton > button {{
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.2), rgba(212, 175, 55, 0.05)) !important;
        color: var(--gold-accent) !important;
        border: 1px solid rgba(212, 175, 55, 0.5) !important;
        border-radius: 12px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        backdrop-filter: blur(5px);
    }}
    .stButton > button:hover {{
        background: rgba(212, 175, 55, 0.2) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px var(--gold-glow) !important;
    }}
    /* Primary download button */
    .stDownloadButton > button {{
        background: linear-gradient(135deg, var(--gold-accent), #B8860B) !important;
        color: var(--space-dark) !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        padding: 0.75rem 2rem !important;
        box-shadow: 0 4px 20px var(--gold-glow) !important;
        transition: all 0.3s ease !important;
    }}
    .stDownloadButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(212, 175, 55, 0.6) !important;
    }}

    /* ── Hero card ── */
    .hero-card {{
        background: rgba(10, 10, 32, 0.5);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 20px;
        padding: 36px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
        z-index: 1;
    }}
    
    /* ── Info card ── */
    .info-card {{
        background: rgba(10, 10, 32, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        z-index: 1;
    }}
    .info-card:hover {{
        border-color: rgba(212, 175, 55, 0.5);
        box-shadow: 0 8px 24px var(--gold-glow);
        transform: translateY(-2px);
    }}

    /* ── Falling Emojis ── */
    .space-fall-container {{
        position: fixed;
        top: -100px;
        left: 0;
        width: 100vw;
        height: 120vh;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }}
    .falling-emoji {{
        position: absolute;
        top: -10vh;
        animation: fall linear infinite;
        opacity: 0.6;
        filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.4));
    }}
    @keyframes fall {{
        0% {{ transform: translateY(0vh) rotate(0deg); opacity: 0; }}
        10% {{ opacity: 0.8; }}
        90% {{ opacity: 0.8; }}
        100% {{ transform: translateY(120vh) rotate(360deg); opacity: 0; }}
    }}

    </style>
    """,
    unsafe_allow_html=True,
)

# ─── Dynamic Falling Emojis ─────────────────────────────────────
emojis = ['🪐', '💫', '☄️', '✨', '🛸', '🛰️', '🚀', '🕳️']
html_items = ""
for i in range(25):
    emoji = random.choice(emojis)
    left = random.uniform(2, 98) 
    delay = random.uniform(0, 15)
    duration = random.uniform(15, 30)
    size = random.uniform(1.2, 2.8)
    html_items += f'<span class="falling-emoji" style="left: {left}%; animation-delay: {delay}s; animation-duration: {duration}s; font-size: {size}rem;">{emoji}</span>\n'

st.markdown(f'<div class="space-fall-container">\n{html_items}\n</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  ORIGINAL CERTIFICATE GENERATOR LOGIC (KEPT INTACT)
# ═══════════════════════════════════════════════════════════════

# Admin credentials (change these!)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()

# Initialize session state for storing configuration
if 'config' not in st.session_state:
    st.session_state.config = {
        'template_path': None,
        'template_image': None,
        'name_x': 500,
        'name_y': 400,
        'font_size': 60,
        'font_color': (0, 0, 0),
        'font_style': 'Arial',
        'font_weight': 'Regular',
        'is_italic': False,
        'custom_font_path': None,
        'stroke_width': 0,
        'stroke_color': (0, 0, 0),
        'participants': []
    }

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'show_login' not in st.session_state:
    st.session_state.show_login = False

# Available font families with fallback options
FONT_FAMILIES = {
    'Arial': {
        'Regular': ['arial.ttf', 'Arial.ttf', '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'],
        'Bold': ['arialbd.ttf', 'Arial-Bold.ttf', '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'],
        'Italic': ['ariali.ttf', 'Arial-Italic.ttf', '/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf'],
        'Bold Italic': ['arialbi.ttf', 'Arial-BoldItalic.ttf', '/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf']
    },
    'Times New Roman': {
        'Regular': ['times.ttf', 'Times-New-Roman.ttf', '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'],
        'Bold': ['timesbd.ttf', 'Times-New-Roman-Bold.ttf', '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'],
        'Italic': ['timesi.ttf', 'Times-New-Roman-Italic.ttf', '/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf'],
        'Bold Italic': ['timesbi.ttf', 'Times-New-Roman-BoldItalic.ttf', '/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf']
    },
    'Courier New': {
        'Regular': ['cour.ttf', 'Courier-New.ttf', '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf'],
        'Bold': ['courbd.ttf', 'Courier-New-Bold.ttf', '/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf'],
        'Italic': ['couri.ttf', 'Courier-New-Italic.ttf', '/usr/share/fonts/truetype/liberation/LiberationMono-Italic.ttf'],
        'Bold Italic': ['courbi.ttf', 'Courier-New-BoldItalic.ttf', '/usr/share/fonts/truetype/liberation/LiberationMono-BoldItalic.ttf']
    }
}


def save_config():
    """Save configuration to a JSON file"""
    config_to_save = {
        'name_x': st.session_state.config['name_x'],
        'name_y': st.session_state.config['name_y'],
        'font_size': st.session_state.config['font_size'],
        'font_color': st.session_state.config['font_color'],
        'font_style': st.session_state.config.get('font_style', 'Arial'),
        'font_weight': st.session_state.config.get('font_weight', 'Regular'),
        'is_italic': st.session_state.config.get('is_italic', False),
        'custom_font_path': st.session_state.config.get('custom_font_path'),
        'stroke_width': st.session_state.config.get('stroke_width', 0),
        'stroke_color': st.session_state.config.get('stroke_color', (0, 0, 0)),
        'participants': st.session_state.config['participants'],
        'template_path': st.session_state.config['template_path']
    }
    with open('cert_config.json', 'w') as f:
        json.dump(config_to_save, f)


def load_config():
    """Load configuration from JSON file"""
    if os.path.exists('cert_config.json'):
        with open('cert_config.json', 'r') as f:
            config = json.load(f)
            if 'font_color' in config and isinstance(config['font_color'], list):
                config['font_color'] = tuple(config['font_color'])
            if 'stroke_color' in config and isinstance(config['stroke_color'], list):
                config['stroke_color'] = tuple(config['stroke_color'])
            st.session_state.config.update(config)


def check_password(username, password):
    """Check if username and password are correct"""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return username == ADMIN_USERNAME and password_hash == ADMIN_PASSWORD_HASH


def login_page():
    """Display login page for admin"""
    st.markdown(
        """
        <div class="info-card" style="text-align:center; max-width:480px; margin:2rem auto;">
            <div style="font-size:2.5rem; margin-bottom:8px;">🔐</div>
            <h2 style="color:var(--gold-accent); margin:0 0 8px;">Admin Login</h2>
            <p style="color:var(--beige-text); font-size:0.9rem;">Enter your credentials to access the admin panel.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("🔓  Login", use_container_width=True)

            if submit:
                if check_password(username, password):
                    st.session_state.authenticated = True
                    st.session_state.show_login = False
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")


def logout():
    """Logout admin"""
    st.session_state.authenticated = False
    st.session_state.show_login = False


def generate_certificate(name, template_img, x, y, font_size, color,
                         font_family='Arial', font_weight='Regular', is_italic=False,
                         custom_font_path=None,
                         stroke_width=0, stroke_color=(0, 0, 0)):
    """Generate certificate with name on template"""
    img = template_img.copy()
    draw = ImageDraw.Draw(img)

    if isinstance(color, (list, tuple)):
        color = tuple(int(c) for c in color)
    else:
        color = (0, 0, 0)

    if isinstance(stroke_color, (list, tuple)):
        stroke_color = tuple(int(c) for c in stroke_color)
    else:
        stroke_color = (0, 0, 0)

    font = None

    # 1. Try custom font first
    if custom_font_path and os.path.exists(custom_font_path):
        try:
            font = ImageFont.truetype(custom_font_path, int(font_size))
        except Exception as e:
            st.warning(f"Failed to load custom font: {e}")

    # 2. Try selected family and weight
    if font is None:
        style_key = font_weight
        if is_italic:
            if font_weight == 'Bold':
                style_key = 'Bold Italic'
            else:
                style_key = 'Italic'
        
        family_config = FONT_FAMILIES.get(font_family, FONT_FAMILIES['Arial'])
        variant_paths = family_config.get(style_key, family_config['Regular'])

        for font_path in variant_paths:
            try:
                font = ImageFont.truetype(font_path, int(font_size))
                break
            except Exception:
                continue

    # 3. Fallback to system defaults
    if font is None:
        fallback_fonts = [
            "arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/Library/Fonts/Arial.ttf",
        ]
        for fallback in fallback_fonts:
            try:
                font = ImageFont.truetype(fallback, int(font_size))
                break
            except Exception:
                continue

    if font is None:
        font = ImageFont.load_default()

    try:
        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
    except Exception:
        text_width = len(name) * (int(font_size) // 2)

    stroke_width = int(stroke_width)
    if stroke_width > 0:
        draw.text((int(x) - text_width // 2, int(y)), name, font=font,
                  fill=color, stroke_width=stroke_width, stroke_fill=stroke_color)
    else:
        draw.text((int(x) - text_width // 2, int(y)), name, font=font, fill=color)

    return img


# Load saved configuration
load_config()


# ═══════════════════════════════════════════════════════════════
#  SIDEBAR  — AWS Cloud Clubs branded
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo
    if logo_b64:
        st.markdown(
            f"""
            <div style="text-align:center; padding:1.5rem 0 0.5rem;">
                <img src="data:image/png;base64,{logo_b64}"
                     style="width:160px; filter:drop-shadow(0 0 12px rgba(141,2,31,0.2));" />
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div style="text-align:center; margin-bottom:0.5rem;">
            <span style="font-size:0.78rem; color:var(--cream-900);">☁️ Certificate Portal</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    mode = st.radio(
        "🧭  Navigate",
        ["📜 Download Certificate", "🔧 Admin Panel"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        """
        <div style="text-align:center; opacity:0.55; font-size:0.78rem; line-height:1.6;">
            Powered by<br/>
            <strong style="color:var(--gold-accent);">AWS Cloud Clubs – Mecs</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("")
    st.markdown(
        """
        <div style="text-align:center; opacity:0.4; font-size:0.72rem;">
            💡 Users download certificates from the main page.<br/>
            Admins configure via the Admin Panel.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════
#  PAGE: DOWNLOAD CERTIFICATE
# ═══════════════════════════════════════════════════════════════
if mode == "📜 Download Certificate":
    # Hero banner
    hero_logo = f'<img src="data:image/png;base64,{logo_b64}" style="width:90px; filter:drop-shadow(0 0 15px rgba(141,2,31,0.2));" />' if logo_b64 else ""
    st.markdown(
        f"""
        <div class="hero-card">
            <div style="display:flex; align-items:center; gap:24px; flex-wrap:wrap;">
                {hero_logo}
                <div>
                    <h1 style="margin:0; font-size:2rem;">Download Your Certificate</h1>
                    <p style="color:var(--cream-900); font-size:1rem; margin-top:6px;">
                        Enter your full name below to generate &amp; download your certificate 🎓
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Load template if exists
    if st.session_state.config.get('template_path') and os.path.exists(st.session_state.config['template_path']):
        try:
            st.session_state.config['template_image'] = Image.open(st.session_state.config['template_path'])
        except Exception as e:
            st.error(f"Error loading template: {e}")
            st.session_state.config['template_image'] = None

    # Name input — always visible
    st.markdown("#### ✍️ Enter your name")
    user_name = st.text_input("Your Full Name", placeholder="e.g., John Doe",
                              key="download_name_input", label_visibility="collapsed")

    # No template warning
    if not st.session_state.config.get('template_image'):
        st.warning("⚠️ No certificate template has been uploaded yet. Please contact the administrator.")
        st.info("🔧 Admin: Go to the **Admin Panel** and upload a certificate template.")

    # Generate if name + template exist
    if user_name and st.session_state.config.get('template_image'):
        if st.session_state.config.get('participants') and user_name not in st.session_state.config['participants']:
            st.error("❌ Name not found in participant list. Please check your spelling or contact the administrator.")
            st.info(f"📋 Total participants registered: {len(st.session_state.config['participants'])}")
        else:
            try:
                cert_color = st.session_state.config.get('font_color', (0, 0, 0))
                if isinstance(cert_color, list):
                    cert_color = tuple(cert_color)

                cert_stroke_color = st.session_state.config.get('stroke_color', (0, 0, 0))
                if isinstance(cert_stroke_color, list):
                    cert_stroke_color = tuple(cert_stroke_color)

                certificate = generate_certificate(
                    user_name,
                    st.session_state.config['template_image'],
                    st.session_state.config.get('name_x', 500),
                    st.session_state.config.get('name_y', 400),
                    st.session_state.config.get('font_size', 60),
                    cert_color,
                    st.session_state.config.get('font_family', 'Arial'),
                    st.session_state.config.get('font_weight', 'Regular'),
                    st.session_state.config.get('is_italic', False),
                    st.session_state.config.get('custom_font_path'),
                    st.session_state.config.get('stroke_width', 0),
                    cert_stroke_color,
                )

                st.success("✅ Certificate generated successfully!")
                st.image(certificate, caption="Your Certificate", use_container_width=True)

                buf = io.BytesIO()
                certificate.save(buf, format='PNG')
                buf.seek(0)

                st.download_button(
                    label="⬇️  Download Certificate",
                    data=buf,
                    file_name=f"certificate_{user_name.replace(' ', '_')}.png",
                    mime="image/png",
                    type="primary",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"❌ Error generating certificate: {str(e)}")
                st.info("Please contact the administrator if this error persists.")


# ═══════════════════════════════════════════════════════════════
#  PAGE: ADMIN PANEL
# ═══════════════════════════════════════════════════════════════
elif mode == "🔧 Admin Panel":
    if not st.session_state.authenticated:
        login_page()
    else:
        # Logout button
        with st.sidebar:
            if st.button("🚪  Logout", use_container_width=True):
                logout()
                st.rerun()

        st.markdown("# 🔧 Admin Panel")

        # ── 1. Template Upload ──
        st.markdown(
            """
            <div class="info-card">
                <h3 style="color:var(--gold-accent); margin-top:0;">1️⃣  Upload Certificate Template</h3>
                <p style="color:var(--beige-text); font-size:0.88rem;">Upload a PNG/JPG image to use as the certificate background.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        uploaded_file = st.file_uploader("Choose a certificate template image",
                                         type=['png', 'jpg', 'jpeg'])

        if uploaded_file:
            template_img = Image.open(uploaded_file)
            st.session_state.config['template_image'] = template_img
            template_img.save('certificate_template.png')
            st.session_state.config['template_path'] = 'certificate_template.png'
            st.success("Template uploaded successfully!")
            st.image(template_img, caption="Certificate Template", use_container_width=True)
        elif st.session_state.config['template_path'] and os.path.exists(st.session_state.config['template_path']):
            template_img = Image.open(st.session_state.config['template_path'])
            st.session_state.config['template_image'] = template_img
            st.image(template_img, caption="Current Certificate Template", use_container_width=True)

        st.markdown("")

        # ── 2. Configure Text Placement ──
        st.markdown(
            """
            <div class="info-card">
                <h3 style="color:var(--gold-accent); margin-top:0;">2️⃣  Configure Text & Typography</h3>
                <p style="color:var(--beige-text); font-size:0.88rem;">Adjust position, font family, and explicit styling.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            name_x = st.number_input("Name X Position (horizontal)",
                                     min_value=0,
                                     value=st.session_state.config['name_x'])
            name_y = st.number_input("Name Y Position (vertical)",
                                     min_value=0,
                                     value=st.session_state.config['name_y'])
            font_size = st.slider("Font Size", 20, 250,
                                  st.session_state.config['font_size'])
        
        with col2:
            st.write("##### 🔠 Font Settings")
            font_family = st.selectbox(
                "Font Family",
                options=list(FONT_FAMILIES.keys()) + ["Custom Upload"],
                index=0 if st.session_state.config.get('font_family') not in FONT_FAMILIES else list(FONT_FAMILIES.keys()).index(st.session_state.config['font_family'])
            )
            
            if font_family == "Custom Upload":
                font_file = st.file_uploader("Upload Font file (.ttf, .otf)", type=['ttf', 'otf'])
                if font_file:
                    with open("custom_font.ttf", "wb") as f:
                        f.write(font_file.read())
                    st.session_state.config['custom_font_path'] = "custom_font.ttf"
                    st.success("Custom font uploaded!")
                elif st.session_state.config.get('custom_font_path'):
                    st.info(f"Using: {st.session_state.config['custom_font_path']}")
            else:
                st.session_state.config['custom_font_path'] = None
                
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                font_weight = st.selectbox("Weight", ["Regular", "Bold"], 
                                           index=0 if st.session_state.config.get('font_weight', 'Regular') == 'Regular' else 1)
            with col_s2:
                is_italic = st.checkbox("Italic Style", value=st.session_state.config.get('is_italic', False))

        st.markdown("##### 🎨 Text Styling")
        col3, col4 = st.columns(2)
        with col3:
            color_hex = st.color_picker("Text Color", "#000000")
            font_color = tuple(int(color_hex[i:i + 2], 16) for i in (1, 3, 5))
        with col4:
            stroke_width = st.slider("Text Outline Thickness", 0, 10,
                                     st.session_state.config.get('stroke_width', 0),
                                     help="0 = No outline")

        if stroke_width > 0:
            stroke_color_hex = st.color_picker("Outline Color", "#000000")
            stroke_color = tuple(int(stroke_color_hex[i:i + 2], 16) for i in (1, 3, 5))
        else:
            stroke_color = (0, 0, 0)

        # Update config
        st.session_state.config['name_x'] = name_x
        st.session_state.config['name_y'] = name_y
        st.session_state.config['font_size'] = font_size
        st.session_state.config['font_family'] = font_family
        st.session_state.config['font_weight'] = font_weight
        st.session_state.config['is_italic'] = is_italic
        st.session_state.config['font_color'] = font_color
        st.session_state.config['stroke_width'] = stroke_width
        st.session_state.config['stroke_color'] = stroke_color

        st.markdown("")

        # ── 3. Preview ──
        st.markdown(
            """
            <div class="info-card">
                <h3 style="color:var(--gold-accent); margin-top:0;">3️⃣  Preview</h3>
                <p style="color:var(--beige-text); font-size:0.88rem;">See how the certificate looks with a sample name.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_prev1, col_prev2 = st.columns([3, 1])
        with col_prev1:
            preview_name = st.text_input("Preview Name", "John Doe", key="preview_name_input")
        with col_prev2:
            st.write("")
            st.write("")
            if st.button("🔄 Refresh Preview", use_container_width=True):
                st.rerun()

        if st.session_state.config['template_image']:
            preview_cert = generate_certificate(
                preview_name,
                st.session_state.config['template_image'],
                int(name_x), int(name_y), int(font_size),
                font_color, 
                font_family=font_family,
                font_weight=font_weight,
                is_italic=is_italic,
                custom_font_path=st.session_state.config.get('custom_font_path'),
                stroke_width=int(stroke_width), 
                stroke_color=stroke_color,
            )
            st.image(preview_cert,
                     caption=f"Preview (Pos: {name_x}, {name_y})",
                     use_container_width=True)

        outline_text = f", Outline: {stroke_width}px" if stroke_width > 0 else ""
        style_text = f"{font_weight} {'Italic' if is_italic else ''}".strip()
        st.info(f"💡 Current: {font_family} ({style_text}), Size={font_size}, "
                f"Position=({name_x}, {name_y}){outline_text}")
        st.caption("💡 Change settings above and click **Refresh Preview** to see changes.")

        st.markdown("")

        # ── 4. Participants ──
        st.markdown(
            """
            <div class="info-card">
                <h3 style="color:var(--gold-accent); margin-top:0;">4️⃣  Manage Participants</h3>
                <p style="color:var(--beige-text); font-size:0.88rem;">Add individual or bulk participant names.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        new_participant = st.text_input("Add Participant Name")
        if st.button("➕ Add Participant"):
            if new_participant and new_participant not in st.session_state.config['participants']:
                st.session_state.config['participants'].append(new_participant)
                save_config()
                st.success(f"Added **{new_participant}**")
                st.rerun()

        st.markdown("##### 📋 Bulk Add")
        bulk_participants = st.text_area("Enter names (one per line)")
        if st.button("➕ Add All"):
            names = [n.strip() for n in bulk_participants.split('\n') if n.strip()]
            for name in names:
                if name not in st.session_state.config['participants']:
                    st.session_state.config['participants'].append(name)
            save_config()
            st.success(f"Added **{len(names)}** participants")
            st.rerun()

        if st.session_state.config['participants']:
            st.markdown(f"##### 👥 Current Participants ({len(st.session_state.config['participants'])})")
            for i, participant in enumerate(st.session_state.config['participants']):
                col_p1, col_p2 = st.columns([4, 1])
                with col_p1:
                    st.text(participant)
                with col_p2:
                    if st.button("🗑️", key=f"remove_{i}"):
                        st.session_state.config['participants'].remove(participant)
                        save_config()
                        st.rerun()

        st.markdown("")
        if st.button("💾  Save All Settings", type="primary", use_container_width=True):
            save_config()
            st.success("✅ Configuration saved successfully!")


# ═══════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    """
    <div class="footer">
        © 2026 AWS Cloud Clubs – Mecs &nbsp;|&nbsp; Built with <span class="heart">❤</span> and Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
