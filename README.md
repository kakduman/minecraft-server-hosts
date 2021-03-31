# Minecraft Server Host Comparisons
This repository aims to benchmark the performance of various hosts in order to obtain numbers that are applicable to real-world performance. The overall load on the server, the storage type, and verious other aspects of a server can have impacts on its speed. These benchmarks aim to account for all factors and reveal numbers corresponding to performance. Please feel free to PR.

# Methodology
The Entity Tick test observes the inverse of MSPT (i.e. TPS) while the server is ticking 2000 minecarts. This entity tick test was chosen to be indicative of single-thread performance.

The Chunk Generation test observes the chunk generation speed while the server is generating 3 overworlds simultaneously using Chunky. If the server crashes due to insufficient overhead, support is contacted to ask to resolve the issue either by (1) modifying heap size, (2) lowering Xmx without lowering the container memory, (3) adding memory for overhead, or (4) adding swap for overhead. If support declines all requests to resolve the issue, a score of 0 is issued. This chunk generation test was chosen to be indicative of multi-thread performance when utilizing all threads.

Results are standardized by setting the dedicated G4400 machine to a score of 100. The G4400 was chosen to standardize results because I had an old G4400 computer lying around, and the processor gives consistent results since datacenter ambient temperature, node load, etc. cannot impact performance.

95% confidence intervals are generated with a t-interval. Results are assumed to be normally distributed across nodes and times of day. Confidence intervals are only available when 3+ measurements of a certain plan have been analyzed. Do NOT attempt to make comparisons between hosts if 1 or more of them does not have a confidence interval present. More testing is needed to generate a significant comparison.

# Results
![image](https://user-images.githubusercontent.com/43528123/113198349-6d4ddb00-922b-11eb-82d5-3e92b1ee5b03.png)

### Disclaimers 
- Confidence intervals can only be generated if identical servers on at least 3 unique nodes of any host were tested. Only results with confidence intervals are shown in the above chart. Comparisons **cannot** be made between hosts with insufficient data for confidence intervals. If you would like to view all results, you can see [single-thread-results.csv](/single-thread-results.csv) for entity tick results, or [multi-thread-results.csv](/multi-thread-results.csv) for chunk generation results. Again, **DO NOT COMPARE HOSTS THAT DON'T HAVE CONFIDENCE INTERVALS.**
- All results were analyzed by Purpur#7580, the owner of Birdflop. All tests were conducted with the same methodology/setup, but a disclaimer for this information is still important.
- Confidence intervals assume that results are normally distributed. In reality, results may not be normally distributed, so the confidence intervals may be inaccurate.
- If you're going to send a screenshot of the charts, please include these disclaimers alongside it.

# Contributing
### Testing
1. Wipe the target directory of the server you are testing.
2. If the host allows for it, use Java 11 and PERMANENT Aikar's Flags. Do not edit any other variables.
3. Upload and extract the [single-thread-test.tar.gz](/single-thread-test.tar.gz) file for Entity Tick tests, or the [multi-thread-test.tar.gz](/multi-thread-test.tar.gz) file for Chunk Generation tests.
4. Create a scheduled task for executing `spark:tps` every minute. You can also create a hotkey or script to execute the command through the console if the host does not allow scheduled tasks
5. Wait at least 2 hours, then stop the server.
6. Clone this GitHub repository
7. Download latest.log into the cloned repository
8. Execute analyze_logs.py. If there is an issue, please report it.
9. Otherwise, type the output along with other relevant information (location, host, plan, memory, PERMANENT link to logs, and node) into the corresponding raw csv: [single-thread-raw.csv](/single-thread-raw.csv) for Entity Tick or [multi-thread-raw.csv](/multi-thread-raw.csv) for Chunk Generation.
10. Execute analyze_csv.py. If there is an issue, please report it.
11. [OPTIONAL] Update the Charts.xlsx spreadsheet to update the graph of performance comparisons. If you do not have Excel or otherwise cannot update the chart, please skip this step.
12. Create a PR to the master branch.

### Other
Please feel free to create a PR for other aspects of this test that could be improved. It is far from perfect.

# Contributors
All contributors are listed below to show appreciation and accountability.

Thank you to the following for their help expanding this experiment:
- Jay from [PebbleHost](https://pebblehost.com) for various PebbleHost servers.
- Tehlo from [DedicatedMC](https://dedicatedmc.io) for various DedicatedMC servers.
- Nerd from [EnviroMC](https://enviromc.com) for various EnviroMC servers.
- Valentijn from [Volcano Hosting](https://volcanohosting.net) for the Volcano Hosting server.
- sprit#0363 for the Daemex server.
- SeaSon#5421 for the SkyNode server.
- JustDoom#1120 for the 4GB PebbleHost Premium server.
- DefineOutside#4497 for the 3GB PebbleHost Budget server.
- Abby from [BloomHost](https://bloom.host) for all BloomHost servers.
- Purpur from [Birdflop Hosting](https://birdflop.com) for the Birdflop servers and the baseline dedicated server.

# Additional Notes
- SkyNode failed the Chunk Generation test because the server kept crashing due to insufficient overhead. Support refused to lower Xmx without lowering the container size, add swap overhead, or add memory overhead.
- Currently waiting on RetroNode servers to test. Support says that they are out of stock right now, but that they will provide servers when stock arrives.
- Currently waiting on a response from HeavyNode regarding servers to test.
