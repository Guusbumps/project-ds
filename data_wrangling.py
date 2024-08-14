import pandas as pd


def getNutritionData():
    nutrition_data_raw = pd.read_csv('data/Nutrition__Physical_Activity__and_Obesity_-_BRFSS_fruitveg_20240707.csv')

    # select the "Total" stratification category (no stratification by Age, Education, Gender, Income, Race/Ethnicity)
    nutrition_data_total = nutrition_data_raw[nutrition_data_raw['StratificationCategory1'] == "Total"]

    df_nutr = nutrition_data_total[['YearStart', 'LocationDesc', 'LocationAbbr', 'Question', 'Data_Value']].copy()
    df_nutr.rename(columns={'YearStart': 'Year', 'LocationDesc': 'State', 'LocationAbbr': 'StateAbbr'},
                   inplace=True)

    return df_nutr


def getCancerDeathData():
    death_data_raw = pd.read_csv('data/NCHS_-_Leading_Causes_of_Death__United_States_20240703.csv')
    death_data_selection = death_data_raw[['Year', 'Cause Name', 'State', 'Deaths', 'Age-adjusted Death Rate']].copy()
    df_cancerdeaths = death_data_selection[(death_data_selection['Cause Name'] == 'Cancer') &
                                           (death_data_selection['State'] != 'United States')]

    return df_cancerdeaths


def getJoinedNutritionCancerData():
    df_nutr = getNutritionData()
    df_cancerdeaths = getCancerDeathData()
    df_nutr_cancerdeaths = pd.merge(df_cancerdeaths, df_nutr, how='inner')
    return df_nutr_cancerdeaths
