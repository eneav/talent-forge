import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict, Any

load_dotenv()
_api_key = os.getenv("OPENAI_API_KEY")
_client = OpenAI(api_key=_api_key)

def get_courses(skills: List[str]) -> List[Dict[str, Any]]:
    """Lädt courses.json und gibt alle Kurse zurück, deren 'skill' in skills enthalten ist."""
    base = os.path.dirname(__file__)
    path = os.path.join(base, "assets", "courses.json")
    with open(path, encoding="utf-8") as f:
        all_data = json.load(f)

    lower = [s.lower() for s in skills]
    matches = []
    for entry in all_data:
        if entry["skill"].lower() in lower:
            for c in entry["courses"]:
                c["skill"] = entry["skill"]
                matches.append(c)
    return matches

def analyse_skill_gap(project_skills: List[str], mitarbeiter: Dict[str, Any]) -> str:
    """Ruft GPT auf, um Skill-Gap-Empfehlungen für einen Mitarbeiter zu generieren."""
    name = mitarbeiter.get("name", "Mitarbeiter")
    levels = "\n".join(f"- {k}: {v}" for k, v in mitarbeiter.items() if k != "name")
    prompt = f"""
Du bist ein KI-Coach für berufliche Weiterbildung.
Projektskills: {', '.join(project_skills)}
Mitarbeiter: {name}
Aktuelle Bewertung:
{levels}

Welche 1–2 Skills sollte diese Person vorrangig verbessern und welche Kurse wären dafür geeignet?
Gib die Empfehlungen als kurze Liste zurück.
"""
    resp = _client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return resp.choices[0].message.content

def analyse_project(prompt: str) -> str:
    """Ruft GPT auf, um eine Projektanalyse zu erstellen."""
    resp = _client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return resp.choices[0].message.content
