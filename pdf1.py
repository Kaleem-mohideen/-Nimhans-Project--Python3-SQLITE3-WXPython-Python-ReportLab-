from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm, inch
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import json
import csv
class Header:
	#__________Head part____________
	def __init__(self):
		
		fileName = "template2.pdf"
		documentTitle = "report"
		flag = False
		y = 780
		self.pdf = canvas.Canvas(fileName, pagesize=A4)
		self.pdf.setTitle(documentTitle)
		self.pdf.line(50, 795, 550,795)
		self.pdf.setFont("Helvetica-Bold", 10)
		self.drawMyRuler()
		# Data as JSON
		with open('Format2_sample3.json', 'r') as f:
			s = f.read()
			s = s.replace('\t','')
			s = s.replace("'", '"')
			s = s.replace('\n','')
			s = s.replace(',}','}')
			s = s.replace(',]',']')
			data1 = json.loads(s)

		for item in data1.items():
			self.align_text(item, flag, y)
			if flag:
				flag = False
				y-=20
			else:
				flag = True
		#self.pdf.drawText(data1)
		ResultTable(self, y)

	def align_text(self, item, flag, y):
		if flag:
			self.pdf.drawString(380, y, "%s: %s" %item)
		else:
			self.pdf.drawString(50, y, "%s: %s" %item)

	def drawMyRuler(self):
		self.pdf.drawString(100,810, 'x100')
		self.pdf.drawString(200,810, 'x200')
		self.pdf.drawString(300,810, 'x300')
		self.pdf.drawString(400,810, 'x400')
		self.pdf.drawString(500,810, 'x500')

		self.pdf.drawString(10,100, 'y100')
		self.pdf.drawString(10,200, 'y200')
		self.pdf.drawString(10,300, 'y300')
		self.pdf.drawString(10,400, 'y400')
		self.pdf.drawString(10,500, 'y500')
		self.pdf.drawString(10,600, 'y600')
		self.pdf.drawString(10,675, 'y675')
		self.pdf.drawString(10,700, 'y700')
		self.pdf.drawString(10,800, 'y800') 

class ResultTable:
	#________Table part________
	def __init__(self, parent, y):
		self.pdf = parent.pdf
		self.drawTable(y)

	def drawTable(self, y):
		
		# Data from CSV
		width, height = A4
		with open('sample.csv', "r") as csvfile:
		    data = list(csv.reader(csvfile))
		#print(data)
		styles = getSampleStyleSheet()
		colWidths = [
		    0.7 * cm,  # Column 0
		    3.1 * cm,  # Column 1
		    3.7 * cm,  # Column 2
		    1.2 * cm,  # Column 3
		    2.5 * cm,  # Column 4
		    6 * cm,  # Column 5
		    1.1 * cm,  # Column 6
		]
		y-=75 #change space (for header) here
		for index, row in enumerate(data):
			for col, val in enumerate(row):
				if col != 5 or index == 0 :
					data[index][col] = val.strip("'[]()")
				else:
					data[index][col] = Paragraph(val, styles['Normal'])
			t = Table([data[index]],style=[('GRID', (0,0), (-1,-1), 0.5, colors.black),('VALIGN',(0,0),(-1,-1),'TOP'),], colWidths=colWidths)
			t.hAlign = 'LEFT'
			w, h = t.wrap(width, height)
			x = self.coord_for_table(50, y)[0]
			y = height - (self.coord_for_table(50,y)[1] + h)
			#print(y)
			if height <= height-y:
				self.pdf.showPage()
				y = A4[1]
				w, h = t.wrap(width, height)
				y = height - (self.coord_for_table(50,y)[1] + h) - 4
				#drawMyRuler(self.pdf)
			t.drawOn(self.pdf, x, y)

		Footer(self, y)

	def coord_for_table(self, x, y, unit=1):
		height = A4[1]
		x, y = x * unit, height - y  * unit
		return x, y

class Footer:
	#________Footer part________
	def __init__(self, parent, y):
		self.pdf = parent.pdf
		y-=100
		if not y>=175:
			self.pdf.showPage()
			y = A4[1] - 75
		self.pdf.line(50, y, 550, y)
		self.pdf.line(150, y-20, 220, y-20)
		self.pdf.line(380, y-20, 450, y-20)
		self.pdf.setFont("Helvetica-Bold", 10)
		self.pdf.drawString(420, y-80, 'Authorized Signatory')
		self.pdf.setFont("Courier", 10)
		self.pdf.drawString(50, y-120, "* This is computer generated report,hence no signature is required.")
		self.pdf.line(50, y-175, 220, y-175)
		self.pdf.drawCentredString(290, y-175, "END OF REPORT")
		self.pdf.line(360, y-175, 550, y-175)
		self.pdf.save()

if __name__ == "__main__":
	#print(width, height)
	Header()