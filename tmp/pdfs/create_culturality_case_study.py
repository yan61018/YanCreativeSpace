from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    Flowable,
    Frame,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUT = Path("output/pdf/Culturality_Case_Study_Yan_Luo.pdf")
OUT.parent.mkdir(parents=True, exist_ok=True)

PAGE_W, PAGE_H = letter


INK = colors.HexColor("#171410")
MUTED = colors.HexColor("#6D6258")
PAPER = colors.HexColor("#F5EDDC")
CREAM = colors.HexColor("#FFF8E8")
PINK = colors.HexColor("#F6BFD0")
GOLD = colors.HexColor("#F4BD34")
GREEN = colors.HexColor("#8FA45E")
RED = colors.HexColor("#A9362D")
BLUE = colors.HexColor("#BCD0E8")
WINE = colors.HexColor("#3A0710")
LINE = colors.HexColor("#D8CDBB")


class Background(Flowable):
    def wrap(self, avail_width, avail_height):
        return (0, 0)

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(PAPER)
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

        # Soft color blocks, inspired by the website palette.
        c.setFillColor(PINK)
        c.setFillAlpha(0.52)
        c.circle(0.7 * inch, 9.7 * inch, 1.4 * inch, fill=1, stroke=0)
        c.setFillColor(BLUE)
        c.setFillAlpha(0.48)
        c.circle(7.9 * inch, 8.8 * inch, 1.7 * inch, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.setFillAlpha(0.24)
        c.circle(7.2 * inch, 1.4 * inch, 1.4 * inch, fill=1, stroke=0)
        c.setFillAlpha(1)

        # Light grid texture.
        c.setStrokeColor(colors.Color(1, 1, 1, alpha=0.35))
        c.setLineWidth(0.35)
        step = 18
        x = 0
        while x < PAGE_W:
            c.line(x, 0, x, PAGE_H)
            x += step
        y = 0
        while y < PAGE_H:
            c.line(0, y, PAGE_W, y)
            y += step
        c.restoreState()


def draw_pill(canvas, x, y, text, fill, text_color=INK):
    canvas.saveState()
    font = "Helvetica-Bold"
    font_size = 8.5
    pad_x = 10
    w = stringWidth(text, font, font_size) + pad_x * 2
    h = 19
    canvas.setFillColor(fill)
    canvas.roundRect(x, y, w, h, h / 2, fill=1, stroke=0)
    canvas.setFillColor(text_color)
    canvas.setFont(font, font_size)
    canvas.drawString(x + pad_x, y + 6, text)
    canvas.restoreState()
    return w


def first_page(canvas, doc):
    Background().drawOn(canvas, 0, 0)
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(1)
    canvas.rect(0.45 * inch, 0.45 * inch, PAGE_W - 0.9 * inch, PAGE_H - 0.9 * inch)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.65 * inch, 0.62 * inch, "Yan Luo | Culturality Case Study")
    canvas.drawRightString(PAGE_W - 0.65 * inch, 0.62 * inch, "Social + Event Marketing")
    canvas.restoreState()


styles = {
    "eyebrow": ParagraphStyle(
        "eyebrow",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=10,
        textColor=RED,
        uppercase=True,
        spaceAfter=8,
    ),
    "title": ParagraphStyle(
        "title",
        fontName="Times-Bold",
        fontSize=25.5,
        leading=28,
        textColor=INK,
        spaceAfter=10,
    ),
    "subtitle": ParagraphStyle(
        "subtitle",
        fontName="Helvetica",
        fontSize=11.2,
        leading=16,
        textColor=MUTED,
        spaceAfter=14,
    ),
    "section": ParagraphStyle(
        "section",
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13,
        textColor=INK,
        spaceAfter=5,
    ),
    "body": ParagraphStyle(
        "body",
        fontName="Helvetica",
        fontSize=9.4,
        leading=13.5,
        textColor=MUTED,
        spaceAfter=7,
    ),
    "bullet": ParagraphStyle(
        "bullet",
        fontName="Helvetica",
        fontSize=9.2,
        leading=13,
        leftIndent=10,
        firstLineIndent=-7,
        textColor=MUTED,
        spaceAfter=4,
    ),
    "metric": ParagraphStyle(
        "metric",
        fontName="Times-Bold",
        fontSize=24,
        leading=26,
        textColor=INK,
        alignment=1,
    ),
    "metric_label": ParagraphStyle(
        "metric_label",
        fontName="Helvetica-Bold",
        fontSize=7.8,
        leading=9,
        textColor=MUTED,
        alignment=1,
    ),
}


def box(title, body):
    return [
        Paragraph(title, styles["section"]),
        Paragraph(body, styles["body"]),
    ]


