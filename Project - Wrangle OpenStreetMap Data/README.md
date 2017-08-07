# Project - Scraping US Air Traffic Data

## Instructions
To perform this analysis on your own (**NOTE**: these are heavy files):

* Download <a href = "https://mapzen.com/data/metro-extracts/metro/new-delhi_india/"> the PBF version of the New Delhi dataset</a>, rename it as *new-delhi_01.osm* and convert it to XML (you can use *osmconvert64*)
* run *process_map* from the notebook to generate 2 CSV files, *nodes.csv* & *nodes_tags.csv*
* Enter your DB credentials and transfer the generated CSV to the databases
* *Directory Information* contains more information about the files in the directory

## Overview
The aim of this project is to explore the OpenStreetMap data, to clean the downloaded parts of the Delhi dataset, and find some features of the data.

## Techniques
* Data Wrangling
* Data Cleaning
* Data Conversion
* Database Management 
* Database Manipulation
 
## Python libraries used
* MySQLdb
* xml
* csv
* cereberus
* pprint
* re

## References
* <a href = "https://classroom.udacity.com/nanodegrees/nd002/parts/860b269a-d0b0-4f0c-8f3d-ab08865d43bf/modules/316820862075463/lessons/3168208620239847/project"> Udacity Nanodegree Program </a>