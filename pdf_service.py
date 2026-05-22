from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
from app.utils.logger import setup_logger

logger = setup_logger("pdf_service")

def generate_report_pdf(report_data: dict) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor("#1e3a8a"),
        spaceAfter=30
    )

    story = []
    story.append(Paragraph("VisionAid Diagnostic Report", title_style))
    story.append(Spacer(1, 0.2*inch))

    meta = [
        ["Patient ID", report_data.get("patient_id", "N/A")],
        ["Date", report_data.get("timestamp", datetime.utcnow().isoformat())],
        ["Diagnosis", report_data.get("diagnosis", "N/A")],
        ["Confidence", f"{report_data.get('confidence', 0)}%"],
        ["Severity", report_data.get("severity", "N/A")],
        ["Recommendation", report_data.get("recommendation", "N/A")],
        ["Report Hash", report_data.get("hash", "N/A")],
        ["Blockchain TX", report_data.get("tx_id", "N/A")],
    ]

    table = Table(meta, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#f1f5f9")),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    story.append(table)
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(
        "This report has been anchored to the Stellar blockchain for integrity verification.",
        styles["Normal"]
    ))

    doc.build(story)
    buffer.seek(0)
    logger.info("PDF generated for patient: %s", report_data.get("patient_id"))
    return buffer
