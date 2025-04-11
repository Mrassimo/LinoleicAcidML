import pytest
import pandas as pd
from bs4 import BeautifulSoup
from src.data_processing.scrape_fire_in_bottle import find_and_parse_pre_blocks, scrape_la_content

def test_find_and_parse_pre_blocks_success():
    """Test parsing of a valid <pre> block with expected table structure."""
    html = """
    <html>
    <body>
    <pre>
| Food | la_cal | cal | percent |
|------|--------|-----|---------|
| Sunflower Oil | 120 | 124 | 97 |
| Corn Oil | 95 | 120 | 79 |
    </pre>
    </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    df = find_and_parse_pre_blocks(soup)
    assert df is not None
    assert len(df) == 2
    assert set(df.columns) >= {'food_name', 'la_cal', 'cal', 'percent'}
    assert df['food_name'].iloc[0] == 'Sunflower Oil'
    assert df['la_cal'].iloc[1] == 95

def test_find_and_parse_pre_blocks_no_pre():
    """Test behaviour when no <pre> tags are present."""
    html = "<html><body><div>No pre tags here</div></body></html>"
    soup = BeautifulSoup(html, "html.parser")
    df = find_and_parse_pre_blocks(soup)
    assert df is None

def test_find_and_parse_pre_blocks_invalid_format():
    """Test <pre> block with no valid table lines."""
    html = "<html><body><pre>Just some text, not a table</pre></body></html>"
    soup = BeautifulSoup(html, "html.parser")
    df = find_and_parse_pre_blocks(soup)
    assert df is None

def test_scrape_la_content_network(monkeypatch):
    """Test scrape_la_content handles network errors gracefully."""
    def mock_requests_get(*args, **kwargs):
        raise Exception("Network error")
    import src.data_processing.scrape_fire_in_bottle as mod
    monkeypatch.setattr(mod.requests, "get", mock_requests_get)
    df = scrape_la_content("http://fakeurl")
    assert df is None

def test_find_and_parse_pre_blocks_partial_columns():
    """Test <pre> block with missing expected columns."""
    html = """
    <html>
    <body>
    <pre>
| Food | la_cal | cal |
|------|--------|-----|
| Sunflower Oil | 120 | 124 |
    </pre>
    </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    df = find_and_parse_pre_blocks(soup)
    # Should still parse, but 'percent' column will be missing
    assert df is not None
    assert 'percent' not in df.columns
    assert df['food_name'].iloc[0] == 'Sunflower Oil'
def test_fallback_to_code_tag():
    """Test fallback to <code> tag when no <pre> is present (Australian English)."""
    html = """
    <html><body>
    <code>
    | Food | la_cal | cal | percent |
    |------|--------|-----|---------|
    | Sunflower Oil | 120 | 124 | 97 |
    </code>
    </body></html>
    """
    soup = BeautifulSoup(html, "html.parser")
def test_tolerant_to_missing_trailing_pipes():
    """Test parser tolerance to missing trailing pipes and extra whitespace (Australian English)."""
    html = """
    <html><body>
    <pre>
    | Food | la_cal | cal | percent
    |------|--------|-----|--------
    | Sunflower Oil | 120 | 124 | 97
    | Corn Oil | 95 | 120 | 79
    </pre>
    </body></html>
    """
    soup = BeautifulSoup(html, "html.parser")
def test_header_data_row_mismatch():
    """Test parser tolerance to header/data row mismatch (Australian English)."""
    html = """
    <html><body>
    <pre>
    | Food | la_cal | cal | percent |
    |------|--------|-----|---------|
    | Sunflower Oil | 120 | 124 |
    | Corn Oil | 95 | 120 | 79 | extra |
    </pre>
    </body></html>
    """
    soup = BeautifulSoup(html, "html.parser")
    df = find_and_parse_pre_blocks(soup)
    assert df is not None
def test_multiple_blocks_one_valid():
    """Test multiple blocks, only one valid (Australian English)."""
    html = """
    <html><body>
    <pre>Not a table</pre>
    <pre>
    | Food | la_cal | cal | percent |
    |------|--------|-----|---------|
    | Sunflower Oil | 120 | 124 | 97 |
    </pre>
    </body></html>
    """
    soup = BeautifulSoup(html, "html.parser")
def test_unrecoverable_malformed_table():
    """Test unrecoverable malformed table returns None (Australian English)."""
    html = """
    <html><body>
    <pre>
    This is not a table at all
    No pipes or headers
    </pre>
    </body></html>
    """
    soup = BeautifulSoup(html, "html.parser")
    df = find_and_parse_pre_blocks(soup)
    assert df is None

    df = find_and_parse_pre_blocks(soup)
    assert df is not None
    assert len(df) == 1
    assert df['food_name'].iloc[0] == 'Sunflower Oil'

    assert len(df) == 2
    # Should pad/truncate as needed, and not crash
    assert df['food_name'].iloc[0] == 'Sunflower Oil'
    assert df['food_name'].iloc[1] == 'Corn Oil'

    df = find_and_parse_pre_blocks(soup)
    assert df is not None
    assert len(df) == 2
    assert set(df.columns) >= {'food_name', 'la_cal', 'cal', 'percent'}

    df = find_and_parse_pre_blocks(soup)
    assert df is not None
    assert len(df) == 1
    assert df['food_name'].iloc[0] == 'Sunflower Oil'


def test_fallback_to_div_tag():
    """Test fallback to <div> tag with table-like content (Australian English)."""
    html = """
    <html><body>
    <div>
    | Food | la_cal | cal | percent |
    |------|--------|-----|---------|
    | Sunflower Oil | 120 | 124 | 97 |
    </div>
    </body></html>
    """
    soup = BeautifulSoup(html, "html.parser")
    df = find_and_parse_pre_blocks(soup)
    assert df is not None
    assert len(df) == 1
    assert df['food_name'].iloc[0] == 'Sunflower Oil'

    """Test fallback to <code> tag when no <pre> is present (Australian English)."""
    html = """
    <html><body>
    <code>
    | Food | la_cal | cal | percent |
    |------|--------|-----|---------|
    | Sunflower Oil | 120 | 124 | 97 |
    </code>
    </body></html>
    """
    soup = BeautifulSoup(html, "html.parser")
    df = find_and_parse_pre_blocks(soup)
    assert df is not None
    assert len(df) == 1
    assert df['food_name'].iloc[0] == 'Sunflower Oil'

