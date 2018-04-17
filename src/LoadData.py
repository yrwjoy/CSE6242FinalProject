import sqlite3
import pandas as pd
from datetime import datetime

FILE_STATE = 'static/data/state_house_values.csv'
FILE_COUNTY = 'static/data/county_house_values.csv'

DATABASE = 'housingdata.db'



def loadTableRegion(conn, file):
    df = pd.read_csv(file)
    region_df = df[['RegionID', 'RegionName', 'SizeRank']]
    region_df.columns = ['ID', 'NAME', 'SIZE_RANK']
    for i in range(len(region_df)):
        try:
            region_df.iloc[i : i + 1].to_sql('REGION', conn, index=False, if_exists='append')
        except sqlite3.IntegrityError:
            pass

def houseTypeConverter(row):
    if row['Category'] == 'housetype':
        if row['Housetype'] == 'Allhome':
            return 1
        elif row['Housetype'] == 'Condo':
            return 2
        elif row['Housetype'] == 'SFR':
            return 3
        else:
            return None
    elif row['Category'] == "bedroom":
        if row['Housetype'] == 'one':
            return 4
        elif row['Housetype'] == 'two':
            return 5
        elif row['Housetype'] == 'third' or row['Housetype'] == 'three':
            return 6
        elif row['Housetype'] == 'four':
            return 7
        elif row['Housetype'] == 'five':
            return 8
        else:
            return None
    else:
        return None

def load_housetype(conn):
    list = [
        [1, 'housetype', 'Allhome'],
        [2, 'housetype', 'Condo'],
        [3, 'housetype', 'SFR'],
        [4, 'bedroom', 'one'],
        [5, 'bedroom', 'two'],
        [6, 'bedroom', 'three'],
        [7, 'bedroom', 'four'],
        [8, 'bedroom', 'five'],
    ]
    houseType_df = pd.DataFrame(list, columns=['ID', 'CATEGORY', 'HOUSE_TYPE'])
    houseType_df.to_sql('HOUSE_TYPE', conn, index=False, if_exists='append')





def colToDateTimeConverter(col_name):
    tokens = col_name.split("-")
    if tokens[1][0] == '9':
        year = 1900 + int(tokens[1])
    else:
        year = 2000 + int(tokens[1])
    time = tokens[0] + ' ' + str(year)
    return datetime.strptime(time, '%b %Y')


def load_HouseValueByMonth_state(conn, file):
    df = pd.read_csv(file)
    df['housetypeID'] = df.apply(lambda row: houseTypeConverter(row),axis=1)
    output_data = []
    for i in range(len(df)):
        row = df.iloc[i]
        for col in df.columns.values:
            if '-' in col:
                datetime = colToDateTimeConverter(col)
                lst = []
                lst.append(row['RegionID'])
                lst.append(row['housetypeID'])
                lst.append(datetime)
                lst.append(row[col])
                output_data.append(lst)
    houseValueByMonth_df = pd.DataFrame(output_data, columns=['REGION_ID', 'HOUSETYPE_ID', 'TIME', 'VALUE'])
    houseValueByMonth_df.to_sql('HOUSE_VALUE_BY_MONTH', conn, index=False, if_exists='append')


def load_HouseValueByMonth_county(conn, file):
    df = pd.read_csv(file)
    df['housetypeID'] = df.apply(lambda row: houseTypeConverter(row),axis=1)
    output_data = []
    for i in range(len(df)):
        row = df.iloc[i]
        for col in df.columns.values:
            if '-' in col:
                time = datetime.strptime(col, '%Y-%m')
                lst = []
                lst.append(row['RegionID'])
                lst.append(row['housetypeID'])
                lst.append(time)
                lst.append(row[col])
                output_data.append(lst)
    houseValueByMonth_df = pd.DataFrame(output_data, columns=['REGION_ID', 'HOUSETYPE_ID', 'TIME', 'VALUE'])
    houseValueByMonth_df.to_sql('HOUSE_VALUE_BY_MONTH', conn, index=False, if_exists='append')













if __name__ == '__main__':
    conn = sqlite3.connect(DATABASE)
    # df = pd.read_csv(FILE)
    # region_df.rename(columns= {'RegionID':'ID'}, {'RegionName':'name'})
    # region_df[['RegionID', 'SizeRank']] = region_df[['RegionID', 'SizeRank']].apply(pd.to_numeric)
    # region_df.to_sql('REGION', conn, index=False, if_exists='append')
    # df = df[df.index < 384]

    # print(df.columns.values.tolist())


    # print(df.shape)
    loadTableRegion(conn, FILE_COUNTY)
    # load_HouseValueByMonth_state(conn, FILE_STATE)
    # load_HouseValueByMonth_county(conn, FILE_COUNTY)
    # load_housetype(conn)



    # df.to_csv(FILE, sep=',')
