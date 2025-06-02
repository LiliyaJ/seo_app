# An Easy SEO App

This project was created to demonstrate the possibilities of cloud computing in combination with tools from the Google ecosystem. It’s designed as an educational resource for students to understand how scalable, data-driven applications can be built using modern technologies.

**Tech stack:**

- **Cloud Run** – for deploying and running containerised Python applications
- **BigQuery** – for storing and analysing large datasets
- **Google Sheets** – as a simple front-end interface
- **Apps Script** – to connect Sheets with APIs and backend logic
- **Python** – for data processing and integration
- **External APIs** – for fetching SEO-related data

## 1. Features

This app demonstrates how to build a cloud-based data pipeline using Google tools and Python.

- Pulls SEO data from the DataForSEO API
- Transforms the JSON response into a list
- Stores the data in BigQuery and sends it back to the **Output** tab in Google Sheets
- Allows users to interact with the app via Google Sheets
- Automatically updates data using Cloud Run and Apps Script

## 2. Architecture

The diagram below shows how the components of the SEO app interact:

![Architecture Diagram](image/seo_app_diagram.jpg)
