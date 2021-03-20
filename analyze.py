import csv
import numpy
import scipy.stats as st
import json

def csv_to_json():
    with open('multi-thread-raw.csv', "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        with open("template.json", "r") as template:
            data = json.load(template)
            i = -1
            for row in csv_reader:
                if line_count > 0:
                    host_found = False
                    plan = f"{row[0]} {row[1]} {row[2]} {row[3]}"
                    for host in data["hosts"]:
                        if host["name"] == plan:
                            host["trials"].append({
                                "cps": float(row[4])
                            })
                            host_found = True
                    if host_found == False:
                        data["hosts"].append({
                            "name": plan,
                            "trials": [
                                {
                                    "cps": float(row[4])
                                }
                            ]
                        })
                        i += 1
                    with open('multi-thread.json', 'w') as file:
                        file.write(json.dumps(data, indent=2))
                    file.close()
                line_count += 1
        print(f'Processed {line_count} lines.')
    with open('single-thread-raw.csv', "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        with open("template.json", "r") as template:
            data = json.load(template)
            i = -1
            for row in csv_reader:
                if line_count > 0:
                    host_found = False
                    plan = f"{row[0]} {row[1]} {row[2]} {row[3]}"
                    for host in data["hosts"]:
                        if host["name"] == plan:
                            host["trials"].append({
                                "mspt": float(row[4]),
                                "tps": 1/float(row[4])
                            })
                            host_found = True
                    if host_found == False:
                        data["hosts"].append({
                            "name": plan,
                            "trials": [
                                {
                                    "mspt": float(row[4]),
                                    "tps": 1000/float(row[4])
                                }
                            ]
                        })
                        i += 1
                    with open('single-thread.json', 'w') as file:
                        file.write(json.dumps(data, indent=2))
                    file.close()
                line_count += 1
        print(f'Processed {line_count} lines.')

def json_to_csv():
    with open('multi-thread.json', 'r') as file:
        data = json.load(file)
    file.close()
    with open('multi-thread-results.csv', 'w', newline="") as file:
        csv_writer = csv.writer(file, delimiter=',')
        csv_writer.writerow(['Plan', 'CPS', 'ME'])
        for host in data["hosts"]:
            cps_list = []
            margin_of_error = 0
            for trial in host["trials"]:
                print(f'{host["name"]} scored {trial["cps"]}')
                cps_list.append(float(trial["cps"]))
            if len(cps_list) >= 3:
                interval = st.t.interval(alpha=0.95, df=len(cps_list)-1, loc=numpy.mean(cps_list), scale=st.sem(cps_list))
                margin_of_error = round(numpy.mean(cps_list) - interval[0],2)
            mean = round(numpy.mean(cps_list),2)
            plan = host["name"]
            csv_writer.writerow([plan, mean, margin_of_error])
    with open('single-thread.json', 'r') as file:
        data = json.load(file)
    file.close()
    with open('single-thread-results.csv', 'w', newline="") as file:
        csv_writer = csv.writer(file, delimiter=',')
        csv_writer.writerow(['Plan', 'TPS', 'ME'])
        for host in data["hosts"]:
            tps_list = []
            margin_of_error = 0
            for trial in host["trials"]:
                print(f'{host["name"]} scored {trial["tps"]}')
                tps_list.append(float(trial["tps"]))
            if len(cps_list) >= 3:
                interval = st.t.interval(alpha=0.95, df=len(tps_list)-1, loc=numpy.mean(tps_list), scale=st.sem(tps_list))
                margin_of_error = round(numpy.mean(tps_list) - interval[0],2)
            mean = round(numpy.mean(tps_list),2)
            plan = host["name"]
            csv_writer.writerow([plan, mean, margin_of_error])

csv_to_json()
json_to_csv()
