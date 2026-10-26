import streamlit as st

st.markdown("""
<style>
.eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem;
           letter-spacing: 0.14em; color: #6F7C90; margin: 56px 0 18px 0; }
.lede { color: #98A5B8; font-size: 1.05rem; line-height: 1.65;
        max-width: 540px; margin: 8px 0 48px 0; }
.rule { border: 0; border-top: 1px solid #1E2733; margin: 0; }
.num { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #55627A; }
.mod-title { font-family: 'Instrument Serif', serif; font-size: 1.9rem;
             color: #E8EDF5; line-height: 1.1; margin: 0; }
.mod-desc { color: #8895A9; font-size: 0.92rem; margin: 6px 0 0 0; }
.algos { font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #7E8CA2; }
.foot { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;
        color: #55627A; margin-top: 56px; }
</style>
<div class="eyebrow">OPERATING SYSTEMS &nbsp;/&nbsp; COURSE PROJECT</div>
""", unsafe_allow_html=True)

st.title("OS Algorithms Visualizer")
st.markdown(
    '<p class="lede">Interactive simulations of the scheduling, memory and deadlock '
    'algorithms covered in class. Enter your own inputs, run the algorithm, and '
    'compare the results.</p>',
    unsafe_allow_html=True,
)

modules = [
    ("01", "CPU Scheduling",
     "Gantt chart with waiting and turnaround times.",
     "FCFS · SJF · Priority · Round Robin",
     "pages/1_CPU_Scheduling.py"),
    ("02", "Page Replacement",
     "Hit and fault trace with a side-by-side comparison.",
     "FIFO · LRU · Optimal",
     "pages/2_Page_Replacement.py"),
    ("03", "Deadlock Avoidance",
     "Need matrix, safety check and safe sequence.",
     "Banker's Algorithm",
     "pages/3_Bankers_Algorithm.py"),
]

for num, title, desc, algos, path in modules:
    st.markdown('<hr class="rule">', unsafe_allow_html=True)
    c0, c1, c2, c3 = st.columns([0.5, 3.2, 2.6, 1.2], vertical_alignment="center")
    c0.markdown(f'<span class="num">{num}</span>', unsafe_allow_html=True)
    c1.markdown(f'<p class="mod-title">{title}</p><p class="mod-desc">{desc}</p>',
                unsafe_allow_html=True)
    c2.markdown(f'<span class="algos">{algos}</span>', unsafe_allow_html=True)
    c3.page_link(path, label="Open  →")
st.markdown('<hr class="rule">', unsafe_allow_html=True)

st.markdown('<div class="foot">PYTHON · STREAMLIT · MATPLOTLIB · PANDAS</div>',
            unsafe_allow_html=True)
