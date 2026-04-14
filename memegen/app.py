import os
import sys
import random

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QTextEdit, QComboBox,
    QFileDialog, QFrame, QSplitter, QSizePolicy,
    QScrollArea, QStatusBar,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QByteArray, pyqtSlot
from PyQt6.QtGui import QPixmap, QImage, QFont, QFontDatabase

from .jokes import TEMPLATES, CATEGORIES, MEMES
from .generator import generate_meme

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


# ── Background worker ─────────────────────────────────────────────────────────

class MemeWorker(QThread):
    done    = pyqtSignal(bytes)   # PNG bytes
    failed  = pyqtSignal(str)     # error message

    def __init__(self, template_key: str, texts: list):
        super().__init__()
        self.template_key = template_key
        self.texts        = texts

    def run(self):
        try:
            data = generate_meme(self.template_key, self.texts)
            if data:
                self.done.emit(data)
            else:
                self.failed.emit("Failed to generate meme — check your internet connection.")
        except Exception as e:
            self.failed.emit(str(e))


# ── Preview widget ────────────────────────────────────────────────────────────

class MemePreview(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(420, 420)
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
        available = self.size()
        scaled = self._pixmap_orig.scaled(
            available,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.setPixmap(scaled)

    def resizeEvent(self, event):
        self._fit()
        super().resizeEvent(event)


# ── Dynamic text-field panel ──────────────────────────────────────────────────

class TextPanel(QFrame):
    """Shows one QTextEdit per template field with a label above each."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"QFrame {{ background: transparent; }}")
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(6)
        self._fields: list = []

    def set_template(self, template_key: str):
        # Clear existing fields
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._fields.clear()

        tmpl = TEMPLATES.get(template_key)
        if not tmpl:
            return

        for label_text in tmpl["labels"]:
            lbl = QLabel(label_text)
            lbl.setStyleSheet(f"color: {TEXT_SEC}; font-size: 11px;")
            self._layout.addWidget(lbl)

            te = QTextEdit()
            te.setFixedHeight(60)
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

    def get_texts(self) -> list:
        return [f.toPlainText().strip() for f in self._fields]

    def set_texts(self, texts: list):
        for i, te in enumerate(self._fields):
            te.setPlainText(texts[i] if i < len(texts) else "")


# ── Main window ───────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DevMemes — Dev & Startup Meme Generator")
        self.setMinimumSize(1000, 680)

        self._current_png:  bytes  = b""
        self._current_tmpl: str   = ""
        self._worker: MemeWorker  = None

        # Track last-used meme index per category to avoid repeats
        self._used_indices: set = set()

        self._build_ui()
        self._apply_theme()
        self._populate_templates()

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Header
        header = QFrame()
        header.setFixedHeight(58)
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

        # Body splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(2)
        splitter.setStyleSheet("QSplitter::handle { background: #2e3250; }")
        outer.addWidget(splitter)

        # ── Left: meme preview ─────────────────────────────────────────────
        left = QWidget()
        left.setMinimumWidth(420)
        llay = QVBoxLayout(left)
        llay.setContentsMargins(16, 16, 8, 16)
        llay.setSpacing(10)

        self._preview = MemePreview()
        llay.addWidget(self._preview)

        # Action buttons under preview
        act_row = QHBoxLayout()
        self._btn_random = QPushButton("🎲  Random Meme")
        self._btn_random.setFixedHeight(38)
        self._btn_random.clicked.connect(self._on_random)

        self._btn_joke   = QPushButton("↺  New Joke")
        self._btn_joke.setFixedHeight(38)
        self._btn_joke.clicked.connect(self._on_new_joke)

        self._btn_save   = QPushButton("💾  Save PNG")
        self._btn_save.setFixedHeight(38)
        self._btn_save.clicked.connect(self._on_save)

        self._btn_copy   = QPushButton("📋  Copy")
        self._btn_copy.setFixedHeight(38)
        self._btn_copy.clicked.connect(self._on_copy)

        for btn in (self._btn_random, self._btn_joke, self._btn_save, self._btn_copy):
            act_row.addWidget(btn)
        llay.addLayout(act_row)
        splitter.addWidget(left)

        # ── Right: controls ────────────────────────────────────────────────
        right = QWidget()
        right.setFixedWidth(320)
        rlay = QVBoxLayout(right)
        rlay.setContentsMargins(8, 16, 16, 16)
        rlay.setSpacing(12)

        # Category
        cat_lbl = QLabel("Category")
        cat_lbl.setStyleSheet(f"color: {TEXT_SEC}; font-size: 11px; font-weight: bold;")
        self._cat_combo = QComboBox()
        self._cat_combo.addItems(CATEGORIES)
        self._cat_combo.currentTextChanged.connect(self._on_category_changed)

        # Template
        tmpl_lbl = QLabel("Template")
        tmpl_lbl.setStyleSheet(f"color: {TEXT_SEC}; font-size: 11px; font-weight: bold;")
        self._tmpl_combo = QComboBox()
        self._tmpl_combo.currentTextChanged.connect(self._on_template_changed)

        rlay.addWidget(cat_lbl)
        rlay.addWidget(self._cat_combo)
        rlay.addWidget(tmpl_lbl)
        rlay.addWidget(self._tmpl_combo)

        # Divider
        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet(f"color: #2e3250;")
        rlay.addWidget(div)

        # Text fields (dynamic)
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

        # Generate button
        self._btn_generate = QPushButton("✨  Generate Meme")
        self._btn_generate.setFixedHeight(42)
        self._btn_generate.setStyleSheet(
            f"QPushButton {{ background: {ACCENT2}; color: white; border: none; "
            f"border-radius: 6px; font-size: 14px; font-weight: bold; }}"
            f"QPushButton:hover {{ background: #f88aa0; }}"
            f"QPushButton:disabled {{ background: #2e3250; color: {TEXT_SEC}; }}"
        )
        self._btn_generate.clicked.connect(self._on_generate)
        rlay.addWidget(self._btn_generate)

        splitter.addWidget(right)
        splitter.setSizes([680, 320])

        # Status bar
        self.statusBar().setStyleSheet(f"background: {BG_CARD}; color: {TEXT_SEC};")
        self.statusBar().showMessage("Ready — pick a category and hit Random Meme")

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
            QScrollArea {{ background: transparent; }}
        """)

    # ── Populate dropdowns ────────────────────────────────────────────────────

    def _populate_templates(self):
        self._tmpl_combo.blockSignals(True)
        self._tmpl_combo.clear()
        for key, tmpl in TEMPLATES.items():
            self._tmpl_combo.addItem(tmpl["name"], userData=key)
        self._tmpl_combo.blockSignals(False)
        # Trigger first selection
        self._on_template_changed()

    def _on_category_changed(self):
        self._used_indices.clear()

    def _on_template_changed(self):
        key = self._tmpl_combo.currentData()
        if key:
            self._current_tmpl = key
            self._text_panel.set_template(key)

    # ── Button handlers ───────────────────────────────────────────────────────

    @pyqtSlot()
    def _on_random(self):
        """Pick a random template+joke from the selected category."""
        category = self._cat_combo.currentText()

        pool = [
            (i, m) for i, m in enumerate(MEMES)
            if category == "All" or m[1] == category
        ]

        if not pool:
            self.statusBar().showMessage(f"No memes for category: {category}")
            return

        # Avoid repeats until pool is exhausted
        fresh = [(i, m) for i, m in pool if i not in self._used_indices]
        if not fresh:
            self._used_indices.clear()
            fresh = pool

        idx, meme = random.choice(fresh)
        self._used_indices.add(idx)

        tmpl_key, _, texts = meme

        # Switch template combo
        for j in range(self._tmpl_combo.count()):
            if self._tmpl_combo.itemData(j) == tmpl_key:
                self._tmpl_combo.setCurrentIndex(j)
                break

        self._text_panel.set_texts(texts)
        self._generate(tmpl_key, texts)

    @pyqtSlot()
    def _on_new_joke(self):
        """Keep the current template, pick a new joke."""
        key      = self._current_tmpl
        category = self._cat_combo.currentText()

        pool = [
            m for m in MEMES
            if m[0] == key and (category == "All" or m[1] == category)
        ]
        if not pool:
            pool = [m for m in MEMES if m[0] == key]
        if not pool:
            self.statusBar().showMessage("No more jokes for this template+category combo.")
            return

        _, _, texts = random.choice(pool)
        self._text_panel.set_texts(texts)
        self._generate(key, texts)

    @pyqtSlot()
    def _on_generate(self):
        key   = self._current_tmpl
        texts = self._text_panel.get_texts()
        if not key:
            return
        self._generate(key, texts)

    def _generate(self, template_key: str, texts: list):
        self._set_busy(True)
        tmpl_name = TEMPLATES.get(template_key, {}).get("name", template_key)
        self.statusBar().showMessage(f"Generating: {tmpl_name} …")

        if self._worker and self._worker.isRunning():
            self._worker.quit()

        self._worker = MemeWorker(template_key, texts)
        self._worker.done.connect(self._on_meme_ready)
        self._worker.failed.connect(self._on_meme_failed)
        self._worker.start()

    # ── Worker callbacks ──────────────────────────────────────────────────────

    @pyqtSlot(bytes)
    def _on_meme_ready(self, png: bytes):
        self._current_png = png
        self._preview.load_bytes(png)
        self._set_busy(False)
        tmpl_name = TEMPLATES.get(self._current_tmpl, {}).get("name", "")
        self.statusBar().showMessage(f"✓ Generated: {tmpl_name}  — Save or Copy to share")

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
        qimg    = QImage.fromData(QByteArray(self._current_png))
        pixmap  = QPixmap.fromImage(qimg)
        QApplication.clipboard().setPixmap(pixmap)
        self.statusBar().showMessage("✓ Meme copied to clipboard — paste into Slack, Twitter, anywhere!")

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
