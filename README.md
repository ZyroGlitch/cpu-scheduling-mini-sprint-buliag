# CPU Scheduling Mini-Project
It is the lightweight Python implementation of a CPU scheduling simulator. It has First- Come, First-Served (FCFS), Round Robin (RR) and with a quantum parametable (default =2) and shortest job first (SJF, non-preemptive) (optional). This simulator creates a kind of Gantt-type execution schedule, calculates process-specific measures (waiting, turnaround, and response times), and provides average values.

# How to Run:
First-Come, First-Served
- python cpu_scheduling.py --algo FCFS

Round Robin with quantum = 2
- python cpu_scheduling.py --algo RR --quantum 2

Shortest Job First
- python cpu_scheduling.py --algo SJF


# OUTPUT
### FCFS

**Gantt Chart:**  
`[P1:0–7][P2:7–11][P3:11–12][P4:12–16][P5:16–19]`

**Per-process metrics**

| PID | Waiting (W) | Turnaround (T) | Response (R) |
|-----|-------------|----------------|--------------|
| P1  | 0           | 7              | 0            |
| P2  | 5           | 9              | 5            |
| P3  | 7           | 8              | 7            |
| P4  | 7           | 11             | 7            |
| P5  | 10          | 13             | 10           |

**Averages**  
- Waiting: **5.8**  
- Turnaround: **9.6**  
- Response: **5.8**


### Round Robin (q=2)

**Gantt Chart:**  
`[P1:0–2][P2:2–4][P1:4–6][P3:6–7][P2:7–9][P4:9–11][P5:11–13][P1:13–15][P4:15–17][P5:17–18][P1:18–19]`

**Per-process metrics**

| PID | Waiting (W) | Turnaround (T) | Response (R) |
|-----|-------------|----------------|--------------|
| P1  | 12          | 19             | 0            |
| P2  | 3           | 7              | 0            |
| P3  | 2           | 3              | 2            |
| P4  | 8           | 12             | 4            |
| P5  | 9           | 12             | 5            |

**Averages**  
- Waiting: **6.8**  
- Turnaround: **10.6**  
- Response: **2.2**


### SJF (Non-preemptive)

**Gantt Chart:**  
`[P1:0–7][P3:7–8][P5:8–11][P2:11–15][P4:15–19]`

**Per-process metrics**

| PID | Waiting (W) | Turnaround (T) | Response (R) |
|-----|-------------|----------------|--------------|
| P1  | 0           | 7              | 0            |
| P3  | 3           | 4              | 3            |
| P5  | 2           | 5              | 2            |
| P2  | 9           | 13             | 9            |
| P4  | 10          | 14             | 10           |

**Averages**  
- Waiting: **4.8**  
- Turnaround: **8.6**  
- Response: **4.8**


# How Metrics are Computed

- **Turnaround Time (T)** = `Finish time − Arrival time`  
- **Waiting Time (W)** = `Turnaround time − Burst time`  
- **Response Time (R)** = `First start time − Arrival time`  






