import pandas as pd

df = pd.read_csv(r"C:\Users\mdw82\python\Duall.csv")
updown = pd.read_csv(r"C:\Users\mdw82\python\minupdowntime.csv")
dugen = pd.read_csv(r"simpledugen.csv")
genperiodidtable = pd.read_csv("simplegenperiodidtable.csv")

dugen["eventDateTime"] =  pd.to_datetime(dugen["eventDateTime"])
# dugen["Month"] = [x.month for x in list(dugen["eventDateTime"])]
# dugen["Year"] = [x.year for x in list(dugen["eventDateTime"])]
dugen["MonthYear"] = [x.month*10000 + x.year for x in list(dugen["eventDateTime"])]
genperiodidtable["STARTDATE"] = pd.to_datetime(genperiodidtable["STARTDATE"])
genperiodidtable["ENDDATE"] = pd.to_datetime(genperiodidtable["ENDDATE"])
# genperiodidtable["Month"] = [x.month for x in list(genperiodidtable["STARTDATE"])]
# genperiodidtable["Year"] = [x.year for x in list(genperiodidtable["STARTDATE"])]
genperiodidtable["MonthYear"] = [x.month*10000 + x.year for x in list(genperiodidtable["STARTDATE"])]

# dugen = dugen[["ITEMCOMPID", "eventDateTime", "GENERATION"]]
# dugen["eventDateTime"] =  pd.to_datetime(dugen["eventDateTime"], format=r'%d%b%Y:%H:%M:%S')

# genperiodidtable = genperiodidtable[["GENERATIONID", "STARTDATE", "ENDDATE", "MAXGENERATION"]]
# genperiodidtable["STARTDATE"] = pd.to_datetime(genperiodidtable["STARTDATE"], format=r'%d%b%Y:%H:%M:%S')
# genperiodidtable["ENDDATE"] = pd.to_datetime(genperiodidtable["ENDDATE"], format=r'%d%b%Y:%H:%M:%S')
# genperiodidtable.to_csv("simplegenperiodidtable.csv")

# print(df.columns.values)
# print(df.index.values)

df = df[["eventDateTime", "ITEMCOMPID", "HOURSRUN"]]
df["eventDateTime"] = pd.to_datetime(df["eventDateTime"], format=r'%d%b%y:%H:%M:%S')

updown = updown[["MinUpTime", "MinDownTime", "ITEMCOMPID", "STARTDATE", "ENDDATE", "RAMPUPRATE", "RAMPDOWNRATE"]]

updown["STARTDATE"] = pd.to_datetime(list(updown["STARTDATE"]), format=r'%d%b%Y:%H:%M:%S')
updown["ENDDATE"] = pd.to_datetime(list(updown["ENDDATE"]), format=r'%d%b%Y:%H:%M:%S')


print("done reading")


def checkminupdowntime(duall, minupdown):
    itemcompids = list(set(duall["ITEMCOMPID"]))
    uptrouble = pd.DataFrame(index = itemcompids, columns=["MINUPTIMEISSUES"])
    downtrouble = pd.DataFrame(index = itemcompids, columns=["MINDOWNTIMEISSUES"])
    # trouble["MINUPTIMEISSUES"] = [[]]*len(itemcompids)

    for id in itemcompids:
        print("processing id: ", id)
        temp = duall[duall["ITEMCOMPID"] == id]
        minupdowntemp = minupdown[minupdown["ITEMCOMPID"] == id]
        updownindices = minupdowntemp.index.values
        #print(updownindices)
        indices = temp.index.values
        i = indices[0]

        start = temp.loc[i, "HOURSRUN"]
        while i < len(indices)+ indices[0] and temp.loc[i, "HOURSRUN"] == start:
            i += 1

        while i < len(indices) + indices[0]:
            if temp.loc[i, "HOURSRUN"] == 0:
                date = temp.loc[i, "eventDateTime"]
                if len(updownindices) == 0:
                    k = updownindices[0]

                    while k in updownindices and not (minupdowntemp.loc[k, "STARTDATE"] < date  and date < minupdowntemp.loc[k, "ENDDATE"]):
                        k += 1
                    if k not in updownindices:
                        #print("Date range not minupdown table. Why?")
                        k -= 1

                    mindowntime = minupdowntemp.loc[k, "MinDownTime"]
                else:
                    mindowntime = 0
                #print("minuptime = ", minuptime)
                #count the number of hours run in a row and check that it's at least minuptime
                i += 1
                count = 1
                while i < (len(indices) + indices[0]) and temp.loc[i, "HOURSRUN"] == 0:
                    i += 1
                    count += 1
                if count < mindowntime and i != (len(indices) + indices[0]):
                    print("found mindowntime error: ", id, date)
                    downtrouble.loc[id, "MINDOWNTIMEISSUES"] = date
                # i += 1
                # continue
            else:
                #find the correct minuptime for the given date
                date = temp.loc[i, "eventDateTime"]
                k = updownindices[0]

                while k in updownindices and not (minupdowntemp.loc[k, "STARTDATE"] < date  and date < minupdowntemp.loc[k, "ENDDATE"]):
                    k += 1
                if k not in updownindices:
                    #print("Date range not minupdown table. Why?")
                    k -= 1
                minuptime = minupdowntemp.loc[k, "MinUpTime"]
                #print("minuptime = ", minuptime)
                #count the number of hours run in a row and check that it's at least minuptime
                i += 1
                count = 1
                while i < (len(indices) + indices[0]) and temp.loc[i, "HOURSRUN"] == 1:
                    i += 1
                    count += 1
                if count < minuptime and i != (len(indices) + indices[0]):
                    print("found minuptime error: ", id, date)
                    uptrouble.loc[id, "MINUPTIMEISSUES"] = date


    uptrouble.to_csv("minupissues.csv")
    downtrouble.to_csv("mindownissues.csv")


def checkmaxgeneration(genperiodidtable, dugen):
    troubleids = set()
    for id in list(set(dugen["ITEMCOMPID"])):
        tempdugen = dugen[dugen["ITEMCOMPID"] == id]
        tempgenperiod = genperiodidtable[genperiodidtable["GENERATIONID"] == id]
        allmonths = set(tempdugen["MonthYear"])
        for monthyear in allmonths:
            temptempdugen = tempdugen[tempdugen["MonthYear"] == monthyear]
            totalgen = sum(temptempdugen["GENERATION"]) - list(temptempdugen["GENERATION"])[0]
            temptempgenperiod = tempgenperiod[tempgenperiod["MonthYear"] == monthyear]
            maxgen = list(temptempgenperiod["MAXGENERATION"])[0]
            if pd.isnull(maxgen) or maxgen == -99999999:
                continue
            elif totalgen > maxgen:
                print("max generation violation for id: ", id, " in month: ", monthyear//10000, " in year: ", monthyear%10000)
                troubleids.add(id)
            # print(temptempgenperiod)
            # maxgen = temptempgenperiod["MAXGENERATION"][0]
            # print("maxgen for id ", id, " and for monthyear ", monthyear, " = ", maxgen)
    print("number of IDs with maxgeneration violations: ", len(troubleids))
    print("IDs with maxgeneration violations: ", troubleids)


checkmaxgeneration(genperiodidtable, dugen)
#checkminupdowntime(df, updown)
