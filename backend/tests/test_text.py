from app.services.text import strip_emojis


def test_strip_emojis_empty_string() -> None:
    assert strip_emojis("") == ""


def test_strip_emojis_plain_ascii_unchanged() -> None:
    text = "Your balance is $12,847.32 as of today."
    assert strip_emojis(text) == text


def test_strip_emojis_removes_single_emoji_in_middle() -> None:
    assert strip_emojis("Hi Alex 👋 welcome back") == "Hi Alex  welcome back"


def test_strip_emojis_removes_leading_and_trailing_emoji() -> None:
    assert strip_emojis("✨ all set ✨") == " all set "


def test_strip_emojis_removes_multiple_emojis() -> None:
    text = "Great 🎉 news 🚀 your transfer 💸 went through"
    assert strip_emojis(text) == "Great  news  your transfer  went through"


def test_strip_emojis_removes_flag_emoji() -> None:
    # 🇺🇸 is a regional indicator pair
    assert strip_emojis("Welcome to Nova 🇺🇸") == "Welcome to Nova "


def test_strip_emojis_removes_zwj_profession_emoji() -> None:
    # 👨‍💻 is man + ZWJ + laptop
    assert strip_emojis("Our engineers 👨‍💻 are on it") == "Our engineers  are on it"


def test_strip_emojis_removes_heart_and_sun_symbols() -> None:
    # ❤ and ☀ live in the misc-symbols range
    assert strip_emojis("Sunny ☀ day, love ❤ it") == "Sunny  day, love  it"


def test_strip_emojis_preserves_punctuation_digits_currency_accents() -> None:
    text = "Café costs €5.50, £4.20, or $6.00 — that's 100% fair!"
    assert strip_emojis(text) == text
