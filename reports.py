#!/usr/bin/env python3

import reportlab

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table, Image 
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from pandas import DataFrame
import numpy as np

import re

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
  pie_drawing = Drawing(300, 175)

  report_piechart = Pie()
  report_piechart.x = 65
  report_piechart.y = 15
  report_piechart.width = 120
  report_piechart.height = 120

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

  pie_drawing.add(report_piechart)

# add bar chart
  bar_drawing = Drawing(300, 175)

  columns = table_data[0]
  table_data = table_data[1:]

  # calculates total revenue from car sales and price
  df['Revenue'] = df['Price']
  
  # removes '$' from Price data, calculats total revenue, 
  # and creates a new Revenue column 
  newlist = []
  for element in (df.loc[:,'Revenue'].values.tolist()):
      newelem = re.sub('[$]', '', element)
      newlist.append(float(newelem))
  df['PriceAsFloat'] = newlist
  df['Revenue'] = df['Total Sales'] * df['PriceAsFloat']
  # sorts dataframe in descending order according to Revenue, resets index otherwise   # a KeyError will occur because the indexes will be out-of-order
  sorted_df = df.sort_values(by=['Revenue'],ascending=False).reset_index(drop = True)
  data = [
  sorted_df.loc[0:10,'Revenue'].values.tolist(), ] 

  bc=VerticalBarChart()
  bc.x = 65  # horizontal position
  bc.y = 15  # vertical position 
  bc.height = 120 # height of the chart area
  bc.width = 270  # width of the chart area
  bc.data = data
  bc.strokeColor = colors.black
  bc.bars[0].fillColor=colors.yellow
  bc.groupSpacing = 24
  bc.barSpacing = 2
  bc.valueAxis.valueMin = 0
  bc.valueAxis.valueMax = 15000000
  bc.valueAxis.valueStep = 1000000
  bc.categoryAxis.labels.boxAnchor = 'ne'
  bc.categoryAxis.labels.dx = -5
  bc.categoryAxis.labels.dy = 0
  bc.categoryAxis.labels.angle = 30
  bc.categoryAxis.categoryNames = sorted_df.loc[0:10,'Car'].values.tolist()

  bar_drawing.add(bc)


  empty_line = Spacer(1,20)
  report.build([report_title, empty_line, report_info, empty_line, report_table, pie_drawing, bar_drawing])
