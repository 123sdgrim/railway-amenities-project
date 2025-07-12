# pages/Heatmap.py

import streamlit as st
import pandas as pd
import re
import altair as alt
from utils import render_logo_and_navbar, render_footer, set_global_background

st.set_page_config(page_title="Heatmap - Railway Amenities", layout="wide")

# UI styling
set_global_background()
render_logo_and_navbar()
st.title("🔥 Division-wise Amenities Heatmap")

# Load dataset
df = pd.read_csv("station_level_data_output.csv")

# Division mapping
div_code_to_name = {
    'ADI': 'AHMEDABAD JN', 'ADRA': 'ADRA JN', 'AGC': 'AGRA CANTT', 'AGRA': 'AGRA',
    'AII': 'AJMER JN', 'ALD': 'ALLAHABAD JN', 'APD': 'ALIPUR DUAR', 'APDJ': 'ALIPUR DUAR JN',
    'ASN': 'ASANSOL JN', 'BCT': 'MUMBAI CENTRAL', 'BKN': 'BIKANER JN', 'BPL': 'BHOPAL JN',
    'BRC': 'VADODARA JN', 'BSB': 'VARANASI JN', 'BSL': 'BHUSAVAL JN', 'BSP': 'BILASPUR JN',
    'BVP': 'BHAVANAGAR PARA', 'BZA': 'VIJAYAWADA JN', 'CKP': 'CHAKRADHARPUR', 'CSTM': 'MUMBAI CST',
    'DDU': 'PTDEENDAYALUPADHAY', 'DHN': 'DHANBAD JN', 'DLI': 'DELHI', 'DNR': 'DANAPUR',
    'FZR': 'FIROZPUR CANT', 'GNT': 'GUNTUR JN', 'GTL': 'GUNTAKAL JN', 'HWH': 'HOWRAH JN',
    'HYB': 'HYDERABAD DECAN', 'IZN': 'IZZATNAGAR', 'JAT': 'JAMMU', 'JBP': 'JABALPUR',
    'JHS': 'JHANSI JN', 'JP': 'JAIPUR', 'JU': 'JODHPUR JN', 'KAWR': 'KARWAR',
    'KGP': 'KHARAGPUR JN', 'KIR': 'KATIHAR JN', 'KOTA': 'KOTA JN', 'KUR': 'KHURDA ROAD JN',
    'LJN': 'LUCKNOW NE', 'LKO': 'LUCKNOW NR', 'LMG': 'LUMDING JN', 'MAS': 'CHENNAI CENTRAL',
    'MB': 'MORADABAD', 'MDU': 'MADURAI JN', 'MGS': 'MUGHAL SARAI JN', 'MLDT': 'MALDA TOWN',
    'MYS': 'MYSORE JN', 'NAG': 'NAGPUR', 'NED': 'H SAHIB NANDED', 'NGP': 'NAGPUR CR',
    'PGT': 'PALAKKAD', 'PRYJ': 'PRAYAGRAJ', 'PUNE': 'PUNE JN', 'R': 'RAIPUR JN',
    'RJT': 'RAJKOT JN', 'RN': 'RATNAGIRI', 'RNC': 'RANCHI', 'RNY': 'RANGIYA JN',
    'RTM': 'RATLAM JN', 'SA': 'SALEM JN', 'SBC': 'BANGALORE CY JN', 'SBP': 'SAMBALPUR',
    'SC': 'SECUNDERABAD JN', 'SDAH': 'SEALDAH', 'SEE': 'SONPUR JN', 'SPJ': 'SAMASTIPUR JN',
    'SUR': 'SOLAPUR JN', 'TPJ': 'TIRUCHCHIRAPALI', 'TSK': 'TINSUKIA JN', 'TVC': 'TRIVANDRUM CNTL',
    'UBL': 'HUBLI JN', 'UMB': 'AMBALA CANT JN', 'WAT': 'WALTAIR'
}
df["STATION_DIV_NAME"] = df["STATION_DIV"].map(div_code_to_name).fillna(df["STATION_DIV"])

# Handle query param for default division selection
query_params = st.query_params
preselected_div = query_params.get("division", [None])[0] if isinstance(query_params.get("division"), list) else query_params.get("division")

# Sidebar selector
divisions = sorted(df["STATION_DIV_NAME"].unique())
selected_div = st.selectbox("Select Division", [""] + divisions, index=(divisions.index(preselected_div) + 1) if preselected_div in divisions else 0)

if selected_div:
    st.markdown(f"### Amenities Heatmap for Division: `{selected_div}`")
    
    df_div = df[df["STATION_DIV_NAME"] == selected_div].copy()
    stations_in_div = df_div['STATION_CODE'].unique()
    station_name_map = df_div.set_index("STATION_CODE")["STATION_NAME"].to_dict()

    # Clean amenities
    def clean_amenity_list(s):
        items = []
        if pd.notna(s) and s.startswith("["):
            try:
                for item in eval(s):
                    clean = re.sub(r"\(\d+\)", "", item).strip()
                    items.append(clean)
            except:
                pass
        return items

    all_amenities = set()
    data = []

    for _, row in df_div.iterrows():
        station = row["STATION_CODE"]
        amenities = clean_amenity_list(row["ALL_AMENITIES"])
        for a in amenities:
            all_amenities.add(a)
            data.append({"Station": station, "Amenity": a, "Available": 1})

    # Fill missing (station, amenity) combos with 0
    for station in stations_in_div:
        for amenity in all_amenities:
            if not any(d["Station"] == station and d["Amenity"] == amenity for d in data):
                data.append({"Station": station, "Amenity": amenity, "Available": 0})

    df_melted = pd.DataFrame(data)
    df_melted["Station Name"] = df_melted["Station"].map(station_name_map)

    # Plot heatmap
    chart = alt.Chart(df_melted).mark_rect().encode(
        x=alt.X("Station:N", title="Station Code", sort=sorted(stations_in_div)),
        y=alt.Y("Amenity:N", title="Amenity", sort="-x"),
        color=alt.Color("Available:Q", scale=alt.Scale(scheme="blues")),
        tooltip=["Station", "Station Name", "Amenity"]
    ).properties(height=600, width=900, title="Amenities Availability Heatmap")

    st.altair_chart(chart, use_container_width=True)

else:
    st.info("Please select a division to see the amenities heatmap.")

render_footer()
