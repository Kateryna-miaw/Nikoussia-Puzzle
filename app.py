import streamlit as st
import base64
import os

st.set_page_config(page_title="✿ Nikoussia Puzzle ✿", layout="wide", page_icon="🧩")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background: #1a0a1e !important; }
    .block-container { padding: 0rem; max-width: 100%; }
    iframe { border: none !important; }
    .stSelectbox { display: none; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────
#  File loaders
# ──────────────────────────────────────

IMAGE_DIR = os.path.join(os.path.dirname(__file__), "images")
AUDIO_DIR = os.path.join(os.path.dirname(__file__), "audio")


def find_puzzle_images():
    if not os.path.exists(IMAGE_DIR):
        return []
    return sorted([
        f for f in os.listdir(IMAGE_DIR)
        if f.lower().startswith("puzzle_")
        and f.lower().rsplit(".", 1)[-1] in ("png", "jpg", "jpeg", "webp", "bmp")
    ])


def load_file_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


def load_image_base64(fname):
    data = load_file_b64(os.path.join(IMAGE_DIR, fname))
    ext = fname.rsplit(".", 1)[-1].lower()
    mime = f"image/{'jpeg' if ext == 'jpg' else ext}"
    return data, mime


# ──────────────────────────────────────
#  Load assets
# ──────────────────────────────────────

available_images = find_puzzle_images()
if not available_images:
    st.error("🧩 Aucune image ! Placez `puzzle_1.png` dans `images/`.")
    st.stop()

selected_image = (
    st.selectbox("img", available_images)
    if len(available_images) > 1
    else available_images[0]
)

img_data, img_mime = load_image_base64(selected_image)
bg_gif_b64 = load_file_b64(os.path.join(IMAGE_DIR, "bgm.gif"))
audio_bgm = load_file_b64(os.path.join(AUDIO_DIR, "bgm.mp3"))
audio_click = load_file_b64(os.path.join(AUDIO_DIR, "btn_click.mp3"))
audio_hover = load_file_b64(os.path.join(AUDIO_DIR, "btn_hover.mp3"))
audio_indice = load_file_b64(os.path.join(AUDIO_DIR, "indice.mp3"))


# ──────────────────────────────────────
#  HTML / CSS / JS
# ──────────────────────────────────────

html_code = r"""
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&family=Baloo+2:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
  --purple-deep:#7B5EA7; --purple-mid:#9B7EC8; --purple-soft:#B8A0D6;
  --purple-pale:#D6C6EC; --purple-wash:#E8DCF5;
  --pink-hot:#E8679A; --pink-mid:#F08EB5; --pink-soft:#F5B0CB; --pink-pale:#FCDAE8;
  --blue-soft:#A8D8EA; --blue-pale:#C8E8F4; --blue-mid:#7EC8E3;
  --gold-star:#F0C060; --text-dark:#3A1D4A; --text-mid:#6B4A7E;
  --panel-bg:rgba(216,190,240,0.14); --panel-pink:rgba(245,176,203,0.12); --panel-blue:rgba(168,216,234,0.12);
  --dev-bg:#0D0A14; --dev-border:#2A1F3D; --dev-accent:#7B5EA7;
  --dev-green:#4ADE80; --dev-yellow:#FBBF24; --dev-red:#F87171;
  --dev-cyan:#22D3EE; --dev-text:#C8B8E8; --dev-dim:#6B5080;
}

* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Quicksand',sans-serif; overflow:hidden; height:100vh; color:var(--text-dark); background:linear-gradient(135deg,#6B4D8A,#8B6AAF 30%,#9B7EC8 60%,#7B5EA7); }

#bg-layer { position:fixed; inset:0; z-index:0; background-size:cover; background-position:center; }
#bg-layer::after { content:''; position:absolute; inset:0; background:rgba(107,77,138,0.04); pointer-events:none; }

.kawaii-panel { background:var(--panel-bg); backdrop-filter:blur(16px); border:3px solid rgba(184,160,214,0.5); border-radius:16px; box-shadow:0 4px 20px rgba(90,61,106,0.15),inset 0 1px 0 rgba(255,255,255,0.2); position:relative; overflow:hidden; }
.kawaii-panel::before { content:''; position:absolute; top:-1px; left:8px; right:8px; height:6px; background:repeating-radial-gradient(circle at 6px 0,transparent 0,transparent 4px,rgba(184,160,214,0.4) 4px,rgba(184,160,214,0.4) 5px); background-size:12px 6px; }
.kawaii-panel-pink { background:var(--panel-pink); border-color:rgba(245,176,203,0.5); }
.kawaii-panel-pink::before { background:repeating-radial-gradient(circle at 6px 0,transparent 0,transparent 4px,rgba(245,176,203,0.4) 4px,rgba(245,176,203,0.4) 5px); background-size:12px 6px; }
.kawaii-panel-blue { background:var(--panel-blue); border-color:rgba(168,216,234,0.5); }
.kawaii-panel-blue::before { background:repeating-radial-gradient(circle at 6px 0,transparent 0,transparent 4px,rgba(168,216,234,0.4) 4px,rgba(168,216,234,0.4) 5px); background-size:12px 6px; }

@keyframes borderGlow {
  0%  {border-color:rgba(184,160,214,0.5);box-shadow:0 4px 20px rgba(90,61,106,0.15),0 0 8px rgba(184,160,214,0.1);}
  33% {border-color:rgba(245,176,203,0.6);box-shadow:0 4px 20px rgba(90,61,106,0.15),0 0 12px rgba(245,176,203,0.15);}
  66% {border-color:rgba(168,216,234,0.6);box-shadow:0 4px 20px rgba(90,61,106,0.15),0 0 12px rgba(168,216,234,0.15);}
  100%{border-color:rgba(184,160,214,0.5);box-shadow:0 4px 20px rgba(90,61,106,0.15),0 0 8px rgba(184,160,214,0.1);}
}
.glow-border { animation:borderGlow 5s ease-in-out infinite; }
@keyframes borderGlowSoft { 0%,100%{border-color:rgba(184,160,214,0.35)} 50%{border-color:rgba(245,176,203,0.45)} }
.glow-soft { animation:borderGlowSoft 4s ease-in-out infinite; }

.ribbon-title { display:inline-block; background:linear-gradient(180deg,var(--purple-soft),var(--purple-mid)); color:white; font-family:'Baloo 2',cursive; font-size:12px; font-weight:700; padding:3px 18px 4px; border-radius:0 0 10px 10px; text-shadow:0 1px 3px rgba(40,10,50,0.5); box-shadow:0 2px 6px rgba(90,61,106,0.2); margin:0 auto; }
.ribbon-title-pink { background:linear-gradient(180deg,var(--pink-soft),var(--pink-hot)); }
.ribbon-title-blue { background:linear-gradient(180deg,var(--blue-pale),var(--blue-mid)); color:var(--text-dark); }

#app-container { display:flex; flex-direction:column; height:100vh; width:100vw; position:relative; z-index:1; padding:6px; gap:6px; }

#top-bar { display:flex; align-items:center; justify-content:space-between; padding:0 16px; height:52px; min-height:52px; border-radius:16px; }
#top-bar h1 { font-family:'Baloo 2',cursive; font-size:16px; font-weight:800; color:white; text-shadow:0 2px 6px rgba(40,10,50,0.7),0 0 12px rgba(40,10,50,0.4); display:flex; align-items:center; gap:6px; }

.flower { display:inline-block; animation:flowerSpin 4s linear infinite; }
@keyframes flowerSpin { 0%{transform:rotate(0deg) scale(1)} 25%{transform:rotate(5deg) scale(1.05)} 50%{transform:rotate(0deg) scale(1)} 75%{transform:rotate(-5deg) scale(1.05)} 100%{transform:rotate(0deg) scale(1)} }
.sparkle-star { display:inline-block; animation:starTwinkle 2s ease-in-out infinite; color:var(--gold-star); }
@keyframes starTwinkle { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.4;transform:scale(0.7)} }

.bar-controls { display:flex; gap:6px; align-items:center; }

.btn { font-family:'Quicksand',sans-serif; font-weight:700; font-size:11px; padding:7px 14px; border:2.5px solid; border-radius:12px; cursor:pointer; transition:all 0.15s; display:flex; align-items:center; gap:5px; box-shadow:0 3px 0 rgba(0,0,0,0.15),0 2px 8px rgba(0,0,0,0.1); text-shadow:0 1px 2px rgba(0,0,0,0.25); }
.btn:active { transform:translateY(3px); box-shadow:none; }
.btn-pink   { background:linear-gradient(180deg,var(--pink-mid),var(--pink-hot)); color:white; border-color:#D05A85; }
.btn-pink:hover { background:linear-gradient(180deg,#F5A0C0,var(--pink-mid)); }
.btn-blue   { background:linear-gradient(180deg,var(--blue-pale),var(--blue-mid)); color:var(--text-dark); border-color:#6AB0CC; }
.btn-blue:hover { background:linear-gradient(180deg,#D8F0FA,var(--blue-pale)); }
.btn-purple { background:linear-gradient(180deg,var(--purple-pale),var(--purple-mid)); color:white; border-color:var(--purple-deep); }
.btn-purple:hover { background:linear-gradient(180deg,var(--purple-wash),var(--purple-soft)); }
.btn-gold   { background:linear-gradient(180deg,#F8E0A0,var(--gold-star)); color:#6A4800; border-color:#C89830; font-weight:800; }
.btn-gold:hover { background:linear-gradient(180deg,#FFF0C0,#F8E0A0); }
.btn-dev    { background:linear-gradient(180deg,#2A1F3D,#1A1228); color:var(--dev-cyan); border-color:#3D2A5A; font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:0.04em; }
.btn-dev:hover { background:linear-gradient(180deg,#3D2A5A,#2A1F3D); border-color:var(--dev-accent); }
.btn-dev.active { background:linear-gradient(180deg,#1A0A2E,#0D0A14); border-color:var(--dev-cyan); box-shadow:0 0 8px rgba(34,211,238,0.2); }
.btn:disabled { opacity:0.4; cursor:not-allowed; }

#timer { font-family:'Baloo 2',cursive; font-size:14px; font-weight:700; color:white; min-width:68px; text-align:center; background:rgba(40,10,50,0.35); border:2.5px solid rgba(184,160,214,0.5); padding:4px 10px; border-radius:12px; text-shadow:0 1px 4px rgba(40,10,50,0.7); }

#middle-area { flex:1; display:flex; gap:6px; min-height:0; overflow:hidden; }
#puzzle-panel { flex:1; position:relative; overflow:hidden; border-radius:16px; }
#puzzle-canvas { position:absolute; top:0; left:0; width:100%; height:100%; }
#scanlines { position:absolute; inset:0; pointer-events:none; z-index:50; background:repeating-linear-gradient(0deg,transparent 0px,transparent 4px,rgba(184,160,214,0.008) 4px,rgba(184,160,214,0.008) 8px); }

#sidebar { width:190px; min-width:190px; display:flex; flex-direction:column; gap:6px; }
.sidebar-panel { border-radius:16px; overflow:hidden; }
.sidebar-header { text-align:center; padding-top:4px; }
.sidebar-body { padding:10px 12px; }

.stat-row { display:flex; justify-content:space-between; align-items:center; font-size:11px; color:white; font-family:'Quicksand',sans-serif; font-weight:700; padding:5px 0; border-bottom:1px dashed rgba(184,160,214,0.3); text-shadow:0 1px 3px rgba(40,10,50,0.6),0 0 8px rgba(40,10,50,0.3); }
.stat-row:last-child { border-bottom:none; }
.stat-value { color:#FFE0F0; font-weight:800; font-family:'Baloo 2',cursive; font-size:13px; text-shadow:0 1px 4px rgba(40,10,50,0.7); }
.cute-progress { width:100%; height:14px; background:rgba(255,255,255,0.25); border:2.5px solid rgba(184,160,214,0.4); border-radius:10px; overflow:hidden; margin-top:6px; }
.cute-progress-fill { height:100%; background:linear-gradient(90deg,var(--pink-hot),var(--pink-mid),var(--purple-soft)); border-radius:8px; transition:width 0.4s; box-shadow:inset 0 -2px 4px rgba(0,0,0,0.1),inset 0 1px 0 rgba(255,255,255,0.3); }
#mini-preview { width:100%; aspect-ratio:1; border:2.5px solid rgba(184,160,214,0.4); border-radius:10px; cursor:pointer; display:block; }

#bottom-tray { height:180px; min-height:180px; display:flex; flex-direction:column; border-radius:16px; transition:height 0.3s ease; }
#bottom-tray.dev-open { height:130px; min-height:130px; }
.tray-header { text-align:center; padding-top:4px; padding-bottom:2px; }
#tray-scroll { flex:1; overflow-y:auto; overflow-x:hidden; padding:6px 8px; display:flex; flex-wrap:wrap; align-content:flex-start; gap:2px; }
#tray-scroll::-webkit-scrollbar { width:8px; }
#tray-scroll::-webkit-scrollbar-track { background:rgba(255,255,255,0.06); border-radius:4px; }
#tray-scroll::-webkit-scrollbar-thumb { background:rgba(184,160,214,0.5); border-radius:4px; }
.tray-piece { display:inline-block; cursor:grab; transition:transform 0.12s; }
.tray-piece:hover { transform:scale(1.12); filter:drop-shadow(0 0 8px rgba(232,103,154,0.4)); }

/* ── DEV PROFILER ── */
#dev-panel { height:0; overflow:hidden; background:var(--dev-bg); border:2px solid var(--dev-border); border-radius:12px; transition:height 0.3s ease; font-family:'JetBrains Mono',monospace; position:relative; }
#dev-panel.open { height:220px; }
#dev-titlebar { background:linear-gradient(90deg,#1A0A2E,#0D0A14); border-bottom:1px solid var(--dev-border); padding:5px 12px; display:flex; align-items:center; gap:8px; position:absolute; top:0; left:0; right:0; height:28px; z-index:1; }
#dev-dot { width:8px; height:8px; border-radius:50%; background:var(--dev-cyan); box-shadow:0 0 6px var(--dev-cyan); animation:devDot 1.5s infinite; }
@keyframes devDot { 0%,100%{opacity:1} 50%{opacity:0.3} }
#dev-titlebar span { font-size:10px; color:var(--dev-dim); letter-spacing:0.08em; text-transform:uppercase; }
#dev-titlebar strong { font-size:10px; color:var(--dev-cyan); letter-spacing:0.06em; }
#dev-body { position:absolute; top:28px; left:0; right:0; bottom:0; display:flex; overflow:hidden; }
.dev-col { flex:1; padding:8px 10px; border-right:1px solid var(--dev-border); overflow:hidden; }
.dev-col:last-child { border-right:none; }
.dev-col-title { font-size:9px; color:var(--dev-accent); letter-spacing:0.1em; text-transform:uppercase; margin-bottom:6px; padding-bottom:3px; border-bottom:1px solid var(--dev-border); }
.dev-metric { display:flex; justify-content:space-between; align-items:center; padding:2px 0; font-size:10px; }
.dev-metric-label { color:var(--dev-dim); }
.dev-metric-val { color:var(--dev-text); font-weight:700; }
.dev-metric-val.good { color:var(--dev-green); }
.dev-metric-val.warn { color:var(--dev-yellow); }
.dev-metric-val.bad  { color:var(--dev-red); }
.dev-sparkline { width:100%; height:40px; margin-top:6px; }
#dev-heatmap { width:100%; flex:1; image-rendering:pixelated; border-radius:4px; margin-top:6px; }
#dev-algo-log { font-size:9px; color:var(--dev-dim); height:85px; overflow-y:auto; margin-top:4px; line-height:1.7; }
#dev-algo-log::-webkit-scrollbar { width:3px; }
#dev-algo-log::-webkit-scrollbar-thumb { background:var(--dev-accent); border-radius:2px; }
.log-ts  { color:var(--dev-accent); }
.log-ok  { color:var(--dev-green); }
.log-err { color:var(--dev-red); }
.log-inf { color:var(--dev-cyan); }
#btn-export-json { margin-top:6px; width:100%; padding:4px 8px; font-size:9px; background:rgba(123,94,167,0.2); border:1px solid var(--dev-accent); color:var(--dev-text); border-radius:5px; cursor:pointer; letter-spacing:0.06em; text-transform:uppercase; font-family:'JetBrains Mono',monospace; transition:background 0.15s; }
#btn-export-json:hover { background:rgba(123,94,167,0.4); }

/* ── CONTEXT MENU ── */
#rotate-menu { display:none; position:absolute; z-index:200; background:rgba(216,190,240,0.92); backdrop-filter:blur(16px); border:2.5px solid rgba(184,160,214,0.6); border-radius:14px; overflow:hidden; box-shadow:0 8px 24px rgba(90,61,106,0.25); }
.rotate-menu-title { background:linear-gradient(90deg,var(--purple-soft),var(--pink-soft)); padding:5px 12px; font-family:'Baloo 2',cursive; font-size:11px; font-weight:700; color:white; text-shadow:0 1px 1px rgba(0,0,0,0.15); border-bottom:2px solid rgba(184,160,214,0.3); }
.rotate-btn { display:block; width:100%; padding:9px 14px; background:none; border:none; border-bottom:1px dashed rgba(184,160,214,0.25); color:var(--text-dark); font-family:'Quicksand',sans-serif; font-size:11px; font-weight:600; cursor:pointer; text-align:left; }
.rotate-btn:hover { background:rgba(232,103,154,0.15); color:var(--pink-hot); }
.rotate-btn:last-child { border-bottom:none; }

/* ── MODALS ── */
.modal-overlay { position:fixed; inset:0; z-index:999; background:rgba(90,61,106,0.4); backdrop-filter:blur(10px); display:none; align-items:center; justify-content:center; }
.modal-overlay.active { display:flex; }
.modal-box { background:rgba(232,220,245,0.92); backdrop-filter:blur(20px); border:3px solid rgba(184,160,214,0.6); border-radius:20px; box-shadow:0 12px 40px rgba(90,61,106,0.3); max-width:440px; width:92%; overflow:hidden; }
.modal-titlebar { background:linear-gradient(90deg,var(--purple-mid),var(--pink-mid),var(--purple-soft)); padding:8px 14px; font-family:'Baloo 2',cursive; font-size:12px; font-weight:700; color:white; text-shadow:0 1px 2px rgba(0,0,0,0.2); text-align:center; }
.modal-body { padding:20px 24px; }
.modal-body h2 { font-family:'Baloo 2',cursive; font-size:20px; font-weight:800; color:var(--purple-deep); margin-bottom:10px; text-align:center; }
.modal-body p { font-family:'Quicksand',sans-serif; font-size:12px; font-weight:600; color:var(--text-mid); text-align:center; margin-bottom:6px; }
.score-line { font-family:'Baloo 2',cursive; font-size:22px; font-weight:800; color:var(--pink-hot); text-align:center; margin:10px 0; }

/* ── RULES ── */
#rules-overlay { position:fixed; inset:0; z-index:1000; background:rgba(70,40,90,0.7); backdrop-filter:blur(14px); display:flex; align-items:center; justify-content:center; }
#rules-overlay.hidden { display:none; }
#rules-content { background:rgba(232,220,245,0.93); backdrop-filter:blur(20px); border:3px solid rgba(184,160,214,0.6); border-radius:20px; box-shadow:0 12px 40px rgba(90,61,106,0.3); max-width:500px; width:92%; max-height:90vh; overflow:hidden; }
#rules-body { padding:16px 22px 20px; overflow-y:auto; max-height:calc(90vh - 50px); }
#rules-body::-webkit-scrollbar { width:5px; }
#rules-body::-webkit-scrollbar-thumb { background:var(--purple-soft); border-radius:3px; }
#rules-body h2 { font-family:'Baloo 2',cursive; font-size:18px; font-weight:800; color:var(--purple-deep); margin-bottom:14px; text-align:center; }
.rule-item { display:flex; gap:10px; align-items:flex-start; padding:8px 0; border-bottom:1px dashed rgba(184,160,214,0.35); }
.rule-item:last-of-type { border-bottom:none; }
.rule-icon { font-size:18px; min-width:26px; text-align:center; }
.rule-title { font-family:'Baloo 2',cursive; font-weight:700; color:var(--pink-hot); font-size:12px; display:block; }
.rule-desc { color:var(--text-mid); font-size:11px; font-family:'Quicksand',sans-serif; font-weight:500; line-height:1.4; }
#rules-start-btn { display:block; margin:16px auto 4px; padding:10px 36px; font-family:'Baloo 2',cursive; font-size:14px; font-weight:800; background:linear-gradient(180deg,var(--pink-mid),var(--pink-hot)); color:white; border:3px solid #D05A85; border-radius:14px; cursor:pointer; box-shadow:0 4px 0 #B04A72,0 6px 16px rgba(232,103,154,0.3); text-shadow:0 1px 1px rgba(0,0,0,0.15); animation:startPulse 2.5s infinite; }
@keyframes startPulse { 0%,100%{box-shadow:0 4px 0 #B04A72,0 6px 16px rgba(232,103,154,0.3)} 50%{box-shadow:0 4px 0 #B04A72,0 6px 24px rgba(232,103,154,0.5)} }
#rules-start-btn:active { transform:translateY(4px); box-shadow:none; }

/* ── PREVIEW ── */
#preview-overlay { display:none; position:fixed; inset:0; z-index:500; background:rgba(90,61,106,0.4); backdrop-filter:blur(8px); align-items:center; justify-content:center; cursor:pointer; }
#preview-overlay img { max-width:75vw; max-height:75vh; border:4px solid var(--purple-soft); border-radius:16px; box-shadow:0 12px 40px rgba(90,61,106,0.3); }

/* ── HINT FLASH ── */
@keyframes hintFlash { 0%{opacity:0;transform:scale(0.8)} 20%{opacity:1;transform:scale(1.06)} 80%{opacity:1;transform:scale(1)} 100%{opacity:0;transform:scale(0.95)} }
.hint-marker { position:absolute; pointer-events:none; z-index:80; border:3px solid var(--gold-star); border-radius:8px; animation:hintFlash 2s forwards; box-shadow:0 0 18px rgba(240,192,96,0.5); background:rgba(240,192,96,0.08); }

/* ── TOASTS ── */
#toast-container { position:absolute; top:10px; right:10px; z-index:300; display:flex; flex-direction:column; gap:6px; }
.toast { font-family:'Quicksand',sans-serif; font-weight:700; font-size:11px; padding:8px 14px; border-radius:12px; border:2.5px solid; animation:toastIn 0.3s,toastOut 0.4s 2.2s forwards; box-shadow:0 3px 12px rgba(0,0,0,0.1); }
.toast-hint   { background:rgba(240,208,128,0.92); color:#6A4800; border-color:#D0A040; }
.toast-combo  { background:rgba(184,160,214,0.92); color:white; border-color:var(--purple-mid); }
.toast-streak { background:rgba(232,103,154,0.92); color:white; border-color:#C05080; }
@keyframes toastIn  { from{opacity:0;transform:translateX(20px)} to{opacity:1;transform:translateX(0)} }
@keyframes toastOut { from{opacity:1} to{opacity:0;transform:translateY(-8px)} }

/* ── ENCOURAGEMENT ── */
.encouragement-bubble { position:absolute; z-index:90; font-family:'Baloo 2',cursive; font-size:14px; font-weight:700; color:white; background:linear-gradient(135deg,rgba(232,103,154,0.85),rgba(155,126,200,0.85)); backdrop-filter:blur(8px); padding:8px 18px; border-radius:20px; border:2px solid rgba(255,255,255,0.3); pointer-events:none; white-space:nowrap; text-shadow:0 1px 3px rgba(40,10,50,0.4); box-shadow:0 4px 16px rgba(90,61,106,0.25); animation:bubbleFloat 3s ease-out forwards; transform:translateX(-50%); }
@keyframes bubbleFloat { 0%{opacity:0;transform:translateX(-50%) translateY(10px) scale(0.7)} 12%{opacity:1;transform:translateX(-50%) translateY(0px) scale(1.05)} 20%{transform:translateX(-50%) translateY(-2px) scale(1)} 75%{opacity:1;transform:translateX(-50%) translateY(-25px) scale(1)} 100%{opacity:0;transform:translateX(-50%) translateY(-45px) scale(0.9)} }
</style>
</head>
<body>

<div id="bg-layer"></div>

<!-- RULES -->
<div id="rules-overlay">
  <div id="rules-content" class="glow-border">
    <div class="modal-titlebar" style="display:flex;align-items:center;justify-content:space-between;">
      <span>✿ règles du jeu ✿</span>
      <span id="rules-close-x" style="display:none;cursor:pointer;font-size:18px;padding:0 4px;opacity:0.8;" onclick="document.getElementById('rules-overlay').classList.add('hidden')">✕</span>
    </div>
    <div id="rules-body">
      <h2>Nikoussia Puzzle</h2>
      <div class="rule-item"><span class="rule-icon">·</span><div><span class="rule-title">Le puzzle</span><span class="rule-desc">256 pièces à remettre en place. Glisse-les depuis le tiroir du bas vers le plateau.</span></div></div>
      <div class="rule-item"><span class="rule-icon">·</span><div><span class="rule-title">Rotation</span><span class="rule-desc">Les pièces sont tournées au hasard. Clic droit ou touche R pour les remettre dans le bon sens.</span></div></div>
      <div class="rule-item"><span class="rule-icon">·</span><div><span class="rule-title">Indices</span><span class="rule-desc">Tu commences avec 5 indices. Un indice place une pièce au hasard pour toi.</span></div></div>
      <div class="rule-item"><span class="rule-icon">·</span><div><span class="rule-title">Gagner des indices</span><span class="rule-desc">Chaque pièce bien placée te donne +1 indice. Avec un combo de 3 ou plus, c'est +2.</span></div></div>
      <div class="rule-item"><span class="rule-icon">·</span><div><span class="rule-title">Combos</span><span class="rule-desc">Place plusieurs pièces d'affilée pour monter ton combo. Il se casse si tu rates.</span></div></div>
      <div class="rule-item"><span class="rule-icon">·</span><div><span class="rule-title">Aimant</span><span class="rule-desc">Quand une pièce bien orientée passe près de sa place, elle est légèrement attirée.</span></div></div>
      <div class="rule-item"><span class="rule-icon">·</span><div><span class="rule-title">Aperçu</span><span class="rule-desc">Tu peux voir l'image complète, mais seulement 3 secondes à chaque fois.</span></div></div>
      <div class="rule-item"><span class="rule-icon">·</span><div><span class="rule-title">Score</span><span class="rule-desc">Pièces placées × meilleur combo, moins le temps. Fais de ton mieux.</span></div></div>
      <button id="rules-start-btn" onclick="startGame()">Commencer</button>
    </div>
  </div>
</div>

<!-- APP -->
<div id="app-container">

  <div id="top-bar" class="kawaii-panel glow-border">
    <h1><span class="flower">🌸</span> Nikoussia Puzzle <span class="sparkle-star">✦</span></h1>
    <div class="bar-controls">
      <div id="timer">00:00</div>
      <button class="btn btn-purple" id="btn-rotate-sel" disabled onclick="rotateSelected()">Tourner</button>
      <button class="btn btn-gold"   id="btn-hint" onclick="useHint()">Indice (5)</button>
      <button class="btn btn-blue"   onclick="showPreview()">Aperçu</button>
      <button class="btn btn-pink"   onclick="showRulesPopup()">Règles</button>
      <button class="btn btn-purple" onclick="resetPuzzle()">Rejouer</button>
      <button class="btn btn-purple" id="btn-mute" onclick="toggleMute()">🔊 Son</button>
      <button class="btn btn-pink"   id="btn-finish" onclick="autoFinish()">Finir pour moi</button>
      <button class="btn btn-dev"    id="btn-dev" onclick="toggleDevPanel()">⌥ PROFILER</button>
    </div>
  </div>

  <div id="middle-area">
    <div id="puzzle-panel" class="kawaii-panel glow-border">
      <canvas id="puzzle-canvas"></canvas>
      <div id="scanlines"></div>
      <div id="toast-container"></div>
    </div>
    <div id="sidebar">
      <div class="sidebar-panel kawaii-panel-pink glow-soft">
        <div class="sidebar-header"><span class="ribbon-title ribbon-title-pink">Stats</span></div>
        <div class="sidebar-body">
          <div class="stat-row"><span>Placées</span><span class="stat-value" id="placed-count">0/256</span></div>
          <div class="stat-row"><span>Indices</span><span class="stat-value" id="hint-count">5</span></div>
          <div class="stat-row"><span>Combo</span><span class="stat-value" id="combo-count">×0</span></div>
          <div class="stat-row"><span>Record</span><span class="stat-value" id="best-combo">×0</span></div>
          <div class="cute-progress"><div class="cute-progress-fill" id="progress-bar" style="width:0%"></div></div>
        </div>
      </div>
      <div class="sidebar-panel kawaii-panel-blue glow-soft" style="flex:1;">
        <div class="sidebar-header"><span class="ribbon-title ribbon-title-blue">Aperçu</span></div>
        <div class="sidebar-body" style="padding:8px;">
          <canvas id="mini-preview" onclick="showPreview()"></canvas>
        </div>
      </div>
    </div>
  </div>

  <div id="bottom-tray" class="kawaii-panel glow-border">
    <div class="tray-header"><span class="ribbon-title">Pièces</span></div>
    <div id="tray-scroll"></div>
  </div>

  <!-- DEV PROFILER PANEL -->
  <div id="dev-panel">
    <div id="dev-titlebar">
      <div id="dev-dot"></div>
      <strong>NIKOUSSIA PROFILER</strong>
      <span>— render · algo · heatmap · export  |  raccourci: F2</span>
    </div>
    <div id="dev-body">

      <div class="dev-col">
        <div class="dev-col-title">⬡ Render</div>
        <div class="dev-metric"><span class="dev-metric-label">FPS</span><span class="dev-metric-val good" id="dev-fps">—</span></div>
        <div class="dev-metric"><span class="dev-metric-label">Frame budget</span><span class="dev-metric-val" id="dev-framems">—</span></div>
        <div class="dev-metric"><span class="dev-metric-label">Draw calls</span><span class="dev-metric-val" id="dev-drawcalls">—</span></div>
        <div class="dev-metric"><span class="dev-metric-label">Canvas</span><span class="dev-metric-val" id="dev-canvaspx">—</span></div>
        <canvas class="dev-sparkline" id="dev-sparkline" width="160" height="40"></canvas>
      </div>

      <div class="dev-col">
        <div class="dev-col-title">⬡ Algorithme snap</div>
        <div class="dev-metric"><span class="dev-metric-label">Tests/drop (O(n))</span><span class="dev-metric-val" id="dev-tests">—</span></div>
        <div class="dev-metric"><span class="dev-metric-label">Magnet actif</span><span class="dev-metric-val" id="dev-magnet">non</span></div>
        <div class="dev-metric"><span class="dev-metric-label">Dist. cible</span><span class="dev-metric-val" id="dev-dist">—</span></div>
        <div class="dev-metric"><span class="dev-metric-label">Snap seuil</span><span class="dev-metric-val" id="dev-snap">—</span></div>
        <div class="dev-metric"><span class="dev-metric-label">Miss streak</span><span class="dev-metric-val warn" id="dev-miss">0</span></div>
        <div id="dev-algo-log"></div>
      </div>

      <div class="dev-col" style="flex:1.4;">
        <div class="dev-col-title">⬡ Heatmap placement</div>
        <canvas id="dev-heatmap" height="150"></canvas>
        <div style="display:flex;gap:4px;align-items:center;margin-top:4px;">
          <div style="width:60px;height:4px;background:linear-gradient(90deg,#1A0A2E,#7B5EA7,#E8679A,#F0C060);border-radius:2px;"></div>
          <span style="font-size:8px;color:var(--dev-dim)">tôt → tard</span>
        </div>
      </div>

      <div class="dev-col">
        <div class="dev-col-title">⬡ Session</div>
        <div class="dev-metric"><span class="dev-metric-label">Durée</span><span class="dev-metric-val" id="dev-elapsed">—</span></div>
        <div class="dev-metric"><span class="dev-metric-label">Pièces/min</span><span class="dev-metric-val good" id="dev-ppm">—</span></div>
        <div class="dev-metric"><span class="dev-metric-label">Précision</span><span class="dev-metric-val" id="dev-accuracy">—</span></div>
        <div class="dev-metric"><span class="dev-metric-label">Hints utilisés</span><span class="dev-metric-val" id="dev-hints-used">0</span></div>
        <div class="dev-metric"><span class="dev-metric-label">Drops totaux</span><span class="dev-metric-val" id="dev-drops">0</span></div>
        <button id="btn-export-json" onclick="exportSession()">↓ Export JSON session</button>
      </div>

    </div>
  </div>

</div>

<!-- Context menu -->
<div id="rotate-menu">
  <div class="rotate-menu-title">↻ Rotation</div>
  <button class="rotate-btn" onclick="rotateContextPiece(90)">90° horaire</button>
  <button class="rotate-btn" onclick="rotateContextPiece(180)">180°</button>
  <button class="rotate-btn" onclick="rotateContextPiece(270)">270° anti-horaire</button>
</div>

<!-- Win modal -->
<div id="win-modal" class="modal-overlay">
  <div class="modal-box glow-border">
    <div class="modal-titlebar">✿ victoire ✿</div>
    <div class="modal-body">
      <h2>🎀 Félicitations ! 🎀</h2>
      <p id="win-text"></p>
      <div class="score-line" id="win-score"></div>
      <p id="win-stats"></p>
      <button class="btn btn-pink" style="margin:14px auto 0;display:flex;" onclick="resetPuzzle();document.getElementById('win-modal').classList.remove('active');">🌸 Rejouer</button>
    </div>
  </div>
</div>

<div id="preview-overlay" onclick="this.style.display='none'"><img id="preview-img"></div>


<script>
/* ─── CONSTANTS ─── */
const GRID=16, TOTAL=256, INITIAL_HINTS=5;
const TAB_SIZE=0.22;

/* ─── GAME STATE ─── */
let hintsLeft=INITIAL_HINTS, placedCount=0, startTime=0, timerInterval=null;
let selectedPieceId=null, contextPieceId=null;
let combo=0, bestCombo=0, score=0, gameStarted=false;
let pieces=[], cellW, cellH, boardX, boardY, boardW, boardH;
let dragging=null, dragOffX=0, dragOffY=0, magnetGlow=null;
let encouragementTimer=null, shownMilestones=new Set();
let hEdges=[], vEdges=[];

/* ─── PROFILER STATE ─── */
let devOpen=false;
let fpsHistory=[], lastFrameTime=performance.now(), frameCount=0;
let fpsDisplayVal=0, lastFpsTick=performance.now();
let totalDrops=0, totalMisses=0, hintsUsed=0, missStreak=0;
let lastDropTests=0, lastDropDist=0;
let placementOrder=new Array(TOTAL).fill(0), placementStep=0;

/* ─── ASSETS ─── */
const IMG_DATA  ="IMG_DATA_PLACEHOLDER";
const IMG_MIME  ="IMG_MIME_PLACEHOLDER";
const BG_GIF    ="BG_GIF_PLACEHOLDER";
const SND_BGM   ="SND_BGM_PLACEHOLDER";
const SND_CLICK ="SND_CLICK_PLACEHOLDER";
const SND_HOVER ="SND_HOVER_PLACEHOLDER";
const SND_INDICE="SND_INDICE_PLACEHOLDER";

if(BG_GIF&&BG_GIF.length>10) document.getElementById('bg-layer').style.backgroundImage=`url(data:image/gif;base64,${BG_GIF})`;

const img=new Image();
img.src=`data:${IMG_MIME};base64,${IMG_DATA}`;
const canvas=document.getElementById('puzzle-canvas');
const ctx=canvas.getContext('2d');

/* ─── AUDIO ─── */
let audioStarted=false, bgmAudio=null, sfxClick=null, sfxHover=null, sfxIndice=null, audioMuted=false;
function initAudio(){
  if(audioStarted)return; audioStarted=true;
  function mk(b64,vol,loop){if(!b64||b64.length<10)return null;const a=new Audio(`data:audio/mp3;base64,${b64}`);a.volume=vol;a.loop=!!loop;return a;}
  bgmAudio=mk(SND_BGM,0.3,true); sfxClick=mk(SND_CLICK,0.5); sfxHover=mk(SND_HOVER,0.2); sfxIndice=mk(SND_INDICE,0.5);
  if(bgmAudio)bgmAudio.play().catch(()=>{});
}
function playSfx(type){
  if(audioMuted)return;
  const src={click:sfxClick,hover:sfxHover,indice:sfxIndice}[type];
  if(!src)return;
  try{const c=src.cloneNode();c.volume=src.volume;c.play().catch(()=>{});}catch(e){}
}
function toggleMute(){audioMuted=!audioMuted;if(bgmAudio)bgmAudio.muted=audioMuted;document.getElementById('btn-mute').textContent=audioMuted?'🔇 Son':'🔊 Son';}
document.addEventListener('mouseover',e=>{if(e.target.closest('.btn,.tray-piece,.rotate-btn'))playSfx('hover');});
document.addEventListener('mousedown',e=>{if(e.target.closest('.btn,.rotate-btn,#rules-start-btn'))playSfx('click');});

/* ─── EDGES ─── */
function generateEdges(){
  hEdges=[]; vEdges=[];
  for(let r=0;r<GRID-1;r++){hEdges[r]=[];for(let c=0;c<GRID;c++)hEdges[r][c]=Math.random()<.5?1:-1;}
  for(let r=0;r<GRID;r++){vEdges[r]=[];for(let c=0;c<GRID-1;c++)vEdges[r][c]=Math.random()<.5?1:-1;}
}

/* ─────────────────────────────────────────────
   EDGE DRAWING — completely rewritten so that
   adjacent pieces share *exactly* the same cubic
   Bézier curve. The trick: always parameterise
   the curve from the cell with the smaller index
   and, when the neighbour needs the same edge,
   just traverse the same control points in
   reverse order.
   ───────────────────────────────────────────── */

/*  Draw one edge of a puzzle piece.
    (x0,y0)→(x1,y1) is the straight baseline.
    `dir`  = 0 → straight (border edge)
           = +1 → tab protrudes to the LEFT of the travel direction
           = -1 → tab protrudes to the RIGHT                       */
function drawPuzzleEdge(c, x0, y0, x1, y1, dir){
  if(!dir){ c.lineTo(x1,y1); return; }

  const dx = x1-x0, dy = y1-y0;
  const len = Math.sqrt(dx*dx + dy*dy);
  if(len < 0.001){ c.lineTo(x1,y1); return; }

  // unit tangent & unit normal (normal points LEFT of travel when dir=+1)
  const tx = dx/len, ty = dy/len;
  const nx = -ty * dir, ny = tx * dir;

  const tabH = len * TAB_SIZE;   // how far the tab sticks out
  const neckW = len * 0.08;      // half-width of the neck
  const headW = len * 0.12;      // extra half-width of the bulge

  // Key points along the baseline
  const neck0 = 0.35, neck1 = 0.65, mid = 0.5;

  // Neck entry / exit
  const n0x = x0 + dx*neck0, n0y = y0 + dy*neck0;
  const n1x = x0 + dx*neck1, n1y = y0 + dy*neck1;

  // Neck inward pinch
  const ni0x = n0x + nx*(-tabH*0.10), ni0y = n0y + ny*(-tabH*0.10);
  const ni1x = n1x + nx*(-tabH*0.10), ni1y = n1y + ny*(-tabH*0.10);

  // Bulge control points
  const bulgeOut = tabH * 1.05;
  const cp0x = n0x + nx*bulgeOut - tx*headW, cp0y = n0y + ny*bulgeOut - ty*headW;
  const cp1x = n1x + nx*bulgeOut + tx*headW, cp1y = n1y + ny*bulgeOut + ty*headW;

  // Tip
  const tipx = x0 + dx*mid + nx*tabH, tipy = y0 + dy*mid + ny*tabH;

  c.lineTo(n0x, n0y);
  c.lineTo(ni0x, ni0y);
  c.bezierCurveTo(cp0x, cp0y, tipx - tx*neckW, tipy - ty*neckW, tipx, tipy);
  c.bezierCurveTo(tipx + tx*neckW, tipy + ty*neckW, cp1x, cp1y, ni1x, ni1y);
  c.lineTo(n1x, n1y);
  c.lineTo(x1, y1);
}

function createPiecePath(c, row, col, px, py, cw, ch){
  c.beginPath();
  c.moveTo(px, py);
  // Top edge (left → right)
  const topDir = row > 0 ? hEdges[row-1][col] : 0;
  drawPuzzleEdge(c, px, py, px+cw, py, topDir);
  // Right edge (top → bottom)
  const rightDir = col < GRID-1 ? vEdges[row][col] : 0;
  drawPuzzleEdge(c, px+cw, py, px+cw, py+ch, rightDir);
  // Bottom edge (right → left)  — negate so the curve mirrors the top of the row below
  const bottomDir = row < GRID-1 ? -hEdges[row][col] : 0;
  drawPuzzleEdge(c, px+cw, py+ch, px, py+ch, bottomDir);
  // Left edge (bottom → top) — negate so it mirrors the right of the column to the left
  const leftDir = col > 0 ? -vEdges[row][col-1] : 0;
  drawPuzzleEdge(c, px, py+ch, px, py, leftDir);
  c.closePath();
}

/* ─── GAME INIT ─── */
function startGame(){
  document.getElementById('rules-overlay').classList.add('hidden');
  document.getElementById('rules-close-x').style.display='inline';
  document.getElementById('rules-start-btn').style.display='none';
  initAudio(); gameStarted=true;
  resizeCanvas(); initPuzzle(); render(); drawMiniPreview();
  startEncouragementLoop();
}
function showRulesPopup(){
  document.getElementById('rules-close-x').style.display='inline';
  document.getElementById('rules-start-btn').style.display='none';
  document.getElementById('rules-overlay').classList.remove('hidden');
}
function initPuzzle(){
  generateEdges();
  placedCount=0;hintsLeft=INITIAL_HINTS;selectedPieceId=null;combo=0;bestCombo=0;score=0;
  magnetGlow=null;shownMilestones=new Set();startTime=Date.now();
  totalDrops=0;totalMisses=0;hintsUsed=0;missStreak=0;
  placementOrder=new Array(TOTAL).fill(0);placementStep=0;fpsHistory=[];

  pieces=[];
  for(let r=0;r<GRID;r++)for(let c=0;c<GRID;c++)
    pieces.push({id:r*GRID+c,row:r,col:c,rotation:[0,90,180,270][Math.floor(Math.random()*4)],placed:false,x:0,y:0,inTray:true});
  for(let i=pieces.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[pieces[i],pieces[j]]=[pieces[j],pieces[i]];}

  updateUI(); buildTray(); startTimer();
  devLog('inf','Puzzle initialisé — 256 pièces 16×16');
}
function resetPuzzle(){document.getElementById('win-modal').classList.remove('active');initPuzzle();render();}

/* ─── TRAY ─── */
function buildTray(){
  const tray=document.getElementById('tray-scroll'); tray.innerHTML='';
  const thumbSize=48,padding=TAB_SIZE*thumbSize*1.2,totalSize=thumbSize+padding*2;
  pieces.filter(p=>p.inTray&&!p.placed).forEach(p=>{
    const cvs=document.createElement('canvas');
    cvs.width=totalSize;cvs.height=totalSize;cvs.className='tray-piece';
    drawPieceThumb(cvs,p,thumbSize,padding);
    cvs.addEventListener('mousedown',e=>startDragFromTray(e,p.id));
    cvs.addEventListener('contextmenu',e=>{e.preventDefault();showRotateMenu(e,p.id);});
    cvs.addEventListener('click',()=>selectPiece(p.id));
    tray.appendChild(cvs);
  });
}

/* ─── DRAWING ─── */
function drawPieceThumb(cvs,piece,size,pad){
  if(!img.complete)return;
  const t=cvs.getContext('2d');t.clearRect(0,0,cvs.width,cvs.height);
  const margin = TAB_SIZE * size * 1.2;

  // Shadow
  t.save();t.translate(cvs.width/2,cvs.height/2);t.rotate(piece.rotation*Math.PI/180);t.translate(-cvs.width/2,-cvs.height/2);
  t.translate(1.5,2);createPiecePath(t,piece.row,piece.col,pad,pad,size,size);t.fillStyle='rgba(40,10,50,0.2)';t.fill();t.restore();

  // Clipped image
  t.save();t.translate(cvs.width/2,cvs.height/2);t.rotate(piece.rotation*Math.PI/180);t.translate(-cvs.width/2,-cvs.height/2);
  createPiecePath(t,piece.row,piece.col,pad,pad,size,size);t.clip();
  const sx=piece.col*(img.width/GRID),sy=piece.row*(img.height/GRID),sw=img.width/GRID,sh=img.height/GRID;
  const sm=TAB_SIZE*Math.max(sw,sh)*1.2;
  t.drawImage(img, sx-sm, sy-sm, sw+sm*2, sh+sm*2,
                    pad-margin, pad-margin, size+margin*2, size+margin*2);
  // Bevel
  createPiecePath(t,piece.row,piece.col,pad,pad,size,size);
  const bv=t.createLinearGradient(pad,pad,pad+size,pad+size);
  bv.addColorStop(0,'rgba(255,255,255,0.2)');bv.addColorStop(.3,'rgba(255,255,255,0.04)');bv.addColorStop(.6,'transparent');bv.addColorStop(1,'rgba(40,10,50,0.12)');
  t.fillStyle=bv;t.fill();t.restore();

  // Stroke
  t.save();t.translate(cvs.width/2,cvs.height/2);t.rotate(piece.rotation*Math.PI/180);t.translate(-cvs.width/2,-cvs.height/2);
  createPiecePath(t,piece.row,piece.col,pad,pad,size,size);t.strokeStyle='rgba(60,20,50,0.18)';t.lineWidth=1.8;t.stroke();
  createPiecePath(t,piece.row,piece.col,pad,pad,size,size);t.strokeStyle=selectedPieceId===piece.id?'#E8679A':'rgba(255,255,255,0.12)';t.lineWidth=selectedPieceId===piece.id?2:.7;t.stroke();t.restore();
}

function drawPieceOnBoard(piece){
  const px = boardX + piece.col * cellW;
  const py = boardY + piece.row * cellH;
  const margin = TAB_SIZE * cellW * 1.2;

  // Shadow
  ctx.save();
  ctx.translate(1.5, 2);
  createPiecePath(ctx, piece.row, piece.col, px, py, cellW, cellH);
  ctx.fillStyle = 'rgba(50,20,60,0.12)';
  ctx.fill();
  ctx.restore();

  // Clipped image
  ctx.save();
  createPiecePath(ctx, piece.row, piece.col, px, py, cellW, cellH);
  ctx.clip();
  const sx = piece.col * (img.width / GRID);
  const sy = piece.row * (img.height / GRID);
  const sw = img.width / GRID;
  const sh = img.height / GRID;
  const sm = TAB_SIZE * Math.max(sw, sh) * 1.2;
  ctx.drawImage(img, sx - sm, sy - sm, sw + sm * 2, sh + sm * 2,
                     px - margin, py - margin, cellW + margin * 2, cellH + margin * 2);

  // Bevel overlay
  createPiecePath(ctx, piece.row, piece.col, px, py, cellW, cellH);
  const bevel = ctx.createLinearGradient(px, py, px + cellW, py + cellH);
  bevel.addColorStop(0, 'rgba(255,255,255,0.18)');
  bevel.addColorStop(.35, 'rgba(255,255,255,0.03)');
  bevel.addColorStop(.65, 'transparent');
  bevel.addColorStop(1, 'rgba(40,10,50,0.1)');
  ctx.fillStyle = bevel;
  ctx.fill();
  ctx.restore();

  // Subtle outline
  ctx.save();
  createPiecePath(ctx, piece.row, piece.col, px, py, cellW, cellH);
  ctx.strokeStyle = 'rgba(184,160,214,0.12)';
  ctx.lineWidth = 0.8;
  ctx.stroke();
  ctx.restore();
}

function drawPieceOnCanvas(piece){
  const px=piece.x, py=piece.y;
  const margin = TAB_SIZE * cellW * 1.2;
  const isDrag = dragging && dragging.id === piece.id;
  const isSel = selectedPieceId === piece.id;
  const lift = isDrag ? 1.04 : 1;
  const sDist = isDrag ? 6 : 3;

  // Shadow
  ctx.save();
  ctx.translate(px+cellW/2, py+cellH/2); ctx.scale(lift,lift); ctx.rotate(piece.rotation*Math.PI/180); ctx.translate(-(px+cellW/2),-(py+cellH/2));
  ctx.translate(sDist, sDist+1);
  createPiecePath(ctx, piece.row, piece.col, px, py, cellW, cellH);
  ctx.fillStyle = isDrag ? 'rgba(40,10,50,0.3)' : 'rgba(40,10,50,0.18)';
  ctx.filter = `blur(${isDrag?6:3}px)`;
  ctx.fill();
  ctx.filter = 'none';
  ctx.restore();

  // Inner shadow
  ctx.save();
  ctx.translate(px+cellW/2, py+cellH/2); ctx.scale(lift,lift); ctx.rotate(piece.rotation*Math.PI/180); ctx.translate(-(px+cellW/2),-(py+cellH/2));
  ctx.translate(1, 2);
  createPiecePath(ctx, piece.row, piece.col, px, py, cellW, cellH);
  ctx.fillStyle = 'rgba(80,30,60,0.25)';
  ctx.fill();
  ctx.restore();

  // Clipped image
  ctx.save();
  ctx.translate(px+cellW/2, py+cellH/2); ctx.scale(lift,lift); ctx.rotate(piece.rotation*Math.PI/180); ctx.translate(-(px+cellW/2),-(py+cellH/2));
  createPiecePath(ctx, piece.row, piece.col, px, py, cellW, cellH);
  ctx.clip();
  const sx = piece.col*(img.width/GRID), sy = piece.row*(img.height/GRID);
  const sw = img.width/GRID, sh = img.height/GRID;
  const sm = TAB_SIZE * Math.max(sw,sh) * 1.2;
  ctx.drawImage(img, sx-sm, sy-sm, sw+sm*2, sh+sm*2,
                     px-margin, py-margin, cellW+margin*2, cellH+margin*2);

  // Bevel + specular
  createPiecePath(ctx, piece.row, piece.col, px, py, cellW, cellH);
  const bevel = ctx.createLinearGradient(px-margin, py-margin, px+cellW+margin, py+cellH+margin);
  bevel.addColorStop(0,'rgba(255,255,255,0.22)'); bevel.addColorStop(.25,'rgba(255,255,255,0.06)');
  bevel.addColorStop(.55,'transparent'); bevel.addColorStop(.85,'rgba(40,10,50,0.08)'); bevel.addColorStop(1,'rgba(40,10,50,0.15)');
  ctx.fillStyle = bevel; ctx.fill();
  const spec = ctx.createRadialGradient(px+cellW*.25, py+cellH*.2, 0, px+cellW*.25, py+cellH*.2, cellW*.45);
  spec.addColorStop(0,'rgba(255,255,255,0.15)'); spec.addColorStop(.5,'rgba(255,255,255,0.03)'); spec.addColorStop(1,'transparent');
  ctx.fillStyle = spec; ctx.fill();
  ctx.restore();

  // Stroke
  ctx.save();
  ctx.translate(px+cellW/2, py+cellH/2); ctx.scale(lift,lift); ctx.rotate(piece.rotation*Math.PI/180); ctx.translate(-(px+cellW/2),-(py+cellH/2));
  createPiecePath(ctx, piece.row, piece.col, px, py, cellW, cellH);
  ctx.strokeStyle = 'rgba(60,20,50,0.2)'; ctx.lineWidth = 2; ctx.stroke();
  createPiecePath(ctx, piece.row, piece.col, px, py, cellW, cellH);
  ctx.strokeStyle = isSel ? '#E8679A' : 'rgba(255,255,255,0.15)';
  ctx.lineWidth = isSel ? 2 : .8;
  ctx.stroke();
  ctx.restore();
}

function drawMiniPreview(){
  if(!img.complete)return;
  const c=document.getElementById('mini-preview'),t=c.getContext('2d');
  c.width=c.clientWidth*2;c.height=c.clientWidth*2;t.drawImage(img,0,0,c.width,c.height);
}

/* ─── CANVAS ─── */
function resizeCanvas(){
  const p=document.getElementById('puzzle-panel');
  canvas.width=p.clientWidth;canvas.height=p.clientHeight;
  computeBoard();render();
}
function computeBoard(){
  const aW=canvas.width*.92,aH=canvas.height*.92;
  if(!img.complete)return;
  const asp=img.width/img.height;
  if(aW/aH>asp){boardH=aH;boardW=boardH*asp;}else{boardW=aW;boardH=boardW/asp;}
  boardX=(canvas.width-boardW)/2;boardY=(canvas.height-boardH)/2;
  cellW=boardW/GRID;cellH=boardH/GRID;
}

/* ─── RENDER LOOP ─── */
function render(){
  if(!img.complete||!gameStarted){requestAnimationFrame(render);return;}
  const now=performance.now(),frameDelta=now-lastFrameTime;lastFrameTime=now;frameCount++;
  if(now-lastFpsTick>500){
    fpsDisplayVal=Math.round(frameCount/((now-lastFpsTick)/1000));frameCount=0;lastFpsTick=now;
    fpsHistory.push(fpsDisplayVal);if(fpsHistory.length>60)fpsHistory.shift();
    if(devOpen)updateDevPanel(frameDelta);
  }
  ctx.clearRect(0,0,canvas.width,canvas.height);
  const br=8;

  // Board background & grid
  ctx.save();ctx.fillStyle='rgba(184,160,214,0.04)';ctx.beginPath();
  ctx.moveTo(boardX-4+br,boardY-4);ctx.lineTo(boardX+boardW+4-br,boardY-4);ctx.quadraticCurveTo(boardX+boardW+4,boardY-4,boardX+boardW+4,boardY-4+br);ctx.lineTo(boardX+boardW+4,boardY+boardH+4-br);ctx.quadraticCurveTo(boardX+boardW+4,boardY+boardH+4,boardX+boardW+4-br,boardY+boardH+4);ctx.lineTo(boardX-4+br,boardY+boardH+4);ctx.quadraticCurveTo(boardX-4,boardY+boardH+4,boardX-4,boardY+boardH+4-br);ctx.lineTo(boardX-4,boardY-4+br);ctx.quadraticCurveTo(boardX-4,boardY-4,boardX-4+br,boardY-4);ctx.fill();
  ctx.strokeStyle='rgba(184,160,214,0.06)';ctx.lineWidth=.5;
  for(let r=0;r<=GRID;r++){ctx.beginPath();ctx.moveTo(boardX,boardY+r*cellH);ctx.lineTo(boardX+boardW,boardY+r*cellH);ctx.stroke();}
  for(let c=0;c<=GRID;c++){ctx.beginPath();ctx.moveTo(boardX+c*cellW,boardY);ctx.lineTo(boardX+c*cellW,boardY+boardH);ctx.stroke();}
  ctx.strokeStyle='rgba(184,160,214,0.35)';ctx.lineWidth=2.5;ctx.beginPath();
  ctx.moveTo(boardX-2+br,boardY-2);ctx.lineTo(boardX+boardW+2-br,boardY-2);ctx.quadraticCurveTo(boardX+boardW+2,boardY-2,boardX+boardW+2,boardY-2+br);ctx.lineTo(boardX+boardW+2,boardY+boardH+2-br);ctx.quadraticCurveTo(boardX+boardW+2,boardY+boardH+2,boardX+boardW+2-br,boardY+boardH+2);ctx.lineTo(boardX-2+br,boardY+boardH+2);ctx.quadraticCurveTo(boardX-2,boardY+boardH+2,boardX-2,boardY+boardH+2-br);ctx.lineTo(boardX-2,boardY-2+br);ctx.quadraticCurveTo(boardX-2,boardY-2,boardX-2+br,boardY-2);ctx.stroke();ctx.restore();

  const floating=pieces.filter(p=>!p.inTray&&!p.placed);
  if(devOpen){document.getElementById('dev-drawcalls').textContent=pieces.filter(p=>p.placed).length+floating.length;document.getElementById('dev-canvaspx').textContent=canvas.width+'×'+canvas.height;}
  pieces.filter(p=>p.placed).forEach(p=>drawPieceOnBoard(p));
  floating.filter(p=>!dragging||dragging.id!==p.id).forEach(p=>drawPieceOnCanvas(p));
  if(dragging){const p=pieces.find(pp=>pp.id===dragging.id);if(p)drawPieceOnCanvas(p);}
  drawMagnetGlow();
  requestAnimationFrame(render);
}

/* ─── INTERACTION ─── */
function selectPiece(id){selectedPieceId=(selectedPieceId===id)?null:id;document.getElementById('btn-rotate-sel').disabled=(selectedPieceId===null);buildTray();render();}
function rotateSelected(){if(selectedPieceId===null)return;const p=pieces.find(pp=>pp.id===selectedPieceId);if(!p||p.placed)return;p.rotation=(p.rotation+90)%360;buildTray();render();}
function showRotateMenu(e,id){contextPieceId=id;const m=document.getElementById('rotate-menu');m.style.display='block';m.style.left=e.pageX+'px';m.style.top=e.pageY+'px';}
function rotateContextPiece(deg){if(contextPieceId===null)return;const p=pieces.find(pp=>pp.id===contextPieceId);if(!p||p.placed)return;p.rotation=(p.rotation+deg)%360;document.getElementById('rotate-menu').style.display='none';contextPieceId=null;buildTray();render();}
document.addEventListener('click',e=>{if(!e.target.closest('#rotate-menu')&&!e.target.closest('.tray-piece'))document.getElementById('rotate-menu').style.display='none';});

function startDragFromTray(e,id){
  if(e.button===2)return;e.preventDefault();
  const p=pieces.find(pp=>pp.id===id);if(!p||p.placed)return;
  selectedPieceId=id;document.getElementById('btn-rotate-sel').disabled=false;
  const rect=canvas.getBoundingClientRect();
  p.inTray=false;p.x=e.clientX-rect.left-cellW/2;p.y=e.clientY-rect.top-cellH/2;
  dragging={id};dragOffX=cellW/2;dragOffY=cellH/2;buildTray();render();
}
canvas.addEventListener('mousedown',e=>{
  if(e.button===2){const rect=canvas.getBoundingClientRect();const hit=hitTest(e.clientX-rect.left,e.clientY-rect.top);if(hit){e.preventDefault();showRotateMenu(e,hit.id);}return;}
  const rect=canvas.getBoundingClientRect(),mx=e.clientX-rect.left,my=e.clientY-rect.top;
  const hit=hitTest(mx,my);
  if(hit){selectedPieceId=hit.id;document.getElementById('btn-rotate-sel').disabled=false;dragging={id:hit.id};dragOffX=mx-hit.x;dragOffY=my-hit.y;}
  else{selectedPieceId=null;document.getElementById('btn-rotate-sel').disabled=true;}
  buildTray();render();
});
canvas.addEventListener('contextmenu',e=>e.preventDefault());
document.addEventListener('mousemove',e=>{
  if(!dragging)return;
  const rect=canvas.getBoundingClientRect(),p=pieces.find(pp=>pp.id===dragging.id);if(!p)return;
  p.x=e.clientX-rect.left-dragOffX;p.y=e.clientY-rect.top-dragOffY;
  updateMagnet(p);render();
});
document.addEventListener('mouseup',()=>{
  if(!dragging)return;
  const p=pieces.find(pp=>pp.id===dragging.id);
  if(p){totalDrops++;if(devOpen)document.getElementById('dev-drops').textContent=totalDrops;tryPlace(p);}
  dragging=null;magnetGlow=null;render();
});
function hitTest(mx,my){
  const c=pieces.filter(p=>!p.inTray&&!p.placed).reverse();
  for(const p of c){const m=TAB_SIZE*cellW*1.2;if(mx>=p.x-m&&mx<=p.x+cellW+m&&my>=p.y-m&&my<=p.y+cellH+m)return p;}
  return null;
}

/* ─── PLACEMENT ─── */
function tryPlace(piece){
  const tx=boardX+piece.col*cellW,ty=boardY+piece.row*cellH,snap=cellW*.4;
  const dx=piece.x-tx,dy=piece.y-ty;
  lastDropDist=Math.round(Math.sqrt(dx*dx+dy*dy));
  lastDropTests=pieces.filter(p=>!p.placed).length;
  if(devOpen){document.getElementById('dev-tests').textContent=lastDropTests;document.getElementById('dev-dist').textContent=lastDropDist+'px';document.getElementById('dev-snap').textContent=Math.round(snap)+'px';}

  if(piece.rotation!==0){
    if(Math.abs(piece.x-tx)<cellW*.6&&Math.abs(piece.y-ty)<cellH*.6){combo=0;totalMisses++;missStreak++;if(devOpen){document.getElementById('dev-miss').textContent=missStreak;document.getElementById('dev-accuracy').textContent=accuracy()+'%';}devLog('err',`Rotation ×${piece.rotation}° raté (${lastDropDist}px)`);updateUI();}
    return;
  }
  if(Math.abs(piece.x-tx)<snap&&Math.abs(piece.y-ty)<snap){
    piece.placed=true;piece.x=tx;piece.y=ty;piece.inTray=false;placedCount++;
    placementStep++;placementOrder[piece.row*GRID+piece.col]=placementStep;missStreak=0;
    playSfx('indice');combo++;if(combo>bestCombo)bestCombo=combo;
    const hg=combo>=3?2:1;hintsLeft+=hg;
    if(combo>=5)showToast(`🔥 COMBO ×${combo} ! +${hg} indices`,'streak');
    else if(combo>=3)showToast(`⚡ Combo ×${combo} ! +${hg} indices`,'combo');
    else showToast(`⭐ +${hg} indice`,'hint');
    if(selectedPieceId===piece.id){selectedPieceId=null;document.getElementById('btn-rotate-sel').disabled=true;}
    if(devOpen){document.getElementById('dev-miss').textContent=0;document.getElementById('dev-accuracy').textContent=accuracy()+'%';drawHeatmap();}
    devLog('ok',`[${piece.row},${piece.col}] ✓ ${lastDropDist}px combo×${combo}`);
    updateUI();buildTray();checkMilestones();
    if(placedCount===TOTAL)setTimeout(showWin,500);
  } else {
    if(piece.x>=boardX-cellW&&piece.x<=boardX+boardW&&piece.y>=boardY-cellH&&piece.y<=boardY+boardH){
      if(combo>0)showToast('Combo perdu !','combo');combo=0;totalMisses++;missStreak++;
      if(devOpen){document.getElementById('dev-miss').textContent=missStreak;document.getElementById('dev-accuracy').textContent=accuracy()+'%';}
      devLog('err',`Miss dist=${lastDropDist}px > seuil=${Math.round(snap)}px`);updateUI();
    }
    if(piece.x<boardX-cellW*2||piece.x>boardX+boardW+cellW||piece.y<boardY-cellH*2||piece.y>boardY+boardH+cellH){piece.inTray=true;buildTray();}
  }
}

/* ─── HINT ─── */
function useHint(){
  if(hintsLeft<=0)return;
  const u=pieces.filter(p=>!p.placed);if(!u.length)return;
  const p=u[Math.floor(Math.random()*u.length)];
  hintsLeft--;hintsUsed++;p.rotation=0;p.placed=true;p.inTray=false;
  p.x=boardX+p.col*cellW;p.y=boardY+p.row*cellH;
  placedCount++;placementStep++;placementOrder[p.row*GRID+p.col]=placementStep;
  playSfx('indice');
  if(devOpen){document.getElementById('dev-hints-used').textContent=hintsUsed;drawHeatmap();}
  if(selectedPieceId===p.id){selectedPieceId=null;document.getElementById('btn-rotate-sel').disabled=true;}
  const panel=document.getElementById('puzzle-panel');
  const m=document.createElement('div');m.className='hint-marker';
  m.style.left=(boardX+p.col*cellW-4)+'px';m.style.top=(boardY+p.row*cellH-4)+'px';
  m.style.width=(cellW+8)+'px';m.style.height=(cellH+8)+'px';
  panel.appendChild(m);setTimeout(()=>m.remove(),2200);
  showToast('💡 Pièce placée par indice !','hint');
  devLog('inf',`Hint → [${p.row},${p.col}]`);
  updateUI();buildTray();render();checkMilestones();
  if(placedCount===TOTAL)setTimeout(showWin,500);
}

/* ─── AUTO-FINISH ─── */
let autoFinishing=false;
function autoFinish(){
  if(autoFinishing)return;const u=pieces.filter(p=>!p.placed);if(!u.length)return;
  autoFinishing=true;document.getElementById('btn-finish').disabled=true;
  showToast('😴 On termine pour toi...','combo');
  let i=0;const iv=setInterval(()=>{
    const rem=pieces.filter(p=>!p.placed);if(!rem.length){clearInterval(iv);autoFinishing=false;return;}
    const p=rem[0];p.rotation=0;p.placed=true;p.inTray=false;
    p.x=boardX+p.col*cellW;p.y=boardY+p.row*cellH;
    placedCount++;placementStep++;placementOrder[p.row*GRID+p.col]=placementStep;
    if(i%4===0)playSfx('indice');i++;
    if(devOpen)drawHeatmap();updateUI();buildTray();render();
    if(placedCount===TOTAL){clearInterval(iv);autoFinishing=false;playSfx('indice');setTimeout(showWin,600);}
  },30);
}

/* ─── PREVIEW ─── */
function showPreview(){
  const o=document.getElementById('preview-overlay');
  document.getElementById('preview-img').src=`data:${IMG_MIME};base64,${IMG_DATA}`;
  o.style.display='flex';setTimeout(()=>{o.style.display='none';},3000);
}

/* ─── TIMER ─── */
function startTimer(){
  if(timerInterval)clearInterval(timerInterval);startTime=Date.now();
  timerInterval=setInterval(()=>{
    const e=Math.floor((Date.now()-startTime)/1000);
    const m=Math.floor(e/60).toString().padStart(2,'0'),s=(e%60).toString().padStart(2,'0');
    document.getElementById('timer').textContent=`${m}:${s}`;
  },1000);
}

/* ─── UI ─── */
function updateUI(){
  document.getElementById('placed-count').textContent=`${placedCount}/${TOTAL}`;
  document.getElementById('hint-count').textContent=`${hintsLeft}`;
  document.getElementById('combo-count').textContent=`×${combo}`;
  document.getElementById('best-combo').textContent=`×${bestCombo}`;
  document.getElementById('btn-hint').textContent=`⭐ Indice (${hintsLeft})`;
  document.getElementById('btn-hint').disabled=(hintsLeft<=0);
  document.getElementById('progress-bar').style.width=`${(placedCount/TOTAL)*100}%`;
}
function showToast(msg,type){
  const c=document.getElementById('toast-container'),el=document.createElement('div');
  el.className=`toast toast-${type}`;el.textContent=msg;c.appendChild(el);setTimeout(()=>el.remove(),2800);
}

/* ─── WIN ─── */
function showWin(){
  const e=Math.floor((Date.now()-startTime)/1000),m=Math.floor(e/60),s=e%60;
  score=Math.max(0,Math.round(placedCount*bestCombo-(e/10)));
  document.getElementById('win-text').textContent=`Temps : ${m}m ${s}s`;
  document.getElementById('win-score').textContent=`🏆 Score : ${score}`;
  document.getElementById('win-stats').textContent=`Meilleur combo : ×${bestCombo} | Indices : ${hintsLeft}`;
  document.getElementById('win-modal').classList.add('active');
  if(timerInterval)clearInterval(timerInterval);stopEncouragementLoop();
}

/* ─── MAGNET ─── */
function updateMagnet(piece){
  if(!piece||piece.placed||piece.rotation!==0){magnetGlow=null;if(devOpen){document.getElementById('dev-magnet').textContent='non';document.getElementById('dev-magnet').className='dev-metric-val';}return;}
  const tx=boardX+piece.col*cellW,ty=boardY+piece.row*cellH;
  const dx=piece.x-tx,dy=piece.y-ty,dist=Math.sqrt(dx*dx+dy*dy);
  const mr=cellW*1.8,sr=cellW*.4;
  if(dist<mr&&dist>sr){
    const strength=1-(dist-sr)/(mr-sr);
    magnetGlow={x:tx,y:ty,w:cellW,h:cellH,strength,row:piece.row,col:piece.col};
    piece.x-=dx*strength*.08;piece.y-=dy*strength*.08;
    if(devOpen){document.getElementById('dev-magnet').textContent=`oui (${Math.round(strength*100)}%)`;document.getElementById('dev-magnet').className='dev-metric-val good';}
    requestAnimationFrame(()=>{if(dragging)render();});
  }else if(dist<=sr){
    magnetGlow={x:tx,y:ty,w:cellW,h:cellH,strength:1,row:piece.row,col:piece.col};
    if(devOpen){document.getElementById('dev-magnet').textContent='snap!';document.getElementById('dev-magnet').className='dev-metric-val good';}
    requestAnimationFrame(()=>{if(dragging)render();});
  }else{
    magnetGlow=null;
    if(devOpen){document.getElementById('dev-magnet').textContent='non';document.getElementById('dev-magnet').className='dev-metric-val';}
  }
}
function drawMagnetGlow(){
  if(!magnetGlow)return;
  const{x,y,w,h,strength,row,col}=magnetGlow;
  const alpha=strength*.6,phase=(Date.now()%1200)/1200,pulse=.7+.3*Math.sin(phase*Math.PI*2);
  ctx.save();ctx.shadowColor=`rgba(232,103,154,${alpha*pulse*.6})`;ctx.shadowBlur=6+strength*8;
  createPiecePath(ctx,row,col,x,y,w,h);ctx.strokeStyle=`rgba(232,103,154,${alpha*pulse*.5})`;ctx.lineWidth=2+strength*2;ctx.stroke();
  createPiecePath(ctx,row,col,x,y,w,h);
  const g=ctx.createRadialGradient(x+w/2,y+h/2,0,x+w/2,y+h/2,w*.8);
  g.addColorStop(0,`rgba(245,176,203,${alpha*pulse*.15})`);g.addColorStop(.6,`rgba(232,103,154,${alpha*pulse*.06})`);g.addColorStop(1,'transparent');
  ctx.fillStyle=g;ctx.fill();
  if(strength>.4){const cnt=Math.floor(strength*6);for(let i=0;i<cnt;i++){const angle=(phase*Math.PI*2)+(i/cnt)*Math.PI*2,r=w*.55+Math.sin(angle*3+Date.now()/300)*4;const sx=x+w/2+Math.cos(angle)*r,sy=y+h/2+Math.sin(angle)*r,sz=1.5+Math.sin(Date.now()/200+i)*.8;ctx.beginPath();ctx.arc(sx,sy,sz,0,Math.PI*2);ctx.fillStyle=`rgba(255,255,255,${.3+strength*.4*pulse})`;ctx.fill();}}
  ctx.restore();
}

/* ─── ENCOURAGEMENT — FIXED ─── */
const ENC_GENERIC=["Tu gères trop bien ! 🌟","Continue comme ça ! 💪","Quelle patience ! 🧘","T'es un pro ! ✨","Magnifique ! 🌸","On y croit ! 🎀","Trop fort·e ! 💖","C'est beau ce que tu fais ! 🎨","Allez, courage ! 🌈","Tu peux le faire ! 🦋","Un puzzle à la fois ! 🍵","Zen et déterminé·e ! 🪷"];
const ENC_MILESTONES=[{threshold:20,text:"Ça prend forme ! 🧩"},{threshold:25,text:"Déjà 10% ! 🎯"},{threshold:64,text:"Le quart est fait ! 🥳"},{threshold:128,text:"À mi-chemin ! 🏃‍♀️💨"},{threshold:156,text:"Plus que 100 pièces ! 😱"},{threshold:200,text:"La fin approche ! 🔥"},{threshold:240,text:"Presque fini !! 🤩"},{threshold:250,text:"Les dernières pièces ! 💎"}];

function checkMilestones(){
  for(const ms of ENC_MILESTONES){
    if(placedCount>=ms.threshold&&!shownMilestones.has(ms.threshold)){
      shownMilestones.add(ms.threshold);showEncouragementBubble(ms.text);return;
    }
  }
}
function startEncouragementLoop(){stopEncouragementLoop();scheduleNextEncouragement();}
function stopEncouragementLoop(){if(encouragementTimer){clearTimeout(encouragementTimer);encouragementTimer=null;}}
function scheduleNextEncouragement(){
  const delay=(15+Math.random()*10)*1000;
  encouragementTimer=setTimeout(()=>{
    if(!gameStarted||placedCount>=TOTAL)return;
    showEncouragementBubble(ENC_GENERIC[Math.floor(Math.random()*ENC_GENERIC.length)]);
    scheduleNextEncouragement();
  },delay);
}
function showEncouragementBubble(text){
  const b=document.createElement('div');b.className='encouragement-bubble';b.textContent=text;
  const bx=boardX+Math.random()*boardW*.6+boardW*.2,by=boardY+Math.random()*boardH*.4+boardH*.1;
  b.style.left=bx+'px';b.style.top=by+'px';
  document.getElementById('puzzle-panel').appendChild(b);setTimeout(()=>b.remove(),3200);
}

/* ─── DEV PROFILER ─── */
function toggleDevPanel(){
  devOpen=!devOpen;
  document.getElementById('dev-panel').classList.toggle('open',devOpen);
  document.getElementById('bottom-tray').classList.toggle('dev-open',devOpen);
  document.getElementById('btn-dev').classList.toggle('active',devOpen);
  if(devOpen){drawHeatmap();drawSparkline();document.getElementById('dev-snap').textContent=Math.round(cellW*.4)+'px';document.getElementById('dev-canvaspx').textContent=canvas.width+'×'+canvas.height;}
}
function accuracy(){if(totalDrops===0)return 100;return Math.round((placedCount/(placedCount+totalMisses))*100);}
function updateDevPanel(frameDelta){
  if(!devOpen)return;
  const el=document.getElementById('dev-fps');el.textContent=fpsDisplayVal;el.className='dev-metric-val '+(fpsDisplayVal>=55?'good':fpsDisplayVal>=30?'warn':'bad');
  const ms=frameDelta.toFixed(1),msEl=document.getElementById('dev-framems');msEl.textContent=ms+'ms';msEl.className='dev-metric-val '+(frameDelta<=20?'good':frameDelta<=33?'warn':'bad');
  const elapsed=Math.floor((Date.now()-startTime)/1000)||1;
  document.getElementById('dev-elapsed').textContent=elapsed+'s';
  document.getElementById('dev-ppm').textContent=((placedCount/elapsed)*60).toFixed(1);
  document.getElementById('dev-accuracy').textContent=accuracy()+'%';
  drawSparkline();
}
function drawSparkline(){
  const c=document.getElementById('dev-sparkline'),t=c.getContext('2d');
  c.width=c.offsetWidth||160;c.height=40;t.clearRect(0,0,c.width,c.height);
  if(fpsHistory.length<2)return;
  t.strokeStyle='rgba(123,94,167,0.15)';t.lineWidth=.5;
  [60,30].forEach(y=>{const py=c.height-(y/70)*c.height;t.beginPath();t.moveTo(0,py);t.lineTo(c.width,py);t.stroke();t.fillStyle='rgba(107,80,128,0.5)';t.font='7px JetBrains Mono';t.fillText(y,2,py-1);});
  const step=c.width/(fpsHistory.length-1);t.beginPath();
  fpsHistory.forEach((v,i)=>{const x=i*step,y=c.height-(Math.min(v,70)/70)*c.height;i===0?t.moveTo(x,y):t.lineTo(x,y);});
  t.strokeStyle='#22D3EE';t.lineWidth=1.5;t.stroke();
  t.lineTo(c.width,c.height);t.lineTo(0,c.height);t.closePath();
  const g=t.createLinearGradient(0,0,0,c.height);g.addColorStop(0,'rgba(34,211,238,0.2)');g.addColorStop(1,'transparent');t.fillStyle=g;t.fill();
}
function drawHeatmap(){
  const c=document.getElementById('dev-heatmap'),t=c.getContext('2d');
  c.width=GRID*8;c.height=GRID*8;const max=placementStep||1;
  for(let r=0;r<GRID;r++)for(let col=0;col<GRID;col++){
    const order=placementOrder[r*GRID+col];
    if(order===0){t.fillStyle='rgba(26,10,46,0.8)';}
    else{
      const ratio=order/max;
      let fr,fg,fb;
      if(ratio<.5){const rr=ratio*2;fr=Math.round(26+(123-26)*rr);fg=Math.round(10+(94-10)*rr);fb=Math.round(46+(167-46)*rr);}
      else{const rr=(ratio-.5)*2;fr=Math.round(123+(232-123)*rr);fg=Math.round(94+(103-94)*rr);fb=Math.round(167+(154-167)*rr);}
      t.fillStyle=`rgb(${fr},${fg},${fb})`;
    }
    t.fillRect(col*8,r*8,8,8);
  }
  t.strokeStyle='rgba(0,0,0,0.2)';t.lineWidth=.5;
  for(let i=0;i<=GRID;i++){t.beginPath();t.moveTo(i*8,0);t.lineTo(i*8,c.height);t.stroke();t.beginPath();t.moveTo(0,i*8);t.lineTo(c.width,i*8);t.stroke();}
}
function devLog(type,msg){
  if(!devOpen)return;
  const el=document.getElementById('dev-algo-log'),now=new Date();
  const ts=`${now.getMinutes().toString().padStart(2,'0')}:${now.getSeconds().toString().padStart(2,'0')}.${Math.floor(now.getMilliseconds()/10).toString().padStart(2,'0')}`;
  const e=document.createElement('div');e.className='log-entry';
  e.innerHTML=`<span class="log-ts">${ts}</span> <span class="log-${type}">${msg}</span>`;
  el.appendChild(e);while(el.children.length>40)el.removeChild(el.firstChild);el.scrollTop=el.scrollHeight;
}
function exportSession(){
  const elapsed=Math.floor((Date.now()-startTime)/1000);
  const data={
    meta:{game:'Nikoussia Puzzle',version:'2.0',exportedAt:new Date().toISOString()},
    config:{grid:GRID,totalPieces:TOTAL,snapThresholdPx:Math.round(cellW*.4),magnetRangePx:Math.round(cellW*1.8)},
    session:{elapsedSeconds:elapsed,placedCount,totalDrops,totalMisses,hintsUsed,accuracy:accuracy()+'%',bestCombo,finalScore:Math.max(0,Math.round(placedCount*bestCombo-(elapsed/10))),piecesPerMinute:parseFloat(((placedCount/(elapsed||1))*60).toFixed(2)),fpsAvg:fpsHistory.length>0?Math.round(fpsHistory.reduce((a,b)=>a+b,0)/fpsHistory.length):0,fpsMin:fpsHistory.length>0?Math.min(...fpsHistory):0},
    heatmap:{description:'Placement order per cell (0=not placed)',grid:GRID,data:Array.from({length:GRID},(_,r)=>Array.from({length:GRID},(_,c)=>placementOrder[r*GRID+c]))},
    renderInfo:{canvasWidth:canvas.width,canvasHeight:canvas.height,boardW:Math.round(boardW),boardH:Math.round(boardH),cellW:Math.round(cellW),cellH:Math.round(cellH)}
  };
  const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  const url=URL.createObjectURL(blob),a=document.createElement('a');
  a.href=url;a.download=`nikoussia_session_${Date.now()}.json`;a.click();URL.revokeObjectURL(url);
  devLog('inf','Session exportée ↓');
}

/* ─── KEYBOARD ─── */
document.addEventListener('keydown',e=>{
  if(e.key==='r'||e.key==='R')rotateSelected();
  if(e.key==='F2'||e.key==='`')toggleDevPanel();
});

/* ─── START ─── */
img.onload=()=>{drawMiniPreview();};
window.addEventListener('resize',()=>{
  if(!gameStarted)return;resizeCanvas();buildTray();
  pieces.filter(p=>p.placed).forEach(p=>{p.x=boardX+p.col*cellW;p.y=boardY+p.row*cellH;});
  render();drawMiniPreview();if(devOpen)drawHeatmap();
});
</script>
</body>
</html>
"""

html_code = html_code.replace("IMG_DATA_PLACEHOLDER",  img_data)
html_code = html_code.replace("IMG_MIME_PLACEHOLDER",   img_mime)
html_code = html_code.replace("BG_GIF_PLACEHOLDER",     bg_gif_b64)
html_code = html_code.replace("SND_BGM_PLACEHOLDER",    audio_bgm)
html_code = html_code.replace("SND_CLICK_PLACEHOLDER",  audio_click)
html_code = html_code.replace("SND_HOVER_PLACEHOLDER",  audio_hover)
html_code = html_code.replace("SND_INDICE_PLACEHOLDER", audio_indice)

import streamlit.components.v1 as components
components.html(html_code, height=920, scrolling=False)