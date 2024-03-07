# Overview
InfluxLogImporter is a Python utility designed to import metric logs into InfluxDB, a time-series database, from various data sources including flat files (CSV, JSON), APIs, and other databases. It automates the process of data transformation and loading, ensuring that metrics are stored efficiently for analysis, monitoring, and alerting purposes. This tool is particularly useful for DevOps, data engineers, and analysts looking to centralize their metric logs for better observability and operational intelligence.

# Features
Supports importing from CSV, JSON files, and external APIs.
Customizable mapping to transform data into InfluxDB-compatible schemas.
Batch processing for efficient data import.
Error handling and logging for reliable imports.
CLI for easy integration with automation scripts.

# Requirements
Python 3.8+
InfluxDB 2.0+
Requests (for API data fetching)
Pandas (for data manipulation)

# Configuration
Before running the importer, configure your data sources and InfluxDB connection settings in config.py. This includes specifying the source file paths or API endpoints, data formats, and InfluxDB credentials (URL, bucket, org, and token).

# Usage
## Importing Data
Run the importer with the following command:

# Copy code
python import.py

# Command-Line Arguments
--source: Specify the data source type (file, api).
--path: Path to the data file or API endpoint URL.
--format: Data format (csv, json).
