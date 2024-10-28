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
#display
# #podp 2

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

#pod4
fig, axes = plt.subplots(nrows = 4, ncols = 2, figsize = (10, 10))

axes = axes.flatten()
palette = sns.color_palette("viridis",len( file_data.columns))
for i, column in enumerate(file_data.columns[1:]):
    axes[i].hist(file_data[column], bins=50, color = palette[i])
    axes[i].set_title(column)

plt.tight_layout()
plt.show()

# pod5
fig, axes = plt.subplots(nrows = 14, ncols = 2,figsize = (100, 100))

axes = axes.flatten()
count=0
for i, column_i in enumerate(file_data.columns[1:]):
    for j, column_j in enumerate(file_data.columns[2+i:], start=i+1):
        print(column_i, column_j, count, i ,j)
        sns.scatterplot(x=file_data[column_i], y=file_data[column_j], hue=file_data[column_i], ax=axes[count])
        axes[count].set_title(f'{column_i} vs {column_j}')
        count += 1
plt.show()

#pod6

df_corr = pd.DataFrame(file_data.iloc[:, 1:]).corr()
print(df_corr)

#pod7
plt.figure(figsize=(10, 10))
sns.heatmap(df_corr, cmap='viridis')
plt.title('Correlation heatmap')
plt.show()

#pod8
sns.regplot(x='Length', y='Diameter', data=file_data,scatter_kws={'s': 10},ci=None)
plt.title('Regression plot')
plt.show()
