import streamlit as st                          
from llm_utils import analyse_skill_gap, get_courses  #Hilfsfunktionen: Kurse holen

def mitarbeiter_app():                           # Hauptfunktion für den Mitarbeiter-Bereich
    st.title("Mitarbeiter Bereich")             
    st.title("Weiterbildungsvorschläge")       

             #skill einageb 
    selected_skill = st.text_input(             
        "Welchen Skill möchtest du verbessern?"
    )

   
    other_wishes = st.text_area(                 #sonst. wünsche t.feld 
        "Sonstige Wünsche / Offene Fragen",
        placeholder="z. B. „Ich möchte neu Fuß fassen im Bereich Data Science. Wo soll ich deiner Meinung nach anfangen?“" 
    )

    if st.button("Kurse & Empfehlung"): 
        #button für kurse und empfehlungen
        
                  
        if not selected_skill:

            #wurde skill eingegeben? ---> fallback                    
            st.warning("Bitte zuerst einen Skill eingeben.")  # Warnung, wenn das Feld leer ist
            return                               # Funktion hier abbrechen, bis ein Skill drinsteht

        
        kurse = get_courses([selected_skill])                   #holt die kurse
        if kurse:                                               # falls diese gefunden werden
            st.success(f"{len(kurse)} Kurse gefunden:") 
            for k in kurse:                      
                st.markdown(                      
                    f"**{k['title']}** (_{k['provider']}_)  [Kurs öffnen]({k['link']})"
                )
        else:    #fallback,wenn no kurse gefudnen                                
            st.info("Keine Kurse in der Datenbank gefunden") 

        # analyse llm | AUSFÜHRLICHER PRMOPT 
        with st.spinner("LLM erstellt Schritt-für-Schritt-Plan…"):  
           


#WICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWICHTIGWIC 

#für andere use case keine eigenen prompt templates nutzen ----> VERNÜNFTIGE PROMPT-STRUKTUR sonst zu viel hallizunation bzw kein vernünftiger output

#jegliche prompt engineering, prompt generatort oder optimizer macht das super einfach 

# punkt 5 im prompt templates anpassen falls mehr als nur 2.3 kurse zurückgegeben werden 

#punkt 3 für andere reihenfolge    


            prompt = f"""
Du bist ein persönlicher Karriere-Coach für berufliche Weiterbildung.
Der Mitarbeiter möchte seinen Skill "{selected_skill}" verbessern.
Zusätzlich hat er folgende offene Wünsche oder Fragen:
{other_wishes}

Gib ihm einen konkreten, schritt-für-schritt Lernplan:                                                  
1. Welche Grundlagenkurse oder Tutorials sollte er zuerst machen?
2. Mit welchen kleinen Projekten oder Übungen kann er das Gelernte anwenden?
3. In welcher Reihenfolge (Kurs → Übung → Projekt) sollte er vorgehen?
4. Welche weiterführenden Themen passen danach (Fortgeschrittene Konzepte)?
5. Empfehle aus der obigen Kursliste genau 2-3 Kurse und verlinke sie.

Antworte als nummerierte Liste mit kurzen, präzisen Anweisungen.
"""
            llm_output = analyse_skill_gap(       #llm abruf für plan erstellen
                [selected_skill],                  #skill übergabe 
                {                                 
                    "name": "Mitarbeiter",
                    "wishes": other_wishes,
                    selected_skill: 1
                }
            )

        
        with st.expander("LLM-Analyse"):          # Aufklappbereich # AUSGABE AUSGABE AUSGABE 
            st.markdown(llm_output)              
