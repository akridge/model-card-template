# model-card-template
model-card-template using quarto

## Quarto Model Card Template

This repository provides a simple, one-page Quarto template for creating model cards for AI models.

### How to Use

1. **Install Quarto:**
   - Download and install from https://quarto.org/docs/get-started/

2. **Add your model details:**
   - Copy `model_card_template.qmd` to a new file (e.g., `my_model_card.qmd`).
   - Replace the placeholders (e.g., `{{< model_name >}}`) with your model's information.
   - Add your subject image as `subject_image.png` and PR curve as `pr_curve.png` in the same folder.

3. **Render the model card:**
   - Open a terminal in this folder and run:
     ```
     quarto render my_model_card.qmd
     ```
   - The output HTML will be in the `_output` folder.

### Template Features
- Clean, one-page layout
- Spaces for subject image and PR curve
- All key model card sections
- Easy to edit and extend

---

For more on Quarto, see [quarto.org](https://quarto.org/).

----------
#### Disclaimer
This repository is a scientific product and is not official communication of the National Oceanic and Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project content is provided on an ‘as is’ basis and the user assumes responsibility for its use. Any claims against the Department of Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.

#### License
- Details in the [LICENSE.md](./LICENSE.md) file.