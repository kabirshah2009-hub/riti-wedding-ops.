import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page & Aesthetic Configuration
st.set_page_config(page_title="Riti's Wedding Master Ops", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8F7F3; }
    h1, h2, h3 { font-family: 'Playfair Display', serif; color: #2D2A26; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF; border-radius: 12px; padding: 10px 20px; border: 1px solid #E5E1DA;
    }
    .stTabs [aria-selected="true"] { background-color: #2D2A26 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Connection to the Massive Data Source
# Replace with your shared Google Sheet URL
URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID_HERE/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. Sidebar Navigation for Better Organization
st.sidebar.title("💎 Riti's Wedding")
st.sidebar.markdown("---")
view_mode = st.sidebar.radio("Switch View", ["Dashboard", "Event Detailed Flow", "Vendor Directory", "Planner Instructions"])

# 4. Global Search (Search across the entire Excel)
search_query = st.sidebar.text_input("🔍 Search anything...")

# 5. PAGE LOGIC
if view_mode == "Dashboard":
    st.header("Master Command Center")
    col1, col2, col3 = st.columns(3)
    col1.metric("Countdown", "12 Days")
    col2.metric("Pending Tasks", "42")
    col3.metric("Vendors Confirmed", "18")
    
    st.subheader("Today's High Priority Timeline")
    # Displaying a summary of the 'Run Sheet' sheet
    run_sheet = conn.read(spreadsheet=URL, worksheet="Event Flow — Run Sheet")
    st.table(run_sheet.head(10))

elif view_mode == "Event Detailed Flow":
    st.header("Event Run Sheets")
    # Tabs for each sheet in your massive Excel
    tab1, tab2, tab3, tab4 = st.tabs(["Ganesh Pooja", "Cocktail", "Mehendi/Haldi", "Wedding"])
    
    event_list = ["Ganesh Pooja", "Cocktail Party", "Mehendi & Haldi", "Wedding Ceremony"]
    tabs = [tab1, tab2, tab3, tab4]
    
    for i, tab in enumerate(tabs):
        with tab:
            # Dynamically read the specific sheet from Excel
            data = conn.read(spreadsheet=URL, worksheet=f"2{i+2} Feb — {event_list[i].split()[0]}")
            st.subheader(f"Detailed Info for {event_list[i]}")
            
            # ALLOW EDITING: This turns the massive Excel into an interactive grid
            edited_data = st.data_editor(data, num_rows="dynamic", key=f"editor_{i}")
            
            if st.button(f"Save Changes to {event_list[i]}", key=f"btn_{i}"):
                conn.update(spreadsheet=URL, worksheet=f"2{i+2} Feb — {event_list[i].split()[0]}", data=edited_data)
                st.success("Master Excel Updated!")

elif view_mode == "Vendor Directory":
    st.header("📞 Master Contact Directory")
    directory_data = conn.read(spreadsheet=URL, worksheet="Master Directory")
    
    # Filter by search
    if search_query:
        directory_data = directory_data[directory_data.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)]
    
    st.dataframe(directory_data, use_container_width=True)

elif view_mode == "Planner Instructions":
    st.header("📋 Standard Operating Procedures")
    instructions = conn.read(spreadsheet=URL, worksheet="Instructions for Planners")
    for index, row in instructions.iterrows():
        with st.expander(f"Instruction {index + 1}"):
            st.write(row.iloc[1]) # Displaying the purpose/instruction
