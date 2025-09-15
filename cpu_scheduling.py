import argparse
from collections import deque, defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

@dataclass
class Process:
    pid: str
    arrival: int
    burst: int
    remaining: int = field(init=False)
    start_time: int = field(default=None) 
    finish_time: int = field(default=None) 

    def __post_init__(self):
        self.remaining = self.burst

def metrics(processes: Dict[str, Process]) -> Tuple[Dict[str, Dict[str, int]], Dict[str, float]]:
    """Compute Waiting, Turnaround, Response for each process + averages."""
    per = {}
    total_w = total_t = total_r = 0.0
    n = len(processes)
    for pid, p in processes.items():
        turnaround = p.finish_time - p.arrival
        waiting = turnaround - p.burst
        response = p.start_time - p.arrival
        per[pid] = {"W": waiting, "T": turnaround, "R": response}
        total_w += waiting
        total_t += turnaround
        total_r += response
    avgs = {
        "Waiting": round(total_w / n, 1),
        "Turnaround": round(total_t / n, 1),
        "Response": round(total_r / n, 1),
    }
    return per, avgs

def print_results(title: str, gantt: List[Tuple[str, int, int]], processes: Dict[str, Process]) -> None:
    print(title)
    timeline = "".join([f"[{pid}:{s}–{e}]" for pid, s, e in gantt])
    print(f"Gantt: {timeline}")
    per, avgs = metrics(processes)
    print("Per-process (W / T / R):")
    for pid in sorted(per.keys(), key=lambda x: int(x[1:]) if x[0] in {"P","p"} and x[1:].isdigit() else x):
        m = per[pid]
        print(f"{pid}: {m['W']} / {m['T']} / {m['R']}")
    print(f"Averages: Waiting {avgs['Waiting']}, Turnaround {avgs['Turnaround']}, Response {avgs['Response']}")
    print()

def schedule_fcfs(procs: List[Process]) -> Tuple[List[Tuple[str, int, int]], Dict[str, Process]]:
    procs = sorted(procs, key=lambda p: (p.arrival, p.pid))
    time = 0
    gantt = []
    proc_map = {p.pid: p for p in procs}

    for p in procs:
        if time < p.arrival:
            time = p.arrival
        if p.start_time is None:
            p.start_time = time
        start = time
        time += p.burst
        p.remaining = 0
        p.finish_time = time
        gantt.append((p.pid, start, time))

    return gantt, proc_map

def schedule_sjf_nonpreemptive(procs: List[Process]) -> Tuple[List[Tuple[str, int, int]], Dict[str, Process]]:
    procs_sorted = sorted(procs, key=lambda p: (p.arrival, p.pid))
    time = 0
    gantt = []
    proc_map = {p.pid: Process(p.pid, p.arrival, p.burst) for p in procs_sorted}

    ready: List[Process] = []
    i = 0
    n = len(procs_sorted)

    while i < n or ready:
        if not ready and time < procs_sorted[i].arrival:
            time = procs_sorted[i].arrival
        while i < n and procs_sorted[i].arrival <= time:
            ready.append(proc_map[procs_sorted[i].pid])
            i += 1
        ready.sort(key=lambda p: (p.burst, p.arrival, p.pid))
        p = ready.pop(0)

        if p.start_time is None:
            p.start_time = time
        start = time
        time += p.burst
        p.remaining = 0
        p.finish_time = time
        gantt.append((p.pid, start, time))

    return gantt, proc_map

def schedule_rr(procs: List[Process], q: int) -> Tuple[List[Tuple[str, int, int]], Dict[str, Process]]:
    procs_sorted = sorted(procs, key=lambda p: (p.arrival, p.pid))
    time = 0
    gantt = []
    proc_map = {p.pid: Process(p.pid, p.arrival, p.burst) for p in procs_sorted}

    i = 0
    ready = deque()

    def enqueue_arrivals_up_to(t_end):
        nonlocal i
        while i < len(procs_sorted) and procs_sorted[i].arrival <= t_end:
            ready.append(proc_map[procs_sorted[i].pid])
            i += 1

    if i < len(procs_sorted):
        time = procs_sorted[i].arrival
        enqueue_arrivals_up_to(time)

    while ready or i < len(procs_sorted):
        if not ready:
            time = procs_sorted[i].arrival
            enqueue_arrivals_up_to(time)

        p = ready.popleft()
        if p.start_time is None:
            p.start_time = time

        run = min(q, p.remaining)
        start = time
        end = time + run

        enqueue_arrivals_up_to(end)

        p.remaining -= run
        time = end
        gantt.append((p.pid, start, end))

        if p.remaining > 0:
            ready.append(p)
        else:
            p.finish_time = time

    return gantt, proc_map


def load_default_dataset() -> List[Process]:
    return [
        Process("P1", 0, 7),
        Process("P2", 2, 4),
        Process("P3", 4, 1),
        Process("P4", 5, 4),
        Process("P5", 6, 3),
    ]

def main():
    parser = argparse.ArgumentParser(description="Tiny CPU Scheduler Simulator")
    parser.add_argument("--algo", choices=["FCFS", "RR", "SJF"], required=True,
                        help="Scheduling algorithm: FCFS | RR | SJF (non-preemptive).")
    parser.add_argument("--quantum", type=int, default=2,
                        help="Time quantum (only used for RR). Default: 2")
    args = parser.parse_args()

    dataset = load_default_dataset()

    if args.algo == "FCFS":
        gantt, proc_map = schedule_fcfs([Process(p.pid, p.arrival, p.burst) for p in dataset])
        print_results("== FCFS ==", gantt, proc_map)

    elif args.algo == "SJF":
        gantt, proc_map = schedule_sjf_nonpreemptive(dataset)
        print_results("== SJF (Non-preemptive) ==", gantt, proc_map)

    elif args.algo == "RR":
        if args.quantum <= 0:
            raise SystemExit("For RR, --quantum must be a positive integer.")
        gantt, proc_map = schedule_rr(dataset, args.quantum)
        print_results(f"== Round Robin (q={args.quantum}) ==", gantt, proc_map)

if __name__ == "__main__":
    main()
