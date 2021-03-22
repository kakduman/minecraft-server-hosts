# Minecraft Server Host Comparisons
This repository aims to benchmark the performance of various hosts in order to obtain numbers that are applicable to real-world performance. The overall load on the server, the storage type, and verious other aspects of a server can have impacts on its speed. These benchmarks aim to account for all factors and reveal numbers corresponding to performance. Please feel free to PR.

# Methodology
The single-thread test observes the inverse of MSPT (i.e. TPS) while the server is ticking 2000 minecarts.
The multi-thread test observes the chunk generation speed while the server is generating 3 overworlds simultaneously using Chunky.
Results are standardized by setting the dedicated G4400 machine to a score of 100. The G4400 was chosen to standardize results because I had an old G4400 computer lying around, and the processor gives consistent results since datacenter ambient temperature, node load, etc. cannot impact performance.
95% confidence intervals are generated with a t-interval. Results are assumed to be normally distributed across nodes and times of day. Confidence intervals are only available when 3+ measurements of a certain plan have been analyzed. Do NOT attempt to make comparisons between hosts if 1 or more of them does not have a confidence interval present. More testing is needed to generate a significant comparison.

# Results
![image](https://user-images.githubusercontent.com/43528123/112066487-6c82be00-8b34-11eb-9521-5a49fe95cbe9.png)
![image](https://user-images.githubusercontent.com/43528123/112066502-74426280-8b34-11eb-88ed-56b12e282dc4.png)

Do **NOT** attempt to make comparisons between hosts if 1 or more of them does not have a confidence interval present. Confidence intervals are only available when 3+ measurements of a certain plan have been analyzed. More testing is needed to generate a significant comparison.


# Contributing
### Testing
1. Wipe the target directory of the server you are testing.
2. Upload and extract the [single-thread-setup.tar.gz](/single-thread-setup.tar.gz) file for single-thread tests, or the [multi-thread-setup.tar.gz](/multi-thread-setup.tar.gz) for multi-thread tests.
3. Create a scheduled task for executing `spark:tps` every minute. You can also create a hotkey or script to execute the command through the console if the host does not allow scheduled tasks
4. Wait at least 2 hours, then stop the server.
5. Clone this GitHub repository
6. Download latest.log into the cloned repository
7. Execute analyze_logs.py. If there is an issue, please report it.
8. Otherwise, type the output along with other relevant information (location, host, plan, memory, PERMANENT link to logs, and node) into the corresponding raw csv: [single-thread-raw.csv](/single-thread-raw.csv) for single-thread or [multi-thread-raw.csv](/multi-thread-raw.csv) for multi-thread.
9. Execute analyze_csv.py. If there is an issue, please report it.
10. [OPTIONAL] Update the Charts.xlsx spreadsheet to update the graph of performance comparisons. If you do not have Excel or otherwise cannot update the chart, please skip this step.
11. Create a PR to the master branch.

### Other
Please feel free to create a PR for other aspects of this test that could be improved. It is far from perfect.
