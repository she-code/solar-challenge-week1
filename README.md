# 🌞 Solar Data Analysis – Benin, Sierra Leone & Togo

##  Project Overview

This project involves analyzing environmental data related to solar farms in **Benin**, **Sierra Leone**, and **Togo**. The goal is to identify trends, extract insights, and provide recommendations for optimal solar installation regions to support long-term sustainability and energy goals.

---

## Tools & Technologies

- Python  
- Pandas  
- NumPy  
- Matplotlib / Seaborn / Plotly  
- Jupyter Notebook  
- Git  
- Streamlit  

---

## Setup

1. **Clone the repository:**

```bash
git clone https://github.com/she-code/solar-challenge-week1.git
cd solar-challenge-week1
```

2. **Create a virtual environment:**

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

## Dataset Description
 
The dataset contains monthly environmental and solar-related measurements with the following columns:

timestamp: Date of observation 

GHI: Global Horizontal Irradiance 

DNI: Direct Normal Irradiance 

DHI: Diffuse Horizontal Irradiance 

ModA, ModB: Module power output values 

Tamb: Ambient temperature 

RH: Relative Humidity 

WS: Wind Speed 

WSgust: Wind Gust Speed 

WSstdev: Wind Speed Standard Deviation 

WD: Wind Direction 

WDstdev: Wind Direction Standard Deviation 

BP: Barometric Pressure 

Cleaning: Cleaning factor

Precipitation: Precipitation level 

TModA, TModB: Module temperatures 

country: Country name (for streamlit dahsboard)

region: Region name (for streamlit dahsboard)


## Streamlit Dashboard
 
Access the live dashboard here: [Solar Insights Streamlit App](https://solarinsightsfre.streamlit.app/)


