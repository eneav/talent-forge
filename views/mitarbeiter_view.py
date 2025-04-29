import streamlit as st
from llm_utils import analyse_skill_gap, get_courses

def mitarbeiter_app():
    st.title("Mitarbeiter Bereich ")
    st.title("Weiterbildungsvorschläge")

    # 1) Skill auswählen
    selected_skill = st.text_input("Welchen Skill möchtest du verbessern?")

    # 2) Freies Textfeld für „Sonstige Wünsche“
    other_wishes = st.text_area(
        "Sonstige Wünsche / Offene Fragen",
        placeholder="z. B. „Ich möchte neu Fuß fassen im Bereich Data Science. Wo soll ich deinermeinung nach anfangen?“"
    )

    if st.button("Kurse & Empfehlung"):
        if not selected_skill:
            st.warning("Bitte zuerst einen Skill eingeben.")
            return

        # 3) Kurse aus deiner JSON holen
        kurse = get_courses([selected_skill])
        if kurse:
            st.success(f"{len(kurse)} Kurse gefunden:")
            for k in kurse:
                st.markdown( f"**{k['title']}** (_{k['provider']}_)  [Kurs öffnen]({k['link']})")
        else:
            st.info("Keine Kurse in der Datenbank gefunden.")

        # 4) LLM-Analyse mit ausführlichem Prompt
        with st.spinner("LLM erstellt Schritt-für-Schritt-Plan…"):
            # Baue den Prompt direkt hier zusammen
            prompt = f"""
Du bist ein persönlicher Karriere-Coach für berufliche Weiterbildung.
Der Mitarbeiter möchte seinen Skill "{selected_skill}" verbessern.
Zusätzlich hat er folgende offene Wünsche oder Fragen:
{other_wishes}

Gib ihm einen **konkreten**, **schritt-für-schritt** Lernplan:
1. Welche Grundlagenkurse oder Tutorials sollte er zuerst machen?
2. Mit welchen kleinen Projekten oder Übungen kann er das Gelernte anwenden?
3. In welcher Reihenfolge (Kurs → Übung → Projekt) sollte er vorgehen?
4. Welche weiterführenden Themen passen danach („Fortgeschrittene Konzepte“)?
5. Empfehle aus der obigen Kursliste genau 2–3 Kurse und verlinke sie.

Liefere die Antwort als nummerierte Liste mit kurzen, präzisen Anweisungen.
"""
            llm_output = analyse_skill_gap([selected_skill], {"name": "Mitarbeiter", "wishes": other_wishes, selected_skill: 1})
        
        # 5) Ergebnis anzeigen
        with st.expander("LLM-Analyse"):
            st.markdown(llm_output)
