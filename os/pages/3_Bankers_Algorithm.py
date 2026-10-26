import streamlit as st
import pandas as pd

st.title("Banker's Algorithm")
st.caption("Check whether a system state is safe and find a safe sequence.")

c1, c2, _ = st.columns([1, 1, 3])
n = int(c1.number_input("Processes", 1, 10, 5))
m = int(c2.number_input("Resource types", 1, 5, 3))
procs = [f"P{i}" for i in range(n)]
res = [chr(65 + j) for j in range(m)]

if n == 5 and m == 3:
    alloc0 = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
    max0 = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
    avail0 = [3, 3, 2]
else:
    alloc0 = [[0] * m for _ in range(n)]
    max0 = [[0] * m for _ in range(n)]
    avail0 = [0] * m

left, right = st.columns(2)
with left:
    st.markdown("##### Allocation")
    alloc = st.data_editor(pd.DataFrame(alloc0, index=procs, columns=res),
                           key=f"a{n}{m}", width="stretch")
with right:
    st.markdown("##### Max")
    mx = st.data_editor(pd.DataFrame(max0, index=procs, columns=res),
                        key=f"m{n}{m}", width="stretch")

st.markdown("##### Available")
av = st.data_editor(pd.DataFrame([avail0], index=["Available"], columns=res),
                    key=f"v{n}{m}", width="stretch")

if st.button("Check safety", type="primary"):
    A = alloc.values.astype(int)
    M = mx.values.astype(int)
    work = list(av.iloc[0].values.astype(int))
    need = M - A

    if (need < 0).any():
        st.error("Max cannot be less than Allocation. Please check the input.")
        st.stop()

    done = [False] * n
    seq, steps = [], []
    progress = True
    while progress:
        progress = False
        for i in range(n):
            if not done[i] and all(need[i][j] <= work[j] for j in range(m)):
                before = work.copy()
                work = [work[j] + A[i][j] for j in range(m)]
                done[i] = True
                seq.append(procs[i])
                steps.append({"Process": procs[i],
                              "Work before": str(before),
                              "Work after": str(work)})
                progress = True

    if all(done):
        st.success("Safe state.  Safe sequence:  " + "  →  ".join(seq))
    else:
        stuck = [procs[i] for i in range(n) if not done[i]]
        st.error("Unsafe state. Risk of deadlock. Blocked processes: " + ", ".join(stuck))

    l2, r2 = st.columns(2)
    with l2:
        st.markdown("##### Need matrix  (Max − Allocation)")
        st.dataframe(pd.DataFrame(need, index=procs, columns=res), width="stretch")
    with r2:
        if steps:
            st.markdown("##### Steps")
            st.dataframe(pd.DataFrame(steps), hide_index=True, width="stretch")
