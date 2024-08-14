import pandas as pd


def getNutritionData():
    nutrition_data_raw = pd.read_csv('data/Nutrition__Physical_Activity__and_Obesity_-_BRFSS_fruitveg_20240707.csv')

    # select the "Total" stratification category (no stratification by Age, Education, Gender, Income, Race/Ethnicity)
    nutrition_data_overall = nutrition_data_raw[nutrition_data_raw['StratificationCategory1'] == "Total"]

    df_nutr = nutrition_data_overall[['YearStart', 'LocationDesc', 'LocationAbbr', 'Question', 'Data_Value']].copy()
    df_nutr.rename(columns={'YearStart': 'Year', 'LocationDesc': 'State', 'LocationAbbr': 'StateAbbr'},
                   inplace=True)

    return df_nutr


def getJoinedNutritionCancerData():
    df_nutr = getNutritionData()
    #data_long = pd.merge(cancerdeath_data, df_nutr, how='inner')