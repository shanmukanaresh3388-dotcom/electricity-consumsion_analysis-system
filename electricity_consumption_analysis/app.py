from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "electricity_data.csv"
UNIT_RATE = 6.0

st.set_page_config(page_title="Electricity Consumption Analysis", page_icon="⚡", layout="wide")
st.title("⚡ Electricity Consumption Analysis System")
st.write("Analyze monthly electricity usage and estimate bills from the supplied CSV dataset.")

rate = st.number_input("Estimated rate per unit (₹/kWh)", min_value=0.0, value=UNIT_RATE, step=0.5)
upload = st.file_uploader("Upload your electricity CSV (columns: Month, Units_kWh)", type=["csv"])
try:
    if upload is not None:
        df = pd.read_csv(upload)
    else:
        df = pd.read_csv(DATA_FILE)
    required = {"Month", "Units_kWh"}
    if not required.issubset(df.columns):
        st.error("CSV must contain these columns: Month, Units_kWh")
        st.stop()
    df["Month"] = pd.to_datetime(df["Month"], format="%Y-%m", errors="coerce")
    df["Units_kWh"] = pd.to_numeric(df["Units_kWh"], errors="coerce")
    df = df.dropna(subset=["Month", "Units_kWh"])
    df = df[df["Units_kWh"] >= 0].sort_values("Month").drop_duplicates("Month", keep="last").copy()
    if df.empty:
        st.warning("No valid records found in the dataset.")
        st.stop()
    df["Estimated_Bill_INR"] = df["Units_kWh"] * rate
    df["Month_Name"] = df["Month"].dt.strftime("%b %Y")
    a, b, c = st.columns(3)
    a.metric("Total consumption", f"{df['Units_kWh'].sum():,.1f} kWh")
    b.metric("Average monthly usage", f"{df['Units_kWh'].mean():,.1f} kWh")
    c.metric("Estimated total bill", f"₹{df['Estimated_Bill_INR'].sum():,.2f}")
    st.subheader("Monthly Consumption")
    st.bar_chart(df.set_index("Month_Name")["Units_kWh"])
    st.subheader("Consumption Trend")
    st.line_chart(df.set_index("Month")["Units_kWh"])
    st.subheader("Estimated Monthly Bill")
    st.bar_chart(df.set_index("Month_Name")["Estimated_Bill_INR"])
    shown = df[["Month_Name", "Units_kWh", "Estimated_Bill_INR"]].rename(columns={"Month_Name":"Month", "Units_kWh":"Units (kWh)", "Estimated_Bill_INR":"Estimated Bill (₹)"})
    st.subheader("Analysis Results")
    st.dataframe(shown, use_container_width=True, hide_index=True)
    st.download_button("Download analysis CSV", shown.to_csv(index=False).encode("utf-8"), file_name="electricity_analysis_results.csv", mime="text/csv")
    st.caption("Bill is an estimate based on a single flat rate; actual utility bills may include slab rates, fixed charges and taxes.")
except FileNotFoundError:
    st.error("Default dataset not found. Upload a CSV to continue.")
except Exception as e:
    st.error(f"Could not process the dataset: {e}")
