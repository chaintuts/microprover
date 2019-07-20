# This file contains code for visualizing data computed by the core hobbystats modules
#
# Author: Josh McIntyre
#
import argparse
import csv
import datetime
import numpy
import matplotlib
from matplotlib import pyplot
import dateutil
import collections

# Format the raw CSV data
def format_data():

    data = []
    with open("pow_log.csv", "r") as f:
        dr = csv.DictReader(f)

        # For each run, get the target and number of attempts from the
        # above data structures
        # We need a list of attempts per target for graphing
        # For example, target 01000000 may have runs with attempts 5, 4, 8
        data = {}
        for run in dr:
            target = run["Target"]
            if not target in data:
                data[target] = []
            data[target].append(run["Attempts"])

    return data 
        
# This function plots a graph
def graph_pow_bar(data, title="Proof of Work Attempts", xlabel="Target (Binary)", ylabel="Attempts"):

    # Set up the basic plot
    dimensions = matplotlib.figure.SubplotParams(left=0.05, right=0.9)
    fig, ax = pyplot.subplots(subplotpars=dimensions)
    barwidth = 0.2

    # Generate the labels for the chart
    xlabels = [ target for target, attempts in data.items() ]

    # For the y axes, simply get each list of attempts
    yaxes = [ attempts for target, attempts in data.items() ]

    # For the x axes, group together attempts for the same target
    xaxes = []
    for i in range(0, len(yaxes)):
        x = [ i ]
        for c in range(0, len(yaxes[i]) - 1):
            x.append(x[c] + barwidth)
        xaxes.append(x)

    # Plot the bar chart
    for i in range(0, len(xaxes)):
        bars = ax.bar(xaxes[i], yaxes[i], width=0.2, color="bgry")

    # Add annotations
    xticks = []
    for i in range(0, len(xlabels)):
        offset = ( len(xaxes[i]) / 2 ) * barwidth - ( barwidth / 2 )
        xticks.append(i + offset)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels, rotation=90)

    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)
    pyplot.title(title)

    # Render the chart
    pyplot.tight_layout()
    pyplot.show()
    return fig, ax

if __name__ == "__main__":
    data = format_data()
    graph_pow_bar(data)    

