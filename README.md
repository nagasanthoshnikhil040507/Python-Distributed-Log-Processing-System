Python Based Distributed Log Processing System (with PySpark)

Project Overview
This project implements a Distributed Log Processing System using PySpark to efficiently analyze large-scale log data. The system ingests, parses, and processes log files, identifies critical errors, extracts key metrics, and provides interactive visual insights via a Streamlit dashboard. A synthetic log dataset was used for testing and demonstration purposes.
The project is divided into two main parts:
Log Processing using PySpark in Jupyter Notebook.
Dashboard Visualization using Streamlit in VS Code.


Features:

Distributed Log Processing: Handles large volumes of log data efficiently using PySpark.


Log Parsing & Analytics:

Extracts relevant fields like timestamp, log level, message, IP address.

Identifies error types and their frequency.

Tracks trends and aggregates metrics (e.g., errors per hour, requests per endpoint).

Reporting & Alerts:

Generates analytics reports in CSV/JSON format.

Configurable alert system for critical events.


Future Enhancements:

Integrate real-time log streaming using Kafka.

Add user authentication to the dashboard.

Extend alert system to send real notifications (email/SMS).

Support multiple log formats and sources.


Interactive Dashboard:

Visualizes key metrics, top errors, and trends.

Filters logs by date range, log level, and other fields.


Tech Stack:

Python 3.x

PySpark

Jupyter Notebook (for development and log analysis)

Streamlit (for interactive dashboard)

Pandas (for data manipulation)

Plotly / Matplotlib (for visualizations)
