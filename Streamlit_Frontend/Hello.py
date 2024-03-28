import streamlit as st

st.set_page_config(
    page_title="Welcome!",
    page_icon="👋",
)

st.write("# Eat Smart, Feel Great: Your Tasty Guide to a Healthier You! Eat Smart, Feel Great: Your Tasty Guide to a Healthier You 👋")

st.sidebar.success("Select a recommendation app.")

st.markdown(
    """
    Our Diet Recommendation System is like having a personal chef and nutritionist rolled into one, creating custom meal plans that match your tastes, lifestyle, and
    health goals. Say goodbye to one-size-fits-all diets and hello to a deliciously personalized journey to wellness. Whether you're a foodie looking to explore new 
    flavors or just want to feel your best, join us on this flavorful adventure to better health! [repo](https://github.com/elvis-kimutai/DietPlanner).
    """
)

# Add an image
st.image("ImageFinder/img2.jpg", caption="Optional Caption", use_column_width=True)
