"""
The Leveler — Construction Bid Leveling & Scope Gap Detection Engine
Senior Full-Stack / Construction Tech Architecture
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO
import json

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="The Leveler | Bid Intelligence Platform",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Midnight Professional CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ── */
.stApp { background-color: #0F172A; color: #F8FAFC; }
html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #020617;
    border-right: 1px solid #334155;
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 { color: #38BDF8; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: #0F172A;
    border-bottom: 1px solid #334155;
    padding-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
    background-color: #1E293B;
    border-radius: 6px 6px 0 0;
    color: #94A3B8;
    border: 1px solid #334155;
    border-bottom: none;
    padding: 8px 20px;
    font-weight: 500;
    transition: all 0.2s ease;
}
.stTabs [aria-selected="true"] {
    background-color: #38BDF8 !important;
    color: #0F172A !important;
    font-weight: 700 !important;
    border-color: #38BDF8 !important;
}
.stTabs [data-baseweb="tab"]:hover { color: #F8FAFC; background-color: #263348; }

/* ── Metrics ── */
[data-testid="stMetric"] {
    background-color: #1E293B;
    padding: 16px 20px;
    border-radius: 10px;
    border: 1px solid #334155;
}
[data-testid="stMetric"] label { color: #94A3B8 !important; font-size: 0.78rem; }
[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #F8FAFC; font-size: 1.5rem; font-weight: 700; }
[data-testid="stMetricDelta"] { font-size: 0.85rem; }

/* ── Inputs ── */
.stTextInput input, .stNumberInput input, .stSelectbox select,
[data-baseweb="input"] input, [data-baseweb="select"] {
    background-color: #1E293B !important;
    border: 1px solid #334155 !important;
    color: #F8FAFC !important;
    border-radius: 6px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #38BDF8 !important;
    box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.15) !important;
}

/* ── Buttons ── */
.stButton button {
    background-color: #38BDF8 !important;
    color: #0F172A !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    padding: 8px 20px !important;
    transition: all 0.2s ease !important;
}
.stButton button:hover {
    background-color: #7DD3FC !important;
    box-shadow: 0 0 16px rgba(56, 189, 248, 0.4) !important;
    transform: translateY(-1px) !important;
}

/* ── Cards / Containers ── */
.card {
    background: linear-gradient(135deg, #1E293B 0%, #162032 100%);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.trade-header {
    background: linear-gradient(90deg, #1E293B 0%, #0F172A 100%);
    border-left: 3px solid #38BDF8;
    padding: 12px 20px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 20px;
}
.trade-header h3 { color: #38BDF8; margin: 0; font-size: 1.1rem; letter-spacing: 0.05em; text-transform: uppercase; }
.trade-header p { color: #94A3B8; margin: 4px 0 0 0; font-size: 0.82rem; }

/* ── Gap / Status Badges ── */
.gap-critical {
    color: #FB7185;
    font-weight: 700;
    background-color: rgba(251, 113, 133, 0.1);
    border: 1px solid rgba(251, 113, 133, 0.3);
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.78rem;
    letter-spacing: 0.05em;
}
.gap-ok {
    color: #34D399;
    background-color: rgba(52, 211, 153, 0.1);
    border: 1px solid rgba(52, 211, 153, 0.3);
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.78rem;
}
.winner-badge {
    background: linear-gradient(90deg, #38BDF8, #0EA5E9);
    color: #0F172A;
    font-weight: 800;
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 0.75rem;
    letter-spacing: 0.06em;
}

/* ── DataFrames ── */
[data-testid="stDataFrame"] { border: 1px solid #334155; border-radius: 8px; overflow: hidden; }
.stDataFrame thead th { background-color: #1E293B !important; color: #38BDF8 !important; }
.stDataFrame tbody tr:nth-child(even) { background-color: #162032 !important; }
.stDataFrame tbody tr:hover { background-color: #1E293B !important; }

/* ── Section Divider ── */
hr { border-color: #334155; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 8px;
}
[data-testid="stExpander"] summary { color: #94A3B8; }

/* ── Selectbox dropdown ── */
[data-baseweb="popover"] { background-color: #1E293B !important; border: 1px solid #334155 !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background-color: #1E293B;
    border: 1px dashed #334155;
    border-radius: 8px;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0F172A; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #475569; }

/* ── Markdown labels ── */
label, .stMarkdown p { color: #94A3B8; }
h1, h2, h3 { color: #F8FAFC; }
</style>
""", unsafe_allow_html=True)

