# 📐 The Leveler — Bid Intelligence Platform

> **A Risk Mitigation and Financial Transparency Tool for Construction Project Management**

---

## What Is This?

The Leveler is a Streamlit-based web application that solves one of construction project management's most persistent problems: **you can't compare three subcontractor bids if they're not quoting the same scope.**

Sub A might be $50,000 cheaper than Sub B — but only because Sub A forgot to include $65,000 of fire-rated drywall. Without a leveled comparison, you don't have a cheaper bid. You have a future change order.

**The Leveler eliminates that risk.**

---

## Core Value Proposition

| Without The Leveler | With The Leveler |
|---|---|
| Three bids in three different formats | Normalized, apples-to-apples comparison |
| Hidden scope gaps cause budget overruns | Critical gaps flagged instantly in real-time |
| Manual spreadsheet leveling takes hours | Automated gap detection in seconds |
| Change orders kill project margins | Plug numbers surface true adjusted costs |
| No visual risk signal | Heatmap shows where bids are divergent |

---

## Features

### 🗂 Master Scope Configuration
- Upload an AI-generated scope sheet (CSV format) from your drawing review process
- Manually add line items by Trade, Item, Unit, Quantity, and Unit Cost
- Scope persists across sessions via `st.session_state`

### 🔍 Gap Detection Engine
The core intelligence of the platform. For each subcontractor bid:
1. Compares the sub's stated inclusions against every line item in the Master Scope
2. Flags missing items as **Critical Gaps** — items in scope but not in the bid
3. Applies configurable **plug costs** (defaulting to the budget unit cost) to calculate a true **Adjusted Total**
4. Presents a **Coverage Matrix** showing ✅ Included / ⚠️ GAP / ❌ Excluded for every scope item

### 📊 Visualizations
- **Grouped Bar Chart**: Raw bid vs. Adjusted bid per subcontractor, with budget baseline
- **Cross-Trade Portfolio View**: See your entire project's bid landscape in one chart
- **Divergence Heatmap**: Color-coded risk map (Green = tight, Red = high risk) showing % delta vs. budget by trade and subcontractor
- **Risk Score Cards**: Automated LOW / MEDIUM / HIGH risk rating per trade

### ⚡ Bid Leveling Metrics
- Lowest adjusted bid highlighted with "Winner" badge
- % delta vs. budget for each sub
- Gap count and gap dollar value per subcontractor

---

## Getting Started

### Prerequisites
```bash
pip install streamlit pandas plotly
```

### Run the App
```bash
streamlit run app.py
```

### Load Your Scope
1. Use `master_scope.csv` (included) as a template
2. Upload via sidebar → "Upload CSV" tab, **or**
3. Add items manually via sidebar → "Manual Entry" tab

### Enter Sub Bids
1. Navigate to the appropriate trade tab (Drywall, MEP, Interiors, Site Work)
2. For each subcontractor, enter:
   - **Company Name**
   - **Bid Total** ($)
   - **Inclusions** — paste their scope inclusions, one item per line
   - **Exclusions** — paste their noted exclusions
3. The gap engine runs automatically

### Configure Plug Costs
- In the sidebar under "Gap Detection Settings," expand "Set Plug Costs"
- Override the default (budget value) with your own plug number for any line item
- This is useful when you have better market intel than the original estimate

---

## master_scope.csv Format

```csv
Trade,Item,Unit,Quantity,Unit_Cost,Budget_Total,Description
Drywall,5/8" Type X GWB,SF,10000,2.85,28500,Fire-rated GWB for corridors
MEP,HVAC Split System 5-Ton,EA,4,8500,34000,5-ton split with thermostat
Interiors,Flooring - LVP,SF,8500,6.25,53125,Luxury vinyl plank 6mm
Site Work,Asphalt Paving,SF,12000,3.80,45600,2" asphalt over 6" base
```

**Column Reference:**

| Column | Required | Description |
|---|---|---|
| `Trade` | ✅ | Must match one of: Drywall, MEP, Interiors, Site Work |
| `Item` | ✅ | Line item description (used for gap matching) |
| `Unit` | ❌ | Unit of measure (SF, LF, EA, CY, etc.) |
| `Quantity` | ❌ | Quantity of units |
| `Unit_Cost` | ❌ | Cost per unit |
| `Budget_Total` | ✅ | Total budget for this line item |
| `Description` | ❌ | Additional notes |

---

## Gap Detection Logic

The engine uses **fuzzy substring matching**:
- A scope item is considered **Included** if its name (lowercased) is a substring of any inclusion line — or vice versa
- A scope item is **Excluded** if it matches any exclusion line
- Anything else on a submitted bid is flagged as a **Critical Gap**

**Best Practice for Inclusions:** Copy the sub's "Scope of Work" section verbatim, one line per item. The more granular the input, the more accurate the gap detection.

---

## Risk Heatmap Interpretation

| Color | Delta Range | Meaning |
|---|---|---|
| 🟢 Green | < 5% | Bid is tight — aligned with budget |
| 🟡 Amber | 5–10% | Moderate variance — review assumptions |
| 🟠 Orange | 10–20% | Elevated risk — investigate scope gaps |
| 🔴 Red/Coral | > 20% | High risk — likely missing major scope |

---

## Workflow Integration

```
Drawings → AI Scope Generation → master_scope.csv
                                         ↓
                              Upload to The Leveler
                                         ↓
                    Sub A Bid + Sub B Bid + Sub C Bid
                                         ↓
                              Gap Detection Engine
                                         ↓
                    Adjusted Totals + Risk Heatmap + Coverage Matrix
                                         ↓
                              Informed Award Decision
```

---

## Technical Architecture

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Data Handling | Pandas |
| Visualizations | Plotly (Graph Objects) |
| State Persistence | `st.session_state` |
| Styling | Custom CSS injection (Midnight Professional theme) |

---

## Design System

The UI uses the **Midnight Professional** color palette:

| Token | Hex | Usage |
|---|---|---|
| Base | `#0F172A` | App background |
| Card | `#1E293B` | Container backgrounds |
| Primary Text | `#F8FAFC` | All primary content |
| Secondary Text | `#94A3B8` | Labels, metadata |
| Accent (Cyber Blue) | `#38BDF8` | Winner highlights, CTAs |
| Gap Alert | `#FB7185` | Critical gaps, high risk |
| Borders | `#334155` | Subtle container definition |

---

## Extending The Leveler

**Add more trades:**
```python
TRADES = ["Drywall", "MEP", "Interiors", "Site Work", "Concrete", "Steel"]
```

**Add more subcontractors:**  
Duplicate the sub input block and extend the `["A", "B", "C"]` loop to `["A", "B", "C", "D"]`.

**Export to Excel:**  
Add `df.to_excel("leveling_report.xlsx")` with `openpyxl` for client-ready reports.

**Connect to an LLM:**  
Feed your drawings PDFs to Claude or GPT-4V to auto-generate the `master_scope.csv` — then pipe it directly into The Leveler.

---

*The Leveler is built for General Contractors, Owner's Representatives, and Construction Managers who believe that financial transparency starts before the contract is signed.*
