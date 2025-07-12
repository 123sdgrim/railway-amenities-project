# pages/About_Us.py

import streamlit as st
from utils import render_logo_and_navbar,render_footer, set_global_background

st.set_page_config(page_title="About Us - Railway Station Amenities", layout="wide")

# Render logo and navbar (shared across pages)
set_global_background()
render_logo_and_navbar()

# ---- ABOUT US PAGE CONTENT ----
about_us_html = """
<style>
.about-heading {
    text-align: center;
    font-size: 60px;
    font-weight: bold;
    color: #0056D2;
    letter-spacing: 4px;
    font-family: 'Orbitron', sans-serif;
}
.about-subheading {
    text-align: center;
    font-size: 24px;
    font-style: italic;
    margin-top: -10px;
    margin-bottom: 30px;
    color: #555;
    font-family: 'Georgia', serif;
}
.about-text {
    text-align: center;
    font-size: 18px;
    max-width: 900px;
    margin: auto;
    line-height: 1.6;
    color: #222;
    padding: 0 20px;
}
</style>

<div class="about-heading">ABOUT US</div>
<div class="about-subheading">WHO WE ARE</div>
<div class="about-text">
    CRIS (Centre for Railway Information Systems) is an organization under the Ministry of Railways. 
    CRIS combines skilled IT professionals and experienced Railway personnel to deliver robust, mission-critical systems for the Indian Railways.<br><br>
    We specialize in the development and maintenance of software for core functions like:<br>
    ➤ Passenger Reservation System (PRS)<br>
    ➤ Freight Operations Information System (FOIS)<br>
    ➤ Unreserved Ticketing System (UTS)<br>
    ➤ Coaching Operations<br>
    ➤ Crew Management System<br>
    ➤ And much more supporting Indian Railways' digital infrastructure.
</div>
"""
st.markdown(about_us_html, unsafe_allow_html=True)



render_footer()