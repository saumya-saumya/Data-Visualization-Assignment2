#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 13:49:50 2019

@author: shraddhanagargoje
"""

from PIL import Image
import plotly.graph_objects as go
import plotly.offline as py

"""
Class to hold a figure for data
"""
class CoverageFigure:
    def __init__(self):
        self.figure = go.Figure()

    """
    Initializes layout of figure
    """
    def initialize_layout(self, img):
        self.figure.update_layout(
            title = go.layout.Title(
                text = 'Fixation Visualization',
                xref = 'paper',
                x = 0.5,
                font = dict(
                    size=36,
                    color = 'black'
                ),
                xanchor = 'center'
            ),
            width = 1600,
            height = 1200,

            legend=dict(
                y = 0.91,
                font = dict(
                    size = 30
                )
            ),

            hoverlabel = dict(
                bgcolor = 'pink',
                font = dict(
                    size = 15
                )
            ),

            images = [go.layout.Image(
                source = Image.open(img),
                opacity = 1.0,
                xref = 'x',
                yref = 'y',
                x = 0,
                y = 0,
                sizex = 1600,
                sizey = 1200,
                sizing = 'stretch',
                layer='below'
            )],

            shapes=[
                go.layout.Shape(
                    type="rect",
                    x0=0,
                    y0=0,
                    x1=1600,
                    y1=1200,
                    fillcolor='black',
                    layer='below'
                )
            ],

            xaxis=dict(
                showline=True,
                showgrid = False,
                mirror=True,
                #tickfont = dict(size = 30),
                linewidth=2,
                linecolor='black',
                #gridcolor='#000000',
                range=[0, 1600],
                tickvals = []
                #tickvals=[k*200+100 for k in range(0, 8)],
                #ticktext=['1', '2', '3', '4', '5', '6', '7', '8', '9']

            ),
            yaxis=dict(
                showline=True,
                showgrid = False,
                mirror=True,
                #tickfont = dict(size = 30),
                linewidth=2,
                linecolor='black',
                #gridcolor='#000000',
                range=[1200, 0],
                tickvals = []
                #tickvals=[k*200+100 for k in range(0, 6)],
                #ticktext=['A', 'B', 'C', 'D', 'E', 'F', 'G']
            )
        )

    """
    Updates figure data/traces
    """
    def update_data(self, data):
        self.figure.data = None

        for trace in data:
            self.figure.add_trace(trace)

        self.figure.data[0].visible = True
        self.figure.data[int(len(data)/2)].visible = True

    """
    Updates figure layout with sliders
    """
    def update_layout(self, sliders, updatemenus):
        self.figure.update_layout(
            sliders=sliders,
            updatemenus = updatemenus,
            showlegend = True,
        )

    """
    Saves figure as html
    """
    def show(self, file_path, file_name):
        py.plot(self.figure, filename=file_path + file_name + '.html')