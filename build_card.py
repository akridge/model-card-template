#!/usr/bin/env python3
"""
Generate a one-page, two-column model card PDF.
Assets expected in ./assets/ (or change paths below).
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from PIL import Image, ImageDraw

ROOT   = Path(__file__).parent
ASSETS = ROOT / "assets"
DETECT = ASSETS / "example_detection.png"
PRCURV = ASSETS / "example_PR_curve.png"
OUTPDF = ROOT / "fish_detector_card.pdf"

# --------------------------------------------------------------------------- helpers
def safe_open(path, size=(640, 400), label="image\nmissing"):
    if path.exists():
        return Image.open(path)
    ph = Image.new("RGB", size, (200, 200, 200))
    d  = ImageDraw.Draw(ph)
    w, h = d.textsize(label)
    d.text(((size[0]-w)/2, (size[1]-h)/2), label, fill=(70, 70, 70), align="center")
    return ph

# --------------------------------------------------------------------------- canvas
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size":   10,
    "axes.facecolor": "#005CB9"        # NOAA blue backdrop
})

fig, ax = plt.subplots(figsize=(8.5, 11))
ax.axis("off")

# White rounded card
card = FancyBboxPatch((0.05, 0.05), 0.90, 0.90,
                      boxstyle="round,pad=0.02,rounding_size=0.02",
                      facecolor="white", linewidth=0,
                      transform=ax.transAxes)
ax.add_patch(card)

# Header ribbon
ax.add_patch(Rectangle((0.05, 0.88), 0.90, 0.07, transform=ax.transAxes,
                       facecolor="#005CB9", linewidth=0))
ax.text(0.5, 0.915, "YOLO-v11 Fish Detector — Model Card",
        ha="center", va="center", transform=ax.transAxes,
        color="white", fontsize=22, weight="bold")

# --------------------------------------------------------------------------- full-width image row
ax_img1 = fig.add_axes([0.08, 0.68, 0.40, 0.17])
ax_img1.imshow(safe_open(DETECT))
ax_img1.axis("off")

ax_img2 = fig.add_axes([0.52, 0.68, 0.40, 0.17])
ax_img2.imshow(safe_open(PRCURV))
ax_img2.axis("off")

# --------------------------------------------------------------------------- LEFT column  (bullets)
left_x  = 0.08
right_x = 0.52           # start of right column
col_w   = 0.40

bullets = (
    "• Finds ≈ 9 of 10 fish per frame\n"
    "• Rarely confuses coral or rocks for fish\n"
    "• Move the confidence slider → right to cut false positives\n"
    "  (you’ll skip a few shy fish)"
)
ax.text(left_x, 0.59, bullets, transform=ax.transAxes,
        fontsize=11, va="top")

# --------------------------------------------------------------------------- RIGHT column  (metrics + threshold)
metrics = (
    "Metric      Value   Meaning\n"
    "Precision   0.885   Share of detections that are real fish\n"
    "Recall      0.861   Share of all fish that are found\n"
    "mAP@0.5     0.937   Combined quality score"
)
ax.text(right_x, 0.59, metrics, transform=ax.transAxes,
        family="monospace", fontsize=10, va="top")

thr = (
    "\nConfidence threshold:\n"
    "  0.20  Catch everything\n"
    "  0.50  Balanced (default)\n"
    "  0.80  Only sure hits"
)
ax.text(right_x, 0.45, thr, transform=ax.transAxes,
        fontsize=10, va="top")

# --------------------------------------------------------------------------- shared bottom section
ax.text(0.08, 0.32, "“All models are wrong, some are useful.”",
        transform=ax.transAxes, fontsize=11, style="italic")

disc = ("Trained on expert-labelled images – humans **and** models err.\n"
        "Use results as a helpful preview, not the final answer.")
ax.text(0.08, 0.26, disc, transform=ax.transAxes, fontsize=10, va="top")

# Footer
ax.text(0.5, 0.11,
        "v1.0 · © 2025 NOAA / CIMAR · Questions: ai4me@noaa.gov",
        transform=ax.transAxes, ha="center", fontsize=9)

fig.savefig(OUTPDF, bbox_inches="tight")
print(f"✓ wrote {OUTPDF}")
