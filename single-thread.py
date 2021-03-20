import statistics

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
                if "âš¡" in line or "?" in line:
                    if ';' in line:
                        i += 1
            else:
                if "âš¡" in line or "?" in line:
                    if ';' in line:
                        i += 1
                        line = line.replace("\n", "")
                        med = float(line.split("/")[6])
                        median_mspt_list.append(med)

median_mspt_dist = statistics.NormalDist.from_samples(median_mspt_list)

print(f"Analyzed data from {i} minutes\n"
      f"Mean MSPT per world is {round(median_mspt_dist.mean, 3)}\n")

