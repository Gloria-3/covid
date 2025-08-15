# covid_tracker.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
import urllib.request

def main():
    print("COVID-19 Data Analysis Starting...")
    
    # Step 1: Data Collection
    print("\nDownloading dataset...")
    try:
        urllib.request.urlretrieve(
            "https://covid.ourworldindata.org/data/owid-covid-data.csv",
            "owid-covid-data.csv"
        )
        print("Dataset downloaded successfully!")
    except Exception as e:
        print(f"Download failed: {e}")
        return

    # Step 2: Data Loading
    print("\nLoading data...")
    df = pd.read_csv('owid-covid-data.csv')
    print(f"\nDataset shape: {df.shape}")
    print("\nFirst 5 rows:")
    print(df.head())

    # Step 3: Data Cleaning
    print("\nCleaning data...")
    df['date'] = pd.to_datetime(df['date'])
    countries = ['United States', 'India', 'Brazil', 'United Kingdom', 'Kenya', 'South Africa']
    df_filtered = df[df['location'].isin(countries)].copy()
    
    cols_to_fill = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths',
                   'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated']
    df_filtered[cols_to_fill] = df_filtered.groupby('location')[cols_to_fill].fillna(method='ffill')
    
    df_filtered['death_rate'] = df_filtered['total_deaths'] / df_filtered['total_cases']
    df_filtered['vaccination_rate'] = df_filtered['people_vaccinated'] / df_filtered['population']

    # Step 4: EDA
    print("\nGenerating visualizations...")
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_filtered, x='date', y='total_cases', hue='location')
    plt.title('Total COVID-19 Cases Over Time')
    plt.ylabel('Total Cases')
    plt.xlabel('Date')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('total_cases.png')
    print("Saved total_cases.png")

    # Step 5: Vaccination Analysis
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_filtered, x='date', y='vaccination_rate', hue='location')
    plt.title('COVID-19 Vaccination Rates Over Time')
    plt.ylabel('Vaccination Rate')
    plt.xlabel('Date')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('vaccination_rates.png')
    print("Saved vaccination_rates.png")

    print("\nAnalysis complete! Check the generated PNG files.")

if __name__ == "__main__":
    main()