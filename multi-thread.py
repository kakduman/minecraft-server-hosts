import statistics

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
                if "âš¡" in line or "?" in line:
                    if ';' in line:
                        i += 1
            else:
                if "âš¡" in line or "?" in line:
                    if ';' in line:
                        i += 1
                elif "Task running for world" in line:
                    world_chunks = line.split(" chunks (")[0]
                    world_chunks = world_chunks.split(". Processed: ")[1]
                    cps = line.split(", Rate: ")[1]
                    cps = float(cps.split(" cps")[0])
                    cps_list.append(cps)

cps_dist = statistics.NormalDist.from_samples(cps_list)

print(f"Analyzed data from {i} minutes\n"
      f"Mean chunk generation speed per world is {round(cps_dist.mean, 3)}\n")
