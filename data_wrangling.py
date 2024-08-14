import pandas as pd


def getNutritionData():
    nutrition_data_raw = pd.read_csv('data/Nutrition__Physical_Activity__and_Obesity_-_BRFSS_fruitveg_20240707.csv')

    df_nutr = nutrition_data_raw[
        ['YearStart', 'LocationDesc', 'LocationAbbr', 'Question', 'Data_Value', 'StratificationCategory1','Stratification1']].copy()
    # rename to match the column names in cause of death datasets
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
