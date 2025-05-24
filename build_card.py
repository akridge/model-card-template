from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor, white
import os

def create_model_card(output_filename="model_card.pdf", logo_path="NOAA_FISHERIES_logoH_web.png",
                      detection_image_path="example_detection.png", pr_curve_path="example_PR_curve.png"):
    """
    Generates a PDF model card for an AI model.

    Args:
        output_filename (str): The name of the output PDF file.
        logo_path (str): Path to the NOAA Fisheries logo image.
        detection_image_path (str): Path to the example detection image.
        pr_curve_path (str): Path to the Precision-Recall curve image.
    """
    doc = SimpleDocTemplate(output_filename, pagesize=letter,
                            rightMargin=0.5*inch, leftMargin=0.5*inch,
                            topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()

    # Define custom colors for NOAA branding
    NOAA_BLUE_DARK = HexColor("#003366")
    NOAA_BLUE_LIGHT = HexColor("#336699")
    BACKGROUND_WHITE = white

    # Custom paragraph styles for a modern look
    styles.add(ParagraphStyle(name='Heading1', fontName='Helvetica-Bold', fontSize=24,
                              leading=28, alignment=TA_CENTER, textColor=NOAA_BLUE_DARK, spaceAfter=12))
    styles.add(ParagraphStyle(name='Heading2', fontName='Helvetica-Bold', fontSize=14,
                              leading=16, textColor=NOAA_BLUE_DARK, spaceAfter=6))
    styles.add(ParagraphStyle(name='BodyText', fontName='Helvetica', fontSize=10,
                              leading=12, textColor=NOAA_BLUE_DARK, spaceAfter=3))
    styles.add(ParagraphStyle(name='ListItem', fontName='Helvetica', fontSize=10,
                              leading=12, textColor=NOAA_BLUE_DARK, spaceBefore=0, spaceAfter=0,
                              leftIndent=18, bulletIndent=0, bulletFontSize=10, bulletFontName='Helvetica'))
    styles.add(ParagraphStyle(name='Quote', fontName='Helvetica-Oblique', fontSize=10,
                              leading=12, textColor=NOAA_BLUE_DARK, spaceBefore=6, spaceAfter=6,
                              alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Footer', fontName='Helvetica', fontSize=8,
                              leading=10, alignment=TA_CENTER, textColor=NOAA_BLUE_DARK,
                              linkAndMouseDefs='<link href="mailto:test@noaa.gov" color="blue">test@noaa.gov</link>'))


    story = []

    # --- Content for the left column ---
    left_column_content = []

    # Spacer to adjust for logo and top margin, ensuring content starts below header
    left_column_content.append(Spacer(1, 1.0 * inch)) # Increased space for header bar and logo

    left_column_content.append(Paragraph("In plain language", styles['Heading2']))
    left_column_content.append(Paragraph("• Finds <font face='Helvetica-Bold'>≈9 of 10</font> fish in a frame", styles['ListItem'], bulletText=""))
    left_column_content.append(Paragraph("• <font face='Helvetica-Bold'>Rarely</font> confuses coral/rocks for fish", styles['ListItem'], bulletText=""))
    left_column_content.append(Paragraph("• Slide the confidence slider → right to cut <i>false positives</i><br/>&nbsp;&nbsp;(you’ll skip a few shy fish)", styles['ListItem'], bulletText=""))
    left_column_content.append(Spacer(1, 0.2 * inch))

    left_column_content.append(Paragraph("---", styles['BodyText'])) # Separator
    left_column_content.append(Spacer(1, 0.1 * inch))

    left_column_content.append(Paragraph("Key numbers", styles['Heading2']))
    key_numbers_data = [
        ['Metric', 'Value', 'What it means'],
        ['Precision', '<b>0.885</b>', 'Share of detections that are real fish'],
        ['Recall', '<b>0.861</b>', 'Share of all fish that are found'],
        ['mAP@0.5', '<b>0.937</b>', 'Combined quality score']
    ]
    # Adjust column widths for better fit
    key_numbers_table = Table(key_numbers_data, colWidths=[1.2*inch, 0.8*inch, 2.5*inch])
    key_numbers_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NOAA_BLUE_LIGHT),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'), # Align values to the right
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), BACKGROUND_WHITE),
        ('GRID', (0, 0), (-1, -1), 0.5, NOAA_BLUE_LIGHT),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    left_column_content.append(key_numbers_table)
    left_column_content.append(Spacer(1, 0.2 * inch))
    left_column_content.append(Paragraph("---", styles['BodyText'])) # Separator
    left_column_content.append(Spacer(1, 0.1 * inch))

    # --- Content for the right column ---
    right_column_content = []

    # Spacer to align with left column content start
    right_column_content.append(Spacer(1, 1.0 * inch))

    right_column_content.append(Paragraph("Tune the confidence threshold", styles['Heading2']))
    tune_threshold_data = [
        ['0.20', '0.50 <i>(default)</i>', '0.80'],
        ['Catch <i>everything</i>', 'Balanced', 'Only sure hits']
    ]
    # Adjust column widths for better fit
    tune_threshold_table = Table(tune_threshold_data, colWidths=[1.7*inch, 1.7*inch, 1.7*inch])
    tune_threshold_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (1, 0), (1, 0), NOAA_BLUE_LIGHT), # Highlight default column header
        ('TEXTCOLOR', (1, 0), (1, 0), white),
        ('BACKGROUND', (0, 1), (-1, 1), BACKGROUND_WHITE),
        ('GRID', (0, 0), (-1, -1), 0.5, NOAA_BLUE_LIGHT),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    right_column_content.append(tune_threshold_table)
    right_column_content.append(Spacer(1, 0.2 * inch))

    # Example detection image
    if os.path.exists(detection_image_path):
        img_detection = Image(detection_image_path)
        img_width = 4.5 * inch # Max width for the column
        img_height = img_detection.drawHeight * (img_width / img_detection.drawWidth)
        img_detection.drawWidth = img_width
        img_detection.drawHeight = img_height
        right_column_content.append(img_detection)
        right_column_content.append(Spacer(1, 0.1 * inch))
    else:
        print(f"Warning: Detection image not found at {detection_image_path}")

    # Precision-Recall curve image
    if os.path.exists(pr_curve_path):
        img_pr = Image(pr_curve_path)
        img_width = 4.5 * inch # Max width for the column
        img_height = img_pr.drawHeight * (img_width / img_pr.drawWidth)
        img_pr.drawWidth = img_width
        img_pr.drawHeight = img_height
        right_column_content.append(img_pr)
        right_column_content.append(Spacer(1, 0.1 * inch))
    else:
        print(f"Warning: PR curve image not found at {pr_curve_path}")

    right_column_content.append(Paragraph("“<i>All models are wrong, some are useful.</i>”", styles['Quote']))
    right_column_content.append(Paragraph("Trained on expert-labelled images – humans <font face='Helvetica-Bold'>and</font> models make mistakes.<br/>Use results as a helpful <font face='Helvetica-Bold'>preview</font>, not the final answer.", styles['BodyText']))
    right_column_content.append(Spacer(1, 0.2 * inch))


    # Use a single table to lay out the two columns side-by-side
    # The sum of colWidths should be less than or equal to doc.width
    # A small gap between columns for visual separation
    column_gap = 0.2 * inch
    col_width = (doc.width - column_gap) / 2.0

    data = [[left_column_content, right_column_content]]
    column_table = Table(data, colWidths=[col_width, col_width])
    column_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
        ('RIGHTPADDING', (0, 0), (0, 0), column_gap / 2), # Padding for the left column
        ('LEFTPADDING', (1, 0), (1, 0), column_gap / 2), # Padding for the right column
        ('RIGHTPADDING', (1, 0), (1, 0), 0),
    ]))
    story.append(column_table)

    # Add a final spacer before the footer to push it to the bottom
    # This might require some trial and error depending on content length
    story.append(Spacer(1, 0.5 * inch)) # Placeholder, adjusted by bottom margin in page_template


    # Define the page template function for header, logo, and footer
    def page_template(canvas, doc):
        canvas.saveState()

        # Background color for the entire page (white)
        canvas.setFillColor(BACKGROUND_WHITE)
        canvas.rect(0, 0, letter[0], letter[1], fill=1)

        # Blue header bar at the top
        header_height = 0.8 * inch # Height of the blue header bar
        canvas.setFillColor(NOAA_BLUE_DARK)
        canvas.rect(0, letter[1] - header_height, letter[0], header_height, fill=1)

        # Draw a subtle blue line above the footer for visual separation
        canvas.setStrokeColor(NOAA_BLUE_LIGHT)
        canvas.setLineWidth(0.5)
        # Position the line relative to the bottom margin
        canvas.line(doc.leftMargin, doc.bottomMargin + 0.3*inch, letter[0] - doc.rightMargin, doc.bottomMargin + 0.3*inch)

        # Logo on top left corner, within the blue header bar
        if os.path.exists(logo_path):
            logo = Image(logo_path)
            logo_width = 1.0 * inch # Adjusted logo size
            logo_height = logo.drawHeight * (logo_width / logo.drawWidth)
            # Position logo inside the blue bar, with a small margin
            canvas.drawImage(logo_path, doc.leftMargin, letter[1] - logo_height - (header_height - logo_height) / 2,
                             width=logo_width, height=logo_height)
        else:
            print(f"Warning: Logo image not found at {logo_path}")

        # Draw the footer text explicitly at the bottom center
        footer_text = Paragraph("v1.0 • © 2025 NOAA / CIMAR • Questions: <a href='mailto:test@noaa.gov'><font color='blue'>test@noaa.gov</font></a>", styles['Footer'])
        # Calculate footer position
        footer_text_width = doc.width # We assume footer text fits in doc width
        footer_text_height = footer_text.wrapOn(canvas, footer_text_width, doc.height)[1]
        footer_y = doc.bottomMargin - 0.05 * inch # Position slightly above the bottom margin
        footer_text.drawOn(canvas, doc.leftMargin, footer_y)


        canvas.restoreState()

    # Build the document using the story and the custom page template
    doc.build(story, onAndAfterPage=page_template)
    print(f"Model card '{output_filename}' created successfully.")

if __name__ == "__main__":
    # Ensure your image files are in the same directory as the script, or provide full paths
    # When running with GitHub Actions, the files will be in the working directory
    # so relative paths are appropriate.
    create_model_card(
        logo_path="NOAA_FISHERIES_logoH_web.png",
        detection_image_path="example_detection.png",
        pr_curve_path="example_PR_curve.png"
    )