story = []
story.append(Background())
story.append(Paragraph("CASE STUDY", styles["eyebrow"]))
story.append(
    Paragraph(
        "Case Study: Growing Culturality's Campus Engagement Through Social & Event Marketing",
        styles["title"],
    )
)
story.append(
    Paragraph(
        "A campus-facing marketing initiative focused on building awareness, increasing Instagram engagement, and translating online attention into in-person event participation.",
        styles["subtitle"],
    )
)

metrics = Table(
    [
        [
            Paragraph("+20.2%", styles["metric"]),
            Paragraph("+5.3%", styles["metric"]),
            Paragraph("Event<br/>Turnout", styles["metric"]),
        ],
        [
            Paragraph("Profile activity", styles["metric_label"]),
            Paragraph("Follower growth", styles["metric_label"]),
            Paragraph("Supported through promotion", styles["metric_label"]),
        ],
    ],
    colWidths=[2.25 * inch, 2.25 * inch, 2.25 * inch],
    rowHeights=[0.48 * inch, 0.36 * inch],
)
metrics.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (0, -1), colors.Color(0.96, 0.75, 0.82, alpha=0.65)),
            ("BACKGROUND", (1, 0), (1, -1), colors.Color(0.76, 0.86, 0.95, alpha=0.75)),
            ("BACKGROUND", (2, 0), (2, -1), colors.Color(0.96, 0.74, 0.20, alpha=0.42)),
            ("BOX", (0, 0), (-1, -1), 0.8, LINE),
            ("INNERGRID", (0, 0), (-1, -1), 0.6, LINE),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]
    )
)
story.append(metrics)
story.append(Spacer(1, 0.18 * inch))

left = [
    *box(
        "Goal",
        "Increase Culturality's visibility on campus by strengthening social media presence, creating clearer event promotion, and encouraging students to move from online awareness to in-person participation.",
    ),
    Spacer(1, 0.06 * inch),
    *box(
        "Audience",
        "College students interested in culture, community, identity, international perspectives, and campus events that create space for connection and conversation.",
    ),
    Spacer(1, 0.06 * inch),
    *box(
        "My Role",
        "Supported content planning, event marketing, social media promotion, and audience-facing communication. Focused on making Culturality feel approachable, active, and relevant to student life.",
    ),
]

right = [
    Paragraph("What I Did", styles["section"]),
    Paragraph("- Developed social media content ideas around community, culture, and event participation.", styles["bullet"]),
    Paragraph("- Helped shape event promotion so students could quickly understand the purpose, timing, and value of attending.", styles["bullet"]),
    Paragraph("- Used platform performance signals to understand what content encouraged interaction.", styles["bullet"]),
    Paragraph("- Connected digital outreach with campus event marketing to support stronger turnout.", styles["bullet"]),
    Spacer(1, 0.08 * inch),
    Paragraph("Results", styles["section"]),
    Paragraph("Profile activity increased by 20.2%, followers grew by 5.3%, and event promotion supported stronger student turnout and awareness for Culturality's campus presence.", styles["body"]),
]

content = Table([[left, right]], colWidths=[3.18 * inch, 3.18 * inch])
content.setStyle(
    TableStyle(
        [
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (0, 0), (0, 0), colors.Color(1, 0.97, 0.91, alpha=0.82)),
            ("BACKGROUND", (1, 0), (1, 0), colors.Color(1, 0.97, 0.91, alpha=0.82)),
            ("BOX", (0, 0), (-1, -1), 0.8, LINE),
            ("INNERGRID", (0, 0), (-1, -1), 0.8, LINE),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 14),
            ("TOPPADDING", (0, 0), (-1, -1), 14),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ]
    )
)
story.append(content)
story.append(Spacer(1, 0.18 * inch))

reflection = Table(
    [
        [
            Paragraph("Strategic takeaway", styles["section"]),
            Paragraph(
                "Campus engagement grows when students can recognize themselves in the message. For Culturality, social content worked best when it connected culture to belonging, curiosity, and real event experiences.",
                styles["body"],
            ),
        ]
    ],
    colWidths=[1.6 * inch, 5.15 * inch],
)
reflection.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, -1), colors.Color(0.56, 0.64, 0.37, alpha=0.2)),
            ("BOX", (0, 0), (-1, -1), 0.8, LINE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]
    )
)
story.append(reflection)

doc = SimpleDocTemplate(
    str(OUT),
    pagesize=letter,
    rightMargin=0.65 * inch,
    leftMargin=0.65 * inch,
    topMargin=0.75 * inch,
    bottomMargin=0.75 * inch,
)
doc.build(story, onFirstPage=first_page)
print(OUT)
