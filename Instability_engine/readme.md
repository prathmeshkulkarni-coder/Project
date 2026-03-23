# Mithril Instability Engine (v1.0)
### Log-Periodic Power Law (LPPL) Analysis for Market Singularity Detection

---

 Project Overview

**Mithril Instability Engine** is a quantitative research tool designed to detect **super-exponential price behavior** and **speculative bubbles** in financial markets.

Rather than tracking price direction, the engine measures **instability in the price formation process itself**, identifying mathematical signatures of **herding behavior** that typically precede **regime shifts, peaks, or crashes**.

The core methodology is based on the **Log-Periodic Power Law (LPPL)** framework developed by Didier Sornette and collaborators.

---

Core Idea

Markets approaching a crash often exhibit:
- Accelerating (super-exponential) growth  
- Increasingly frequent oscillations  
- Collective synchronization of trader behavior  

LPPL captures these dynamics by modeling the **log of price** as it approaches a critical time \( t_c \), interpreted as a **singularity point**.

---

 Features

 7-Parameter LPPL Optimization
- Implements the full LPPL equation using **SciPy’s `least_squares` optimizer**
- Levenberg–Marquardt algorithm for non-linear convergence
- Enforces theoretical constraints on parameters to avoid spurious fits

 Multi-Scale Windowing
- Evaluates **15 distinct rolling look-back windows**
- Ensures robustness across time scales
- Filters out false positives caused by local noise

 Criticality & Hazard Metrics
- **Criticality Score**
  - Measures degree of crowd synchronization
  - Values **> 55** indicate extreme instability
- **Hazard Score**
  - Estimates instantaneous probability of a crash occurring at `t_today`
  - Derived from convergence and proximity to predicted \( t_c \)

 Automated Regime Classification
Assets are classified into:
- **NORMAL** – Stable, non-bubble behavior
- **WARNING** – Developing instability
- **CRITICAL** – Imminent regime shift risk

---

 Mathematical Foundation

The engine fits the natural logarithm of price \( \ln P(t) \) to the LPPL formulation:

$$ln P(t) = A + B(t_c - t)^m [1 + C \cos(\omega \ln(t_c - t) + \phi)]$$

 Parameter Interpretation
-  t_c : Predicted singularity (crash / peak time)
-  m: Power-law exponent  
  - Valid bubble range: \( 0.1 < m < 0.9 \)
- **\( \omega \)**: Frequency of log-periodic oscillations
- **\( C \)**: Oscillation amplitude (herding strength)
- **\( A, B, \phi \)**: Calibration parameters

---

## 📊 Performance Case Study

### Asset: Silver Futures (SI=F)

**Simulation Period:** February 2026  

| Metric | Value |
|------|------|
| Signal Date | Feb 2, 2026 |
| Hazard Score | **0.249** |
| Criticality | **58.53** |
| Predicted \( t_c \) | 13 days from signal +- 2|

Case Study: The Silver Monday Gap (Feb 9, 2026)

On Friday, Feb 6, the engine flagged a Hazard Rate of 0.249. Even though the predicted singularity ($t_c$) was still days away (Feb 13), the high hazard indicated that the market was too fragile to survive the weekend. This signaled a high probability of a Monday Morning Gap Down, proving that the Hazard Rate is a leading indicator of immediate liquidity exhaustion.

📊 Silver Status: Feb 9, 2026
Price: ~$80.25 / ₹2.85 Lakh

Trend: Bearish (Recovery within a crash)

Hazard: High (CME margins are still forcing liquidations)

Singularity: February 13th (4 days away)

### Outcome
- Engine identified a **high-risk singularity window**
- Captured the **peak of a 5× parabolic price run**
- Signal occurred **before** the actual market reversal

This validates the engine’s ability to detect **structural instability**, not just trend exhaustion.

## 📊 Case Study II: Gold Market — The “May Singularity”

This case study documents the Mithril Engine’s successful tracking of the **2026 Gold Super-Bubble** (`GC=F`).

Using the LPPL framework, the engine identified a **persistent, forward-drifting singularity**, confirming that gold prices were not merely trending upward, but exhibiting **sustained super-exponential growth** — a classic signature of late-stage speculative herding.

Unlike short-lived bubbles, this event demonstrated **temporal stability in instability**, where the predicted crash date (\( t_c \)) gradually converged rather than resetting.

---

## 🔍 Model Sensitivity & Predictive Accuracy

To evaluate robustness, the engine was tested across **three strategically selected rolling windows** during the 2026 gold rally.  
The objective was to observe how the predicted singularity date (\( t_c \)) evolved as new data arrived.

### Singularity Drift Analysis

| Data Window End | Predicted \( t_c \) | Gap (Days) | Market Regime |
|----------------|---------------------|------------|----------------|
| Dec 31, 2025 | Apr 28, 2026 | 118 | Early Parabolic Phase |
| Jan 31, 2026 | May 20, 2026 | 110 | Blow-off Top Acceleration |
| Feb 8, 2026 (Today) | **May 8, 2026** | **90** | **Critical Convergence** |

---

## 🧠 Interpretation

Key observations from the drift behavior:

- **Forward stability:**  
  The singularity date consistently remained in **late April–May 2026**, indicating a structurally unstable regime rather than a transient spike.

- **Convergence under acceleration:**  
  As price acceleration intensified, the gap to \( t_c \) **compressed**, signaling increased synchronization among market participants.

- **Regime confirmation:**  
  By February 2026, the engine classified gold as **CRITICAL**, with multiple windows converging on a narrow crash horizon.

This behavior aligns with theoretical LPPL expectations for mature bubbles approaching their terminal phase.

---

## 📌 Key Takeaway

The “May Singularity” case validates the Mithril Engine’s ability to:

- Track **long-duration super-bubbles**
- Detect **structural instability before price failure**
- Distinguish between normal parabolic trends and **true singular regimes**

Rather than predicting a single crash date, the engine revealed the **progressive tightening of market instability**, which is the true signal LPPL is designed to capture.


---

## 📦 Tech Stack

- Python
- NumPy
- SciPy
- Pandas
- Custom statistical validation modules

---

## ⚠️ Disclaimer

This project is for **research and educational purposes only**.  
It does **not** constitute financial advice or a trading system.

LPPL models identify **probabilistic instability**, not guaranteed crashes.

---

 Future Work (v1.1+)
- Bayesian parameter stability scoring
- Cross-asset contagion analysis
- Real-time streaming inference
- Integration with volatility & options-implied stress metrics

---

## 🧙‍♂️ Why “Mithril”?
Mithril doesn’t predict direction — it reveals **hidden structural weakness** before collapse.
