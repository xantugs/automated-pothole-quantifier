# Automated Pothole Quantifier

## Result
![Demo Result](demo_result.png)
*Automated detection and area measurement of road defects.*

## Overview
This tool uses Computer Vision (OpenCV) to automatically detect, outline, and measure the area of potholes in road imagery. It uses Canny Edge Detection and morphological transformations to distinguish potholes from road texture and gravel.

## Features
- **Noise Filtering:** Uses solidity and aspect ratio checks to ignore loose gravel and road markings.
- **Area Calculation:** Converts pixel area to approximate real-world square meters.
- **Visual Output:** Draws bounding boxes and contours for visual verification.

## Usage
1. Install dependencies: `pip install -r requirements.txt`
2. Run the script: `python pothole_detector.py`