import streamlit as st
import os

st.set_page_config(page_title="CrewAI Dashboard", layout="wide")

if 'agents' not in st.session_state:
    st.session_state.agents = []
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'results' not in st.session_state:
    st.session_state.results = None

st.title("🎮 CrewAI Dashboard")

with st.sidebar:
    st.header("⚙️ Configuration")
    
    st.subheader("👤 Nouvel Agent")
    agent_name = st.text_input("Nom", key="agent_name")
    agent_role = st.text_input("Rôle", key="agent_role")
    agent_goal = st.text_area("Objectif", key="agent_goal")
    
    if st.button("➕ Ajouter Agent"):
        if agent_name and agent_role and agent_goal:
            st.session_state.agents.append({
                'name': agent_name,
                'role': agent_role,
                'goal': agent_goal
            })
            st.success(f"Agent {agent_name} ajouté!")
            st.rerun()
    
    if st.session_state.agents:
        st.subheader("Agents créés")
        for agent in st.session_state.agents:
            st.write(f"- **{agent['name']}** ({agent['role']})")
    
    st.subheader("📋 Nouvelle Tâche")
    task_name = st.text_input("Nom de la tâche", key="task_name")
    task_agent = st.selectbox("Assigné à", [a['name'] for a in st.session_state.agents]) if st.session_state.agents else None
    task_desc = st.text_area("Description", key="task_desc")
    
    if st.button("➕ Ajouter Tâche"):
        if task_name and task_agent and task_desc:
            st.session_state.tasks.append({
                'name': task_name,
                'agentName': task_agent,
                'description': task_desc
            })
            st.success(f"Tâche {task_name} ajoutée!")
            st.rerun()
    
    if st.button("🚀 Lancer le Crew", type="primary"):
        if st.session_state.agents and st.session_state.tasks:
            st.session_state.run_crew = True
            st.rerun()
        else:
            st.error("Créez au moins un agent et une tâche!")

if st.session_state.get('run_crew'):
    st.header("⏳ Exécution en cours...")
    progress_bar = st.progress(0)
    
    import time
    total_steps = len(st.session_state.tasks)
    
    for i, task in enumerate(st.session_state.tasks):
        progress = (i + 1) / total_steps
        progress_bar.progress(progress)
        st.info(f"🤖 Exécution: {task['name']}")
        time.sleep(1)
    
    st.session_state.run_crew = False
    st.session_state.results = {"Résultat": "Tâches exécutées!"}
    progress_bar.empty()
    st.success("✅ Terminé!")
    st.rerun()

if st.session_state.results:
    st.header("📄 Résultats")
    st.write(st.session_state.results)

col1, col2 = st.columns(2)

with col1:
    st.subheader("👥 Agents")
    for agent in st.session_state.agents:
        st.write(f"- {agent['name']}")

with col2:
    st.subheader("📋 Tâches")
    for task in st.session_state.tasks:
        st.write(f"- {task['name']} → {task.get('description', 'N/A')[:30]}...")
