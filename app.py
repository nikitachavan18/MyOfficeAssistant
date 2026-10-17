"""MyOfficeAssistant: Streamlit web app on top of the OfficeAgent."""
import streamlit as st
 
from agent import MyOfficeAgent
from tools import list_meetings, list_tasks
 
st.set_page_config(page_title="MyOfficeAssistant", page_icon="💼", layout="wide")
st.title("💼 MyOfficeAssistant")
st.caption("Manage tasks, meetings and notes, and draft emails, by chatting.")
 
# Keep the agent and chat history between reruns
if "agent" not in st.session_state:
    st.session_state.agent = MyOfficeAgent()
    st.session_state.messages = []
 
# Sidebar: live view of tasks and meetings
with st.sidebar:
    st.header("📝 Open tasks")
    tasks = list_tasks()["tasks"]
    if tasks:
        for t in tasks:
            due = f" (due {t['due_date']})" if t["due_date"] else ""
            st.write(f"**#{t['id']}** {t['title']}{due} [{t['priority']}]")
    else:
        st.write("No open tasks.")
 
    st.header("📅 Meetings")
    meetings = list_meetings()["meetings"]
    if meetings:
        for m in meetings:
            st.write(f"**{m['date']} {m['time']}**: {m['title']}")
    else:
        st.write("No meetings.")
 
    if st.button("🗑️ Clear chat"):
        st.session_state.agent = MyOfficeAgent()
        st.session_state.messages = []
        st.rerun()
 
# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
 
# Handle new input
prompt = st.chat_input("e.g. Add a task to send the report tomorrow")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                reply = st.session_state.agent.chat(prompt)
            except Exception as e:
                reply = f"Error: {e}"
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun() 
     # refresh the sidebar