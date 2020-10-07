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
	def __init__(self, data1, data):
		
		self.fileName = data1['reportFile']
		documentTitle = "report"
		flag = False
		y = 780
		self.pdf = canvas.Canvas(self.fileName, pagesize=A4)
		self.pdf.setTitle(documentTitle)
		self.pdf.line(50, 795, 550,795)
		self.pdf.setFont("Helvetica-Bold", 10)
		#self.drawMyRuler()

		for item in data1.items():
			if item[0] != 'reportFile':
				self.align_text(item, flag, y)
				if flag:
					flag = False
					y-=20
				else:
					flag = True
		#self.pdf.drawText(data1)
		ResultTable(self, y, data)

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
	def __init__(self, parent, y, data):
		self.pdf = parent.pdf
		self.fileName = parent.fileName
		self.drawTable(y, data)

	def drawTable(self, y, data):
		
		width, self.height = A4

		print(data)
		styles = getSampleStyleSheet()
		colWidths = [
		    5.7 * cm,  # Column 0
		    4.7 * cm,  # Column 1
		    7.7 * cm,  # Column 2
		]
		y -= 0 # Trigger here to check
		for assayId in data:
			y -= 75 #change space (for header) here
			flag = 1
			dataTable = data[assayId]
			for index, row in enumerate(dataTable):
				for col, val in enumerate(row):
					dataTable[index][col] = Paragraph(val, styles['Normal'])

				if flag:
					######### Heading #############
					t1 = Table([["Antibodies", "Results", "Comments"]], style=[('ALIGN',(0,0),(-1,-1),'CENTER'),], colWidths=colWidths)
					t1.setStyle (TableStyle ([('VALIGN',(0,0),(-1,-1),'TOP'),
											  # ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
											  ('FONTSIZE', (0, 0), (-1, -1), 14),
											  ('TEXTFONT', (0, 0), (-1, -1), 'Times-Bold')]))

					w1, h1 = t1.wrap(width, self.height)
					x, y = self.endCoOrdToDrawTable(y, h1)
					t1.drawOn(self.pdf, x, y)
					y-=5
					flag = 0
					###############################

				t = Table([dataTable[index]], style=[('GRID', (0,0), (-1,-1), 0.5, colors.black),('VALIGN',(0,0),(-1,-1),'TOP'),('ALIGN',(0,1),(-1,1),'CENTER'),], colWidths=colWidths)
				t.hAlign = 'LEFT'
				w, h = t.wrap(width, self.height)
				x, y = self.endCoOrdToDrawTable(y, h)
				# x = self.coord_for_table(50, y)[0]
				# y = self.height - (self.coord_for_table(50,y)[1] + h)
				#print(y)
				if self.height <= (self.height-y) + 50:
					self.pdf.showPage()
					y = 780
					######### Heading #############
					t1 = Table([["Antibodies", "Results", "Comments"]], style=[('ALIGN',(0,0),(-1,-1),'CENTER'),], colWidths=colWidths)
					t1.setStyle (TableStyle ([('VALIGN',(0,0),(-1,-1),'TOP'),
											  # ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
											  ('FONTSIZE', (0, 0), (-1, -1), 14),
											  ('TEXTFONT', (0, 0), (-1, -1), 'Times-Bold')]))

					w1, h1 = t1.wrap(width, self.height)
					y = self.endCoOrdToDrawTable(y, h1)[1]
					t1.drawOn(self.pdf, x, y)
					###############################
					y-=5
					w, h = t.wrap(width, self.height)
					y = self.endCoOrdToDrawTable(y, h)[1]
				t.drawOn(self.pdf, x, y)

		Footer(self, y)

	def endCoOrdToDrawTable(self, y, h):
		xdownWeightTook, ydownWeightTook = self.coord_of_space_took_byY(50,y)
		xPdfCoOrdEndToFitAndDraw = xdownWeightTook
		totalSpaceTookByY = (ydownWeightTook + h)
		yPdfCoOrdEndToFitAndDraw = self.height - totalSpaceTookByY
		return xPdfCoOrdEndToFitAndDraw, yPdfCoOrdEndToFitAndDraw

	def coord_of_space_took_byY(self, x, y, unit=1):
		x, y = x * unit, self.height - y  * unit
		return x, y

class Footer:
	#________Footer part________
	def __init__(self, parent, y):
		self.pdf = parent.pdf
		y-=100
		if not y>=175+50:
			self.pdf.showPage()
			y = 780
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
	print(width, self.height)
	#Header()