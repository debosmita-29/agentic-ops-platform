import os

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Agentic Operational Dashboard", layout="wide")
st.title("Agentic Operational Dashboard")
st.caption("GenAI-powered operational intelligence for SRE, QA, release, and leadership teams.")

prompt = st.text_area(
    "Ask the operational agents",
    value="Analyze current production readiness, explain key risks, summarize test instability, and generate an executive update.",
    height=100,
)

if st.button("Run Agentic Analysis", type="primary"):
    with st.spinner("Operational agents are analyzing signals..."):
        response = requests.post(f"{API_BASE}/analyze", json={"prompt": prompt}, timeout=120)
        response.raise_for_status()
        result = response.json()

    st.subheader("Executive Summary")
    st.write(result["summary"])

    c1, c2, c3 = st.columns(3)
    c1.metric("Health Score", result["scores"]["health_score"])
    c2.metric("Test Stability", result["scores"]["test_stability_score"])
    c3.metric("Release Readiness", result["scores"]["release_readiness_score"])

    st.subheader("Agent Findings")
    for agent_result in result["agent_results"]:
        with st.expander(agent_result["agent_name"]):
            st.write(agent_result["summary"])
            if agent_result["risks"]:
                st.warning("\n".join(agent_result["risks"]))
            for rec in agent_result["recommendations"]:
                st.success(rec)

st.divider()

metrics = requests.get(f"{API_BASE}/metrics", timeout=30).json()
tests = requests.get(f"{API_BASE}/test-runs", timeout=30).json()
incidents = requests.get(f"{API_BASE}/incidents", timeout=30).json()

tab1, tab2, tab3 = st.tabs(["Service Health", "Test Stability", "Incidents"])

with tab1:
    df = pd.DataFrame(metrics)
    st.dataframe(df, use_container_width=True)
    if not df.empty:
        fig = px.bar(df, x="service_name", y="error_rate_pct", title="Error Rate by Service")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    df = pd.DataFrame(tests)
    st.dataframe(df, use_container_width=True)
    if not df.empty:
        fig = px.bar(df, x="pipeline_name", y=["failed_tests", "flaky_tests"], barmode="group", title="Failures and Flakiness")
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.dataframe(pd.DataFrame(incidents), use_container_width=True)