# ── Plotly Dark Template ────────────────────────────────────────────────────────
PLOTLY_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        font=dict(family="Inter, Segoe UI, sans-serif", color="#F8FAFC", size=12),
        title=dict(font=dict(color="#F8FAFC", size=16), x=0.02),
        xaxis=dict(gridcolor="#334155", linecolor="#334155", tickfont=dict(color="#94A3B8")),
        yaxis=dict(gridcolor="#334155", linecolor="#334155", tickfont=dict(color="#94A3B8")),
        legend=dict(bgcolor="#0F172A", bordercolor="#334155", borderwidth=1, font=dict(color="#94A3B8")),
        coloraxis_colorbar=dict(tickfont=dict(color="#94A3B8")),
        margin=dict(l=20, r=20, t=50, b=20),
    )
)

COLORS = {
    "sub_a": "#38BDF8",
    "sub_b": "#A78BFA",
    "sub_c": "#34D399",
    "budget": "#FB923C",
    "gap": "#FB7185",
    "bg_card": "#1E293B",
    "border": "#334155",
}

TRADES = ["Drywall", "MEP", "Interiors", "Site Work"]

# ── Session State Init ──────────────────────────────────────────────────────────
def init_session_state():
    if "master_scope" not in st.session_state:
        st.session_state.master_scope = pd.DataFrame(
            columns=["Trade", "Item", "Unit", "Quantity", "Unit_Cost", "Budget_Total", "Description"]
        )
    if "subs" not in st.session_state:
        st.session_state.subs = {}
        for trade in TRADES:
            st.session_state.subs[trade] = {
                "A": {"name": "", "total": 0.0, "inclusions": [], "exclusions": []},
                "B": {"name": "", "total": 0.0, "inclusions": [], "exclusions": []},
                "C": {"name": "", "total": 0.0, "inclusions": [], "exclusions": []},
            }
    if "plug_rates" not in st.session_state:
        st.session_state.plug_rates = {}

init_session_state()

# ── Helper Functions ────────────────────────────────────────────────────────────
def get_trade_scope(trade: str) -> pd.DataFrame:
    df = st.session_state.master_scope
    if df.empty:
        return pd.DataFrame()
    return df[df["Trade"] == trade].copy()

def detect_gaps(trade: str, sub_key: str) -> dict:
    """Returns dict with 'missing_items' list and 'gap_cost' float."""
    scope_df = get_trade_scope(trade)
    if scope_df.empty:
        return {"missing_items": [], "gap_cost": 0.0}
    sub = st.session_state.subs[trade][sub_key]
    inclusions = [i.strip().lower() for i in sub["inclusions"] if i.strip()]
    missing = []
    gap_cost = 0.0
    for _, row in scope_df.iterrows():
        item_name = str(row["Item"]).lower()
        is_included = any(item_name in inc or inc in item_name for inc in inclusions) if inclusions else False
        if not is_included:
            plug = st.session_state.plug_rates.get(
                f"{trade}::{row['Item']}", float(row.get("Budget_Total", 0))
            )
            missing.append({
                "item": row["Item"],
                "budget": float(row.get("Budget_Total", 0)),
                "plug": plug,
            })
            gap_cost += plug
    return {"missing_items": missing, "gap_cost": gap_cost}

def get_adjusted_total(trade: str, sub_key: str) -> float:
    sub = st.session_state.subs[trade][sub_key]
    gaps = detect_gaps(trade, sub_key)
    return sub["total"] + gaps["gap_cost"]

def fmt_currency(val: float) -> str:
    return f"${val:,.0f}"

def pct_delta(val: float, ref: float) -> float:
    if ref == 0:
        return 0.0
    return ((val - ref) / ref) * 100

