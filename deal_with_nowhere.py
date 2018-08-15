import pandas as pd
import glob
import os

xls = pd.ExcelFile('CustomParameters.xlsx')
df2 = pd.read_excel(xls, 'Sheet2')
df2.set_index(df2['Parameter Name'], inplace=True)
df2 = df2[~df2.index.duplicated()]
print(df2)

path = r'C:\Users\mdw82\python\sasmacroExport'
nowhere = open("nowhere.txt", "r")

def list_all_files(folder):
    list_of_filepaths = []
    for filepath in glob.glob(os.path.join(folder, "*.sas")):
        list_of_filepaths.append(filepath)
    for subfolder in [f.path for f in os.scandir(folder) if f.is_dir()]:
        list_of_filepaths.extend(list_all_files(subfolder))
    return list_of_filepaths

def get_folder(file_path):
    i = -1
    while file_path[i] != "\\":
        i-=1
    folder = file_path[:len(file_path) + i]
    folder = folder[len(path):]
    return folder

all_sas_files = list_all_files(path)

for parameter in nowhere.readlines():
    parameter = parameter.strip()
    examples = ""
    for file in all_sas_files:

        contents = open(file, "r")
        for line in contents.readlines():
            line = line.strip()
            if parameter in line.lower():
                examples += line + ", "
    examples = examples[:len(examples) - 2]
    df2.loc[parameter, ["Examples"]] = examples

df2.to_csv("nowhere.csv", index = False)
nowhere.close()
