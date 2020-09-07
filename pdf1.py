from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm, inch
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import json
import csv

fileName = "template2.pdf"
documentTitle = "report"
y = 780
flag = False
width, height = A4

def drawMyRuler(pdf):
	pdf.drawString(100,810, 'x100')
	pdf.drawString(200,810, 'x200')
	pdf.drawString(300,810, 'x300')
	pdf.drawString(400,810, 'x400')
	pdf.drawString(500,810, 'x500')

	pdf.drawString(10,100, 'y100')
	pdf.drawString(10,200, 'y200')
	pdf.drawString(10,300, 'y300')
	pdf.drawString(10,400, 'y400')
	pdf.drawString(10,500, 'y500')
	pdf.drawString(10,600, 'y600')
	pdf.drawString(10,700, 'y700')
	pdf.drawString(10,800, 'y800')

def align_text(item, flag, y):
	if flag:
		pdf.drawString(380, y, "%s: %s" %item)
	else:
		pdf.drawString(50, y, "%s: %s" %item)

def coord(x, y, unit=1):

    x, y = x * unit, height - y  * unit
    return x, y    


pdf = canvas.Canvas(fileName, pagesize=A4)
pdf.setTitle(documentTitle)

#drawMyRuler(pdf)
pdf.line(50, 795, 550,795)
pdf.setFont("Helvetica-Bold", 10)

with open('Format2_sample3.json', 'r') as f:
	s = f.read()
	s = s.replace('\t','')
	s = s.replace("'", '"')
	s = s.replace('\n','')
	s = s.replace(',}','}')
	s = s.replace(',]',']')
	data1 = json.loads(s)

for item in data1.items():
	align_text(item, flag, y)
	if flag:
		flag = False
		y-=20
	else:
		flag = True

# Data from CSV
with open('sample.csv', "r") as csvfile:
    data = list(csv.reader(csvfile))


styles = getSampleStyleSheet()

all_cells = [(0, 0), (-1, -1)]
header = [(0, 0), (-1, -1)]
column0 = [(0, 0), (0, -1)]
column1 = [(1, 0), (1, -1)]
column2 = [(2, 0), (2, -1)]
column3 = [(3, 0), (3, -1)]
column4 = [(4, 0), (4, -1)]
column5 = [(5, 0), (5, -1)]
column6 = [(6, 0), (6, -1)]
table_style = TableStyle([
    ('VALIGN', all_cells[0], all_cells[1], 'TOP'),
   # ('LINEBELOW', header[0], header[1], 1, colors.black),
    ('ALIGN', column0[0], column0[1], 'LEFT'),
    ('ALIGN', column1[0], column1[1], 'LEFT'),
    ('ALIGN', column2[0], column2[1], 'LEFT'),
    ('ALIGN', column3[0], column3[1], 'RIGHT'),
    ('ALIGN', column4[0], column4[1], 'RIGHT'),
    ('ALIGN', column5[0], column5[1], 'LEFT'),
    ('ALIGN', column6[0], column6[1], 'RIGHT'),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX',(0,0),(-1,-1),1,colors.black),
])


colWidths = [
    0.7 * cm,  # Column 0
    3.1 * cm,  # Column 1
    3.7 * cm,  # Column 2
    1.2 * cm,  # Column 3
    2.5 * cm,  # Column 4
    6 * cm,  # Column 5
    1.1 * cm,  # Column 6
]


for index, row in enumerate(data):
    for col, val in enumerate(row):
        if col != 5 or index == 0:
            data[index][col] = val.strip("'[]()")
        else:
            data[index][col] = Paragraph(val, styles['Normal'])

t = Table(data, colWidths=colWidths, repeatRows=1, splitByRow=1)
t.hAlign = 'LEFT'
t.setStyle(table_style)

#print(height)
#print(y)

pdf.saveState()
w, h = t.wrapOn(pdf, width, height)
#print(w , h )
x = coord(50, y)[0]
y = height - (coord(50,y)[1] + h) - 75
t.drawOn(pdf, x, y)
#pdf.showPage()

#pdf.drawText(text)
pdf.line(50, y-100, 550, y-100)
pdf.line(150, y-120, 220, y-120)
pdf.line(380, y-120, 450, y-120)
pdf.setFont("Helvetica-Bold", 10)
pdf.drawString(420, y-180, 'Authorized Signatory')
pdf.setFont("Courier", 10)
pdf.drawString(50, y-220, "* This is computer generated report,hence no signature is required.")
pdf.line(50, y-275, 220, y-275)
pdf.drawCentredString(290, y-275, "END OF REPORT")
pdf.line(360, y-275, 550, y-275)
pdf.save()


