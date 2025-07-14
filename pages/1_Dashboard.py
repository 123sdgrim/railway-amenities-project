# pages/1_Dashboard.py

import streamlit as st
import pandas as pd
import altair as alt
from utils import render_logo_and_navbar, render_footer, set_global_background

st.set_page_config(page_title="Dashboard - Railway Station Amenities", layout="wide")

# Header & Background
set_global_background()
render_logo_and_navbar()
st.title("📊 Dashboard")

# ---------------------- MAPPINGS ----------------------
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

zone_code_to_name = {
    'KR': 'KONKAN RAILWAY', 'CR': 'CENTRAL RAILWAY', 'ER': 'EASTERN RAILWAY', 'NR': 'NORTHERN RAILWAY',
    'NE': 'NORTH EASTERN', 'NF': 'NORTH EAST FRONTIER', 'SR': 'SOUTHERN RAILWAY', 'SE': 'SOUTH EASTERN',
    'WR': 'WESTERN RAILWAY', 'SC': 'SOUTH CENTRAL', 'EC': 'EAST CENTRAL', 'NW': 'NORTH WESTERN',
    'EO': 'EAST COAST', 'NC': 'NORTH CENTRAL', 'SB': 'SOUTH EAST CENTRAL', 'SW': 'SOUTH WESTERN',
    'WC': 'WEST CENTRAL'
}

# ---------------------- LOAD & PREP DATA ----------------------

df = pd.read_csv("station_level_data_output.csv")
df["STATION_ZONE"] = df["STATION_ZONE"].astype(str).str.strip()
df["STATION_DIV"] = df["STATION_DIV"].astype(str).str.strip()
df["STATION_DIV_NAME"] = df["STATION_DIV"].map(div_code_to_name).fillna(df["STATION_DIV"])
df["STATION_ZONE_NAME"] = df["STATION_ZONE"].map(zone_code_to_name).fillna(df["STATION_ZONE"])

# Fix amenity list display
def format_amenity_list(lst):
    return "\n".join(eval(lst)) if isinstance(lst, str) and lst.startswith("[") else str(lst)

for col in ['amenities1', 'amenities2', 'ALL_AMENITIES']:
    df[col] = df[col].apply(format_amenity_list)

# ---------------------- SIDEBAR FILTERS ----------------------
with st.sidebar:
    st.header("Filter Options")

    zone_filter = st.selectbox("Zone", ["All"] + sorted(df['STATION_ZONE_NAME'].unique()))
    filtered_df = df.copy()
    if zone_filter != "All":
        filtered_df = filtered_df[filtered_df["STATION_ZONE_NAME"] == zone_filter]

    div_filter = st.selectbox("Division", ["All"] + sorted(filtered_df['STATION_DIV_NAME'].unique()))
    if div_filter != "All":
        filtered_df = filtered_df[filtered_df["STATION_DIV_NAME"] == div_filter]

    station_options = filtered_df[['STATION_CODE', 'STATION_NAME']].drop_duplicates()
    station_options["label"] = station_options["STATION_CODE"] + " - " + station_options["STATION_NAME"]

    if "selected_code" not in st.session_state:
        st.session_state.selected_code = "All"
    if "selected_name" not in st.session_state:
        st.session_state.selected_name = "All"

    code_labels = ["All"] + station_options["STATION_CODE"].tolist()
    selected_code = st.selectbox("Station Code", code_labels, index=code_labels.index(st.session_state.selected_code) if st.session_state.selected_code in code_labels else 0)
    st.session_state.selected_code = selected_code

    if selected_code != "All":
        match_name = station_options[station_options["STATION_CODE"] == selected_code]["STATION_NAME"].values[0]
        st.session_state.selected_name = match_name

    name_labels = ["All"] + station_options["STATION_NAME"].tolist()
    selected_name = st.selectbox("Station Name", name_labels, index=name_labels.index(st.session_state.selected_name) if st.session_state.selected_name in name_labels else 0)
    st.session_state.selected_name = selected_name

    if selected_name != "All":
        match_code = station_options[station_options["STATION_NAME"] == selected_name]["STATION_CODE"].values[0]
        st.session_state.selected_code = match_code

    if st.session_state.selected_code != "All":
        filtered_df = filtered_df[filtered_df["STATION_CODE"] == st.session_state.selected_code]

# ---------------------- TABLE ----------------------
st.markdown("### 📋 Stationwise Amenities Details")
st.caption("Based on one month of station-level data (April 2025) provided by CRIS Delhi.")
st.dataframe(
    filtered_df[['STATION_ZONE_NAME', 'STATION_DIV_NAME', 'STATION_CODE', 'STATION_NAME', 'TOTAL_AMENITIES', 'ALL_AMENITIES']]
    .rename(columns={
        'STATION_ZONE_NAME': 'Zone',
        'STATION_DIV_NAME': 'Division',
        'STATION_CODE': 'Station Code',
        'STATION_NAME': 'Station Name',
        'TOTAL_AMENITIES': 'Total Amenities',
        'ALL_AMENITIES': 'Recommended Amenities'
    }).style.set_properties(**{
        'white-space': 'pre-wrap',
        'text-align': 'left'
    }),
    use_container_width=True,
    hide_index=True
)

