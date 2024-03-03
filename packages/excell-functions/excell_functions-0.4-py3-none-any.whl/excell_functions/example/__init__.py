import pandas as pd

df = pd.DataFrame({
#'Animal's nick'
'A': ['Bert', 'Martha', 'Noah', 'Emma', 'Liam', 'Oliver', 'Lucas', 'Isabella', 'Henry', 'Amelia', 'Evelyn', 'Mia'],
#'Animal's type (on sex and age)'
'B': ['bool', 'cow', 'calf', 'heifer', 'calf', 'calf', 'bool', 'cow', 'calf', 'cow', 'cow', 'cow'],
#'Animal's life time (days)'
'C': [1873, 2524, 269, 67, 167, 67, 3258, 2811, 177, 2119, 3132, 2489],
#'Animal's age (years)'
'D': [5.13150684931507, 6.91506849315068, 0.736986301369863, 0.183561643835616, 0.457534246575342, 0.183561643835616, 8.92602739726027, 7.7013698630137, 0.484931506849315, 5.80547945205479, 8.58082191780822, 6.81917808219178],
#'Animal's sex (male - True, female - False)'
'E': [True, False, True, False, True, True, True, False, True, False, False, False],
#'Birthday (datetime)'
'F': ['20.08.2018', '07.11.2016', '10.01.2023', '31.07.2023', '22.04.2023', '31.07.2023', '04.11.2014', '25.01.2016', '12.04.2023', '17.12.2017', '10.03.2015', '12.12.2016'],
#'Animal's price'
'G': [4868493.15, 4627397.26, 9263013.7, 14724657.53, 9542465.75, 9816438.36, 1073972.60, 3447945.21, 9515068.49, 6291780.82, 2128767.12, 4771232.88],
})
df['F'] = pd.to_datetime(df['F'])
# 'Empty column'
df['H'] = None

df.index = df.index + 1
