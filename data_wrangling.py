import pandas as pd


def getNutritionData():
    nutrition_data_raw = pd.read_csv('data/Nutrition__Physical_Activity__and_Obesity_-_BRFSS_fruitveg_20240707.csv')

    df_nutr = nutrition_data_raw[
        ['YearStart', 'LocationDesc', 'LocationAbbr', 'Question', 'Data_Value', 'StratificationCategory1','Stratification1']].copy()
    # rename to match the column names in cause of death datasets
    df_nutr.rename(columns={'YearStart': 'Year', 'LocationDesc': 'State', 'LocationAbbr': 'StateAbbr'},
                   inplace=True)

    return df_nutr


def getCancerSiteDeathData():
    df_cancersite_deaths = pd.read_csv('data/United States and Puerto Rico Cancer Statistics, 1999-2020 Mortality.txt',
                                       sep="\t")
    return df_cancersite_deaths


def getJoinedNutritionCancerSiteData():
    df_nutr = getNutritionData()
    df_cancersitedeaths = getCancerSiteDeathData()
    df_nutr_cancersitedeaths = pd.merge(df_cancersitedeaths, df_nutr, how='inner')
    return df_nutr_cancersitedeaths
