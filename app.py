import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Solar Village Tracker", layout="wide")

DATA_FILE = "data_store.xlsx"

# Initializing Excel template data if file is missing
if not os.path.exists(DATA_FILE):
    initial_template = pd.DataFrame([
        {"Village": "Rampur", "Consumer Name": "K. Rama Rao", "Meter Number": "MTR99812", "Partial Installation": "No", "Complete Installation": "No", "Civil Work Done": "No"},
        {"Village": "Rampur", "Consumer Name": "P. Laxmi", "Meter Number": "MTR99815", "Partial Installation": "No", "Complete Installation": "No", "Civil Work Done": "No"},
        {"Village": "Chandrapur", "Consumer Name": "B. Mahesh", "Meter Number": "MTR55421", "Partial Installation": "No", "Complete Installation": "No", "Civil Work Done": "No"}
    ])
    initial_template.to_excel(DATA_FILE, index=False)

if 'survey_df' not in st.session_state:
    st.session_state.survey_df = pd.read_excel(DATA_FILE)

df = st.session_state.survey_df

st.markdown("<h2 style='text-align: center; color: #e67e22;'>☀️ Solar Installation Live Grid Portal</h2>", unsafe_allow_html=True)
st.write("---")

search_input = st.text_input("🔍 Village Peru Type Cheyandi:", "").strip()

if search_input:
    matched_indices = df[df['Village'].str.lower() == search_input.lower()].index
    
    if len(matched_indices) > 0:
        st.success(f"📋 Records matched for: *{search_input.upper()}* village.")
        
        for idx in matched_indices:
            row = df.loc[idx]
            
            with st.container():
                st.markdown(
                    f"""
                    <div style='border: 2px solid #34495e; padding: 15px; border-radius: 8px; background-color: #f8f9fa; margin-bottom: 10px;'>
                        <h4 style='margin: 0px 0px 5px 0px; color: #2c3e50;'>👤 Name: {row['Consumer Name']}</h4>
                        <p style='margin: 0px; font-weight: bold; color: #7f8c8d;'>⚡ Meter Number: <span style='color:#2980b9;'>{row['Meter Number']}</span></p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    is_partial = row['Partial Installation'] == "Partial Installation"
                    p_val = st.checkbox("Partial Installation", value=is_partial, key=f"p_{idx}")
                    df.at[idx, 'Partial Installation'] = "Partial Installation" if p_val else "No"
                    
                with col2:
                    is_complete = row['Complete Installation'] == "Complete"
                    c_val = st.checkbox("Complete Installation", value=is_complete, key=f"c_{idx}")
                    df.at[idx, 'Complete Installation'] = "Complete" if c_val else "No"
                    
                with col3:
                    is_done = row['Civil Work Done'] == "Done"
                    d_val = st.checkbox("Civil Work Done", value=is_done, key=f"d_{idx}")
                    df.at[idx, 'Civil Work Done'] = "Done" if d_val else "No"
                    
                st.markdown("<br>", unsafe_allow_html=True)
                
        if st.button("💾 UPDATE DATA SHEETS", use_container_width=True):
            df.to_excel(DATA_FILE, index=False)
            st.session_state.survey_df = df
            st.toast("Data updated successfully!", icon="✅")
            st.rerun()
    else:
        st.error("⚠️ Ee village details database lo levu.")