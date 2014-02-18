#!/usr/bin/python
import csv, json


def csv_to_json(csv_filename, delimiter=',', quotechar='"'):
    """
    Convert csv file to json
    Thanks to http://stackoverflow.com/questions/662859/converting-csv-xls-to-json
    """

    csvreader = csv.reader(open(csv_filename, 'rb'), delimiter=delimiter, quotechar=quotechar)
    data = []
    for row in csvreader:
        r = []
        for field in row:
            if field == '':
                field = None
            else:
                field = unicode(field, 'ISO-8859-1')
            r.append(field)
        data.append(r)
    jsonStruct = {
        'header': data[0],
        'data': data[1:]
    }
    return jsonStruct
    #open('data.json', 'wb').write(json.dumps(jsonStruct))