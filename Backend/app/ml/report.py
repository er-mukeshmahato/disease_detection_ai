# app/ml/report.py

import uuid
import requests
import os
import tempfile
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors


def generate_pdf_report(image_url, gradcam_url, predicted_label, confidence, explanation, name, email):

    temp_dir = tempfile.gettempdir()
    file_id = str(uuid.uuid4())

    pdf_path = os.path.join(temp_dir, f"report_{file_id}.pdf")
    xray_path = os.path.join(temp_dir, f"xray_{file_id}.png")
    gradcam_path = os.path.join(temp_dir, f"gradcam_{file_id}.png")

    # Download images
    with open(xray_path, "wb") as f:
        f.write(requests.get(image_url).content)

    with open(gradcam_path, "wb") as f:
        f.write(requests.get(gradcam_url).content)

    styles = getSampleStyleSheet()
    story = []

    # ============================
    # Header
    # ============================
    story.append(Paragraph("<b>X-Ray AI Prediction Report</b>", styles["Title"]))
    story.append(Spacer(1, 16))

    # Patient Info
    story.append(Paragraph(f"<b>Name:</b> {name}", styles["Normal"]))
    story.append(Paragraph(f"<b>Email:</b> {email}", styles["Normal"]))
    story.append(Spacer(1, 10))

    # A subtle divider
    story.append(Paragraph("<u>Patient Prediction Details</u>", styles["Heading3"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph(f"<b>Predicted Label:</b> {predicted_label}", styles["Normal"]))
    story.append(Paragraph(f"<b>Confidence:</b> {confidence * 100:.2f}%", styles["Normal"]))
    story.append(Spacer(1, 20))

    # ============================
    # Image Section
    # ============================

    story.append(Paragraph("<u>X-Ray Visual Analysis</u>", styles["Heading3"]))
    story.append(Spacer(1, 14))

    xray_title = Paragraph("<b>Original X-Ray</b>", styles["Normal"])
    gradcam_title = Paragraph("<b>Grad-CAM Visualization</b>", styles["Normal"])

    xray_img = Image(xray_path, width=217, height=217)
    gradcam_img = Image(gradcam_path, width=217, height=217)

    xray_cell = [xray_title, Spacer(1, 8), xray_img]
    gradcam_cell = [gradcam_title, Spacer(1, 8), gradcam_img]

    image_table = Table(
        [[xray_cell, gradcam_cell]],
        colWidths=[230, 230]
    )

    image_table.setStyle(
        TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 20),
        ])
    )

    story.append(image_table)
    story.append(Spacer(1, 20))

    # ============================
    # Explanation
    # ============================

    story.append(Paragraph("<u>AI Interpretation</u>", styles["Heading3"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(explanation, styles["Normal"]))
    story.append(Spacer(1, 20))

    # ============================
    # Medical Notice
    # ============================
    story.append(
    Paragraph(
        "<b>Note:</b> This AI-generated result is intended for screening and research purposes only. "
        "It should not be considered a definitive medical diagnosis. "
        "Please consult a qualified radiologist or healthcare professional "
        "for clinical confirmation and further evaluation.",
        styles["Normal"]
    )
    )

    story.append(Spacer(1, 14))


    # Final build
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    doc.build(story)

    return pdf_path
