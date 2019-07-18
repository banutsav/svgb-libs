#!/bin/python

import os
import logging
import datetime
import numpy as np
import colorsys
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from pathlib import Path

# Create and save a Donut chart
def saveDonutChart(data, labels, plt, des, filename):
	# Explode the slices
	explode = (0.05,)*(len(labels))
	colors = getUniqueColors(len(labels))
	patches, texts, autotexts = plt.pie(data, labels=labels, colors=colors, startangle=90, explode=explode, pctdistance=0.85, autopct='%.2f%%')
	# Make texts grey, hence lighter	
	for text in texts:
		text.set_color('grey')
	
	# Draw circle to create donut chart
	centre_circle = plt.Circle((0,0),0.70,fc='white')
	fig = plt.gcf()
	fig.gca().add_artist(centre_circle)
	plt.tight_layout()
	
	# Save and clear
	plt.savefig(getFilePath(des, filename, 0))
	plt.clf()

# Construct a list of unique colors to be used for plotting
def getUniqueColors(num_colors):
    colors=[]
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i/360.
        lightness = (50 + np.random.rand() * 10)/100.
        saturation = (90 + np.random.rand() * 10)/100.
        colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
    return colors

# Save a single line graph
def saveLineGraph(plt,x_label,y_label,title,des,filename):
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.title(title)
	plt.tight_layout()
	plt.legend()
	plt.savefig(getFilePath(des, filename, 0))
	plt.clf()

# Standard source and destination folders for all projects
def getDataSource():
	data_source = Path(Path(os.getcwd()) / 'input')
	logging.info('Data Source is set to ' + str(data_source))
	return data_source

def getDataDestinantion():
	output_des = Path(Path(os.getcwd()) / 'output')
	logging.info('Data Destination is set to ' + str(output_des))
	return output_des

# Specify the log file and start logging
def setLogging():
	name = 'logs/log.txt'
	log_file = Path(Path(os.getcwd()) / name)
	print('In case you need them, the log files are at ' + str(log_file))
	logging.basicConfig(level=logging.INFO, filename=log_file, filemode='w', format='%(levelname)s - %(message)s')
	logging.info('Execution started for ' + name + ' at ' + str(datetime.datetime.now()))

# Check if the required file exists and return path
# Type=1(input, read from file), 0(output, write to file)
def getFilePath(data_source, filename, type):
    data_folder = Path(data_source)
    file_to_open = data_folder / filename
    file_path = Path(file_to_open)

    if type==0:
    	logging.info('Output file: ' + str(file_path))
    	return file_to_open

    logging.info('Searching for file: ' + str(file_to_open))
    if not file_path.exists() and type==1:
        logging.info('Oops, the file ' + str(file_path) + ' does not exist...')
        return 0
    
    logging.info('Yay, file exists...')

    return file_to_open

# Create a Data Frame 
def createDataFrame(data, column_values, index=None):
	logging.info('Creating a Data frame...')
	df = pd.DataFrame(data, columns = column_values)
	if index is not None:
		df.set_index(index, inplace=True)
	return df

# Get data from CSV, construct dataframe and return
def putCSVToDf(source, file, index=None):
	file_path = getFilePath(source, file, 1)
	logging.info('Importing data from ' + str(file_path) + ' into a DataFrame')
	df = pd.read_csv(file_path)
	if index is not None:
		df.set_index(index, inplace=True)
	return df

# Write a DataFrame to CSV output file    
def writeDfToCSV(df, source, filename):
	out_file_path = getFilePath(source, filename, 0)
	logging.info('Writing DataFrame to output file ' + str(out_file_path))
	df.to_csv(out_file_path)

