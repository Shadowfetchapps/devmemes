"""
Meme image generator — downloads template images, caches them, and
renders meme text using PIL with classic Impact-style white-with-black-outline.

Also fetches Imgflip's top-100 template catalog for the Browse panel.
"""

import os
import io
import json
import time
import hashlib
from typing import List, Tuple, Optional

import requests
from PIL import Image, ImageDraw, ImageFont

from .jokes import TEMPLATES

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "cache")
FONT_DIR  = os.path.join(os.path.dirname(__file__), "..", "fonts")
TARGET_W  = 800   # normalised output width

# ── Font loading ──────────────────────────────────────────────────────────────

def _download_anton(path: str):
    try:
        url = "https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf"
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as f:
                f.write(r.content)
    except Exception:
        pass


def get_font(size: int) -> ImageFont.ImageFont:
    paths = [
        "/System/Library/Fonts/Supplemental/Impact.ttf",
        "/Library/Fonts/Impact.ttf",
        os.path.expanduser("~/Library/Fonts/Impact.ttf"),
        "/System/Library/Fonts/Impact.ttf",
        os.path.join(FONT_DIR, "Anton-Regular.ttf"),
    ]
    for p in paths:
        if os.path.isfile(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    anton = os.path.join(FONT_DIR, "Anton-Regular.ttf")
    if not os.path.isfile(anton):
        _download_anton(anton)
    if os.path.isfile(anton):
        try:
            return ImageFont.truetype(anton, size)
        except Exception:
            pass
    return ImageFont.load_default()


# ── Template image downloading / caching ─────────────────────────────────────

def get_template_image(url: str) -> Optional[Image.Image]:
    os.makedirs(CACHE_DIR, exist_ok=True)
    slug = hashlib.md5(url.encode()).hexdigest()[:12]
    ext  = os.path.splitext(url.split("?")[0])[1] or ".jpg"
    path = os.path.join(CACHE_DIR, f"{slug}{ext}")

    if not os.path.isfile(path):
        try:
            r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            with open(path, "wb") as f:
                f.write(r.content)
        except Exception as e:
            print(f"[generator] Failed to download {url}: {e}")
            return None

    try:
        img = Image.open(path).convert("RGBA")
        w, h = img.size
        if w != TARGET_W:
            img = img.resize((TARGET_W, int(h * TARGET_W / w)), Image.LANCZOS)
        return img
    except Exception as e:
        print(f"[generator] Failed to open {path}: {e}")
        return None


def get_template_thumbnail(url: str, size: int = 120) -> Optional[bytes]:
    """Download, crop to square, return JPEG bytes for the Browse panel."""
    img = get_template_image(url)
    if img is None:
        return None
    w, h = img.size
    sq   = min(w, h)
    left = (w - sq) // 2
    top  = (h - sq) // 2
    thumb = img.crop((left, top, left + sq, top + sq))
    thumb = thumb.resize((size, size), Image.LANCZOS)
    buf   = io.BytesIO()
    thumb.convert("RGB").save(buf, format="JPEG", quality=85)
    return buf.getvalue()


# ── Imgflip template catalog ──────────────────────────────────────────────────

_IMGFLIP_CACHE_FILE = os.path.join(CACHE_DIR, "imgflip_catalog.json")
_IMGFLIP_CACHE_TTL  = 86_400  # 24 hours


def fetch_imgflip_templates() -> List[dict]:
    """
    Return Imgflip's top-100 meme templates.
    Caches results for 24 hours. Returns [] on failure.
    Each entry: {id, name, url, width, height, box_count}
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    if os.path.isfile(_IMGFLIP_CACHE_FILE):
        if time.time() - os.path.getmtime(_IMGFLIP_CACHE_FILE) < _IMGFLIP_CACHE_TTL:
            try:
                with open(_IMGFLIP_CACHE_FILE) as f:
                    return json.load(f)
            except Exception:
                pass
    try:
        r = requests.get("https://api.imgflip.com/get_memes", timeout=15)
        data = r.json()
        if data.get("success"):
            memes = data["data"]["memes"]
            with open(_IMGFLIP_CACHE_FILE, "w") as f:
                json.dump(memes, f)
            return memes
    except Exception as e:
        print(f"[generator] Imgflip catalog fetch failed: {e}")
    return []


# ── Text rendering helpers ────────────────────────────────────────────────────

def _word_wrap(text: str, font: ImageFont.ImageFont,
               draw: ImageDraw.ImageDraw, max_w: int) -> List[str]:
    words  = text.split()
    lines: List[str] = []
    cur:   List[str] = []
    for word in words:
        test = " ".join(cur + [word])
        bb   = draw.textbbox((0, 0), test, font=font)
        if bb[2] - bb[0] <= max_w:
            cur.append(word)
        else:
            if cur:
                lines.append(" ".join(cur))
                cur = [word]
            else:
                lines.append(word)
    if cur:
        lines.append(" ".join(cur))
    return lines or [""]


def _fit_text(text: str, draw: ImageDraw.ImageDraw,
              zone_w: int, zone_h: int,
              max_size: int = 72, min_size: int = 14):
    for size in range(max_size, min_size - 1, -2):
        font  = get_font(size)
        lines = _word_wrap(text, font, draw, zone_w - 10)
        line_h = draw.textbbox((0, 0), "Ag", font=font)[3]
        total_h = line_h * len(lines) + 4 * (len(lines) - 1)
        if total_h <= zone_h:
            return font, lines
    return get_font(min_size), lines


def _draw_text_outlined(draw, xy, text, font,
                        fill="white", outline="black", outline_w=3):
    x, y = xy
    for dx in range(-outline_w, outline_w + 1):
        for dy in range(-outline_w, outline_w + 1):
            if dx or dy:
                draw.text((x + dx, y + dy), text, font=font, fill=outline)
    draw.text((x, y), text, font=font, fill=fill)


def _render_zone(draw, text: str, zone: Tuple[int, int, int, int],
                 valign: str = "center",
                 fill: str = "white", outline: str = "black",
                 max_font: int = 72):
    if not text.strip():
        return
    text = text.upper()
    zx, zy, zw, zh = zone

    font, lines = _fit_text(text, draw, zw, zh, max_size=max_font)
    line_h  = draw.textbbox((0, 0), "Ag", font=font)[3]
    spacing = max(3, line_h // 6)
    total_h = line_h * len(lines) + spacing * (len(lines) - 1)

    if valign == "top":
        y0 = zy + 6
    elif valign == "bottom":
        y0 = zy + zh - total_h - 6
    else:
        y0 = zy + (zh - total_h) // 2

    outline_w = max(2, line_h // 10)
    for i, line in enumerate(lines):
        bb  = draw.textbbox((0, 0), line, font=font)
        lw  = bb[2] - bb[0]
        x   = zx + (zw - lw) // 2
        y   = y0 + i * (line_h + spacing)
        _draw_text_outlined(draw, (x, y), line, font,
                            fill=fill, outline=outline, outline_w=outline_w)


# ── Per-render-type composers ─────────────────────────────────────────────────

def _render_top_bottom(img, texts):
    out  = img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    band = int(h * 0.20)
    margin = int(h * 0.04)
    if len(texts) > 0 and texts[0].strip():
        _render_zone(draw, texts[0], (0, margin, w, band), valign="top")
    if len(texts) > 1 and texts[1].strip():
        _render_zone(draw, texts[1], (0, h - band - margin, w, band), valign="bottom")
    return out


def _render_bottom_only(img, texts):
    out  = img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    if texts and texts[0].strip():
        _render_zone(draw, texts[0], (0, h - int(h * 0.20), w, int(h * 0.18)),
                     valign="bottom")
    return out


def _render_drake(img, texts):
    out  = img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    half   = h // 2
    left_x = int(w * 0.56)
    zone_w = w - left_x - 10
    zone_h = int(half * 0.80)
    if len(texts) > 0 and texts[0].strip():
        _render_zone(draw, texts[0], (left_x, (half - zone_h) // 2, zone_w, zone_h))
    if len(texts) > 1 and texts[1].strip():
        _render_zone(draw, texts[1], (left_x, half + (half - zone_h) // 2, zone_w, zone_h))
    return out


def _render_two_button(img, texts):
    out  = img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    zone_h = int(h * 0.28)
    zone_w = int(w * 0.36)
    margin = int(w * 0.06)
    if len(texts) > 0 and texts[0].strip():
        _render_zone(draw, texts[0], (margin, int(h * 0.05), zone_w, zone_h),
                     max_font=52)
    if len(texts) > 1 and texts[1].strip():
        _render_zone(draw, texts[1], (w - zone_w - margin, int(h * 0.05), zone_w, zone_h),
                     max_font=52)
    return out


def _render_four_panel(img, texts):
    out  = img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    panel_h = h // 4
    left_x  = w // 2 + 10
    zone_w  = w // 2 - 20
    for i, text in enumerate(texts[:4]):
        if text.strip():
            zy = i * panel_h + int(panel_h * 0.08)
            zh = int(panel_h * 0.84)
            _render_zone(draw, text, (left_x, zy, zone_w, zh), max_font=44)
    return out


def _render_sign(img, texts):
    out  = img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    if texts and texts[0].strip():
        _render_zone(draw, texts[0],
                     (int(w * 0.04), int(h * 0.50), int(w * 0.52), int(h * 0.30)),
                     fill="black", outline="white", max_font=36)
    return out


def _render_handshake(img, texts):
    out  = img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    arm_w = int(w * 0.32)
    arm_h = int(h * 0.30)
    arm_y = int(h * 0.08)
    if len(texts) > 0 and texts[0].strip():
        _render_zone(draw, texts[0], (int(w * 0.02), arm_y, arm_w, arm_h), max_font=40)
    if len(texts) > 1 and texts[1].strip():
        _render_zone(draw, texts[1], (w - arm_w - int(w * 0.02), arm_y, arm_w, arm_h),
                     max_font=40)
    if len(texts) > 2 and texts[2].strip():
        _render_zone(draw, texts[2],
                     (int(w * 0.18), int(h * 0.45), int(w * 0.64), int(h * 0.28)),
                     max_font=48)
    return out


def _render_side_by_side(img, texts):
    """Two panels left/right — Woman Yelling at Cat, Tuxedo Pooh, etc."""
    out  = img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    mid  = w // 2
    if len(texts) > 0 and texts[0].strip():
        _render_zone(draw, texts[0], (4, 0, mid - 8, h), max_font=52)
    if len(texts) > 1 and texts[1].strip():
        _render_zone(draw, texts[1], (mid + 4, 0, mid - 8, h), max_font=52)
    return out


def _render_three_vertical(img, texts):
    """Three horizontal bands — Panik Kalm Panik."""
    out  = img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    band_h = h // 3
    # Use right 55% to avoid covering faces/icons on the left
    for i, text in enumerate(texts[:3]):
        if text.strip():
            zy = i * band_h + int(band_h * 0.08)
            zh = int(band_h * 0.84)
            _render_zone(draw, text,
                         (int(w * 0.45), zy, int(w * 0.52), zh),
                         max_font=46)
    return out


def _render_distracted_bf(img, texts):
    """
    Distracted Boyfriend — three labels in specific areas.
    texts[0] = shiny new thing (walking left)
    texts[1] = boyfriend / dev (center)
    texts[2] = current project / girlfriend (right)
    """
    out  = img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    if len(texts) > 0 and texts[0].strip():
        _render_zone(draw, texts[0],
                     (int(w * 0.02), int(h * 0.32), int(w * 0.28), int(h * 0.32)),
                     max_font=38)
    if len(texts) > 1 and texts[1].strip():
        _render_zone(draw, texts[1],
                     (int(w * 0.33), int(h * 0.55), int(w * 0.32), int(h * 0.26)),
                     max_font=38)
    if len(texts) > 2 and texts[2].strip():
        _render_zone(draw, texts[2],
                     (int(w * 0.66), int(h * 0.28), int(w * 0.30), int(h * 0.30)),
                     max_font=38)
    return out


def _render_three_labels(img, texts):
    """Left Exit / similar 3-label templates."""
    out  = img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    # Car (center-left)
    if len(texts) > 0 and texts[0].strip():
        _render_zone(draw, texts[0],
                     (int(w * 0.20), int(h * 0.36), int(w * 0.34), int(h * 0.24)),
                     max_font=38)
    # Straight road (upper right)
    if len(texts) > 1 and texts[1].strip():
        _render_zone(draw, texts[1],
                     (int(w * 0.56), int(h * 0.05), int(w * 0.40), int(h * 0.28)),
                     max_font=38)
    # Off-ramp exit (lower left)
    if len(texts) > 2 and texts[2].strip():
        _render_zone(draw, texts[2],
                     (int(w * 0.04), int(h * 0.62), int(w * 0.36), int(h * 0.26)),
                     max_font=38)
    return out


def _render_generic(img, texts, box_count=2):
    """
    Fallback renderer for unknown Imgflip templates.
    Uses top_bottom for 2 zones, bottom_only for 1, four_panel for 4+.
    """
    if box_count == 1:
        return _render_bottom_only(img, texts)
    if box_count >= 4:
        return _render_four_panel(img, texts)
    return _render_top_bottom(img, texts)


# ── Render dispatch ───────────────────────────────────────────────────────────

RENDER_FNS = {
    "top_bottom":    _render_top_bottom,
    "bottom_only":   _render_bottom_only,
    "drake":         _render_drake,
    "two_button":    _render_two_button,
    "four_panel":    _render_four_panel,
    "sign":          _render_sign,
    "handshake":     _render_handshake,
    "side_by_side":  _render_side_by_side,
    "three_vertical": _render_three_vertical,
    "distracted_bf": _render_distracted_bf,
    "three_labels":  _render_three_labels,
}


# ── Public API ────────────────────────────────────────────────────────────────

def generate_meme(template_key: str, texts: List[str],
                  imgflip_url: str = "", box_count: int = 2) -> Optional[bytes]:
    """
    Generate a meme PNG and return it as raw bytes, or None on failure.

    For hardcoded templates pass template_key.
    For Imgflip browser templates, pass template_key='_imgflip',
    imgflip_url=<url>, box_count=<n>.
    """
    if template_key == "_imgflip":
        img = get_template_image(imgflip_url)
        if img is None:
            return None
        result = _render_generic(img, texts, box_count)
    else:
        tmpl = TEMPLATES.get(template_key)
        if not tmpl:
            return None
        img = get_template_image(tmpl["url"])
        if img is None:
            return None
        render_fn = RENDER_FNS.get(tmpl["render"], _render_top_bottom)
        result    = render_fn(img, texts)

    buf = io.BytesIO()
    result.convert("RGB").save(buf, format="PNG")
    return buf.getvalue()
