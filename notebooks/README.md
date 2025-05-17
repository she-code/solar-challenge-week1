# 🌞 Solar Radiation and Environmental Measurements Dataset

## 📄 Overview

This dataset contains time-series observations of solar radiation and various environmental parameters collected from **three different countries**. The data is derived from solar radiation measurement instruments and weather sensors, and is designed to support analysis for solar energy generation, weather modeling, and environmental forecasting.

## 🌍 Countries Covered

- Togo 
- Sierraleone 
- Benin  


## 📁 File Structure

Each row in the dataset represents a single timestamped measurement.

### Columns Description

| Column Name       | Unit / Type             | Description |
|-------------------|-------------------------|-------------|
| `Timestamp`       | yyyy-mm-dd hh:mm        | Date and time of the observation |
| `GHI`             | W/m²                    | Global Horizontal Irradiance |
| `DNI`             | W/m²                    | Direct Normal Irradiance |
| `DHI`             | W/m²                    | Diffuse Horizontal Irradiance |
| `ModA`            | W/m²                    | Irradiance from Module A |
| `ModB`            | W/m²                    | Irradiance from Module B |
| `Tamb`            | °C                      | Ambient air temperature |
| `RH`              | %                       | Relative Humidity |
| `WS`              | m/s                     | Wind Speed |
| `WSgust`          | m/s                     | Wind Gust Speed |
| `WSstdev`         | m/s                     | Wind Speed Standard Deviation |
| `WD`              | Degrees (°N to east)    | Wind Direction from North (clockwise) |
| `WDstdev`         | Degrees                 | Wind Direction Standard Deviation |
| `BP`              | hPa                     | Barometric Pressure |
| `Cleaning`        | Binary (1 = Yes, 0 = No)| Cleaning event occurred |
| `Precipitation`   | mm/min                  | Rainfall rate |
| `TModA`           | °C                      | Temperature of Module A |
| `TModB`           | °C                      | Temperature of Module B |
| `Comments`        | Text                    | Optional notes or remarks |

## 💡 Use Cases

- Solar panel performance modeling  
- Irradiance forecast modeling  
- Cleaning event impact analysis  
- Climate and environmental studies  
- Renewable energy resource evaluation  
