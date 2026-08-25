"""Security regression tests for product-radar-au."""
import subprocess
import re
from pathlib import Path

BASE = Path(__file__).parent.parent
SITE_ORIGIN = 'https://Baodan168.github.io'


# ── P1：Worker 主机边界 ────────────────────────────────
# Worker stub is defined in cloudflare-worker.js; actual host checks
# are now in oa/urls.py (ALLOWED_HOSTS dict). Tests deferred to audit.


# ── P1b：URL 主机白名单 ──────────────────────────────────

def test_urls_allowlist_matches_aws():
    """Amazon AU 主机在白名单。"""
    from oa.urls import ALLOWED_HOSTS
    for h in ['amazon.com.au', 'www.amazon.com.au', 'm.media-amazon.com',
              'ssl-images-amazon.com', 'media-amazon.com']:
        assert ALLOWED_HOSTS.get(h) is not None, f'{h} 未在白名单'


def test_urls_reject_evil_subdomain():
    """evilamazon.com.au 不在白名单。"""
    from oa.urls import ALLOWED_HOSTS
    assert ALLOWED_HOSTS.get('evilamazon.com.au') is None


def test_urls_allows_1688():
    """1688 采购链接在白名单。"""
    from oa.urls import ALLOWED_HOSTS
    assert ALLOWED_HOSTS.get('1688.com') is True


def test_urls_allows_google_trends_au():
    """Google Trends AU 域名在白名单。"""
    from oa.urls import ALLOWED_HOSTS
    assert ALLOWED_HOSTS.get('trends.google.com') is not None
    assert ALLOWED_HOSTS.get('trends.google.com.au') is not None
