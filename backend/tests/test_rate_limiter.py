"""Unit tests for the in-memory rate limiter."""

from datetime import timedelta

from app.services.rate_limiter import RateLimiter


def test_allows_requests_within_limit() -> None:
    limiter = RateLimiter(limit=3, window=timedelta(hours=1))
    assert limiter.is_allowed("1.2.3.4") is True
    assert limiter.is_allowed("1.2.3.4") is True
    assert limiter.is_allowed("1.2.3.4") is True


def test_blocks_when_limit_reached() -> None:
    limiter = RateLimiter(limit=3, window=timedelta(hours=1))
    for _ in range(3):
        limiter.is_allowed("1.2.3.4")
    assert limiter.is_allowed("1.2.3.4") is False


def test_different_ips_are_independent() -> None:
    limiter = RateLimiter(limit=1, window=timedelta(hours=1))
    assert limiter.is_allowed("1.1.1.1") is True
    assert limiter.is_allowed("2.2.2.2") is True


def test_limit_resets_after_window_expires() -> None:
    limiter = RateLimiter(limit=1, window=timedelta(seconds=0))
    limiter.is_allowed("1.2.3.4")
    # window=0 means all prior entries are immediately expired
    assert limiter.is_allowed("1.2.3.4") is True
