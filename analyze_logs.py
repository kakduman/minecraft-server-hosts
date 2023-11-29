import statistics
# import csv
# import numpy
# import scipy.stats as st
# import json

multi = False
with open("latest.log", 'r') as file:
    file_string = file.read()
if "Task continuing for world3." in file_string:
    multi = True
if multi:
    with open("latest.log", 'r') as file:
        i = -10
        initial_world = 0
        initial_world2 = 0
        initial_world3 = 0
        cps_list = []
        gen_started = False
        for line in file:
            if not gen_started:
                if "Task continuing for world3." in line:
                    gen_started = True
            elif i < 110:
                if i < 0:
                    if "âš¡" in line or "?" in line or "⚡" in line:
                        if ';' in line:
                            i += 1
                else:
                    if "âš¡" in line or "?" in line or "⚡" in line:
                        if ';' in line:
                            i += 1
                    elif "Task running for world" in line:
                        world_chunks = line.split(" chunks (")[0]
                        world_chunks = world_chunks.split(". Processed: ")[1]
                        cps = line.split(", Rate: ")[1]
                        cps = float(cps.split(" cps")[0])
                        cps_list.append(cps)
        cps_dist = statistics.NormalDist.from_samples(cps_list)
        score = round(cps_dist.mean, 3)
        print(f"Analyzed data from {i} minutes\n"
              f"Mean chunk generation speed per world is {score}\n")
elif not multi:
    with open("latest.log", 'r') as file:
        i = -10
        median_mspt_list = []
        gen_started = False
        for line in file:
            if not gen_started:
                if "Timings Reset" in line:
                    gen_started = True
            elif i < 110:
                if i < 0:
                    if "âš¡" in line or "?" in line or "⚡" in line:
                        if ';' in line:
                            i += 1
                else:
                    if "âš¡" in line or "?" in line or "⚡" in line:
                        if ';' in line:
                            i += 1
                            line = line.replace("\n", "")
                            med = float(line.split("/")[5])
                            median_mspt_list.append(med)
        median_mspt_dist = statistics.NormalDist.from_samples(median_mspt_list)
        score = round(median_mspt_dist.mean, 3)
        print(f"Analyzed data from {i} minutes\n"
              f"Mean MSPT per world is {score}\n")

# Might implement this later, probably going to confuse more than it helps so maybe not
# location_var = input("What is the location? ")
# host_var = input("What is the host? ")
# plan_var = input("What is the plan? ")
# ram_var = input("How much memory? ")
# score_bool = input(f"Override the score ({score})? (y/n) ")
# failed = False
# if score_bool.lower == "y":
#     score = input('What is the score? If the test failed, say "FAIL". ')
#     if score.lower == "fail":
#         failed = True
#     else:
#         score_var = score.lower()
# else:
#     score_var = score
#     failed = False

