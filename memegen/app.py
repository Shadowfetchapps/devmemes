import os
import sys
import random

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QComboBox,
    QFileDialog, QFrame, QSplitter, QSizePolicy,
    QScrollArea, QTabWidget, QLineEdit, QGridLayout,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QByteArray, pyqtSlot, QTimer
from PyQt6.QtGui import QPixmap, QImage, QFont

from .jokes import TEMPLATES, CATEGORIES, MEMES
from .generator import generate_meme, fetch_imgflip_templates, get_template_thumbnail

# ── Palette ────────────────────────────────────────────────────────────────────
BG_DEEP  = "#0f1117"
BG_CARD  = "#1a1d27"
BG_INPUT = "#22253a"
ACCENT   = "#6e84f7"
ACCENT2  = "#f76e8a"
TEXT_PRI = "#e8eaf6"
TEXT_SEC = "#8890b5"
SUCCESS  = "#4caf82"
WARNING  = "#f5a623"
DANGER   = "#e57373"

OUTPUT_DIR = os.path.expanduser("~/Downloads/DevMemes")

# ── Known template URLs for badge detection ───────────────────────────────────
_OUR_URLS = {t["url"] for t in TEMPLATES.values()}


# ── Background workers ────────────────────────────────────────────────────────

class MemeWorker(QThread):
    done   = pyqtSignal(bytes)
    failed = pyqtSignal(str)

    def __init__(self, template_key, texts, imgflip_url="", box_count=2):
        super().__init__()
        self.template_key = template_key
        self.texts        = texts
        self.imgflip_url  = imgflip_url
        self.box_count    = box_count

    def run(self):
        try:
            data = generate_meme(self.template_key, self.texts,
                                  self.imgflip_url, self.box_count)
            if data:
                self.done.emit(data)
            else:
                self.failed.emit("Failed to generate — check your internet connection.")
        except Exception as e:
            self.failed.emit(str(e))


class CatalogWorker(QThread):
    """Fetches the Imgflip catalog in the background."""
    ready = pyqtSignal(list)

    def run(self):
        self.ready.emit(fetch_imgflip_templates())


class ThumbnailWorker(QThread):
    """Loads thumbnails one at a time and emits each as it arrives."""
    thumb_ready = pyqtSignal(int, bytes)   # index, JPEG bytes
    finished    = pyqtSignal()

    def __init__(self, templates):
        super().__init__()
        self._templates = templates
        self._stop      = False

    def stop(self):
        self._stop = True

    def run(self):
        for i, tmpl in enumerate(self._templates):
            if self._stop:
                break
            try:
                data = get_template_thumbnail(tmpl["url"], size=110)
                if data:
                    self.thumb_ready.emit(i, data)
            except Exception:
                pass
        self.finished.emit()


# ── Meme preview ──────────────────────────────────────────────────────────────

