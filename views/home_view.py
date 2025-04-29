import streamlit as st

def home_view():
    st.image("assets/image3.png", width=300)
    st.title("TalentForge - Dein Karriere-Coach")
    # st.image("assets/image3.png", width=300)    
    
    # Ausklappbare Gesamt-Anleitung
    with st.expander(" Kurzanleitung", expanded=True):
        st.markdown("""
        
       
        - Mitarbeiter-Bereich: Ermöglicht die Eingabe eines Wunsch-Skills und offener Fragen, um passende Kurse und einen Lernplan zu erhalten
        - Abteilungsleiter-Bereich: Lässt Projektname, wichtige Kompetenzen, Mitarbeiterbewertungen sowie Zeitplan, Budget und Teamgröße eingeben und liefert darauf basierende Analysen
        """)

    st.markdown("---")
    st.write("Wähle links deinen Bereich aus")
