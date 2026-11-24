# London AirCast
London AirCast is a data engineering project that uses the London Air Quality Network (LAQN) API to collect, process and analyse historical air polution measurements across London.

The aim is to at somepoint develop an interactive website that allows users to explore pollution level across London and replay historical measurements using an animated map. 

**Status:** In development

## 1. What I will build 

The planned application will allow users to:

- Explore air pollution measurements across London monitoring stations.
- Replay historical pollution llevels using an interactive map and timeline slider.

The project primarily focuses on building a reliable and reproducable data engineering pipeline.


### Repository structure

    london-aircast/
    |
    |-- data/
    |   |-- raw/
    |   |   |-- readings/
    |   |   |   `-- *.json
    |   |   |-- site_species.json
    |   |   |-- sites.json
    |   |   `-- species.json
    |   |
    |   `-- london_aircast.duckdb
    |
    |-- exploration/
    |   |-- date_distribution.py
    |   |-- inspect_api.py
    |   `-- monitoring_site_operating_periods.py
    |
    |-- sql/
    |   |-- 01_create_staging.sql
    |   `-- 02_profile_readings.sql
    |
    |-- src/
    |   |-- explore_api.py
    |   |-- extract_readings.py
    |   |-- load_staging.py
    |   |-- setup_database.py
    |   `-- transform_readings.py
    |
    |-- .gitignore
    `-- README.md

### Source
The project uses data from the London Air Quality Network (LAQN), operated by the Environmental Research Group at Imperial Collage London.

API documentation:
https://api.erg.ic.ac.uk/AirQuality/help

LAQN website
https://www.londonair.org.uk/

### AIP endpoints
...


### Folder descriptions
**data/**
Contains API responses and the local DuckDB database.

**exploration/**
Contains scripts used to explore the API.

**src/**
Contains the Python scripts used to extract, transform and load data.

**sql/**
Contains SQL scripts for setting up the database, data profiling and further transformations.