# ---------------------- CHARTS ----------------------
color_scale = alt.Scale(domain=sorted(df['STATION_ZONE_NAME'].unique()), scheme='category20')

if st.session_state.selected_code != "All":
    row = filtered_df.iloc[0]
    st.markdown(f"### 🏷️ Station Summary: `{row['STATION_CODE']} - {row['STATION_NAME']}`")
    st.markdown(f"**Zone**: {row['STATION_ZONE_NAME']}  \n**Division**: {row['STATION_DIV_NAME']}")
    st.markdown("#### List of Recommended Amenities:")
    st.markdown(f"```\n{row['ALL_AMENITIES']}\n```")

else:
    st.subheader("📉 Amenities Distribution")

    if div_filter != "All":
        st.markdown(f"**Number of Stations in Division `{div_filter}`**: `{filtered_df['STATION_CODE'].nunique()}`")
        chart_df = filtered_df[['STATION_CODE', 'STATION_NAME', 'STATION_ZONE_NAME', 'TOTAL_AMENITIES']].copy()
        chart_df['STATION_CODE_CLEAN'] = chart_df['STATION_CODE'].str.replace("_", " ")
        chart_df['STATION_NAME_CLEAN'] = chart_df['STATION_NAME'].str.replace("_", " ")
        chart_df['ZONE_CLEAN'] = chart_df['STATION_ZONE_NAME'].str.replace("_", " ")

        bar = alt.Chart(chart_df).mark_bar().encode(
            x=alt.X('STATION_CODE_CLEAN:N', sort='-y', title='Station Code'),
            y=alt.Y('TOTAL_AMENITIES:Q', title='Number of Amenities'),
            tooltip=[
                alt.Tooltip('STATION_NAME_CLEAN:N', title='Station Name'),
                alt.Tooltip('STATION_CODE_CLEAN:N', title='Station Code'),
                alt.Tooltip('ZONE_CLEAN:N', title='Zone'),
                alt.Tooltip('TOTAL_AMENITIES:Q', title='Amenities')
            ],
            color=alt.value("#4682b4")
        ).properties(height=400, width=700, title=f"Amenities per Station in Division: {div_filter}")
        st.altair_chart(bar, use_container_width=True)

        st.markdown(
            f"""
            <p style='margin-top:10px;'>
                <a href='Heatmap?division={div_filter}' style='color:#1f77b4; font-weight:600;'>
                🔍 View Amenities Heatmap for {div_filter} ➜</a>
            </p>
            """,
            unsafe_allow_html=True
        )

    elif zone_filter != "All":
        st.markdown(f"**Number of Divisions in Zone `{zone_filter}`**: `{filtered_df['STATION_DIV_NAME'].nunique()}`")
        chart_df = filtered_df.groupby('STATION_DIV_NAME')[['TOTAL_AMENITIES']].sum().reset_index()
        chart_df['DIVISION_CLEAN'] = chart_df['STATION_DIV_NAME'].str.replace("_", " ")

        bar = alt.Chart(chart_df).mark_bar().encode(
            x=alt.X('DIVISION_CLEAN:N', sort='-y', title='Division'),
            y=alt.Y('TOTAL_AMENITIES:Q', title='Number of Amenities'),
            tooltip=[
                alt.Tooltip('DIVISION_CLEAN:N', title='Division'),
                alt.Tooltip('TOTAL_AMENITIES:Q', title='Amenities')
            ],
            color=alt.value("#4682b4")
        ).properties(height=400, width=700, title=f"Amenities per Division in Zone: {zone_filter}")
        st.altair_chart(bar, use_container_width=True)

    else:
        chart_df = df.groupby('STATION_ZONE_NAME')[['TOTAL_AMENITIES']].sum().reset_index()
        chart_df['ZONE_CLEAN'] = chart_df['STATION_ZONE_NAME'].str.replace("_", " ")

        bar = alt.Chart(chart_df).mark_bar().encode(
            x=alt.X('ZONE_CLEAN:N', sort='-y', title='Zone'),
            y=alt.Y('TOTAL_AMENITIES:Q', title='Number of Amenities'),
            tooltip=[
                alt.Tooltip('ZONE_CLEAN:N', title='Zone'),
                alt.Tooltip('TOTAL_AMENITIES:Q', title='Amenities')
            ],
            color=alt.Color('ZONE_CLEAN:N', scale=color_scale, legend=alt.Legend(title="Zone"))
        ).properties(height=400, width=700, title="Zone-wise Amenities Distribution")
        st.altair_chart(bar, use_container_width=True)

# ---------------------- FOOTER ----------------------
render_footer()
