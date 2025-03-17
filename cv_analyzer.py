import streamlit as st
import pandas as pd
import plotly.express as px
import time
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import tempfile
import base64

# Import CV Analyzer and Debugger
from cv_analyzer import CVAnalyzer
from utils.debugger import Debugger

# Initialize debugger
debugger = Debugger()

# App configuration
st.set_page_config(
    page_title="CV Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Page title and info
st.title("CV Analyzer")
st.markdown("Ein leistungsstarkes Tool zur Analyse von Lebensläufen und Bewertung von Fähigkeiten")

# Initialize analyzer
@st.cache_resource
def get_analyzer():
    return CVAnalyzer()

analyzer = get_analyzer()

# Function to download files
def get_download_link(data, filename, text):
    if isinstance(data, str):
        data = data.encode()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Page navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["CV Analyse", "Job Matching", "Batch Analyse", "Einstellungen"]
)

# CV Analysis page
if page == "CV Analyse":
    st.header("Lebenslauf analysieren")
    
    # File upload
    uploaded_file = st.file_uploader("Wählen Sie einen Lebenslauf (PDF, DOCX)", type=["pdf", "docx"])
    
    if uploaded_file is not None:
        # Save temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        
        try:
            # Progress bar
            progress_bar = st.progress(0)
            start_time = time.time()
            
            # Perform analysis
            with st.spinner("Analysiere Lebenslauf..."):
                for i in range(100):
                    # Simulate progress
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                # Actual analysis
                results = analyzer.analyze_cv_file(tmp_path)
                
                # Log performance metric
                duration = time.time() - start_time
                debugger.log_performance_metric("analysis_duration", duration)
            
            # Display results
            st.success("Analyse abgeschlossen!")
            
            # Overview
            st.subheader("Übersicht")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Beruf", results.get("profession", "Nicht erkannt"))
            
            with col2:
                st.metric("Erfahrungslevel", results.get("experience_level", "Nicht erkannt"))
            
            with col3:
                st.metric("Relevanz Score", f"{results.get('relevance_score', 0):.0f}%")
            
            # Visualize skills
            st.subheader("Fähigkeiten")
            if "skills" in results and results["skills"]:
                skills_df = pd.DataFrame({
                    "Fähigkeit": list(results["skills"].keys()),
                    "Bewertung": list(results["skills"].values())
                })
                
                fig = px.bar(
                    skills_df, 
                    x="Fähigkeit", 
                    y="Bewertung",
                    color="Bewertung",
                    color_continuous_scale="viridis",
                    title="Fähigkeiten-Bewertung"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Keine Fähigkeiten erkannt.")
            
            # Visualize experience
            st.subheader("Berufserfahrung")
            if "experience" in results and results["experience"]:
                st.markdown("### Zeitleiste")
                
                # Experience timeline
                experience_df = pd.DataFrame(results["experience"])
                experience_df["start_date"] = pd.to_datetime(experience_df["start_date"])
                experience_df["end_date"] = pd.to_datetime(experience_df["end_date"])
                experience_df["duration"] = (experience_df["end_date"] - experience_df["start_date"]).dt.days / 365.25
                
                fig = px.timeline(
                    experience_df,
                    x_start="start_date",
                    x_end="end_date",
                    y="title",
                    color="company",
                    title="Berufserfahrung"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Experience table
                st.dataframe(
                    experience_df[["title", "company", "start_date", "end_date", "duration"]].rename(
                        columns={
                            "title": "Position",
                            "company": "Unternehmen",
                            "start_date": "Startdatum",
                            "end_date": "Enddatum",
                            "duration": "Dauer (Jahre)"
                        }
                    ).sort_values("Startdatum", ascending=False)
                )
            else:
                st.info("Keine Berufserfahrung erkannt.")
            
            # Recommendations
            st.subheader("Empfehlungen")
            recommendations = results.get("recommendations", [])
            if recommendations:
                for i, rec in enumerate(recommendations):
                    st.markdown(f"**{i+1}.** {rec}")
            else:
                st.info("Keine Empfehlungen verfügbar.")
            
            # Export options
            st.subheader("Ergebnisse exportieren")
            col1, col2, col3 = st.columns(3)
            
            # JSON Export
            with col1:
                json_data = json.dumps(results, indent=2)
                st.markdown(
                    get_download_link(json_data, "cv_analysis.json", "Als JSON herunterladen"),
                    unsafe_allow_html=True
                )
            
            # CSV Export
            with col2:
                csv_data = analyzer.export_results(results, format="csv")
                st.markdown(
                    get_download_link(csv_data, "cv_analysis.csv", "Als CSV herunterladen"),
                    unsafe_allow_html=True
                )
            
            # Excel Export
            with col3:
                excel_data = analyzer.export_results(results, format="excel")
                st.markdown(
                    get_download_link(excel_data, "cv_analysis.xlsx", "Als Excel herunterladen"),
                    unsafe_allow_html=True
                )
                
        except Exception as e:
            st.error(f"Fehler bei der Analyse: {str(e)}")
            debugger.log_error(e, "cv_analysis")
        
        finally:
            # Delete temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

# Job Matching page
elif page == "Job Matching":
    st.header("Lebenslauf mit Stellenbeschreibung abgleichen")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Lebenslauf")
        cv_file = st.file_uploader("Lebenslauf hochladen (PDF, DOCX)", type=["pdf", "docx"])
    
    with col2:
        st.subheader("Stellenbeschreibung")
        job_description = st.text_area("Fügen Sie die Stellenbeschreibung ein oder laden Sie eine Datei hoch", height=300)
        job_file = st.file_uploader("Stellenbeschreibung hochladen (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
        
        if job_file is not None:
            # Save temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{job_file.name.split('.')[-1]}") as tmp:
                tmp.write(job_file.getvalue())
                job_path = tmp.name
            
            # Read file
            try:
                job_description = analyzer.extract_text(job_path)
                st.success("Stellenbeschreibung erfolgreich geladen!")
            except Exception as e:
                st.error(f"Fehler beim Lesen der Stellenbeschreibung: {str(e)}")
                debugger.log_error(e, "job_description_reading")
            
            # Delete temporary file
            if os.path.exists(job_path):
                os.unlink(job_path)
    
    # Match button
    if cv_file and (job_description or job_file):
        if st.button("Lebenslauf mit Stellenbeschreibung abgleichen"):
            # Save temporary file for CV
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{cv_file.name.split('.')[-1]}") as tmp:
                tmp.write(cv_file.getvalue())
                cv_path = tmp.name
            
            try:
                # Progress bar
                progress_bar = st.progress(0)
                start_time = time.time()
                
                with st.spinner("Führe Matching durch..."):
                    for i in range(100):
                        # Simulate progress
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    # Actual analysis
                    results = analyzer.analyze_cv_file(cv_path, job_description)
                    
                    # Log performance metric
                    duration = time.time() - start_time
                    debugger.log_performance_metric("match_duration", duration)
                
                st.success("Matching abgeschlossen!")
                
                # Match score
                st.subheader("Match-Ergebnisse")
                
                # Gauge chart for match score
                match_score = results.get("relevance_score", 0)
                fig = px.pie(
                    values=[match_score, 100-match_score],
                    names=["Match", "Gap"],
                    hole=0.7,
                    color_discrete_sequence=["#4B8BBE", "#E2E8F0"]
                )
                fig.update_layout(
                    annotations=[{
                        "text": f"{match_score:.0f}%",
                        "showarrow": False,
                        "font": {"size": 40}
                    }],
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Missing skills
                st.subheader("Empfohlene Verbesserungen")
                
                if "missing_skills" in results and results["missing_skills"]:
                    missing_skills_df = pd.DataFrame({
                        "Fähigkeit": list(results["missing_skills"].keys()),
                        "Wichtigkeit": list(results["missing_skills"].values())
                    })
                    
                    fig = px.bar(
                        missing_skills_df,
                        x="Fähigkeit",
                        y="Wichtigkeit",
                        color="Wichtigkeit", 
                        color_continuous_scale="oranges",
                        title="Fehlende oder zu verbessernde Fähigkeiten"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Keine fehlenden Fähigkeiten identifiziert.")
                
                # Recommendations
                if "recommendations" in results and results["recommendations"]:
                    for i, rec in enumerate(results["recommendations"]):
                        st.markdown(f"**{i+1}.** {rec}")
                
                # Export options
                st.subheader("Er