class MemePreview(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(420, 380)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet(f"background: {BG_CARD}; border-radius: 10px;")
        self._pixmap_orig = None
        self._set_placeholder()

    def _set_placeholder(self):
        self.setText(
            f"<span style='color:{TEXT_SEC}; font-size:16px;'>"
            f"🎨  Click <b>Random Meme</b> to generate</span>"
        )

    def load_bytes(self, png_bytes: bytes):
        qimg = QImage.fromData(QByteArray(png_bytes))
        self._pixmap_orig = QPixmap.fromImage(qimg)
        self._fit()

    def _fit(self):
        if not self._pixmap_orig:
            return
        scaled = self._pixmap_orig.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.setPixmap(scaled)

    def resizeEvent(self, event):
        self._fit()
        super().resizeEvent(event)


# ── Dynamic text fields ───────────────────────────────────────────────────────

class TextPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QFrame { background: transparent; }")
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(5)
        self._fields = []

    def set_template(self, template_key: str, imgflip_box_count: int = 2):
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._fields.clear()

        if template_key == "_imgflip":
            n_fields = min(imgflip_box_count, 4)
            labels   = [f"Text {i+1}:" for i in range(n_fields)]
        else:
            tmpl   = TEMPLATES.get(template_key)
            if not tmpl:
                return
            labels = tmpl["labels"]

        for label_text in labels:
            lbl = QLabel(label_text)
            lbl.setStyleSheet(f"color: {TEXT_SEC}; font-size: 11px;")
            self._layout.addWidget(lbl)
            te = QTextEdit()
            te.setFixedHeight(58)
            te.setStyleSheet(f"""
                QTextEdit {{
                    background: {BG_INPUT};
                    color: {TEXT_PRI};
                    border: 1px solid #2e3250;
                    border-radius: 5px;
                    padding: 5px 8px;
                    font-size: 12px;
                }}
                QTextEdit:focus {{ border-color: {ACCENT}; }}
            """)
            self._layout.addWidget(te)
            self._fields.append(te)
        self._layout.addStretch()

    def get_texts(self):
        return [f.toPlainText().strip() for f in self._fields]

    def set_texts(self, texts: list):
        for i, te in enumerate(self._fields):
            te.setPlainText(texts[i] if i < len(texts) else "")


# ── Template card (browse panel) ──────────────────────────────────────────────

class TemplateCard(QFrame):
    selected = pyqtSignal(dict)   # emits the template info dict

    def __init__(self, info: dict, has_jokes: bool, parent=None):
        super().__init__(parent)
        self._info      = info
        self._has_jokes = has_jokes
        self.setFixedSize(132, 158)
        self.setStyleSheet(f"""
            QFrame {{
                background: {BG_CARD};
                border-radius: 7px;
                border: 1px solid #2e3250;
            }}
            QFrame:hover {{
                border-color: {ACCENT};
                background: #20243a;
            }}
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(4, 4, 4, 4)
        lay.setSpacing(3)

        self._img_lbl = QLabel()
        self._img_lbl.setFixedSize(124, 110)
        self._img_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._img_lbl.setStyleSheet(f"background: {BG_INPUT}; border-radius: 4px;")
        self._img_lbl.setText("⏳")
        lay.addWidget(self._img_lbl)

        name_lbl = QLabel(info["name"])
        name_lbl.setWordWrap(True)
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_lbl.setStyleSheet(f"color: {TEXT_PRI}; font-size: 10px;")
        lay.addWidget(name_lbl)

        if has_jokes:
            badge = QLabel("✓ Dev Jokes")
            badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            badge.setStyleSheet(
                f"color: {SUCCESS}; font-size: 9px; font-weight: bold;"
            )
            lay.addWidget(badge)

    def set_thumbnail(self, jpeg_bytes: bytes):
        qimg   = QImage.fromData(QByteArray(jpeg_bytes))
        pixmap = QPixmap.fromImage(qimg)
        self._img_lbl.setPixmap(
            pixmap.scaled(124, 110,
                          Qt.AspectRatioMode.KeepAspectRatio,
                          Qt.TransformationMode.SmoothTransformation)
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.selected.emit(self._info)
        super().mousePressEvent(event)


# ── Browse tab ────────────────────────────────────────────────────────────────

class BrowseTab(QWidget):
    template_chosen = pyqtSignal(dict)   # info dict from Imgflip or local

    def __init__(self, parent=None):
        super().__init__(parent)
        self._cards: list       = []
        self._catalog: list     = []
        self._thumb_worker      = None
        self._loaded            = False

        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 12, 12, 12)
        lay.setSpacing(8)

        # Controls row
        ctrl = QHBoxLayout()
        self._search = QLineEdit()
        self._search.setPlaceholderText("Search templates…")
        self._search.textChanged.connect(self._filter)
        self._search.setStyleSheet(f"""
            QLineEdit {{
                background: {BG_INPUT};
                color: {TEXT_PRI};
                border: 1px solid #2e3250;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 13px;
            }}
            QLineEdit:focus {{ border-color: {ACCENT}; }}
        """)

        self._filter_btn = QPushButton("Dev Jokes Only")
        self._filter_btn.setCheckable(True)
        self._filter_btn.setFixedWidth(130)
        self._filter_btn.toggled.connect(self._filter)

        self._count_lbl = QLabel("")
        self._count_lbl.setStyleSheet(f"color: {TEXT_SEC}; font-size: 11px;")

        ctrl.addWidget(self._search)
        ctrl.addWidget(self._filter_btn)
        ctrl.addWidget(self._count_lbl)
        lay.addLayout(ctrl)

        # Scrollable grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        self._grid_widget = QWidget()
        self._grid_widget.setStyleSheet("background: transparent;")
        self._grid = QGridLayout(self._grid_widget)
        self._grid.setSpacing(8)
        self._grid.setContentsMargins(0, 0, 0, 0)
        scroll.setWidget(self._grid_widget)
        lay.addWidget(scroll)

        self._status = QLabel("Click this tab to load templates…")
        self._status.setStyleSheet(f"color: {TEXT_SEC}; font-size: 11px;")
        lay.addWidget(self._status)

    def load(self):
        """Called the first time the Browse tab becomes visible."""
        if self._loaded:
            return
        self._loaded = True
        self._status.setText("⏳  Fetching template catalog…")
        w = CatalogWorker()
        w.ready.connect(self._on_catalog)
        w.finished.connect(w.deleteLater)
        w.start()
        self._catalog_worker = w

    @pyqtSlot(list)
    def _on_catalog(self, catalog: list):
        # Merge our local templates first (with dev-jokes flag), then Imgflip extras
        seen_urls = set()
        merged    = []

        # Local templates first
        for key, tmpl in TEMPLATES.items():
            info = {
                "id":        key,
                "name":      tmpl["name"],
                "url":       tmpl["url"],
                "box_count": len(tmpl["labels"]),
                "_local_key": key,
                "_has_jokes": True,
            }
            merged.append(info)
            seen_urls.add(tmpl["url"])

        # Imgflip extras not already covered
        for item in catalog:
            if item["url"] not in seen_urls:
                item["_local_key"] = None
                item["_has_jokes"] = False
                merged.append(item)
                seen_urls.add(item["url"])

        self._catalog = merged
        self._build_grid(merged)

        # Start loading thumbnails
        if self._thumb_worker and self._thumb_worker.isRunning():
            self._thumb_worker.stop()
        self._thumb_worker = ThumbnailWorker(merged)
        self._thumb_worker.thumb_ready.connect(self._on_thumb)
        self._thumb_worker.finished.connect(lambda: self._status.setText(
            f"Showing {len(self._cards)} templates — click any to use it"))
        self._thumb_worker.start()
        self._status.setText(f"Loading {len(merged)} templates…")

    def _build_grid(self, items: list):
        # Clear existing cards
        while self._grid.count():
            item = self._grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._cards.clear()

        cols = 5
        for i, info in enumerate(items):
            card = TemplateCard(info, info.get("_has_jokes", False))
            card.selected.connect(self._on_card_selected)
            self._grid.addWidget(card, i // cols, i % cols)
            self._cards.append(card)

        self._update_count()

    @pyqtSlot(int, bytes)
    def _on_thumb(self, idx: int, jpeg: bytes):
        if 0 <= idx < len(self._cards):
            self._cards[idx].set_thumbnail(jpeg)

    def _filter(self):
        q          = self._search.text().strip().lower()
        jokes_only = self._filter_btn.isChecked()
        for card in self._cards:
            name    = card._info["name"].lower()
            visible = (not q or q in name) and (not jokes_only or card._has_jokes)
            card.setVisible(visible)
        self._update_count()

    def _update_count(self):
        visible = sum(1 for c in self._cards if c.isVisible())
        self._count_lbl.setText(f"{visible} templates")

    @pyqtSlot(dict)
    def _on_card_selected(self, info: dict):
        self.template_chosen.emit(info)


# ── Main window ───────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DevMemes — Dev & Startup Meme Generator")
        self.setMinimumSize(1060, 700)

        self._current_png:      bytes = b""
        self._current_tmpl:     str   = ""
        self._current_iurl:     str   = ""
        self._current_boxcount: int   = 2
        self._worker                  = None
        self._used_indices: set       = set()

        self._build_ui()
        self._apply_theme()
        self._populate_templates()

    # ── Build UI ──────────────────────────────────────────────────────────────

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Header
        header = QFrame()
        header.setFixedHeight(54)
        header.setStyleSheet(f"background: {BG_CARD};")
        h_lay = QHBoxLayout(header)
        h_lay.setContentsMargins(20, 0, 20, 0)
        title = QLabel("DevMemes")
        title.setStyleSheet(f"color: {ACCENT}; font-size: 22px; font-weight: bold;")
        sub = QLabel("Meme generator for devs who've seen some things")
        sub.setStyleSheet(f"color: {TEXT_SEC}; font-size: 12px;")
        h_lay.addWidget(title)
        h_lay.addSpacing(14)
        h_lay.addWidget(sub)
        h_lay.addStretch()
        outer.addWidget(header)

        # Tabs
        self._tabs = QTabWidget()
        self._tabs.setStyleSheet(f"""
            QTabWidget::pane  {{ border: none; background: {BG_DEEP}; }}
            QTabBar::tab {{
                background: {BG_CARD};
                color: {TEXT_SEC};
                padding: 8px 22px;
                font-size: 13px;
                border: none;
            }}
            QTabBar::tab:selected {{
                background: {BG_DEEP};
                color: {TEXT_PRI};
                font-weight: bold;
                border-bottom: 2px solid {ACCENT};
            }}
            QTabBar::tab:hover {{ color: {TEXT_PRI}; }}
        """)
        outer.addWidget(self._tabs)

        # ── Tab 1: Create ──────────────────────────────────────────────────
        create_tab = QWidget()
        self._tabs.addTab(create_tab, "🎨  Create")

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(2)
        splitter.setStyleSheet("QSplitter::handle { background: #2e3250; }")
        QVBoxLayout(create_tab).addWidget(splitter)
        QVBoxLayout(create_tab).setContentsMargins(0, 0, 0, 0)

        # Left: preview + action buttons
        left = QWidget()
        left.setMinimumWidth(440)
        llay = QVBoxLayout(left)
        llay.setContentsMargins(16, 14, 8, 14)
        llay.setSpacing(10)

        self._preview = MemePreview()
        llay.addWidget(self._preview)

        act = QHBoxLayout()
        self._btn_random   = QPushButton("🎲  Random Meme")
        self._btn_random.setFixedHeight(36)
        self._btn_random.clicked.connect(self._on_random)

        self._btn_joke     = QPushButton("↺  New Joke")
        self._btn_joke.setFixedHeight(36)
        self._btn_joke.clicked.connect(self._on_new_joke)

        self._btn_save     = QPushButton("💾  Save PNG")
        self._btn_save.setFixedHeight(36)
        self._btn_save.clicked.connect(self._on_save)

        self._btn_copy     = QPushButton("📋  Copy")
        self._btn_copy.setFixedHeight(36)
        self._btn_copy.clicked.connect(self._on_copy)

        for b in (self._btn_random, self._btn_joke, self._btn_save, self._btn_copy):
            act.addWidget(b)
        llay.addLayout(act)
        splitter.addWidget(left)

        # Right: controls
        right = QWidget()
        right.setFixedWidth(310)
        rlay = QVBoxLayout(right)
        rlay.setContentsMargins(8, 14, 16, 14)
        rlay.setSpacing(10)

        cat_lbl = QLabel("Category")
        cat_lbl.setStyleSheet(f"color: {TEXT_SEC}; font-size: 11px; font-weight: bold;")
        self._cat_combo = QComboBox()
        self._cat_combo.addItems(CATEGORIES)
        self._cat_combo.currentTextChanged.connect(lambda: self._used_indices.clear())

        tmpl_lbl = QLabel("Template")
        tmpl_lbl.setStyleSheet(f"color: {TEXT_SEC}; font-size: 11px; font-weight: bold;")
        self._tmpl_combo = QComboBox()
        self._tmpl_combo.currentIndexChanged.connect(self._on_template_changed)

        rlay.addWidget(cat_lbl)
        rlay.addWidget(self._cat_combo)
        rlay.addWidget(tmpl_lbl)
        rlay.addWidget(self._tmpl_combo)

        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet(f"color: #2e3250;")
        rlay.addWidget(div)

        text_lbl = QLabel("Meme Text")
        text_lbl.setStyleSheet(f"color: {TEXT_SEC}; font-size: 11px; font-weight: bold;")
        rlay.addWidget(text_lbl)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        self._text_panel = TextPanel()
        scroll.setWidget(self._text_panel)
        rlay.addWidget(scroll, stretch=1)

        self._btn_generate = QPushButton("✨  Generate Meme")
        self._btn_generate.setFixedHeight(40)
        self._btn_generate.setStyleSheet(
            f"QPushButton {{ background: {ACCENT2}; color: white; border: none; "
            f"border-radius: 6px; font-size: 14px; font-weight: bold; }}"
            f"QPushButton:hover {{ background: #f88aa0; }}"
            f"QPushButton:disabled {{ background: #2e3250; color: {TEXT_SEC}; }}"
        )
        self._btn_generate.clicked.connect(self._on_generate)
        rlay.addWidget(self._btn_generate)
        splitter.addWidget(right)
        splitter.setSizes([740, 310])

        # ── Tab 2: Browse ──────────────────────────────────────────────────
        self._browse_tab = BrowseTab()
        self._browse_tab.template_chosen.connect(self._on_browse_chosen)
        self._tabs.addTab(self._browse_tab, "📚  Browse Templates")
        self._tabs.currentChanged.connect(self._on_tab_changed)

        # Status bar
        self.statusBar().setStyleSheet(f"background: {BG_CARD}; color: {TEXT_SEC};")
        self.statusBar().showMessage("Ready — hit Random Meme or browse the template library")

    def _apply_theme(self):
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background: {BG_DEEP};
                color: {TEXT_PRI};
                font-size: 13px;
            }}
            QComboBox {{
                background: {BG_INPUT};
                color: {TEXT_PRI};
                border: 1px solid #2e3250;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 13px;
            }}
            QComboBox:focus {{ border-color: {ACCENT}; }}
            QComboBox::drop-down {{ border: none; width: 20px; }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid {TEXT_SEC};
                margin-right: 6px;
            }}
            QComboBox QAbstractItemView {{
                background: {BG_INPUT};
                color: {TEXT_PRI};
                selection-background-color: {ACCENT};
            }}
            QPushButton {{
                background: {ACCENT};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 6px 14px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover    {{ background: #8095f8; }}
            QPushButton:disabled {{ background: #2e3250; color: {TEXT_SEC}; }}
            QPushButton:checked  {{ background: {ACCENT2}; }}
            QScrollArea {{ background: transparent; }}
        """)

    # ── Template dropdowns ────────────────────────────────────────────────────

    def _populate_templates(self):
        self._tmpl_combo.blockSignals(True)
        self._tmpl_combo.clear()
        for key, tmpl in TEMPLATES.items():
            self._tmpl_combo.addItem(tmpl["name"], userData=key)
        self._tmpl_combo.blockSignals(False)
        self._on_template_changed()

    def _on_template_changed(self):
        key = self._tmpl_combo.currentData()
        if key:
            self._current_tmpl     = key
            self._current_iurl     = ""
            self._current_boxcount = 2
            self._text_panel.set_template(key)

    @pyqtSlot(int)
    def _on_tab_changed(self, idx: int):
        if idx == 1:
            self._browse_tab.load()

    # ── Browse → Create handoff ───────────────────────────────────────────────

    @pyqtSlot(dict)
    def _on_browse_chosen(self, info: dict):
        """User clicked a card in Browse — switch to Create tab with it loaded."""
        self._tabs.setCurrentIndex(0)
        local_key = info.get("_local_key")

        if local_key:
            # One of our hardcoded templates — select it in the combo
            for j in range(self._tmpl_combo.count()):
                if self._tmpl_combo.itemData(j) == local_key:
                    self._tmpl_combo.setCurrentIndex(j)
                    break
        else:
            # Pure Imgflip template — inject a temporary entry
            display = f"[Imgflip] {info['name']}"
            # Check if already in combo
            found = False
            for j in range(self._tmpl_combo.count()):
                if self._tmpl_combo.itemText(j) == display:
                    self._tmpl_combo.setCurrentIndex(j)
                    found = True
                    break
            if not found:
                self._tmpl_combo.addItem(display, userData="_imgflip")
                self._tmpl_combo.setCurrentIndex(self._tmpl_combo.count() - 1)

            self._current_tmpl     = "_imgflip"
            self._current_iurl     = info["url"]
            self._current_boxcount = info.get("box_count", 2)
            self._text_panel.set_template("_imgflip", self._current_boxcount)

        self.statusBar().showMessage(
            f"Template loaded: {info['name']} — fill in the text and hit ✨ Generate Meme"
        )

    # ── Button handlers ───────────────────────────────────────────────────────

    @pyqtSlot()
    def _on_random(self):
        category = self._cat_combo.currentText()
        pool = [(i, m) for i, m in enumerate(MEMES)
                if category == "All" or m[1] == category]
        if not pool:
            self.statusBar().showMessage(f"No memes for: {category}")
            return
        fresh = [(i, m) for i, m in pool if i not in self._used_indices]
        if not fresh:
            self._used_indices.clear()
            fresh = pool
        idx, meme = random.choice(fresh)
        self._used_indices.add(idx)
        tmpl_key, _, texts = meme
        for j in range(self._tmpl_combo.count()):
            if self._tmpl_combo.itemData(j) == tmpl_key:
                self._tmpl_combo.setCurrentIndex(j)
                break
        self._text_panel.set_texts(texts)
        self._generate(tmpl_key, texts)

    @pyqtSlot()
    def _on_new_joke(self):
        key      = self._current_tmpl
        category = self._cat_combo.currentText()
        pool = [m for m in MEMES
                if m[0] == key and (category == "All" or m[1] == category)]
        if not pool:
            pool = [m for m in MEMES if m[0] == key]
        if not pool:
            self.statusBar().showMessage("No saved jokes for this template — type your own!")
            return
        _, _, texts = random.choice(pool)
        self._text_panel.set_texts(texts)
        self._generate(key, texts)

    @pyqtSlot()
    def _on_generate(self):
        key = self._current_tmpl
        if not key:
            return
        texts = self._text_panel.get_texts()
        self._generate(key, texts, self._current_iurl, self._current_boxcount)

    def _generate(self, template_key, texts, iurl="", box_count=2):
        self._set_busy(True)
        name = TEMPLATES.get(template_key, {}).get("name", template_key)
        self.statusBar().showMessage(f"Generating: {name} …")
        if self._worker and self._worker.isRunning():
            self._worker.quit()
        self._worker = MemeWorker(template_key, texts, iurl, box_count)
        self._worker.done.connect(self._on_meme_ready)
        self._worker.failed.connect(self._on_meme_failed)
        self._worker.start()

    # ── Worker callbacks ──────────────────────────────────────────────────────

    @pyqtSlot(bytes)
    def _on_meme_ready(self, png: bytes):
        self._current_png = png
        self._preview.load_bytes(png)
        self._set_busy(False)
        name = TEMPLATES.get(self._current_tmpl, {}).get("name", self._current_tmpl)
        self.statusBar().showMessage(f"✓ {name} — Save or Copy to share")

    @pyqtSlot(str)
    def _on_meme_failed(self, msg: str):
        self._set_busy(False)
        self.statusBar().showMessage(f"⚠ {msg}")

    # ── Save / Copy ───────────────────────────────────────────────────────────

    @pyqtSlot()
    def _on_save(self):
        if not self._current_png:
            self.statusBar().showMessage("Generate a meme first!")
            return
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        default = os.path.join(OUTPUT_DIR, f"{self._current_tmpl}_meme.png")
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Meme", default, "PNG Image (*.png)"
        )
        if path:
            with open(path, "wb") as f:
                f.write(self._current_png)
            self.statusBar().showMessage(f"Saved: {path}")

    @pyqtSlot()
    def _on_copy(self):
        if not self._current_png:
            self.statusBar().showMessage("Generate a meme first!")
            return
        pixmap = QPixmap.fromImage(QImage.fromData(QByteArray(self._current_png)))
        QApplication.clipboard().setPixmap(pixmap)
        self.statusBar().showMessage("✓ Copied to clipboard — paste into Slack, Twitter, Discord!")

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _set_busy(self, busy: bool):
        self._btn_random.setEnabled(not busy)
        self._btn_joke.setEnabled(not busy)
        self._btn_generate.setEnabled(not busy)
        self._btn_save.setEnabled(not busy and bool(self._current_png))
        self._btn_copy.setEnabled(not busy and bool(self._current_png))
        if busy:
            self._preview.setText(
                f"<span style='color:{TEXT_SEC}; font-size:15px;'>⏳  Generating…</span>"
            )


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont(".AppleSystemUIFont", 13))
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
