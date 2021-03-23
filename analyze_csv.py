import csv
import numpy
import scipy.stats as st
import json
import requests

def csv_to_json():
    response = requests.get(f"https://api.exchangeratesapi.io/latest?base=USD")
    if response.status_code == 200:
        print("Currency conversions API queried successfully. Analyzing data...")
    else:
        print(f"There was an error querying the currency conversions API. Error code: {response.status_code}")
        return
    json_response = response.json()
    with open('multi-thread-raw.csv', "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        with open("template.json", "r") as template:
            data = json.load(template)
            i = -1
            for row in csv_reader:
                if line_count > 0:
                    host_found = False
                    node = row[7]
                    price_string = row[4]
                    if price_string == "N/A":
                        price = "N/A"
                    else:
                        price_units = price_string.split(" ")[1]
                        price = round(float(price_string.split(" ")[0]), 2)
                        if price_units != "USD":
                            price = round(float(price_string.split(" ")[0]) / json_response["rates"][price_units], 2)
                        price = f"${price}"
                    plan = f"{row[0]} {row[1]} {row[2]} {row[3]} ({price})"
                    for host in data["hosts"]:
                        if host["name"] == plan:
                            trial_added = False
                            for trial in host["trials"]:
                                if trial["node"] == node and trial["node"] != "N/A":
                                    trial["samples"] = trial["samples"] + 1
                                    trial["cps"] = (trial["cps"] + float(row[5])) / trial["samples"]
                                    trial_added = True
                                    host_found = True
                            if trial_added == False:
                                host["trials"].append({
                                    "cps": float(row[5]),
                                    "node": row[7],
                                    "samples": 1
                                })
                                host_found = True
                    if host_found == False:
                        data["hosts"].append({
                            "name": plan,
                            "trials": [
                                {
                                    "cps": float(row[5]),
                                    "node": row[7],
                                    "samples": 1
                                }
                            ]
                        })
                        i += 1
                    with open('multi-thread.json', 'w') as file:
                        file.write(json.dumps(data, indent=2))
                    file.close()
                line_count += 1
    with open('single-thread-raw.csv', "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        with open("template.json", "r") as template:
            data = json.load(template)
            i = -1
            for row in csv_reader:
                if line_count > 0:
                    host_found = False
                    node = row[7]
                    price_string = row[4]
                    if price_string == "N/A":
                        price = "N/A"
                    else:
                        price_units = price_string.split(" ")[1]
                        price = round(float(price_string.split(" ")[0]), 2)
                        if price_units != "USD":
                            response = requests.get(f"https://api.exchangeratesapi.io/latest?base={price_units}")
                            json_response = response.json()
                            price = round(json_response["rates"]["USD"] * float(price_string.split(" ")[0]), 2)
                        price = f"${price}"
                    plan = f"{row[0]} {row[1]} {row[2]} {row[3]} ({price})"
                    for host in data["hosts"]:
                        if host["name"] == plan:
                            trial_added = False
                            for trial in host["trials"]:
                                if trial["node"] == node and trial["node"] != "N/A":
                                    trial["samples"] = trial["samples"] + 1
                                    trial["mspt"] = (trial["mspt"] + float(row[5])) / trial["samples"]
                                    trial["tps"] = 1000/trial["mspt"]
                                    trial_added = True
                                    host_found = True
                            if trial_added == False:
                                host["trials"].append({
                                    "mspt": float(row[5]),
                                    "tps": 1000/float(row[5]),
                                    "node": node,
                                    "samples": 1
                                })
                                host_found = True
                    if host_found == False:
                        data["hosts"].append({
                            "name": plan,
                            "trials": [
                                {
                                    "mspt": float(row[5]),
                                    "tps": 1000/float(row[5]),
                                    "node": node,
                                    "samples": 1
                                }
                            ]
                        })
                        i += 1
                    with open('single-thread.json', 'w') as file:
                        file.write(json.dumps(data, indent=2))
                    file.close()
                line_count += 1

def json_to_csv():
    with open('multi-thread.json', 'r') as file:
        data = json.load(file)
    file.close()
    with open('multi-thread-temp.csv', 'w', newline="") as file:
        csv_writer = csv.writer(file, delimiter=',')
        csv_writer.writerow(['Plan', 'CPS', 'ME'])
        for host in data["hosts"]:
            cps_list = []
            margin_of_error = 0
            for trial in host["trials"]:
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
    with open('single-thread-temp.csv', 'w', newline="") as file:
        csv_writer = csv.writer(file, delimiter=',')
        csv_writer.writerow(['Plan', 'TPS', 'ME'])
        for host in data["hosts"]:
            tps_list = []
            margin_of_error = 0
            for trial in host["trials"]:
                tps_list.append(float(trial["tps"]))
            if len(tps_list) >= 3:
                interval = st.t.interval(alpha=0.95, df=len(tps_list)-1, loc=numpy.mean(tps_list), scale=st.sem(tps_list))
                margin_of_error = round(numpy.mean(tps_list) - interval[0],2)
            mean = round(numpy.mean(tps_list),2)
            plan = host["name"]
            csv_writer.writerow([plan, mean, margin_of_error])

def standardize():
    print("Data successfully analyzed. Standardizing data...")
    with open('multi-thread-temp.csv', 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            if row[0] == "GLOBAL Baseline G4400 4GB (N/A)":
                st_value = 100/float(row[1])
        i = 0
        with open('multi-thread-temp.csv', 'r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            with open('multi-thread-results.csv', 'w', newline='') as file:
                csv_writer = csv.writer(file, delimiter=',')
                for row in csv_reader:
                    if i == 0:
                        csv_writer.writerow(['Plan', 'Score', 'ME'])
                    if i > 0:
                        plan = row[0]
                        st_score = round(float(row[1])*st_value)
                        st_me = round(float(row[2])*st_value,2)
                        csv_writer.writerow([plan, st_score, st_me])
                    i += 1
    with open('single-thread-temp.csv', 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            if row[0] == "GLOBAL Baseline G4400 4GB (N/A)":
                st_value = 100/float(row[1])
        i = 0
        with open('single-thread-temp.csv', 'r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            with open('single-thread-results.csv', 'w', newline='') as file:
                csv_writer = csv.writer(file, delimiter=',')
                for row in csv_reader:
                    if i == 0:
                        csv_writer.writerow(['Plan', 'Score', 'ME'])
                    if i > 0:
                        plan = row[0]
                        st_score = round(float(row[1])*st_value)
                        st_me = round(float(row[2])*st_value,2)
                        csv_writer.writerow([plan, st_score, st_me])
                    i += 1
    print("Data successfully standardized. Please view the results in single-thread-results.csv and multi-thread-results.csv")

csv_to_json()
json_to_csv()
standardize()
