from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def generate_pdf_report(disease_name, probability, risk_level, info, specialist):
    """
    Build a PDF report for a single chest X-ray finding and
    return it as bytes (ready for st.download_button).
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=18,
        spaceAfter=6
    )
    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontSize=13,
        spaceBefore=12,
        spaceAfter=4,
        textColor=colors.HexColor("#1f4e79")
    )
    normal_style = styles["Normal"]
    disclaimer_style = ParagraphStyle(
        "DisclaimerStyle",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.grey
    )

    elements = []

    # Header
    elements.append(Paragraph("🩺 Chest X-ray Disease Detection Report", title_style))
    elements.append(Paragraph(
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        disclaimer_style
    ))
    elements.append(Spacer(1, 10))

    # Summary table
    risk_color = {
        "High": colors.HexColor("#d9534f"),
        "Moderate": colors.HexColor("#f0ad4e"),
        "Low": colors.HexColor("#5cb85c")
    }.get(risk_level, colors.black)

    summary_data = [
        ["Disease", disease_name],
        ["Probability", f"{probability}%"],
        ["Risk Level", risk_level],
        ["Recommended Specialist", specialist],
    ]
    summary_table = Table(summary_data, colWidths=[150, 300])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eaf1f8")),
        ("TEXTCOLOR", (1, 2), (1, 2), risk_color),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 12))

    # Description
    elements.append(Paragraph("Description", heading_style))
    elements.append(Paragraph(info.get("description", "N/A"), normal_style))

    # Helper to render a bullet section
    def add_bullet_section(title, items):
        elements.append(Paragraph(title, heading_style))
        if items:
            for item in items:
                elements.append(Paragraph(f"• {item}", normal_style))
        else:
            elements.append(Paragraph("N/A", normal_style))

    add_bullet_section("Symptoms", info.get("symptoms", []))
    add_bullet_section("Possible Causes", info.get("causes", []))
    add_bullet_section("Treatment", info.get("treatment", []))
    add_bullet_section("Prevention", info.get("prevention", []))

    # Emergency warning
    elements.append(Paragraph("Emergency Warning", heading_style))
    elements.append(Paragraph(
        "🚨 Seek immediate medical care if oxygen saturation falls below 90%, "
        "severe chest pain develops, or breathing becomes very difficult.",
        normal_style
    ))

    # Disclaimer
    elements.append(Spacer(1, 14))
    elements.append(Paragraph(
        "Disclaimer: This AI prediction is for screening purposes only and "
        "is not a confirmed medical diagnosis. Please consult a qualified "
        "healthcare professional for an accurate diagnosis and treatment plan.",
        disclaimer_style
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()