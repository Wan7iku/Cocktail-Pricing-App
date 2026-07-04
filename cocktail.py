import streamlit as st 
import pricing 
import recipe_builder 
import dashboard 
# ----------------------- # PAGE CONFIG # -----------------------
st.set_page_config( page_title="Cocktail Management System", page_icon="🍸", layout="wide", )
 # ----------------------- # SIDEBAR # ----------------------- 
st.sidebar.title("🍸 Cocktail Management System") 
page = st.sidebar.radio( "Navigation", [ "Recipe Builder", "Pricing Engine", "Dashboard", ], )
 # ----------------------- # PAGE ROUTING # ----------------------- 
if page == "Recipe Builder": recipe_builder.show() 
elif page == "Pricing Engine": pricing.show() 
elif page == "Dashboard": dashboard.show()