# ── Sidebar — Master Scope Config ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 16px 0 8px 0;'>
        <div style='font-size:1.6rem; font-weight:900; color:#38BDF8; letter-spacing:0.05em;'>📐 THE LEVELER</div>
        <div style='font-size:0.75rem; color:#94A3B8; margin-top:2px; letter-spacing:0.12em; text-transform:uppercase;'>Bid Intelligence Platform</div>
    </div>
    <hr style='border-color:#1E293B; margin: 8px 0 16px 0;'>
    """, unsafe_allow_html=True)

    st.markdown("### 🗂 Master Scope Configuration")

    upload_tab, manual_tab = st.tabs(["📤 Upload CSV", "✏️ Manual Entry"])

    with upload_tab:
        st.markdown("<p style='font-size:0.82rem;'>Upload a CSV matching the sample format.</p>", unsafe_allow_html=True)
        uploaded = st.file_uploader("Master Scope CSV", type=["csv"], label_visibility="collapsed")
        if uploaded:
            try:
                df = pd.read_csv(uploaded)
                required = {"Trade", "Item", "Budget_Total"}
                if required.issubset(set(df.columns)):
                    st.session_state.master_scope = df
                    st.success(f"✅ Loaded {len(df)} scope items.")
                else:
                    st.error(f"Missing columns: {required - set(df.columns)}")
            except Exception as e:
                st.error(f"Parse error: {e}")

    with manual_tab:
        st.markdown("<p style='font-size:0.82rem;'>Add individual scope line items.</p>", unsafe_allow_html=True)
        with st.form("manual_scope_form", clear_on_submit=True):
            m_trade = st.selectbox("Trade", TRADES)
            m_item = st.text_input("Item Description", placeholder="5/8\" Type X GWB")
            m_unit = st.selectbox("Unit", ["SF", "LF", "EA", "CY", "LB", "LS", "HR"])
            m_qty = st.number_input("Quantity", min_value=0.0, value=1000.0, step=100.0)
            m_unit_cost = st.number_input("Unit Cost ($)", min_value=0.0, value=2.85, step=0.05, format="%.2f")
            m_desc = st.text_input("Notes (optional)")
            if st.form_submit_button("➕ Add to Scope"):
                if m_item:
                    new_row = pd.DataFrame([{
                        "Trade": m_trade, "Item": m_item, "Unit": m_unit,
                        "Quantity": m_qty, "Unit_Cost": m_unit_cost,
                        "Budget_Total": round(m_qty * m_unit_cost, 2),
                        "Description": m_desc,
                    }])
                    st.session_state.master_scope = pd.concat(
                        [st.session_state.master_scope, new_row], ignore_index=True
                    )
                    st.success(f"Added: {m_item}")
                else:
                    st.warning("Item description is required.")

    # Scope Summary
    if not st.session_state.master_scope.empty:
        st.markdown("<hr style='border-color:#334155; margin:16px 0;'>", unsafe_allow_html=True)
        st.markdown("### 📊 Scope Summary")
        df = st.session_state.master_scope
        total_budget = df["Budget_Total"].astype(float).sum()
        st.metric("Total Budget", fmt_currency(total_budget))
        st.metric("Line Items", len(df))
        st.metric("Trades Covered", df["Trade"].nunique())

        if st.button("🗑 Clear Master Scope"):
            st.session_state.master_scope = pd.DataFrame(
                columns=["Trade", "Item", "Unit", "Quantity", "Unit_Cost", "Budget_Total", "Description"]
            )
            st.rerun()

    st.markdown("<hr style='border-color:#334155; margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Gap Detection Settings")
    st.markdown("<p style='font-size:0.79rem; color:#94A3B8;'>Plug costs override budget values for missing items.</p>", unsafe_allow_html=True)

    scope_df = st.session_state.master_scope
    if not scope_df.empty:
        with st.expander("Set Plug Costs", expanded=False):
            for _, row in scope_df.iterrows():
                key = f"{row['Trade']}::{row['Item']}"
                current = st.session_state.plug_rates.get(key, float(row.get("Budget_Total", 0)))
                new_val = st.number_input(
                    f"{row['Item'][:30]}", value=current, min_value=0.0,
                    step=500.0, key=f"plug_{key}", label_visibility="visible"
                )
                st.session_state.plug_rates[key] = new_val

# ── Main Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex; align-items:center; gap:16px; margin-bottom:8px;'>
    <div>
        <h1 style='margin:0; font-size:2rem; font-weight:900; background: linear-gradient(90deg, #F8FAFC, #38BDF8);
                   -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
            Bid Leveling Dashboard
        </h1>
        <p style='margin:4px 0 0 0; color:#94A3B8; font-size:0.88rem;'>
            Risk Mitigation & Financial Transparency Platform · Compare · Detect · Decide
        </p>
    </div>
</div>
<hr style='border-color:#334155; margin:12px 0 20px 0;'>
""", unsafe_allow_html=True)

