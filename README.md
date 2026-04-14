# DSA210_MyProject
Term project for Spring 2026

# Project Overview
This project analyzes personal scuba dive logs recorded by a Suunto Ocean diving computer. The goal is to investigate whether a significant inverse relationship exists between maximum dive depth and dive duration, motivated by the physiological constraints of nitrogen loading and decompression limits.

# Requirements
Python 3.12 or higher. Install dependencies with: pip install -r requirements.txt

# How to Reproduce
Step 1: Place your Suunto .fit dive log files in the data/ folder and run: python parse.py
This generates data/dives_parsed.csv. Note: raw .fit files are excluded from this repository as they contain personal data. The parsed CSV is provided instead.
Step 2: Run the analysis: python eda.py
This prints summary statistics and hypothesis test results to the console and saves all figures to the figures/ folder.

# Data
Source: Personal dive logs exported from the Suunto app in .fit format. Device: Suunto Ocean diving computer. Period: July 2024 to January 2026. Total logs: 118 raw dives. After noise filtering: 85 clean dives. Variables: Date, Maximum Depth (m), Duration (seconds), Avg Temperature (C), Min Temperature (C).

# Hypothesis
H0: There is no significant relationship between maximum dive depth and dive duration.
HA: Deeper dives have significantly shorter durations due to nitrogen loading and decompression constraints.

# Key Findings
All three hypothesis tests (t-test, Mann-Whitney U, Spearman correlation) returned non-significant results. The data do not support the hypothesis. Dive duration appears consistent regardless of depth, suggesting that as an experienced diver, bottom time is planned consistently across all depths.

# AI Assistance Disclosure
This project was developed with assistance from Claude (Anthropic). AI assistance was used for data parsing code and EDA structure. All core decisions were made independently by me, including the project idea, hypothesis formulation, choice of data source, data cleaning rules and thresholds, interpretation of results, and selection of appropriate hypothesis tests based on course material. I also identified and resolved issues with the raw data format, determined noise filtering criteria based on personal domain knowledge as a certified diving instructor, and drew all analytical conclusions from the results.
