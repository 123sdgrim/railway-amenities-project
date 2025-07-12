import streamlit as st
from utils import render_logo_and_navbar, render_footer, set_global_background

st.set_page_config(page_title="Home - Railway Station Amenities", layout="wide")

# Background color
set_global_background()

# Logo and navbar
render_logo_and_navbar()

# Home content
st.markdown("""
## 👋 Welcome to the Railway Station Amenities Portal

This application provides intelligent recommendations for amenities across railway stations in India, based on real passenger data and station activity.

Use the navigation bar above to explore:
- 📊 Dashboard for analytics
- 🧑‍💼 About Us to know our mission
- 📫 Contact Us (scrolls below)

We aim to empower smarter infrastructure decisions through data.
""")

# Footer
render_footer()
