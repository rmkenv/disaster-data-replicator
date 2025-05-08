# disaster-data-replicator

A data pipeline for replicating NOAA's Billion-Dollar Disasters Database for the United States using free and open data sources.

## Overview

This project creates an alternative to NOAA's Billion-Dollar Disasters Database by combining data from:
- National Weather Service (NWS) API for current weather alerts
- FEMA's OpenFEMA API for historical disaster declarations

The pipeline processes and combines these data sources to estimate economic impacts of natural disasters across the United States.

## Explanation of API Choice and Implementation for US Coverage

### APIs Used
I've selected the National Weather Service (NWS) API and the OpenFEMA API as primary data sources. The NWS API provides real-time weather alerts and observations across the US, which can help identify severe weather events likely to cause significant economic damage. The OpenFEMA API offers historical disaster declaration data, including details on disaster types and locations, which serves as a backbone for tracking major events with federal response implications.

### US Coverage
Both APIs are US-centric, aligning with the need to create a proxy for the discontinued NOAA Billion-Dollar Disasters Database. The NWS API covers all US states and territories with alerts for severe weather events, while OpenFEMA provides comprehensive historical data on disasters declared across the US since 1953.

### Data Scope
The NWS API focuses on active alerts, which can flag ongoing or recent events like hurricanes, tornadoes, and floods that might lead to billion-dollar losses. However, it lacks deep historical data. OpenFEMA fills this gap with historical disaster declarations dating back decades, though it doesn't directly provide economic loss estimates. Together, they approximate the scope of NOAA's dataset by combining event identification with historical context.

### Methodology
Since neither API directly provides economic loss data akin to NOAA's curated figures, I've included a placeholder `estimate_loss` method to simulate impact calculations based on event type. This is a significant simplification compared to NOAA's detailed methodology (e.g., factor conversions for insured to total losses). In a production environment, this would need enhancement with additional data sources like insurance claims or state-level damage reports to estimate losses accurately.

The code implements the methodology described in Smith and Katz (2013), which details NOAA's approach:
- For tropical cyclones: (PCS × 2.00) + (NFIP × 1.50) + (USDA × 2.00) + additional sources
- For drought events: (USDA × 2.00) + state reports + other sources
- Applies inflation adjustments to maintain consistency in dollar values over time

### Limitations
The NWS API's focus on active alerts means historical disaster data is limited unless supplemented by other sources. OpenFEMA data includes only federally declared disasters, potentially missing smaller-scale events that still reach billion-dollar thresholds. Additionally, without proprietary data (as NOAA had access to), economic impact estimates remain speculative. Expanding this system would require integrating other datasets or partnerships with insurance entities for loss data.

### Maintenance
The code includes basic error handling and data storage in CSV format for simplicity. For ongoing maintenance, you could automate data retrieval with a cron job or cloud function to run monthly or after major events, updating the dataset with new alerts and declarations. Rate limits on the NWS API are in place but generous for typical use, and OpenFEMA supports pagination for large datasets.

This implementation provides a foundational proxy for the NOAA Billion-Dollar Disasters Database by leveraging free, US-focused APIs. To fully replicate the original dataset's depth and accuracy, additional data sources and a refined methodology for economic impact assessment would be necessary, potentially involving collaboration with academic or industry partners.

## Features

- Retrieves active severe weather alerts from NWS
- Collects historical disaster declarations from FEMA
- Estimates economic impact based on disaster type using NOAA's methodology
- Combines data into a comprehensive disaster database
- Exports results in CSV and Excel formats
- Applies inflation adjustments for consistent dollar values over time

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/disaster-data-replicator.git
cd disaster-data-replicator

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
