import pandas as pd

data1 = pd.read_csv('ratings.csv')
data2 = pd.read_csv('OtherRatting.csv')

temp_data1 = data1[data1['Date'].isin(data2['Date'])]
temp_data2 = data2[data2['Date'].isin(data1['Date'])]
for i in range(0, min(len(temp_data1), len(temp_data2)), 10):
    temp1 = temp_data1.iloc[i:i+10]
    minDate = temp1['Date'].min()
    maxDate = temp1['Date'].max()

    t1 = temp_data1[(temp_data1['Date'] >= minDate) & (temp_data1['Date'] <= maxDate)]
    t2 = temp_data2[(temp_data2['Date'] >= minDate) & (temp_data2['Date'] <= maxDate)]
    print ('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(t1)
    print(t2)
    print ('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

