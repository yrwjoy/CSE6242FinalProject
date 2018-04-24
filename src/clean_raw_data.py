import glob
import pandas as pd



def get_regionnames_to_delete():
    region_names = set()
    regions_to_delete = set()

    file_names = glob.glob('static/data/raw_trainning_data/*.csv')
    for file_name in file_names:
        df = pd.read_csv(file_name)

        for idx in range(len(df['RegionName'])):
            if df.iloc[idx].isnull().sum() < 10:
                region_names.add(df['RegionName'][idx])
            else:
                regions_to_delete.add(df['RegionName'][idx])
    return regions_to_delete


def delete_region_name(file_name, region_to_delete):
    df = pd.read_csv(file_name)
    print(file_name)
    count = 0
    for index, row in df.iterrows():
        if row['RegionName'] in regions_to_delete:
            df.drop(index, inplace=True)
            count += 1
    print count
    df.to_csv(file_name, sep=',')


if __name__ == '__main__':
    print('clean start')
    # print(df.columns.values.tolist())

    regions_to_delete = get_regionnames_to_delete()
    print(regions_to_delete)

    file_names = glob.glob('static/data/raw_trainning_data/*.csv')
    print file_names
    for file_name in file_names:
        delete_region_name(file_name, regions_to_delete)







