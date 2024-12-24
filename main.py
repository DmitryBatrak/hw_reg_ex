import re
import csv

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

for row in contacts_list:
    separate_name = row[0].split()
    separate_last_name = row[1].split()
    if len(separate_name) == 3:
        row[0] = separate_name[0]
        row[1] = separate_name[1]
        row[2] = separate_name[2]
    elif len(separate_name) == 2:
        row[0] = separate_name[0]
        row[1] = separate_name[1]

    if len(separate_last_name) == 2:
        row[1] = separate_last_name[0]
        row[2] = separate_last_name[1]

for row in contacts_list:
    for double in contacts_list:
        if row[0] == double[0] and row[1] == double[1]:
            for i in range(2, len(row)):
                if row[i] == '':
                    row[i] = double[i]
                if double[i] == '':
                    double[i] = row[i]

counter = 0
for row in contacts_list:
    for double in contacts_list:
        if row[0] == double[0] and row[1] == double[1] and counter == 0:
            counter += 1
            continue
        if row[0] == double[0] and row[1] == double[1] and counter > 0:
            contacts_list.remove(double)
            counter += 1
    counter = 0

for row in contacts_list:
    telephone_draft = row[5]
    telephone_draft = re.sub(r"\D", "", telephone_draft)
    tail = ""
    number = ""

    if len(telephone_draft) > 11:
        tail = telephone_draft[11:]
        number = telephone_draft[:11]
    elif len(telephone_draft) == 11:
        number = telephone_draft

    if len(number) and number[0] == "8":
        number = "7" + number[1:]

    if number:
        true_number = re.sub(r"(.*?)(.{3})(.{3})(.{2})(.{2})$", r"\1(\2)\3-\4-\5", number)
        true_number_and_tail = f"+{true_number} доб.{tail}" if tail else f"+{true_number}"
    else:
        true_number_and_tail = "phone"

    row[5] = true_number_and_tail


with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)