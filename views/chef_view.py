import streamlit as st
from llm_utils import analyse_skill_gap, analyse_project, get_courses

def chef_view():
    st.title("Abteilungsleiter-Bereich")
    st.title("Projekt- & Skill-Analyse")

    
    st.header("1. Projektdefinition")
    projektname = st.text_input("Projektname")
    projektbeschreibung = st.text_area("Projektbeschreibung")               #abschnitt für projektbeschreibung
    st.markdown(
        "Bitte beschreibe dein Projekt in 1-2 Sätzen. "
        "Das hilft uns, die richtigen Skills und Kurse zu finden."
    )                                                                       #gggfs TODO/ platzhalter, oder stätige doku? 
    st.markdown("---")

    st.header("2. Kompetenzentwicklung im Projekt")

    verfuegbare_skills = [
        "Python", "Machine Learning", "Teamarbeit", "Scrum", "React", "Kommunikation",
        "Dokumentation", "SQL", "Leadership", "Cloud Computing", "Zeitmanagement",
        "Konfliktmanagement", "Java", "Change Management", "Kritisches Denken",
        "PowerPoint", "Networking", "Kundenservice", "Data Analysis",
        "Business Intelligence"
    ]

    ausgewaehlte_skills = st.multiselect(
        "Welche Skills sind im Projekt wichtig?",                               #checnox lsite für alle Skills

        verfuegbare_skills
    )

    if not ausgewaehlte_skills:
        st.info("Bitte wähle mindestens eine Kompetenz aus.")
    else:
        st.success(f"Ausgewählte Skills: {', '.join(ausgewaehlte_skills)}")

    # Freitext für Sonstiges
    sonstiges = st.text_area("Sonstige Wünsche / Rahmenbedingungen")
    st.markdown("---")

    # mitarbeitende bewerten
    st.header("3. Mitarbeitende bewerten")
    anzahl = st.number_input("Anzahl Mitarbeitende", min_value=1, max_value=10, value=1)
    mitarbeitende = []

    for i in range(int(anzahl)):
        name = st.text_input(f"Mitarbeiter {i+1} Name", key=f"name_{i}")
        bewertungen = {
            skill: st.slider(f"{skill}-Kompetenz", 0, 5, 3, key=f"skill_{skill}_{i}")
            for skill in ausgewaehlte_skills
        }
        mitarbeitende.append({"name": name, **bewertungen})

    if st.button("Kurs- & Skill-Empfehlung generieren"):
        for m in mitarbeitende:
            st.subheader(m.get("name") or "Unbenannter Mitarbeiter")
            low = [s for s in ausgewaehlte_skills if m.get(s, 0) <= 3]
            kurse = get_courses(low)
            if kurse:
                for k in kurse:
                    st.markdown(
                        f"**{k['title']}** (_{k['provider']}_)\n"
                        f"[Kurs öffnen]({k['link']})"
                    )
            else:
                st.info("Keine Kurse gefunden.")

            #analyse pro Mitarbeiter
            with st.spinner(f"Analyse für {m['name']}…"):
                
                prompt = (
                    f"Projekt-Skills: {', '.join(ausgewaehlte_skills)}\n"
                    f"Mitarbeiter: {m['name']}\n"
                    f"Aktuelle Bewertungen:\n" +
                    "\n".join(f"- {s}: {m[s]}" for s in low)
                )
                if sonstiges:
                    prompt += f"\nSonstige Wünsche: {sonstiges}"

                llm_out = analyse_skill_gap(ausgewaehlte_skills, m)

            with st.expander(f"LLM für {m['name']}"):
                st.markdown(llm_out, unsafe_allow_html=True)

    st.markdown("---")

    # projektanalyse
    st.header("4. Projektanalyse und Ressourcenskalierung")
    start = st.date_input("Start-Datum")
    ende = st.date_input("Ende-Datum")
    budget = st.number_input("Budget (€)", min_value=0, step=100)
    team = st.number_input("Team-Größe", min_value=1, step=1)

    if st.button("Projekt bewerten"):
        if projektname:
            with st.spinner("KI bewertet dein Projekt…"):
                projekt_prompt = (
                    f"Ein Abteilungsleiter plant das Projekt '{projektname}'. "
                    f"Start: {start}, Ende: {ende}. Budget: {budget} Euro. "
                    f"Teamgröße: {team}. Beschreibung: {projektbeschreibung}\n"
                    f"Erstelle eine Empfehlung:\n"
                    "- Ressourcenmanagement\n"
                    "- Realistischer Zeitplan\n"
                    "- Wichtige Meilensteine\n"
                    "- Risikoabschätzung\n"
                    "- Hinweise zur Budgetnutzung\n"
                )
                analyse_text = analyse_project(projekt_prompt)
            st.success("Projektanalyse abgeschlossen!")
            st.markdown(analyse_text, unsafe_allow_html=True)
        else:
            st.warning("Bitte zuerst den Projektnamen eingeben.")
