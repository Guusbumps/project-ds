import pandas as pd


def getNutritionData():
    nutrition_data_raw = pd.read_csv('data/Nutrition__Physical_Activity__and_Obesity_-_BRFSS_fruitveg_20240707.csv')

    df_nutr = nutrition_data_raw[
        ['YearStart', 'LocationDesc', 'LocationAbbr', 'Question', 'Data_Value', 'StratificationCategory1','Stratification1']].copy()
    # rename to match the column names in cause of death datasets
    df_nutr.rename(columns={'YearStart': 'Year', 'LocationDesc': 'State', 'LocationAbbr': 'StateAbbr'},
                   inplace=True)
    df_nutr['Stratification1'] = df_nutr['Stratification1'].replace({
        'Asian': 'Asian or Pacific Islander'
        })
    return df_nutr


def getCancerDeathsData(filepath):
    df_cancerdeaths = pd.read_csv(filepath, sep="\t")
    return df_cancerdeaths


def getCancerDeathsDataStratAge(filepath):
    df_cancerdeaths_age = pd.read_csv(
        filepath,
        sep="\t"
    )
    return df_cancerdeaths_age


def getCancerDeathsDataStratRaceEthnicity(filepath):
    df_cancerdeaths_race = pd.read_csv(
        filepath,
        sep="\t"
    )
    # combine Race and Ethnicity columns into one, to match the nutrition data
    df_cancerdeaths_race['Race/Ethnicity'] = df_cancerdeaths_race['Race'] + '/' + df_cancerdeaths_race['Ethnicity']
    # rename Race/Ethnicity values to match the nutrition data
    df_cancerdeaths_race['Race/Ethnicity'] = df_cancerdeaths_race['Race/Ethnicity'].replace(
        {
            "White/Non-Hispanic": "Non-Hispanic White",
            "Black or African American/Non-Hispanic": "Non-Hispanic Black",
            "American Indian or Alaska Native/Non-Hispanic": "American Indian/Alaska Native",
            "Asian or Pacific Islander/Non-Hispanic": "Asian or Pacific Islander",
            "White/Hispanic": "Hispanic",
        })

    return df_cancerdeaths_race


def getCancerDeathsDataStratSex(filepath):
    df_cancerdeaths_sex = pd.read_csv(
        filepath,
        sep="\t"
    )
    return df_cancerdeaths_sex


def getCancerDeathsPerSiteData():
    df_sites = getCancerDeathsData(
        'data/Cancer Statistics, 1999-2020 Mortality Archive_LeadingSites_nostrat.txt')
    return df_sites


def getCombinedCancerDeathsData():
    df_total = getCancerDeathsData('data/United States and Puerto Rico Cancer Statistics, 1999-2020 Mortality.txt')
    df_total['StratificationCategory1'] = 'Total'
    df_total['Stratification1'] = 'Total'
    df_total = df_total[df_total['Cancer Sites'] == 'All Cancer Sites Combined']

    df_age = getCancerDeathsDataStratAge(
        'data/Cancer Statistics, 1999-2020 Mortality Archive_SitesCombined_Age.txt')
    df_age['StratificationCategory1'] = 'Age (years)'
    df_age['Stratification1'] = df_age['Age Group']
    df_race = getCancerDeathsDataStratRaceEthnicity(
        'data/Cancer Statistics, 1999-2020 Mortality Archive_SitesCombined_RaceEthnicity.txt')
    df_race['StratificationCategory1'] = 'Race/Ethnicity'
    df_race['Stratification1'] = df_race['Race/Ethnicity']
    df_sex = getCancerDeathsDataStratSex(
        'data/Cancer Statistics, 1999-2020 Mortality Archive_SitesCombined_Sex.txt')
    df_sex['StratificationCategory1'] = 'Gender'
    df_sex['Stratification1'] = df_sex['Sex']
    df_combined = pd.concat([df_total, df_race, df_age, df_sex])
    df_combined = df_combined[df_combined['Age-Adjusted Rate']!='Not Applicable']
    df_combined['Age-Adjusted Rate'] = df_combined['Age-Adjusted Rate'].astype(float)

    # select useful columns
    df_combined = df_combined[
        ['Cancer Sites', 'State', 'Year', 'Deaths', 'Population', 'Age-Adjusted Rate',
         'StratificationCategory1', 'Stratification1', 'Crude Rate', 'Race/Ethnicity',
         'Sex', 'Age Group']]

    return df_combined


def getJoinedNutritionCancerData():
    df_nutr = getNutritionData()
    df_cancerdeaths = getCombinedCancerDeathsData()
    df_nutr_cancerdeaths = pd.merge(df_cancerdeaths, df_nutr, how='inner')
    return df_nutr_cancerdeaths


def getJoinedNutritionCancerSitesData():
    df_nutr = getNutritionData()
    df_cancerdeaths = getCancerDeathsPerSiteData()
    df_nutr_cancersites_deaths = pd.merge(df_cancerdeaths, df_nutr, how='inner')
    return df_nutr_cancersites_deaths
