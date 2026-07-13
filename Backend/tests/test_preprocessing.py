from app.services.preprocessing import clean_text, normalize_text

def test_normalize_text_collapses_whitespace():
    assert normalize_text("hello    world") == "hello world"

def test_normalize_text_strips_control_chars():
    assert normalize_text("hello\x00\x1fworld") == "hello world"

def test_normalize_text_handles_none():
    assert normalize_text(None) == ""

def test_normalize_text_strips_leading_trailing_whitespace():
    assert normalize_text("   hello world   ") == "hello world"

def test_clean_text_replaces_url_placeholder():
    assert clean_text("check this out URL_0 now") == "check this out <URL> now"

def test_clean_text_replaces_multiple_url_placeholders():
    result = clean_text("see URL_1 and also URL_23")
    assert result == "see <URL> and also <URL>"

def test_clean_text_does_not_lowercase():
    # RoBERTa was tokenized on answer_text_clean WITHOUT lowercasing —
    # only the Logistic Regression / TF-IDF branch lowercases text.
    assert clean_text("This Is Mixed Case") == "This Is Mixed Case"

def test_clean_text_collapses_whitespace_after_url_substitution():
    assert clean_text("a   URL_5    b") == "a <URL> b"
