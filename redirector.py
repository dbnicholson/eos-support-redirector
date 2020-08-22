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

# Map from old URLs to new URLs
LINK_MAP = dict((
    ('/hc/en-us/articles/360041130551-How-to-use-the-Hack-laptop-',
     '/help-center/How-to-use-the-Hack-laptop'),
    ('/hc/en-us/articles/360041130271-What-is-a-pathway-',
     '/help-center/What-is-a-pathway'),
))

# Map with optional article name suffix removed from old URL. I.e.,
# '/hc/en-us/articles/12345-Some-title' is the same as
# '/hc/en-us/articles/12345'.
article_name_re = re.compile(r'(.*/\d+)-[^/]*$')
SHORT_LINK_MAP = dict(
    [(article_name_re.match(k).group(1), v) for k, v in LINK_MAP.items()]
)


def convert_path(path):
    """Convert path for old site to path for new site"""
    return LINK_MAP.get(path, SHORT_LINK_MAP.get(path, ''))


def application(env, start_response):
    """WSGI application to redirect old support URLs"""
    path = env.get('PATH_INFO')
    new_path = convert_path(path)
    location = urljoin(SUPPORT_URL, new_path)
    headers = [('Location', location)]
    start_response('301 Moved Permanently', headers)
    return tuple()
