# views/layout.py
import streamlit as st

def layout_generale():
    """
    Layout generale della Dashboard
    """
    st.markdown("<link href='views/styles.css' rel='stylesheet'>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='header-title'>
            Baku Grand Slam 2025
        </div>
        <p style='text-align: center; color: #A6A9B6;'>36 nations / 258 judoka</p>
    """, unsafe_allow_html=True)
