#!/usr/bin/env python3
"""
Generate a one-page PDF model card (fish_detector_card.pdf)
Completely self-contained – just needs matplotlib + Pillow.
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from PIL import Image, ImageDraw

ROOT    = Path(__file__).parent
ASSETS  = ROOT / "assets"
DETECT  = ASSETS / "example_detection.png"      # change path if needed
PR_CURV = ASSETS / "example_PR_curve.png"
OUTPDF  = ROOT / "fish_detector_card.pdf"

# ---------- helper ----------------------------------------------------------
def safe_open(path, ph_size=(640, 400), label="image\nmissing"):
    """Open image or return gray placeholder (never crash CI)."""
    if path.exists():
        return Image.open(path)
    ph = Image.new("RGB", ph_size, (200, 200, 200))
    d  = ImageDraw.Draw(ph)
    w, h = d.textsize(label)
    d.text(((ph_size[0]-w)/2, (ph_size[1]-h)/2), label, fill=(80, 80, 80),
           align="center")
    return ph

# ---------- drawing ---------------------------------------------------------
plt.rcParams.update({"font.family": "sans-serif",
                     "font.size": 10,
                     "axes.facecolor": "#005CB9"})          # NOAA blue

fig, ax = plt.subplots(figsize=(8.5, 11))
ax.axis("off")

# white rounded card
card = FancyBboxPatch((0.05, 0.05), 0.90, 0.90,
                      boxstyle="round,pad=0.02,rounding_size=0.02",
                      facecolor="white", linewidth=0,
                      transform=ax.transAxes)
ax.add_patch(card)

# header ribbon
ax.add_patch(Rectangle((0.05, 0.88), 0.90, 0.07,
                       transform=ax.transAxes,
                       facecolor="#005CB9", linewidth=0))
ax.text(0.5, 0.915, "YOLO-v11 Fish Detector — Model Card",
        ha="center", va="center", transform=ax.transAxes,
        color="white", fontsize=22, weight="bold")

# images (49 % width each, under ribbon)
ax_left  = fig.add_axes([0.08, 0.67, 0.40, 0.17])
ax_left.imshow(safe_open(DETECT))
ax_left.axis("off")

ax_right = fig.add_axes([0.52, 0.67, 0.40, 0.17])
ax_right.imshow(safe_open(PR_CURV))
ax_right.axis("off")

# bullet section
bullets = (
    "• Finds ≈9 of 10 fish in a frame\n"
    "• Rarely confuses coral or rocks for fish\n"
    "• Move the confidence slider → right to cut false positives\n"
    "  (you’ll skip a few shy fish)"
)
ax.text(0.08, 0.58, bullets, transform=ax.transAxes,
        fontsize=11, va="top")

# key numbers table (monospace)
metrics = (
    "Metric      Value   Meaning\n"
    "Precision   0.885   Share of detections that are real fish\n"
    "Recall      0.861   Share of all fish that are found\n"
    "mAP@0.5     0.937   Combined quality score"
)
ax.text(0.08, 0.46, metrics, transform=ax.transAxes,
        family="monospace", fontsize=10, va="top")

# threshold strip
thresh = (
    "Tune the confidence threshold\n"
    "0.20  Catch everything   |   0.50  Balanced   |   0.80  Only sure hits"
)
ax.text(0.08, 0.38, thresh, transform=ax.transAxes,
        fontsize=10, va="top")

# aphorism & disclaimer
ax.text(0.08, 0.30, "“All models are wrong, some are useful.”",
        transform=ax.transAxes, fontsize=11, style="italic")
ax.text(0.08, 0.25,
        ("Trained on expert-labelled images – humans and models both err.\n"
         "Use results as a helpful preview, not the final answer."),
        transform=ax.transAxes, fontsize=10, va="top")

# footer
ax.text(0.5, 0.11,
        "v1.0 · © 2025 NOAA / CIMAR · Questions: ai4me@noaa.gov",
        transform=ax.transAxes, ha="center", fontsize=9)

fig.savefig(OUTPDF, bbox_inches="tight")
print(f"✓ Wrote {OUTPDF}")
