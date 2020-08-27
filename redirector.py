# Redirect URLs from old Endless support site to new support site
#
# Copyright (C) 2020  Endless OS Foundation LLC
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import re
from urllib.parse import urljoin

# Base URL to redirect to
SUPPORT_URL = os.getenv('SUPPORT_URL', 'https://support.endlessos.org')

# Regex matching old Zendesk article URL paths. The language component,
# slug suffix and trailing / are optional. Some valid Zendesk article
# URLs:
#
# /hc/en-us/articles/12345-Some-title
# /hc/en-us/articles/12345
# /hc/articles/12345-Blah-blah-blah
# /hc/pt/articles/67890
# /hc/pt/articles/67890/
ARTICLE_PATH_RE = re.compile(
    # All paths begin with /hc
    r'^/hc'
    # Language is optional
    r'(?:/(?P<lang>[^/]+))?'
    # All paths contain /articles
    r'/articles'
    # The article number
    r'/(?P<article>\d+)'
    # Optional title slug
    r'(?:-[^/]+)?'
    # Optional trailing /
    r'/?$'
)

# Map from article number to new article slug
ARTICLE_MAP = {
    '360041130551': 'How-to-use-the-Hack-laptop',
    '360041130271': 'What-is-a-pathway',
}


# FIXME: Currently no language conversion is done until the language
# handling of wiki.js is better understood.
def convert_path(path):
    """Convert URL path for old site to path for new site"""
    match = ARTICLE_PATH_RE.match(path)
    if not match:
        return ''
    dest_article = ARTICLE_MAP.get(match.group('article'))
    if not dest_article:
        return ''
    return f'/help-center/{dest_article}'


def application(env, start_response):
    """WSGI application to redirect old support URLs"""
    path = env.get('PATH_INFO')
    new_path = convert_path(path)
    location = urljoin(SUPPORT_URL, new_path)
    headers = [('Location', location)]
    start_response('301 Moved Permanently', headers)
    return tuple()
