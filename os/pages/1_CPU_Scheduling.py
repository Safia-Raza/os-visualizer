import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("CPU Scheduling")
st.caption("Pick an algorithm, edit the process table, and run the simulation.")

top1, top2, top3 = st.columns([2, 1, 1])
algo = top1.selectbox("Algorithm", ["FCFS", "SJF (Non-Preemptive)",
                                    "Priority (Non-Preemptive)", "Round Robin"])
quantum = top2.number_input("Time quantum", min_value=1, value=2,
                            disabled=(algo != "Round Robin"))
n = int(top3.number_input("Number of processes", min_value=1, max_value=10, value=4))

st.markdown("##### Processes")
base = pd.DataFrame({
    "Process": [f"P{i + 1}" for i in range(n)],
    "Arrival": [i for i in range(n)],
    "Burst": [3] * n,
    "Priority": [i + 1 for i in range(n)],
})
table = st.data_editor(
    base, key=f"procs_{n}", hide_index=True, width="stretch",
    disabled=["Process"],
    column_config={
        "Arrival": st.column_config.NumberColumn(min_value=0, step=1),
        "Burst": st.column_config.NumberColumn(min_value=1, step=1),
        "Priority": st.column_config.NumberColumn(min_value=1, step=1,
                                                  help="Lower number = higher priority. Used by Priority scheduling only."),
    },
)

procs = [{"pid": r.Process, "at": int(r.Arrival), "bt": max(1, int(r.Burst)),
          "pr": int(r.Priority)} for r in table.itertuples()]


def fcfs(p):
    p = sorted(p, key=lambda x: x["at"])
    t, gantt = 0, []
    for x in p:
        t = max(t, x["at"])
        gantt.append((x["pid"], t, t + x["bt"]))
        t += x["bt"]
    return gantt


def sjf(p):
    p = [x.copy() for x in p]
    t, gantt = 0, []
    while p:
        ready = [x for x in p if x["at"] <= t]
        if not ready:
            t = min(x["at"] for x in p)
            continue
        x = min(ready, key=lambda r: (r["bt"], r["at"]))
        gantt.append((x["pid"], t, t + x["bt"]))
        t += x["bt"]
        p.remove(x)
    return gantt


def priority(p):
    p = [x.copy() for x in p]
    t, gantt = 0, []
    while p:
        ready = [x for x in p if x["at"] <= t]
        if not ready:
            t = min(x["at"] for x in p)
            continue
        x = min(ready, key=lambda r: (r["pr"], r["at"]))
        gantt.append((x["pid"], t, t + x["bt"]))
        t += x["bt"]
        p.remove(x)
    return gantt


def rr(p, q):
    p = sorted(p, key=lambda x: x["at"])
    rem = {x["pid"]: x["bt"] for x in p}
    t, gantt, queue, i = 0, [], [], 0
    while i < len(p) or queue:
        if not queue:
            t = max(t, p[i]["at"])
        while i < len(p) and p[i]["at"] <= t:
            queue.append(p[i]["pid"])
            i += 1
        pid = queue.pop(0)
        run = min(q, rem[pid])
        gantt.append((pid, t, t + run))
        t += run
        rem[pid] -= run
        while i < len(p) and p[i]["at"] <= t:
            queue.append(p[i]["pid"])
            i += 1
        if rem[pid] > 0:
            queue.append(pid)
    return gantt


if st.button("Run simulation", type="primary"):
    if algo == "FCFS":
        gantt = fcfs(procs)
    elif algo.startswith("SJF"):
        gantt = sjf(procs)
    elif algo.startswith("Priority"):
        gantt = priority(procs)
    else:
        gantt = rr(procs, int(quantum))

    rows = []
    for x in procs:
        ct = max(e for pid, s, e in gantt if pid == x["pid"])
        tat = ct - x["at"]
        wt = tat - x["bt"]
        rows.append({"Process": x["pid"], "Arrival": x["at"], "Burst": x["bt"],
                     "Completion": ct, "Turnaround": tat, "Waiting": wt})
    df = pd.DataFrame(rows)

    st.markdown("##### Results")
    m1, m2, m3 = st.columns(3)
    m1.metric("Average waiting time", f"{df['Waiting'].mean():.2f}")
    m2.metric("Average turnaround time", f"{df['Turnaround'].mean():.2f}")
    m3.metric("Total time", max(e for _, _, e in gantt))
    st.dataframe(df, width="stretch", hide_index=True)

    st.markdown("##### Gantt chart")
    palette = ["#7FA6E8", "#6FC2B5", "#E0B472", "#D68C7C", "#9FC27F",
               "#8FB5D6", "#D6C27F", "#9AA9C2", "#C9A08A", "#7FC0C9"]
    bg = "#0A0E14"
    fig, ax = plt.subplots(figsize=(11, 1.9))
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    for pid, s, e in gantt:
        k = int(pid[1:]) - 1
        ax.barh(0, e - s, left=s, height=0.55, color=palette[k % 10],
                edgecolor=bg, linewidth=1.5)
        ax.text((s + e) / 2, 0, pid, ha="center", va="center",
                color=bg, fontsize=10, fontweight="bold")
    ax.set_xticks(sorted({s for _, s, _ in gantt} | {e for _, _, e in gantt}))
    ax.tick_params(axis="x", colors="#8A97AB", labelsize=9, length=3)
    ax.set_yticks([])
    ax.set_ylim(-0.5, 0.5)
    for name, sp in ax.spines.items():
        sp.set_visible(name == "bottom")
        sp.set_color("#2A3544")
    fig.tight_layout()
    st.pyplot(fig)
