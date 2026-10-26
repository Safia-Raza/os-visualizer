import streamlit as st
import pandas as pd

st.title("Page Replacement")
st.caption("Compare how FIFO, LRU and Optimal handle the same reference string.")

c1, c2, c3 = st.columns([4, 1, 1.5])
text = c1.text_input("Reference string (separated by spaces)",
                     "7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1")
n = int(c2.number_input("Frames", min_value=1, max_value=10, value=3))
algo = c3.selectbox("Algorithm", ["FIFO", "LRU", "Optimal"])


def run(pages, n, algo):
    frames, rows, faults = [], [], 0
    for i, p in enumerate(pages):
        hit = p in frames
        if not hit:
            faults += 1
            if len(frames) < n:
                frames.append(p)
            elif algo == "FIFO":
                frames.pop(0)
                frames.append(p)
            elif algo == "LRU":
                victim = min(frames, key=lambda f: max(j for j in range(i) if pages[j] == f))
                frames[frames.index(victim)] = p
            else:
                def next_use(f):
                    for j in range(i + 1, len(pages)):
                        if pages[j] == f:
                            return j
                    return float("inf")
                victim = max(frames, key=next_use)
                frames[frames.index(victim)] = p
        rows.append({"Step": i + 1, "Page": p,
                     "Frames": " | ".join(map(str, frames)),
                     "Result": "Hit" if hit else "Fault"})
    return rows, faults


if st.button("Run simulation", type="primary"):
    pages = text.split()
    if not pages:
        st.warning("Enter at least one page number.")
        st.stop()
    rows, faults = run(pages, n, algo)
    total = len(pages)

    st.markdown("##### Results")
    m1, m2, m3 = st.columns(3)
    m1.metric("Page faults", faults)
    m2.metric("Page hits", total - faults)
    m3.metric("Hit ratio", f"{(total - faults) / total * 100:.1f}%")
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)

    st.markdown("##### Comparison")
    comp = {a: run(pages, n, a)[1] for a in ["FIFO", "LRU", "Optimal"]}
    st.bar_chart(pd.Series(comp, name="Page faults"))
