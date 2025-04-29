import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session", autouse=True)
def start_streamlit():

    yield


@pytest.mark.parametrize("skill,wishes", [
    ("Python", "Ich möchte Data Science, wo fange ich am besten an?"),
    ("Teamarbeit", ""),
])
def test_mitarbeiter_flow(skill, wishes):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8501")

        page.click("text=Mitarbeiter")

        page.fill("input[aria-label='Welchen Skill möchtest du verbessern?']", skill)

        page.fill("textarea[aria-label='Sonstige Wünsche / Offene Fragen']", wishes)

        page.click("text=Kurse & Empfehlung")

        assert page.locator("text=Kurse gefunden").count() == 1

        page.click("text=LLM-Analyse")
        assert page.locator("Skills zu verbessern:").first.is_visible()

        browser.close()
