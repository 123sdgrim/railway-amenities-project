import streamlit as st
import base64

def set_global_background():
    st.markdown("""
    <style>
    body, .stApp {
        background-color: #f9f9f9 !important;
        scroll-behavior: smooth;
    }
    </style>
    """, unsafe_allow_html=True)


def render_logo_and_navbar():
    # Load CRIS logo with transparent background
    with open("cris_logo-removebg-preview.png", "rb") as file_:
        contents = base64.b64encode(file_.read()).decode("utf-8")

    logo_html = f'''
    <div style="text-align: center; background-color: #e6f2ff; padding: 30px 0;">
        <img src="data:image/png;base64,{contents}" width="200"/>
    </div>
    '''

    navbar_html = """
    <style>
    .navbar {
        display: flex;
        justify-content: center;
        background-color: #004080;
        padding: 1rem;
        margin-bottom: 2rem;
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    .navbar a {
        color: white;
        padding: 0.5rem 1.5rem;
        text-decoration: none;
        font-weight: bold;
        transition: background 0.3s ease;
    }
    .navbar a:hover {
        background-color: #0066cc;
        border-radius: 5px;
    }
    </style>
    <div class="navbar">
        <a href="/">Home</a>
        <a href="/Dashboard" target="_self">Dashboard</a>
        <a href="/About_Us" target="_self">About Us</a>
        <a href="/#contact-us-section">Contact Us</a>
    </div>
    """

    st.markdown(logo_html, unsafe_allow_html=True)
    st.markdown(navbar_html, unsafe_allow_html=True)


def render_footer():
    footer_html = """
    <hr style="margin-top:50px;">
    <div id="contact-us-section" style="background-color: #000; padding: 2rem; text-align: center; font-size: 0.95rem; color: #fff;">
        <p style="font-size: 1.2rem;"><b>📫 Contact Us</b></p>
        <p>
            📍 Centre for Railway Information Systems, Chanakyapuri, New Delhi - 110021<br>
            ☎️ Phone: 011-24104525, 011-24106717<br>
            📠 Fax: 26877893 <br>
            🌐 Website: <a href="https://cris.org.in" target="_blank" style="color: #66b2ff;">https://cris.org.in</a>
        </p>
        <p>
            👤 <b>Chief Public Information Officer:</b> Ms. Rohita Mishra (Registrar)<br>
            <a href="mailto:mishra.rohita@cris.org.in" style="color: #66b2ff;">mishra.rohita@cris.org.in</a>
        </p>
        <p>
            👤 <b>Appellate Authority:</b> Shri Dharmendra Kumar<br>
            <a href="mailto:kumar.dharmendra@cris.org.in" style="color: #66b2ff;">kumar.dharmendra@cris.org.in</a>
        </p>
        <p>
            👤 <b>Asst. Public Information Officer:</b> Virender Kumar Setia (Additional Registrar)<br>
            <a href="mailto:kumar.virender@cris.org.in" style="color: #66b2ff;">kumar.virender@cris.org.in</a>
        </p>
        <div style="margin-top: 30px;">
            Made with ❤️ by CRIS Delhi
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)
