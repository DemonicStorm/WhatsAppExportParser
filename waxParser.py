import datetime
import re

class workday():
    def __init__(self):
        self.day = None
        self.workstart = None
        self.workend = None
        self.breakstart = None
        self.breakend = None
        self.worktime = None
        self.breaktime = None
        self.total = None
        self.misc = None

timepattern = r'\d\d?:\d\d'
dayTimeP = '%d.%m.%y, %H:%M:%S'

def readExport(file):
    with open(file, encoding="utf-8") as f:
        lineList = f.readlines()
        lineList = [x.rstrip("\n") for x in lineList]
    dateCheckList = []
    resultList = []
    for line in lineList:
        if line.startswith("["):
            date = line[1:9]
            if date not in dateCheckList:
                dateCheckList.append(date)
                dct = workday()
                dct.day = datetime.datetime.strptime(date,'%d.%m.%y').date()
                for l in lineList:
                    if l[1:].startswith(date):
                        correction = re.findall(timepattern,l[20:])
                        if "kommen" in l.lower() or "beginn" in l.lower() and dct.workstart == None:
                            if  correction != []:
                                dct.workstart = datetime.datetime.combine(datetime.datetime.strptime(l[1:9],'%d.%m.%y').date(),datetime.time(int(correction[0].split(':')[0]),int(correction[0].split(':')[1])))
                            else:
                                dct.workstart = datetime.datetime.strptime(l[1:19],dayTimeP)
                            if "feiertag" in l.lower():
                                dct.misc = "Feiertag"
                            if "krank" in l.lower():
                                dct.misc = "krank"
                            if "urlaub" in l.lower():
                                dct.misc = "Urlaub"
                        elif "gehen" in l.lower() or "fertig" in l.lower() and dct.workend == None:
                            if  correction != []:
                                dct.workend = datetime.datetime.combine(datetime.datetime.strptime(l[1:9],'%d.%m.%y').date(),datetime.time(int(correction[0].split(':')[0]),int(correction[0].split(':')[1])))
                            else:
                                dct.workend = datetime.datetime.strptime(l[1:19], dayTimeP)
                        elif "pause" in l.lower() and dct.breakstart == None:
                            dct.breakstart = datetime.datetime.strptime(l[1:19], dayTimeP)
                        elif "ende" in l.lower() and dct.breakend == None:
                            dct.breakend = datetime.datetime.strptime(l[1:19], dayTimeP)
                    else:
                        pass
                try:
                    dct.worktime = dct.workend - dct.workstart
                except TypeError:
                    dct.worktime = None
                    print(f"Beginn oder End-Zeit fehlt für {dct.day}")
                if dct.breakend and dct.breakstart:
                    dct.breaktime = dct.breakend - dct.breakstart
                    dct.total = dct.worktime - dct.breaktime
                else:
                    dct.total = dct.worktime
                resultList.append(dct)

    return resultList
def monthly(data):
    summen = {
        "jan": [],
        "feb": [],
        "mar": [],
        "apr": [],
        "mai": [],
        "jun": [],
        "jul": [],
        "aug": [],
        "sep": [],
        "okt": [],
        "nov": [],
        "dez": []
    }
    for day in data:
        if day.day.month == 2:
            summen['feb'].append(day)
        elif day.day.month == 1:
            summen['jan'].append(day)
        elif day.day.month == 3:
            summen['mar'].append(day)
        elif day.day.month == 4:
            summen['apr'].append(day)
        elif day.day.month == 5:
            summen["mai"].append(day)
        elif day.day.month == 6:
            summen["jun"].append(day)
        elif day.day.month == 7:
            summen["jul"].append(day)
        elif day.day.month == 8:
            summen["aug"].append(day)
        elif day.day.month == 9:
            summen["sep"].append(day)
        elif day.day.month == 10:
            summen["okt"].append(day)
        elif day.day.month == 11:
            summen["nov"].append(day)
        elif day.day.month == 12:
            summen["dez"].append(day)

    for month in summen:
        if len(summen[month]) == 0:
            pass
        else:
            total = []
            for x in summen[month]:
                total.append(x.total.seconds)
            summe = sum(total)/60/60
            print(f'{month}: {round(summe,2)}')

    return summen
def ausgabe(monthlydata):
    pattern = '%H:%M:%S'
    for x in monthlydata:
        if len(monthlydata[x]) > 0:
            file = "".join([x,'.csv'])
            with open(file,'w', encoding='utf-8') as f:
                f.write('Datum,Arbeitssumme,Arbeitsbeginn,Arbeitsende,Pausenzeit,Urlaub/krank\n')
                [f.write(f'{monthlydata[x][i].day}, {monthlydata[x][i].total}, {monthlydata[x][i].workstart.time().strftime(pattern)}, {monthlydata[x][i].workend.time().strftime(pattern)}, {monthlydata[x][i].breaktime}, {monthlydata[x][i].misc}\n') for i in range(len(monthlydata[x]))]
                f.write(f'Monatssumme:, {round(sum([i.total.seconds for i in monthlydata[x]])/60/60,2)}')
if __name__ == '__main__':
    ausgabe(monthly(readExport('_chat.txt')))


