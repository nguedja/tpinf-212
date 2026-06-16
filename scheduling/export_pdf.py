import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)


def exporter_pdf(planning, chemin="static/planning.pdf"):

    os.makedirs(os.path.dirname(chemin), exist_ok=True)

    doc = SimpleDocTemplate(
        chemin,
        pagesize=landscape(A4),
        leftMargin=20,
        rightMargin=20,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()
    elements = []

    title_style = styles["Title"]
    title_style.fontSize = 20
    title_style.spaceAfter = 10
    title_style.textColor = colors.HexColor("#1e293b")

    elements.append(
        Paragraph("Planning des Examens", title_style)
    )

    subtitle_style = styles["Normal"]
    subtitle_style.fontSize = 11
    subtitle_style.textColor = colors.HexColor("#64748b")
    subtitle_style.spaceAfter = 20

    elements.append(
        Paragraph(
            "Planification automatique par coloration de graphe",
            subtitle_style
        )
    )

    elements.append(Spacer(1, 10))

    creneaux = sorted(set(l["creneau"] for l in planning))
    salles = sorted(set(l["salle"] for l in planning))

    cellules = {}
    for l in planning:
        cellules[(l["creneau"], l["salle"])] = (
            f"{l['ue']} ({l['effectif']})"
        )

    data = [["Creneau \\ Salle"] + salles]

    for c in creneaux:
        ligne = [c]
        for s in salles:
            ligne.append(cellules.get((c, s), ""))
        data.append(ligne)

    tableau = Table(data, repeatRows=1)

    violet = colors.HexColor("#7c3aed")
    violet_light = colors.HexColor("#ede9fe")
    gray_light = colors.HexColor("#f8fafc")
    gray_border = colors.HexColor("#e2e8f0")
    text_dark = colors.HexColor("#1e293b")
    text_muted = colors.HexColor("#64748b")

    style = TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0), violet),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        ("BACKGROUND", (0, 1), (0, -1), violet_light),
        ("TEXTCOLOR", (0, 1), (0, -1), violet),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 1), (0, -1), 9),

        ("TEXTCOLOR", (1, 1), (-1, -1), text_dark),
        ("FONTSIZE", (1, 1), (-1, -1), 9),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ("GRID", (0, 0), (-1, -1), 0.5, gray_border),

        ("ROWBACKGROUNDS", (1, 1), (-1, -1),
         [colors.white, gray_light]),

        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),

    ])

    tableau.setStyle(style)
    elements.append(tableau)

    elements.append(Spacer(1, 20))

    info_style = styles["Normal"]
    info_style.fontSize = 9
    info_style.textColor = text_muted

    elements.append(
        Paragraph(
            f"Total : {len(creneaux)} creneau(x) | "
            f"{len(salles)} salle(s) | "
            f"{len(planning)} examen(s)",
            info_style
        )
    )

    doc.build(elements)

    return chemin
