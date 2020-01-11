from bs4 import BeautifulSoup
import requests
import time
import csv
import numpy as np

#url = 'https://usapl.liftingdatabase.com/competitions-view?id=1964'
#html = requests.get(url).text

numbers = ['1','2','3','4','5','6','7','8','9','0','.', '-']


def get_page_data(html, id_num):
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.select('tbody tr')
    date = get_id_field(rows, 'Date')
    sanction = get_id_field(rows, 'Sanction #')
    state = get_id_field(rows, 'State')
    director = get_id_field(rows, 'Meet Director')
    #print('Date: ' + date)
    #print('Sanction #: ' + sanction)
    #print('State: ' + state)
    #print('Meet Director: ' + director)
    i = 0
    entries = list()
    for row in rows:
        if not str(row).find('a href') == -1 and str(row).find('td id') > -1:
            #print('---')
            vector = parse_tag_tree(row, print_output = False)
            vector.append(date)
            vector.append(sanction)
            vector.append(state)
            vector.append(director)
            vector.append(str(id_num))
            #print(vector)
            #for items in row:
            #    print(items)
            i += 1
            entries.append(vector)
    return entries

def get_id_field(rows, field):
    for row in rows:
        if str(row).find(field) > -1:
            for subrow in row:
                if str(subrow).find('td') > -1:
                    for subsubrow in subrow:
                        if not '>' in str(subsubrow) and not '<' in str(subsubrow):
                            return subsubrow
    return ''

def get_personal_data(rows, field):
    for row in rows:
        if str(row).find(field) > -1:
            for subrow in row:
                if not '>' in str(subrow) and not '<' in str(subrow):
                    return subrow
    return ''

def parse_tag_tree(row, print_output):
    data_vector = list()
    after_lift = 0
    counter = 1
    column_tracker = 0
    after_name = 0
    for entry in row:
        if after_name == 1:
            yob = "".join([c for c in str(entry) if c in numbers])
            if len(yob) > 0:
                data_vector.append(yob)
                data_vector.append(get_personal_data(row, 'competition_view_club'))
                data_vector.append(get_personal_data(row, 'competition_view_state'))
                data_vector.append(get_personal_data(row, 'competition_view_weight'))
                if print_output == True:
                    print('YOB: ' + yob)
                    print('Club: ' + get_personal_data(row, 'competition_view_club'))
                    print('State: ' + get_personal_data(row, 'competition_view_state'))
                    print('Weight: ' + get_personal_data(row, 'competition_view_weight'))
                after_name = 0
        if str(entry).find('td id') > 0:
            for field in entry:
                for things in field:
                    if not '>' in things and not '<' in things:
                        data_vector.append(things)
                        if print_output == True:
                            print('Name: ' + things)
            after_name = 1
        elif str(entry).find('competition_view_lift') > 0:
            if counter < 4:
                gen_label = 'Squat attempt ' + str(counter)+ ':'
            elif counter < 7:
                gen_label = 'Bench attempt ' + str(counter - 3) + ':'
            elif counter < 10:
                gen_label = 'Deadlift attempt ' + str(counter - 6) + ':'
            for field in entry:
                try:
                    if print_output == True:
                        print(gen_label + ' ' + str(int(str(field).strip())))
                    data_vector.append(str(int(str(field).strip())))
                except:
                    if print_output == True:
                        print(gen_label + ' -')
                    data_vector.append('0')
            counter += 1
            after_lift = 1
        else:
            if after_lift > 0:
                value = "".join([c for c in str(entry) if c in numbers])
                if after_lift == 1:
                    label = 'Total: '
                elif after_lift == 2:
                    label = 'Points: '
                if len(value) > 0 and not value == '-':
                    if print_output == True:
                        print(label + value)
                    data_vector.append(value)
                    after_lift += 1
    return data_vector


#url = 'https://usapl.liftingdatabase.com/competitions-view?id=' + str(1)
#html = requests.get(url).text
#print(get_page_data(html))

#get_page_data(2475)
variables = ['name', 'yob', 'club', 'state', 'weight', 'squat1', 'squat2', 'squat3', 'bench1', 'bench2', 'bench3', 'dead1', 'dead2', 'dead3',
             'total', 'points', 'date', 'meetid', 'location', 'director']
#print(variables)

data = list()
data.append(variables)

i = 1
for idnum in [2000]:
#for idnum in range(2000, 3000):
    url = 'https://usapl.liftingdatabase.com/competitions-view?id=' + str(idnum)
    html = requests.get(url).text
    print(html)
    new_data = get_page_data(html, idnum)
    if len(new_data) > 0:
        data = data + new_data
        print('Added meet # ' + str(i) + ' with meetid ' + str(idnum))
        i += 1
    time.sleep(10)
'''
with open('usapl_data.csv', mode='w', newline = '') as csv_file:
    writer = csv.writer(csv_file)
    for row in data:
        writer.writerow(row)
'''