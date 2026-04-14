"""
Meme image generator — downloads template images, caches them, and
renders meme text using PIL with classic Impact-style white-with-black-outline.
"""

import os
import io
import hashlib
import textwrap
from typing import List, Tuple, Optional

import requests
from PIL import Image, ImageDraw, ImageFont

from .jokes import TEMPLATES

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "cache")
FONT_DIR  = os.path.join(os.path.dirname(__file__), "..", "fonts")
TARGET_W  = 800   # all memes normalised to this width

# ── Font loading ──────────────────────────────────────────────────────────────

def _download_anton(path: str):
    """Download Anton (Impact-like Google Font) if available."""
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
    """Return the best available meme font at the given point size."""
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

    # Download Anton as fallback
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
    """Return the template PIL Image, downloading and caching as needed."""
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
        # Normalise width
        w, h = img.size
        if w != TARGET_W:
            img = img.resize((TARGET_W, int(h * TARGET_W / w)), Image.LANCZOS)
        return img
    except Exception as e:
        print(f"[generator] Failed to open {path}: {e}")
        return None


# ── Text rendering helpers ────────────────────────────────────────────────────

def _word_wrap(text: str, font: ImageFont.ImageFont,
               draw: ImageDraw.ImageDraw, max_w: int) -> List[str]:
    """Wrap text so no line exceeds max_w pixels."""
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
                lines.append(word)  # word alone is too wide — live with it

    if cur:
        lines.append(" ".join(cur))
    return lines or [""]


def _fit_text(text: str, draw: ImageDraw.ImageDraw,
              zone_w: int, zone_h: int,
              max_size: int = 72, min_size: int = 14
              ) -> Tuple[ImageFont.ImageFont, List[str]]:
    """Find the largest font size at which text fits in the given zone."""
    for size in range(max_size, min_size - 1, -2):
        font  = get_font(size)
        lines = _word_wrap(text, font, draw, zone_w - 10)
        line_h = draw.textbbox((0, 0), "Ag", font=font)[3]
        total_h = line_h * len(lines) + 4 * (len(lines) - 1)
        if total_h <= zone_h:
            return font, lines
    return get_font(min_size), lines


def _draw_text_outlined(draw: ImageDraw.ImageDraw, xy: Tuple[int, int],
                        text: str, font: ImageFont.ImageFont,
                        fill: str = "white", outline: str = "black",
                        outline_w: int = 3):
    """Draw text with a solid outline (classic meme style)."""
    x, y = xy
    for dx in range(-outline_w, outline_w + 1):
        for dy in range(-outline_w, outline_w + 1):
            if dx or dy:
                draw.text((x + dx, y + dy), text, font=font, fill=outline)
    draw.text((x, y), text, font=font, fill=fill)


def _render_zone(draw: ImageDraw.ImageDraw, text: str,
                 zone: Tuple[int, int, int, int],
                 valign: str = "center",
                 fill: str = "white", outline: str = "black",
                 max_font: int = 72):
    """
    Render impact-style text inside a zone (x, y, w, h).
    valign: 'top' | 'center' | 'bottom'
    """
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
    else:  # center
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

def _render_top_bottom(img: Image.Image, texts: List[str]) -> Image.Image:
    out  = img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    margin = int(h * 0.04)
    band   = int(h * 0.20)

    if len(texts) > 0 and texts[0].strip():
        _render_zone(draw, texts[0], (0, margin, w, band), valign="top")
    if len(texts) > 1 and texts[1].strip():
        _render_zone(draw, texts[1], (0, h - band - margin, w, band), valign="bottom")
    return out


def _render_bottom_only(img: Image.Image, texts: List[str]) -> Image.Image:
    out  = img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    if texts and texts[0].strip():
        _render_zone(draw, texts[0], (0, h - int(h * 0.20), w, int(h * 0.18)),
                     valign="bottom")
    return out


def _render_drake(img: Image.Image, texts: List[str]) -> Image.Image:
    """Text in the right 44% of each horizontal half."""
    out  = img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    half   = h // 2
    left_x = int(w * 0.56)
    zone_w = w - left_x - 10
    zone_h = int(half * 0.80)

    if len(texts) > 0 and texts[0].strip():
        _render_zone(draw, texts[0],
                     (left_x, (half - zone_h) // 2, zone_w, zone_h),
                     valign="center")
    if len(texts) > 1 and texts[1].strip():
        _render_zone(draw, texts[1],
                     (left_x, half + (half - zone_h) // 2, zone_w, zone_h),
                     valign="center")
    return out


def _render_two_button(img: Image.Image, texts: List[str]) -> Image.Image:
    """Labels on left and right buttons (upper area)."""
    out  = img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    zone_h = int(h * 0.28)
    zone_w = int(w * 0.36)
    margin = int(w * 0.06)

    if len(texts) > 0 and texts[0].strip():
        _render_zone(draw, texts[0],
                     (margin, int(h * 0.05), zone_w, zone_h),
                     valign="center", max_font=52)
    if len(texts) > 1 and texts[1].strip():
        _render_zone(draw, texts[1],
                     (w - zone_w - margin, int(h * 0.05), zone_w, zone_h),
                     valign="center", max_font=52)
    return out


def _render_four_panel(img: Image.Image, texts: List[str]) -> Image.Image:
    """Text in the RIGHT half of each of 4 horizontal panels."""
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
            _render_zone(draw, text,
                         (left_x, zy, zone_w, zh),
                         valign="center", max_font=44)
    return out


def _render_sign(img: Image.Image, texts: List[str]) -> Image.Image:
    """Text on the sign/whiteboard area (Change My Mind template)."""
    out  = img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    if texts and texts[0].strip():
        # Sign is roughly in the lower-left quadrant
        zx = int(w * 0.04)
        zy = int(h * 0.50)
        zw = int(w * 0.52)
        zh = int(h * 0.30)
        _render_zone(draw, texts[0], (zx, zy, zw, zh),
                     valign="center", fill="black", outline="white", max_font=36)
    return out


def _render_handshake(img: Image.Image, texts: List[str]) -> Image.Image:
    """Labels on left arm, right arm, and center handshake."""
    out  = img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    arm_w  = int(w * 0.32)
    arm_h  = int(h * 0.30)
    arm_y  = int(h * 0.08)

    if len(texts) > 0 and texts[0].strip():
        _render_zone(draw, texts[0], (int(w * 0.02), arm_y, arm_w, arm_h),
                     valign="center", max_font=40)
    if len(texts) > 1 and texts[1].strip():
        _render_zone(draw, texts[1], (w - arm_w - int(w * 0.02), arm_y, arm_w, arm_h),
                     valign="center", max_font=40)
    if len(texts) > 2 and texts[2].strip():
        center_y = int(h * 0.45)
        center_h = int(h * 0.28)
        _render_zone(draw, texts[2],
                     (int(w * 0.18), center_y, int(w * 0.64), center_h),
                     valign="center", max_font=48)
    return out


# ── Public API ────────────────────────────────────────────────────────────────

RENDER_FNS = {
    "top_bottom":   _render_top_bottom,
    "bottom_only":  _render_bottom_only,
    "drake":        _render_drake,
    "two_button":   _render_two_button,
    "four_panel":   _render_four_panel,
    "sign":         _render_sign,
    "handshake":    _render_handshake,
}


def generate_meme(template_key: str, texts: List[str]) -> Optional[bytes]:
    """
    Generate a meme PNG and return it as raw bytes, or None on failure.

    Args:
        template_key: key from TEMPLATES dict
        texts: list of text strings, one per template zone

    Returns:
        PNG bytes or None
    """
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
