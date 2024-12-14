import csv
import re

lname = 'Car'
fname = 'Corey'
pin = '10001'


with open('data.csv', 'r') as csv_file:

    #newline=''


    next(csv_file)
    line = csv_file.readline().split(',')
    total_customers = line[2]

    print(total_customers)
    for line in csv_file:
        if re.search(f'{lname},{fname}', line):
            if line[-6:-1] == pin:
                verified = True
                #return match, verified
                print('verified')
            else:
                print('wrong pin')
    #return

    # csvreader = csv.reader(csv_file)
    # for row in csvreader:
    #     if row[1] == 'last_account': last_account = row[2]
    #     print(row)
    # print(last_account)


    #https://www.tutorialspoint.com/python/file_seek.htm seek