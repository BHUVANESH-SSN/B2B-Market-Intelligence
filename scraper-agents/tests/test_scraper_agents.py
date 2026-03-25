from scraper.diff_agent import diff_sections
from scraper.html_utils import extract_sections


def test_extract_sections_returns_business_sections() -> None:
    html = """
    <html>
      <body>
        <main>
          <h1>Automation for revenue teams</h1>
          <p>Run workflows faster.</p>
          <a href="/demo">Book demo</a>
          <ul>
            <li>Salesforce integration</li>
            <li>Slack alerts</li>
          </ul>
        </main>
      </body>
    </html>
    """
    sections = extract_sections(html)
    assert "hero" in sections
    assert "features" in sections
    assert "ctas" in sections


def test_diff_sections_keeps_only_new_changes() -> None:
    current = {"features": ["Salesforce integration", "Slack alerts"]}
    previous = {"features": ["Slack alerts"]}
    diffs = diff_sections(current, previous)
    assert diffs == {"features": ["Salesforce integration"]}
