# Swarm_Robots
Miami University Senior Capstone Project 2021-2022

Copyright 2022 Cole Hengstebeck, Noah Macdonald, Grant Parker 

Project supervisors Dr Peter Jamieson, Dr Brian Van Scoy

## UDP
This branch creates the source code for UDP communications on the central system end to the agents. This module uses the MAVLink libraries. Dependencies should be included, but if not, run:
```bash
git clone git@github.com:mavlink/c_library_v2.git
```

run
```bash
C_INCLUDE_PATH=~/Git/Swarm_Robots/include/Mavlink/
export C_INCLUDE_PATH
```

gcc publisher.c -o publisher -I /home/coleh/Git/Swarm_Robots/include/Mavlink -I /home/coleh/Git/Swarm_Robots/include/Mavlink/common