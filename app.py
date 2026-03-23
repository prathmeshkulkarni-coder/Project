import streamlit as st
import json
import os
import sys
import datetime

st.set_page_config(page_title="Quant Platform", page_icon="📈", layout="centered")
# Ensure the project root and Quant_pipeline are in the path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, "Quant_pipeline"))

try:
    from storage.pipeline import ingest_stock_to_db
except ImportError as e:
    ingest_stock_to_db = None
    st.error(f"Failed to import pipeline: {e}")

try:
    from Instability_engine.main import run_lppl
except ImportError as e:
    run_lppl = None
    st.error(f"Failed to import instability engine: {e}")

st.title("📈 Quant Platform")

tab1, tab2 = st.tabs(["🗄️ Data Ingestion", "📉 Instability Analysis"])

with tab1:
    st.header("Data Ingestion to PostgreSQL")
    st.markdown("Fetch stock data from Yahoo Finance and store it directly into your local database.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        ingest_symbol = st.text_input("Asset Symbol (e.g., SI=F, AAPL)", value="SI=F", key="ingest_symbol")
    with col_b:
        start_date = st.date_input("Start Date", value=datetime.date(2024, 1, 1))
        end_date = st.date_input("End Date", value=datetime.date.today())
        
    if st.button("Run Ingestion Pipeline", type="primary"):
        if ingest_stock_to_db:
            with st.spinner(f"Ingesting data for {ingest_symbol}..."):
                try:
                    s_date = start_date.strftime("%Y-%m-%d")
                    e_date = end_date.strftime("%Y-%m-%d")
                    
                    result_msg = ingest_stock_to_db(ingest_symbol, start=s_date, end=e_date)
                    if "skipped" in result_msg or "already up to date" in result_msg:
                        st.info(result_msg)
                    else:
                        st.success(result_msg)
                except Exception as e:
                    st.error(f"Ingestion failed: {e}")
        else:
            st.error("Pipeline module could not be loaded. Please check your path configuration.")

with tab2:
    st.header("Market Instability LPPL Engine")
    st.markdown("Analyze financial assets for market bubbles and impending crashes using the **Log-Periodic Power Law (LPPL)** model.")

    if run_lppl is None:
        st.error("LPPL Engine module could not be loaded. Please check your path configuration.")
    else:
        instability_symbol = st.text_input("Asset Symbol for Analysis (e.g., SI=F, AAPL)", value="SI=F", key="instability_symbol")
        
        if st.button("Calculate Instability", type="primary", key="calc_instability_btn"):
            with st.spinner(f"Running LPPL analysis for {instability_symbol}... This may take a few moments."):
                try:
                    output = run_lppl(instability_symbol)
                    
                    st.success(f"Showing latest analysis for **{instability_symbol}**")

                    col1, col2, col3 = st.columns(3)

                    regime = output.get("regime", "N/A")
                    regime_color = "🔴" if regime in ["WARNING", "CRITICAL"] else "🟢"

                    with col1:
                        st.metric("Market Regime", f"{regime_color} {regime}")
                    with col2:
                        st.metric("Criticality Index", f"{output.get('criticality', 0):.2f}")
                    with col3:
                        st.metric("Hazard Score", f"{output.get('hazard', 0):.4f}")

                    st.subheader("Raw Signal Details")
                    st.json(output)
                    
                except Exception as e:
                    st.error(f"Analysis failed for {instability_symbol}: {e}")
