import streamlit as st
from datetime import datetime

def add_history(kind, raw, result):
    if "history" not in st.session_state: st.session_state.history=[]
    st.session_state.history.insert(0,{
        "time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type":kind,"input_preview":raw.replace("\\n"," ")[:65],
        "classification":result.get("classification","Unknown"),
        "risk_score":result.get("risk_score",0)
    })
    st.session_state.history=st.session_state.history[:50]
def get_history(): return st.session_state.get("history",[])
def clear_history(): st.session_state.history=[]
