import argparse # Requires Python 3.2+
from datetime import date
import urllib3
from bs4 import BeautifulSoup

admits = 0
rejects = 0
stop = 0

parser = argparse.ArgumentParser(description='Calculate GradCafe acceptance rates.')
parser.add_argument('--school', nargs=1, help='a school name, in quotation marks', default='')
parser.add_argument('--subject', nargs=1, help='a subject name, in quotation marks', default='')
parser.add_argument('--year', type=int, nargs='?', help='a year to search through', default=int(date.today().year))
args = parser.parse_args()

school = str(args.school)
subject = str(args.subject)
year = str(args.year)

def parsePage(page):
    global school
    global subject
    global year
    # url = 'https://www.thegradcafe.com/survey/index.php'
    school = school.replace(" ", "+")
    subject = subject.replace(" ", "+")
    # if(school != '' or subject != ''):
        # query = school + '%22+' + subject + '&t=a&o=d&pp=250' + suffix
    suffix = ''
    if(page >= 2): suffix = "&p=" + str(page)
    req = urllib3.PoolManager().request(
        'GET',
        'https://www.thegradcafe.com/survey/index.php?q=%22' + school + '%22+' + subject + '&t=a&o=d&pp=250' + suffix,
        headers={'User-Agent' : "Chrome Browser"}
    )

    soup = BeautifulSoup(req.data, "html.parser")
    table = soup.find('table',class_="submission-table")

    global stop

    if(table is None):
        stop = 2
        return

    institutes, programs, decisions, statuses, dates, notes = [],[],[],[],[],[]

    rows = table.findAll("tr")
    rows.pop(0)

    for row in rows:
        cells = row.findAll("td")
        date = cells[4].get_text()
        decision = cells[2].get_text()
        if year in date:
            stop = 1
            if "Accepted" in decision or "Rejected" in decision:
                # if "Undergrad GPA: n/a" not in decision and "Undergrad GPA: n/a" not in decision:
                institutes.append(cells[0].get_text())
                programs.append(cells[1].get_text())
                decisions.append(cells[2].get_text())
                statuses.append(cells[3].get_text())
                dates.append(cells[4].get_text())
                notes.append(cells[5].get_text())
        elif stop == 1:
            stop = 2

    uniqueInstitutes = list(set(institutes))
    # print uniqueInstitutes
    global admits
    global rejects
    admits += len([i for i in decisions if "Accepted" in i])
    rejects += len([i for i in decisions if "Rejected" in i])

if(school == '' and subject == ''):
    print('Please enter a school and/or subject. The year argument is optional.')
else:
    i = 1
    while(stop != 2):
        parsePage(i)
        i += 1

    if((admits + rejects) == 0):
        print('No decisions found for the given year.')
    else:
        print("Admits: " + str(admits))
        print("Rejects: " + str(rejects))
        print("Acceptance Rate: " + str( round( (admits/(admits+rejects))*10000 ) / 100 ) + "%")
