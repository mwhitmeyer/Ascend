import glob
import os
import pandas as pd

spreadsheet = pd.read_csv('CustomParameters.csv')
spreadsheet.set_index(spreadsheet['Parameter name'], inplace=True)
spreadsheet = spreadsheet[~spreadsheet.index.duplicated()]
path = r'C:\Users\mdw82\python\sasmacroExport'

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

list_of_parameters = []

bloop = open("bloop.txt", "r")
for line in bloop.readlines():
    line = line.strip()
    list_of_parameters.append(line)

# output = open("output.txt", "a")

for parameter in list_of_parameters:
    folders = ""
    files = ""
    examples = ""
    for file in all_sas_files:
        flag = False
        contents = open(file, "r")
        for line in contents.readlines():
            line = line.strip()
            if parameter[-1] != ".":
                with_period = parameter + "."
            else:
                with_period = parameter
            if with_period  in line.lower():
                if flag == False:
                    flag = True
                    folder = get_folder(file)
                    if folders.find(folder + ",") == -1:
                        folders += folder + ", "
                    thefile = file[len(path):]
                    if files.find(thefile + ",") == -1:
                        files += thefile + ", "
                if len(examples) < 1000:
                    examples += line + "\r\n"
        contents.close()

    k = examples.find("\r\n")
    spreadsheet.loc[parameter, ["Exact macros which it appears"]] = files[:len(files) - 2]
    spreadsheet.loc[parameter, ["Folders in which it appears"]] = folders[:len(folders)-2]
    spreadsheet.loc[parameter, ["Code example"]] = examples[:k]
    # output.write("Parameter: " + parameter + "\r\n\r\n")
    # output.write("Folders: " + folders[:len(folders) - 2] + "\r\n\r\n")
    # output.write("Files: " + files[:len(files) - 2] + "\r\n\r\n")
    # output.write("Examples: " + examples + "\r\n\r\n")

spreadsheet.to_csv('CustomParameters.csv', index=False)
# output.close()
