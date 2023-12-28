#!/usr/bin/env python3

import reportlab

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table, Image 
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from pandas import DataFrame
import numpy as np

def generate(filename, title, additional_info, table_data):
  styles = getSampleStyleSheet()
  report = SimpleDocTemplate(filename)
  report_title = Paragraph(title, styles["h1"])
  report_info = Paragraph(additional_info, styles["BodyText"])
  table_style = [('GRID', (0,0), (-1,-1), 1, colors.black),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('ALIGN', (0,0), (-1,-1), 'CENTER')]
  report_table = Table(data=table_data, style=table_style, hAlign="LEFT")

  # add pie chart
  drawing = Drawing(450, 225)

  report_piechart = Pie()
  report_piechart.x = 65
  report_piechart.y = 15
  report_piechart.width = 140
  report_piechart.height = 140

  columns = table_data[0]
  table_data = table_data[1:]
  df = DataFrame(table_data,columns=columns)
  report_piechart.data = df.loc[:,'Total Sales'].values.tolist()
  report_piechart.labels = df.loc[:,'Car'].values.tolist()

  report_piechart.slices.strokeWidth=0.5
  report_piechart.slices[3].popout = 10
  report_piechart.slices[3].strokeWidth = 2
  report_piechart.slices[3].strokeDashArray = [2,2]
  report_piechart.slices[3].labelRadius = 1.75
  report_piechart.slices[3].fontColor = colors.red

  report_piechart.sideLabels = True

  drawing.add(report_piechart)

  # add bar chart

  empty_line = Spacer(1,20)
  report.build([report_title, empty_line, report_info, empty_line, report_table, drawing])
