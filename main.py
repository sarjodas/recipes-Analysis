import pandas as pd
import re
from isodate import parse_duration

def Assign(read_path, write_path):
    print('Fetching File')
    path = '/Users/sarjodas/Downloads/recipes.json'
    data = pd.read_json(path, lines=True)
    data = data.replace('\n', ' ', regex=True)

    data = data[data['ingredients'].str.contains('Chilies|Chiles|Chili', regex=True, flags=re.IGNORECASE)]
    data['prepTime'] = data['prepTime'].replace('', 'PT0M', regex=True)
    data['cookTime'] = data['cookTime'].replace('', 'PT0M', regex=True)


    time_prepTime_sec = pd.DataFrame()
    j=0
    for i in data['prepTime']:
        temp = pd.DataFrame({'prepTimeinSec': parse_duration(i).total_seconds()}, index=[j])
        time_prepTime_sec = pd.concat([time_prepTime_sec, temp])
        j+=1
    print(time_prepTime_sec)

    time_cookTime_sec = pd.DataFrame()
    j=0
    for i in data['cookTime']:
        temp = pd.DataFrame({'cookTimeinSec': parse_duration(i).total_seconds()}, index=[j])
        time_cookTime_sec = pd.concat([time_cookTime_sec, temp])
        j += 1
    print(time_cookTime_sec)

    data.reset_index(level=0, inplace=True)

    data['total_time'] = time_prepTime_sec['prepTimeinSec'] + time_cookTime_sec['cookTimeinSec']

    data['difficulty'] = 'Unknown'

    data.loc[(data['total_time'] > 3600), 'difficulty'] = 'Hard'
    data.loc[(data['total_time'] <= 3600) & (data['total_time'] >= 1800), 'difficulty'] = 'Medium'
    data.loc[(data['total_time'] < 1800) & (data['total_time'] > 0), 'difficulty'] = 'Medium'

    data.to_csv(write_path, index=False)


if __name__ == '__main__':
    read_path = '/Users/sarjodas/Downloads/recipes.json'
    write_path = '/Users/sarjodas/Downloads/recipes-etl.csv'
    Assign(read_path, write_path)
