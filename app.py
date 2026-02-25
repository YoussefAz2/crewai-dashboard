import streamlit as st
import os

# Configuration
st.set_page_config(page_title="CrewAI Dashboard", layout="wide")

# Session state
if 'agents' not in st.session_state:
    st.session_state.agents = []
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'results' not in st.session_state:
    st.session_state.results = None

st.title("🎮 CrewAI Dashboard")
st.markdown("**Créez et lancez vos équipes d'agents**")

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Ajouter agent
    st.subheader("👤 Nouvel Agent")
    agent_name = st.text_input("Nom", key="agent_name")
    agent_role = st.text_input("Rôle", key="agent_role")
    agent_goal = st.text_area("Objectif", key="agent_goal")
    agent_backstory = st.text_area("Backstory", key="agent_backstory")
    
    if st.button("➕ Ajouter Agent"):
        if agent_name and agent_role and agent_goal:
            st.session_state.agents.append({
                'name': agent_name,
                'role': agent_role,
                'goal': agent_goal,
                'backstory': agent_backstory
            })
            st.success(f"Agent {agent_name} ajouté!")
            st.rerun()
    
    # Liste des agents
    if st.session_state.agents:
        st.subheader("Agents créés")
        for agent in st.session_state.agents:
            st.write(f"- **{agent['name']}** ({agent['role']})")
    
    # Ajouter tâche
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
    
    # Lancer
    st.subheader("🚀 Lancer")
    if st.button("🚀 Lancer le Crew", type="primary"):
        if st.session_state.agents and st.session_state.tasks:
            st.session_state.run_crew = True
            st.rerun()
        else:
            st.error("Créez au moins un agent et une tâche!")

# Main content
if st.session_state.get('run_crew'):
    st.header("⏳ Exécution en cours...")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    logs_container = st.container()
    
    # Simuler l'exécution
    import time
    
    total_steps = len(st.session_state.tasks)
    results = {}
    
    for i, task in enumerate(st.session_state.tasks):
        progress = (i + 1) / total_steps
        progress_bar.progress(progress)
        status_text.text(f"Exécution: {task['name']}...")
        
        # Trouver l'agent
        agent = next((a for a in st.session_state.agents if a['name'] == task['agentName']), None)
        
        with logs_container:
            st.info(f"🤖 **{agent['name']}** exécute: {task['name']}")
            st.write(f"*{task['description'][:100]}...*")
        
        # Simuler le travail
        time.sleep(2)
        
        # Générer un résultat
        result = f"Résultat de la tâche '{task['name']}':\n\n"
        result += f"Agent {agent['name']} ({agent['role']}) a analysé la demande.\n"
        result += f"Objectif: {agent['goal']}\n\n"
        result += f"Travail effectué sur: {task['description'][:50]}...\n\n"
        result += "✅ Tâche terminée avec succès!"
        
        results[task['name']] = result
        
        with logs_container:
            st.success(f"✅ {task['name']} terminé!")
    
    st.session_state.results = results
    st.session_state.run_crew = False
    progress_bar.empty()
    status_text.empty()
    st.success("✅ Crew terminé!")
    st.rerun()

# Afficher résultats
if st.session_state.results:
    st.header("📄 Résultats")
    for task_name, result in st.session_state.results.items():
        with st.expander(f"📋 {task_name}"):
            st.markdown(result)

# Vue d'ensemble
if not st.session_state.results and not st.session_state.get('run_crew'):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👥 Agents")
        if st.session_state.agents:
            for agent in st.session_state.agents:
                with st.expander(f"🤖 {agent['name']}"):
                    st.write(f"**Rôle:** {agent['role']}")
                    st.write(f"**Objectif:** {agent['goal']}")
        else:
            st.info("Aucun agent créé")
    
    with col2:
        st.subheader("📋 Tâches")
        if st.session_state.tasks:
            for task in st.session_state.tasks:
                with st.expander(f"📌 {task['name']}"):
                    st.write(f"**Assigné à:** {task['agentName']}")
                    st.write(f"**Description:** {task['desc']}")
        else:
            st.info("Aucune tâche créée")
    
    if not st.session_state.agents and not st.session_state.tasks:
        st.info("👈 **Commence par créer des agents et des tâches dans le menu de gauche!**")