# Scope load prompt
if st.session_state.master_scope.empty:
    st.markdown("""
    <div class='card' style='border-left:3px solid #38BDF8; text-align:center; padding:40px;'>
        <div style='font-size:2.5rem; margin-bottom:12px;'>📋</div>
        <h3 style='color:#38BDF8; margin:0 0 8px 0;'>No Master Scope Loaded</h3>
        <p style='color:#94A3B8; max-width:480px; margin:0 auto;'>
            Upload your AI-generated scope CSV or manually enter line items in the sidebar
            to begin bid leveling analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── Trade Tabs ──────────────────────────────────────────────────────────────────
tab_objects = st.tabs([f"🔧 {t}" for t in TRADES] + ["📈 Analytics"])

for tab_idx, trade in enumerate(TRADES):
    with tab_objects[tab_idx]:
        trade_scope = get_trade_scope(trade)
        trade_budget = trade_scope["Budget_Total"].astype(float).sum() if not trade_scope.empty else 0

        st.markdown(f"""
        <div class='trade-header'>
            <h3>{trade} — Subcontractor Bid Leveling</h3>
            <p>Trade Budget: <strong style='color:#F8FAFC;'>{fmt_currency(trade_budget)}</strong>
               &nbsp;·&nbsp; {len(trade_scope)} scope items</p>
        </div>
        """, unsafe_allow_html=True)

        # ── Subcontractor Input ──
        st.markdown("#### 📥 Subcontractor Bids")
        sub_cols = st.columns(3)
        sub_colors = {"A": "#38BDF8", "B": "#A78BFA", "C": "#34D399"}
        sub_labels = {"A": "Sub A", "B": "Sub B", "C": "Sub C"}

        for sub_key, col in zip(["A", "B", "C"], sub_cols):
            with col:
                color = sub_colors[sub_key]
                st.markdown(f"""
                <div style='border-top:2px solid {color}; background:#1E293B; border-radius:0 0 8px 8px;
                            padding:16px; border:1px solid #334155; border-top:3px solid {color}; border-radius:8px;'>
                    <div style='color:{color}; font-weight:700; font-size:0.85rem; letter-spacing:0.08em;
                                text-transform:uppercase; margin-bottom:12px;'>● Subcontractor {sub_key}</div>
                """, unsafe_allow_html=True)

                name = st.text_input(
                    "Company Name", key=f"name_{trade}_{sub_key}",
                    value=st.session_state.subs[trade][sub_key]["name"],
                    placeholder=f"Company {sub_key}"
                )
                total = st.number_input(
                    "Bid Total ($)", key=f"total_{trade}_{sub_key}",
                    value=st.session_state.subs[trade][sub_key]["total"],
                    min_value=0.0, step=1000.0, format="%.0f"
                )

                inclusions_raw = st.text_area(
                    "✅ Inclusions (one per line)",
                    key=f"inc_{trade}_{sub_key}",
                    value="\n".join(st.session_state.subs[trade][sub_key]["inclusions"]),
                    height=100,
                    placeholder="5/8 Type X GWB\nMetal Stud Framing\nTape & Finish..."
                )
                exclusions_raw = st.text_area(
                    "❌ Exclusions (one per line)",
                    key=f"exc_{trade}_{sub_key}",
                    value="\n".join(st.session_state.subs[trade][sub_key]["exclusions"]),
                    height=70,
                    placeholder="Acoustical work\nPainting..."
                )

                # Persist to session state
                st.session_state.subs[trade][sub_key]["name"] = name
                st.session_state.subs[trade][sub_key]["total"] = total
                st.session_state.subs[trade][sub_key]["inclusions"] = [
                    l.strip() for l in inclusions_raw.split("\n") if l.strip()
                ]
                st.session_state.subs[trade][sub_key]["exclusions"] = [
                    l.strip() for l in exclusions_raw.split("\n") if l.strip()
                ]

                st.markdown("</div>", unsafe_allow_html=True)

        # ── Gap Detection + Adjusted Totals ──
        st.markdown("<hr style='border-color:#334155; margin:20px 0;'>", unsafe_allow_html=True)
        st.markdown("#### 🔍 Gap Detection & Adjusted Bid Analysis")

        if trade_scope.empty:
            st.markdown("""
            <div class='card' style='text-align:center; padding:24px;'>
                <p style='color:#94A3B8;'>No scope items for this trade. Add items via the sidebar.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Build comparison table
            any_bid = any(st.session_state.subs[trade][k]["total"] > 0 for k in ["A", "B", "C"])

            # Summary metrics row
            metric_cols = st.columns(4)
            adjusted_totals = {}
            for idx, sub_key in enumerate(["A", "B", "C"]):
                sub = st.session_state.subs[trade][sub_key]
                adj = get_adjusted_total(trade, sub_key)
                adjusted_totals[sub_key] = adj
                name = sub["name"] or f"Sub {sub_key}"
                gaps = detect_gaps(trade, sub_key)
                n_gaps = len(gaps["missing_items"])

                with metric_cols[idx]:
                    delta_pct = pct_delta(adj, trade_budget) if trade_budget else 0
                    delta_str = f"{delta_pct:+.1f}% vs Budget"
                    st.metric(
                        label=name if name else f"Subcontractor {sub_key}",
                        value=fmt_currency(adj) if adj > 0 else "—",
                        delta=f"{n_gaps} gap(s) · {delta_str}" if adj > 0 else None,
                        delta_color="inverse" if delta_pct > 5 else "normal"
                    )

            with metric_cols[3]:
                st.metric("Trade Budget", fmt_currency(trade_budget), delta="Baseline")

            # Lowest adjusted bid highlight
            active_subs = {k: v for k, v in adjusted_totals.items()
                           if st.session_state.subs[trade][k]["total"] > 0}
            if active_subs:
                winner = min(active_subs, key=active_subs.get)
                winner_name = st.session_state.subs[trade][winner]["name"] or f"Sub {winner}"
                st.markdown(f"""
                <div style='background:rgba(56,189,248,0.07); border:1px solid #38BDF8; border-radius:8px;
                            padding:10px 18px; margin:12px 0; display:inline-flex; align-items:center; gap:10px;'>
                    <span style='color:#38BDF8; font-weight:700;'>⚡ Lowest Adjusted Bid</span>
                    <span class='winner-badge'>{winner_name}</span>
                    <span style='color:#F8FAFC; font-weight:700;'>{fmt_currency(adjusted_totals[winner])}</span>
                </div>
                """, unsafe_allow_html=True)

            # Scope item gap table
            st.markdown("##### 📋 Scope Item Coverage Matrix")

            table_rows = []
            for _, row in trade_scope.iterrows():
                item = row["Item"]
                budget = float(row.get("Budget_Total", 0))
                r = {"Scope Item": item, "Budget": fmt_currency(budget)}

                for sub_key in ["A", "B", "C"]:
                    sub = st.session_state.subs[trade][sub_key]
                    name = sub["name"] or f"Sub {sub_key}"
                    inclusions = [i.strip().lower() for i in sub["inclusions"]]
                    excluded = [e.strip().lower() for e in sub["exclusions"]]

                    item_lower = item.lower()
                    is_excluded = any(item_lower in ex or ex in item_lower for ex in excluded)
                    is_included = any(item_lower in inc or inc in item_lower for inc in inclusions) if inclusions else False

                    if is_excluded:
                        status = "❌ EXCLUDED"
                    elif is_included:
                        status = "✅ Included"
                    elif sub["total"] == 0:
                        status = "—"
                    else:
                        status = "⚠️ GAP"

                    r[name] = status
                table_rows.append(r)

            if table_rows:
                gap_df = pd.DataFrame(table_rows)

                def color_status(val):
                    if "GAP" in str(val):
                        return "color: #FB7185; font-weight: bold;"
                    elif "✅" in str(val):
                        return "color: #34D399;"
                    elif "❌" in str(val):
                        return "color: #F97316;"
                    return "color: #94A3B8;"

                styled = gap_df.style.map(color_status, subset=[
                    c for c in gap_df.columns if c not in ["Scope Item", "Budget"]
                ])
                st.dataframe(styled, use_container_width=True, hide_index=True)

            # Per-sub gap detail
            st.markdown("##### 🚨 Critical Gap Details")
            gap_detail_cols = st.columns(3)
            for idx, sub_key in enumerate(["A", "B", "C"]):
                with gap_detail_cols[idx]:
                    sub = st.session_state.subs[trade][sub_key]
                    if sub["total"] == 0:
                        continue
                    name = sub["name"] or f"Sub {sub_key}"
                    gaps = detect_gaps(trade, sub_key)
                    if not gaps["missing_items"]:
                        st.markdown(f"""
                        <div style='background:rgba(52,211,153,0.07); border:1px solid rgba(52,211,153,0.3);
                                    border-radius:8px; padding:12px 16px;'>
                            <span style='color:#34D399; font-weight:700;'>✓ {name}</span>
                            <p style='color:#94A3B8; font-size:0.82rem; margin:4px 0 0 0;'>No critical gaps detected.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        gap_html = f"""
                        <div style='background:rgba(251,113,133,0.06); border:1px solid rgba(251,113,133,0.25);
                                    border-radius:8px; padding:12px 16px;'>
                            <div style='color:#FB7185; font-weight:700; margin-bottom:8px;'>
                                ⚠ {name} — {len(gaps["missing_items"])} Gap(s)
                            </div>
                        """
                        for g in gaps["missing_items"]:
                            gap_html += f"""
                            <div style='display:flex; justify-content:space-between; align-items:center;
                                        padding:4px 0; border-bottom:1px solid rgba(51,65,85,0.5);'>
                                <span style='color:#FB7185; font-size:0.8rem; font-weight:600;'>{g["item"][:28]}</span>
                                <span style='color:#F97316; font-size:0.78rem; font-weight:700;'>+{fmt_currency(g["plug"])}</span>
                            </div>
                            """
                        gap_html += f"""
                            <div style='margin-top:8px; padding-top:6px; text-align:right;'>
                                <span style='color:#94A3B8; font-size:0.78rem;'>Plug Total: </span>
                                <span style='color:#FB7185; font-weight:800;'>{fmt_currency(gaps["gap_cost"])}</span>
                            </div>
                        </div>
                        """
                        st.markdown(gap_html, unsafe_allow_html=True)

            # ── Bar Chart ──
            active_any = any(st.session_state.subs[trade][k]["total"] > 0 for k in ["A", "B", "C"])
            if active_any:
                st.markdown("<hr style='border-color:#334155; margin:20px 0;'>", unsafe_allow_html=True)
                st.markdown("#### 📊 Bid Comparison Chart")

                chart_data = {
                    "Subcontractor": [],
                    "Bid Total": [],
                    "Adjusted Total": [],
                    "Color": [],
                }
                colors_list = [COLORS["sub_a"], COLORS["sub_b"], COLORS["sub_c"]]

                bar_fig = go.Figure()
                names_list = []
                bids_list = []
                adj_list = []

                for si, sub_key in enumerate(["A", "B", "C"]):
                    sub = st.session_state.subs[trade][sub_key]
                    if sub["total"] == 0:
                        continue
                    name = sub["name"] or f"Sub {sub_key}"
                    adj = get_adjusted_total(trade, sub_key)
                    names_list.append(name)
                    bids_list.append(sub["total"])
                    adj_list.append(adj)

                    bar_fig.add_trace(go.Bar(
                        name=f"{name} (Raw)",
                        x=[name],
                        y=[sub["total"]],
                        marker_color=colors_list[si],
                        marker_line=dict(width=0),
                        opacity=0.7,
                        text=[fmt_currency(sub["total"])],
                        textposition="outside",
                        textfont=dict(color=colors_list[si], size=11),
                    ))
                    bar_fig.add_trace(go.Bar(
                        name=f"{name} (Adjusted)",
                        x=[name],
                        y=[adj],
                        marker_color=colors_list[si],
                        marker_line=dict(color="#FB7185", width=2),
                        opacity=1.0,
                        text=[fmt_currency(adj)],
                        textposition="outside",
                        textfont=dict(color="#FB7185", size=11, family="Inter"),
                    ))

                # Budget line
                bar_fig.add_hline(
                    y=trade_budget, line_dash="dot", line_color=COLORS["budget"],
                    line_width=2,
                    annotation_text=f"Budget: {fmt_currency(trade_budget)}",
                    annotation_font_color=COLORS["budget"],
                )

                bar_fig.update_layout(
                    **PLOTLY_TEMPLATE["layout"],
                    title=f"{trade} — Raw vs. Adjusted Bid Comparison",
                    barmode="group",
                    showlegend=True,
                    height=420,
                    yaxis_tickprefix="$",
                    yaxis_tickformat=",",
                )
                st.plotly_chart(bar_fig, use_container_width=True)

# ── Analytics Tab ───────────────────────────────────────────────────────────────
with tab_objects[-1]:
    st.markdown("""
    <div class='trade-header'>
        <h3>Cross-Trade Analytics & Risk Intelligence</h3>
        <p>Heatmap analysis · Bid delta visualization · Portfolio-level risk scoring</p>
    </div>
    """, unsafe_allow_html=True)

    df_scope = st.session_state.master_scope

    if df_scope.empty:
        st.markdown("""
        <div class='card' style='text-align:center; padding:40px;'>
            <p style='color:#94A3B8;'>Load a Master Scope to enable analytics.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # ── Heatmap: Bid Divergence ──
        st.markdown("#### 🌡 Bid Divergence Heatmap")
        st.markdown("<p style='color:#94A3B8; font-size:0.85rem;'>Shows % deviation of each sub's adjusted bid vs. trade budget. Red = divergent (high risk). Green = tight.</p>", unsafe_allow_html=True)

        heatmap_trades = []
        heatmap_subs = []
        heatmap_values = []
        heatmap_text = []

        sub_names = {k: f"Sub {k}" for k in ["A", "B", "C"]}
        for trade in TRADES:
            scope = get_trade_scope(trade)
            budget = scope["Budget_Total"].astype(float).sum() if not scope.empty else 0
            for sub_key in ["A", "B", "C"]:
                sub = st.session_state.subs[trade][sub_key]
                name = sub["name"] or f"Sub {sub_key}"
                sub_names[sub_key] = name
                adj = get_adjusted_total(trade, sub_key) if sub["total"] > 0 else None
                if adj is not None and budget > 0:
                    delta_pct = pct_delta(adj, budget)
                else:
                    delta_pct = None
                heatmap_trades.append(trade)
                heatmap_subs.append(name)
                heatmap_values.append(round(delta_pct, 1) if delta_pct is not None else 0)
                heatmap_text.append(
                    f"{delta_pct:+.1f}%" if delta_pct is not None else "No bid"
                )

        heat_df = pd.DataFrame({
            "Trade": heatmap_trades,
            "Sub": heatmap_subs,
            "Delta": heatmap_values,
            "Text": heatmap_text,
        })

        pivot = heat_df.pivot_table(index="Sub", columns="Trade", values="Delta", aggfunc="first")
        text_pivot = heat_df.pivot_table(index="Sub", columns="Trade", values="Text", aggfunc="first")

        heat_fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns.tolist(),
            y=pivot.index.tolist(),
            text=text_pivot.values,
            texttemplate="%{text}",
            textfont=dict(size=13, color="#F8FAFC", family="Inter"),
            colorscale=[
                [0.0, "#34D399"],    # tight — green
                [0.4, "#FBBF24"],    # moderate — amber
                [0.7, "#FB923C"],    # elevated — orange
                [1.0, "#FB7185"],    # divergent — red
            ],
            zmid=0,
            zmin=-20,
            zmax=20,
            showscale=True,
            colorbar=dict(
                title=dict(text="% vs Budget", font=dict(color="#94A3B8")),
                tickfont=dict(color="#94A3B8"),
                bordercolor="#334155",
                bgcolor="#1E293B",
            ),
            hovertemplate="<b>%{y}</b> — %{x}<br>Delta: %{text}<extra></extra>",
        ))
        heat_fig.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            title="Bid Risk Heatmap: % Delta vs. Budget by Trade",
            height=360,
            xaxis=dict(side="bottom", tickfont=dict(color="#94A3B8", size=12)),
            yaxis=dict(tickfont=dict(color="#94A3B8", size=12)),
        )
        st.plotly_chart(heat_fig, use_container_width=True)

        # ── Cross-Trade Grouped Bar ──
        st.markdown("#### 📊 Cross-Trade Budget vs. Adjusted Bids")

        sub_colors_list = [COLORS["sub_a"], COLORS["sub_b"], COLORS["sub_c"]]
        ct_fig = go.Figure()

        # Budget bars
        budgets = []
        trade_labels = []
        for trade in TRADES:
            scope = get_trade_scope(trade)
            budget = scope["Budget_Total"].astype(float).sum() if not scope.empty else 0
            budgets.append(budget)
            trade_labels.append(trade)

        ct_fig.add_trace(go.Bar(
            name="Budget",
            x=trade_labels,
            y=budgets,
            marker_color=COLORS["budget"],
            opacity=0.6,
            marker_line=dict(width=0),
        ))

        for si, sub_key in enumerate(["A", "B", "C"]):
            sub_adj = []
            for trade in TRADES:
                sub = st.session_state.subs[trade][sub_key]
                adj = get_adjusted_total(trade, sub_key) if sub["total"] > 0 else 0
                sub_adj.append(adj)

            if any(v > 0 for v in sub_adj):
                name = st.session_state.subs[TRADES[0]][sub_key]["name"] or f"Sub {sub_key}"
                ct_fig.add_trace(go.Bar(
                    name=name,
                    x=trade_labels,
                    y=sub_adj,
                    marker_color=sub_colors_list[si],
                    marker_line=dict(width=0),
                    opacity=0.9,
                ))

        ct_fig.update_layout(
            **PLOTLY_TEMPLATE["layout"],
            title="Portfolio View: Budget vs. Adjusted Bids per Trade",
            barmode="group",
            height=420,
            yaxis_tickprefix="$",
            yaxis_tickformat=",",
        )
        st.plotly_chart(ct_fig, use_container_width=True)

        # ── Risk Score Summary ──
        st.markdown("#### 🎯 Risk Score Summary")
        risk_cols = st.columns(4)
        for ti, trade in enumerate(TRADES):
            with risk_cols[ti]:
                scope = get_trade_scope(trade)
                budget = scope["Budget_Total"].astype(float).sum() if not scope.empty else 0
                deltas = []
                for sub_key in ["A", "B", "C"]:
                    sub = st.session_state.subs[trade][sub_key]
                    if sub["total"] > 0 and budget > 0:
                        adj = get_adjusted_total(trade, sub_key)
                        deltas.append(abs(pct_delta(adj, budget)))

                if deltas:
                    avg_delta = sum(deltas) / len(deltas)
                    if avg_delta < 5:
                        risk_label = "🟢 LOW"
                        risk_color = "#34D399"
                    elif avg_delta < 15:
                        risk_label = "🟡 MEDIUM"
                        risk_color = "#FBBF24"
                    else:
                        risk_label = "🔴 HIGH"
                        risk_color = "#FB7185"
                else:
                    risk_label = "⚪ NO DATA"
                    risk_color = "#475569"
                    avg_delta = 0

                st.markdown(f"""
                <div class='card' style='text-align:center;'>
                    <div style='color:#94A3B8; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.08em;'>{trade}</div>
                    <div style='color:{risk_color}; font-size:1.6rem; font-weight:900; margin:8px 0;'>{risk_label}</div>
                    <div style='color:#F8FAFC; font-size:1.1rem; font-weight:700;'>{avg_delta:.1f}% avg delta</div>
                    <div style='color:#94A3B8; font-size:0.78rem; margin-top:4px;'>vs. {fmt_currency(budget)} budget</div>
                </div>
                """, unsafe_allow_html=True)

# ── Footer ──────────────────────────────────────────────────────────────────────
st.markdown("""
<hr style='border-color:#1E293B; margin:32px 0 16px 0;'>
<div style='text-align:center; color:#334155; font-size:0.75rem; padding-bottom:16px;'>
    The Leveler · Bid Intelligence Platform · Built for Construction Risk Mitigation & Financial Transparency
</div>
""", unsafe_allow_html=True)
