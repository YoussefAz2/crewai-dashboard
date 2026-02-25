import streamlit as st

st.title("🎮 CrewAI Dashboard")

# Session state
if 'agents' not in st.session_state:
    st.session_state.agents = []

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    name = st.text_input("Nom de l'agent")
    role = st.text_input("Rôle")
    
    if st.button("Ajouter Agent"):
        st.session_state.agents.append({'name': name, 'role': role})
        st.rerun()

# Main
st.write("Agents:", st.session_state.agents)
