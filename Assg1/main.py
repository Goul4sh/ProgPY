import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

columns = ['sex', 'Length', 'Diameter', 'Height', 'Whole weight', 'Shucked weight', 'Viscera weight', 'Shell weight',
           'Rings']
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

#podp 2

stats = {}
for column in file_data.columns[1:]:
    stats[column] = {

        'mean': file_data[column].mean(),
        'std': file_data[column].std(),
        'min': file_data[column].min(),
        '25%': file_data[column].quantile(0.25),
        '50%': file_data[column].quantile(0.5),
        '75%': file_data[column].quantile(0.75),
        'max': file_data[column].max(),
    }

df = pd.DataFrame(stats)

df.index.name = None
df = df.T
print(df)

#podp3

sns.barplot(x='category', y='count', data=data)
plt.show()