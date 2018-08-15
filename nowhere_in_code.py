import pandas as pd

spreadsheet = pd.read_csv('CustomParameters.csv')
spreadsheet.set_index(spreadsheet['Parameter name'], inplace=True)

nowhere = []
for row in spreadsheet.iterrows():
    # print(row[0])
    if type(row[1][3]) is not str:
        nowhere.append(row[0])

file = open("nowhere.txt", "w")
for variable in nowhere:
    print(variable)
    if type(variable) is str:
        file.write(variable.strip()[1:] + "\n")

file.close()
