import streamlit as st
from views.home_view        import home_view
from views.mitarbeiter_view import mitarbeiter_app
from views.chef_view        import chef_view

st.set_page_config(
    page_title="TalentForge",
    page_icon="assets/talent-icon.png",
    layout="wide",
)


st.markdown(                            #css injektion für die Sidebar
                                        #DONT TOUCH THIS, IT WORKS FINE 
    """
    <style>
      /* Container der Radio-Group ins Visuelle heben und full-width */
      div[role="radiogroup"] > label {
        display: block;
        width: 100% !important;
        box-sizing: border-box;
        border: 1px solid #2b2d3b;
        border-radius: 6px;
        padding: 8px 12px;
        margin: 4px 0;
        transition: background-color 0.2s ease;
      }
      /* Hover-Effekt */
      div[role="radiogroup"] > label:hover {
        background-color: rgba(255, 255, 255, 0.05);
      }
      /* Ausgewählte Option hervorheben */
      div[role="radiogroup"] > label input:checked + span {
        font-weight: bold;
      }
      /* Für Safari/Chrome-Edge: sicherstellen, dass input versteckt ist, Span übernimmt Breite */
      div[role="radiogroup"] > label input {
        position: absolute;
        opacity: 0;
      }
      div[role="radiogroup"] > label span {
        display: inline-block;
        width: calc(100% - 24px); /* für Checkbox plus Padding */
      }
    </style>
    """,
    unsafe_allow_html=True,
)

#auf garkein fall anfassen 



with st.sidebar:
    col_icon, col_title = st.columns([1, 4])
    col_icon.image("assets/talent-icon.png", width=48)
    col_title.markdown(
        "<div style='line-height:1;'>"
        "<span style='font-size:1.2em;font-weight:bold;'>TalentForge</span><br>"                #sidebar  
        "<span style='font-size:0.9em;color:#aaaaaa;'>Dein Karriere-Coach</span>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.title("Bereich wählen")

    wahl = st.radio(
        "",
        ["Startseite", "Mitarbeiter", "Abteilungsleiter"]
    )

    # ganz unten in main.py, nach dem Radio-Button-Aufruf
st.sidebar.markdown("---")
st.sidebar.caption("2025 - Enes Avsar")



if wahl == "Startseite":
    home_view()
elif wahl == "Mitarbeiter":             #hauptbereich für rolle abrufen 
    mitarbeiter_app()
else:
    chef_view()
