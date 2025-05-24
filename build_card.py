#!/usr/bin/env python
"""
Generate a one-page model card PDF with NOAA-blue styling.
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
import matplotlib.font_manager as fm
from PIL import Image

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
OUTFILE = ROOT / "fish_detector_card.pdf"

# ---- basic canvas ----------------------------------------------------------
plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.size": 10,
        "axes.facecolor": "#005CB9",  # deep NOAA blue background
    }
)
fig, ax = plt.subplots(figsize=(8.5, 11))
ax.axis("off")

# ---- white card with rounded corners --------------------------------------
card = FancyBboxPatch((0.05, 0.05), 0.90, 0.90,
                      boxstyle="round,pad=0.02,rounding_size=0.02",
                      facecolor="white", transform=ax.transAxes)
ax.add_patch(card)

# Convenience for placing things in Axes coordinates
def A(x, y):
    return ax.transAxes.transform((x, y))

# ---- header ribbon --------------------------------------------------------
ax.add_patch(Rectangle((0.05, 0.88), 0.90, 0.07,
                       transform=ax.transAxes, color="#005CB9"))
ax.text(0.5, 0.915, "YOLO-v11 Fish Detector – Model Card",
        ha="center", va="center", transform=ax.transAxes,
        color="white", fontsize=20, weight="bold")

# ---- images side by side ---------------------------------------------------
left_img  = Image.open(ASSETS / "example_detection.png")
right_img = Image.open(ASSETS / "example_PR_curve.png")

axfig1 = fig.add_axes([0.08, 0.66, 0.40, 0.18])
axfig1.imshow(left_img)
axfig1.axis("off")

axfig2 = fig.add_axes([0.52, 0.66, 0.40, 0.18])
axfig2.imshow(right_img)
axfig2.axis("off")

# ---- plain-language bullets ------------------------------------------------
bullets = (
    "• Finds ≈9 of 10 fish in a frame\n"
    "• Rarely confuses coral or rocks for fish\n"
    "• Slide the confidence slider → right to cut false positives\n"
    "  (you’ll skip a few shy fish)"
)
ax.text(0.08, 0.57, bullets, transform=ax.transAxes, fontsize=11, va="top")

# ---- key numbers table -----------------------------------------------------
metrics = (
    "Metric      Value   Meaning\n"
    "Precision   0.885   Share of detections that are real fish\n"
    "Recall      0.861   Share of all fish that are found\n"
    "mAP@0.5     0.937   Combined quality score"
)
ax.text(0.08, 0.45, metrics, transform=ax.transAxes, fontsize=10,
        family="monospace", va="top")

# ---- threshold mini-table --------------------------------------------------
threshold = (
    "Tune the confidence threshold\n"
    "0.20  Catch everything | 0.50  Balanced | 0.80  Only sure hits"
)
ax.text(0.08, 0.37, threshold, transform=ax.transAxes, fontsize=10, va="top")

# ---- aphorism + disclaimer -------------------------------------------------
quote = "“All models are wrong, some are useful.”"
ax.text(0.08, 0.28, quote, transform=ax.transAxes,
        fontsize=11, style="italic")
disc = ("Trained on expert-labelled images – humans and models both err.\n"
        "Use results as a helpful preview, not the final answer.")
ax.text(0.08, 0.23, disc, transform=ax.transAxes, fontsize=10, va="top")

# ---- footer ----------------------------------------------------------------
footer = "v1.0 · © 2025 NOAA / CIMAR · Questions: ai4me@noaa.gov"
ax.text(0.5, 0.10, footer, transform=ax.transAxes,
        ha="center", fontsize=9)

# ---- output ----------------------------------------------------------------
fig.savefig(OUTFILE, bbox_inches="tight")
print(f"Wrote {OUTFILE}")
