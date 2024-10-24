import pandas as pd
import seaborn as sns

columns = ['sex', 'length', 'diameter', 'height', 'whole_weight', 'shucked weight', 'viscera weight', 'shell weight',
           'rings']
file_data = pd.read_csv('data.csv', header=None, names=columns)
male_count, female_count, infant_count = file_data['sex'].value_counts()
male_percent = round(male_count / len(file_data) * 100, 2)
female_percent = round(female_count / len(file_data) * 100, 2)
infant_percent = round(infant_count / len(file_data) * 100, 2)
data = {
    'category': ['Male', 'Infant', 'Female'],
    'count': [male_count, infant_count, female_count],
    '%': [male_percent, infant_percent, female_percent]
}

df = pd.DataFrame(data)

df.set_index('category', inplace=True)
df.index.name = None
print(df)
