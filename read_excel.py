import pandas as pd

spreadsheet = pd.read_csv('CustomParameters.csv')
spreadsheet.set_index(spreadsheet['Parameter name'], inplace=True)


spreadsheet = spreadsheet[~spreadsheet.index.duplicated()]

for row in spreadsheet.iterrows():
    print(row[1][5])
    example = row[1][5]
    if type(example) is str:
        example = example.lower()
    else:
        continue
    index = row[0]

    if " gt " in example or "interval" in example or "count" in example:
        spreadsheet.loc[index, ["Effective Variable Type"]] = "Integer"
    elif " ne 0" in example or "=1" in example or " eq 1" in example or " ne 1" in example or "eq 0" in example or "=0" in example:
        spreadsheet.loc[index, ["Effective Variable Type"]] = "binary"
    elif "list" in example or "array" in example:
        spreadsheet.loc[index, ["Effective Variable Type"]] = "array"
    elif "\"yes\"" in example or "\"no\"" in example:
        spreadsheet.loc[index, ["Effective Variable Type"]] = "Varchar (YES/NO)"
    elif "upcase" in example:
        spreadsheet.loc[index, ["Effective Variable Type"]] = "Varchar"
    elif "date" in example:
        spreadsheet.loc[index, ["Effective Variable Type"]] = "Datetime"


# spreadsheet.loc["&copy", ["Example Values"]] = " "

# print(spreadsheet.index.values)

spreadsheet.to_csv('CustomParameters.csv', index=False)
