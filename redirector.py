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
    '360041082851': 'How-to-upgrade-to-Hack',
    '360041082791': 'Does-Hack--require-internet-access',
    '360040652892': ('How-do-I-know-if-I-still-have-the-old-version-of-Hack-'
                     'instead-of-the-new-one'),
    '360040652872': 'If-I-have-Hack-Key-how-can-I-upgrade-to-Hack',
    '360040652832': 'What-is-the-Hack-switch',
    '360040652772': 'Purchase-and-Shipping-FAQs',
    '360041081951': 'What-are-the-Hack-Laptop-specs',
    '360041081911': 'Is-this-computer-good-for-teaching-my-children-coding',
    '360040651932': 'Can-the-Hack-Laptop-be-used-as-a-normal-laptop-as-well',
    '360040651912': 'What-parental-control-does-the-Hack-Laptop-has',
    '360041081691': 'Purchase-and-Shipping-FAQ',
    '360040651832': 'Can-I-install-Windows-in-the-Hack-Laptop',
    '360040651792': 'Are-screen-and-keyboard-protectors-available',
    '360040651732': 'What-applications-can-be-used-on-the-Hack-Laptop',
    '360040651392': 'Getting-started',
    '360041081211': 'Forgotten-password',
    '360041081131': ('I-am-unable-to-connect-the-computer-to-any-Wi-Fi-'
                     'network-What-do-I-do'),
    '360041081111': 'How-do-I-install-a-printer-to-this-computer',
    '360040651132': 'Which-printers-are-supported-by-Endless-OS',
    '360041080831': 'Can-I-install-new-apps-or-software',
    '360040650872': 'How-to-add-users',
    '360040650812': ('Why-does-the-computer-seem-to-get-slower-over-time-or-'
                     'when-visiting-a-lot-of-websites'),
    '360041080431': 'Ordering-Pricing-Subscription',
    '360039501332': 'Which-keyboard-shortcuts-are-available-in-Endless-OS',
    '360039665771': 'How-to-install-Endless-OS-on-Raspberry-Pi',
    '360039661071': 'Endless-OS-Releases-History',
    '360039254812': 'Introduction-video-to-Endless-OS',
    '360037107312': ('A-Hack-icon-suddenly-appeared-on-the-desktop-of-my-'
                     'Endless-OS-computer-What-is-going-on'),
    '360013334552': 'How-can-I-become-an-Endless-OS-mirror',
    '360013050691': ('My-GB-Endless-One-cannot-be-upgraded-because-the-disk-'
                     'is-full-What-should-I-do'),
    '360006862391': ('After-an-OS-upgrade-why-is-the-previous-version-of-'
                     'Endless-OS-kept-on-my-computer-Can-I-remove-it'),
    '360006827311': 'How-do-I-delete-all-users-from-my-computer',
    '360006685771': ('How-do-I-create-a-USB-stick-to-reformat-one-or-more-'
                     'computers-with-a-particular-Endless-OS-image'),
    '360002546631': 'How-can-I-add-tools-like-GCC-on-EOS',
    '115005151806': ('How-to-record-Endless-OS-screen-and-create-a-tutorial-'
                     'video'),
    '115004976986': ('How-can-I-install-Endless-OS-on-a-computer-replacing-'
                     'its-current-OS'),
    '115004795106': 'Is-Endless-OS-based-on-Debian',
    '115004778083': 'Does-the-EOS-Updates-change-my-customized-desktop',
    '115004774606': 'How-can-I-access-my-Windows-files-through-Endless-OS',
    '115004169706': ('Do-I-need-anti-virus-software-on-Endless-OS-What-makes-'
                     'Endless-OS-more-secure'),
    '115004159706': 'Does-Endless-OS-have-an-FTP-app',
    '115003751803': ('After-an-update-my-computer-does-not-boot-How-do-I-'
                     'recover'),
    '115003637063': ('What-s-the-difference-between-installing-Endless-OS-and-'
                     'reformatting-with-Endless-OS'),
    '115003662326': ('The-installer-cannot-connect-to-the-server-even-though-'
                     'I-am-online'),
    '115003058803': ('How-do-I-make-a-debug-log-for-the-Endless-Installer-for-'
                     'Windows'),
    '115002984283': 'How-do-I-create-an-Endless-OS-USB-stick-on-Windows',
    '115002335646': ('After-installing-Endless-OS-the-GRUB-menu-does-not-'
                     'appear-and-it-starts-directly-in-Windows'),
    '115001980483': 'What-s-Flatpak',
    '115001689683': ('I-want-to-remove-Windows-and-keep-only-Endless-OS-How-'
                     'can-i-do-this'),
    '115001629603': ('How-can-I-create-and-boot-an-Endless-USB-stick-from-'
                     'macOS'),
    '214475643': 'Why-can-t-I-watch-Netflix-or-YouTube-videos',
    '210527203': 'Am-I-allowed-to-redistribute-Endless-OS',
    '208416346': 'How-do-I-make-a-debug-log-of-Endless-OS',
    '208248636': 'Is-your-OS-open-source',
    '209763383': 'Can-I-connect-your-computer-to-a-local-network',
    '208248376': 'How-do-I-connect-a-Bluetooth-device-to-my-Endless-computer',
    '360040652612': 'Hack-USB-Requirements',
    '360040650212': 'How-do-I-get-more-information-about-Hack',
    '115000923843': ('Can-not-boot-Windows-after-installing-Endless-can-not-'
                     'load-image'),
    '214369466': 'Why-can-t-I-play-video',
    '208248646': 'Can-I-develop-a-program-for-your-computer',
    '208248606': 'How-can-I-have-access-to-the-super-user-in-your-computer',
    '208248586': 'I-forgot-my-password',
    '208248076': ('Can-I-use-the-Internet-if-I-don-t-have-WiFi-but-I-do-have-'
                  'a-cable-connection'),
    '360040652492': 'How-to-check-if-your-computer-has-USB',
    '360040650332': 'How-do-I-get-help-for-Hack',
    '216454503': ('If-I-change-hardware-like-add-a-new-graphics-card-will-'
                  'Endless-OS-recognize-it'),
    '215071586': 'How-often-is-Endless-OS-updated',
    '208920886': 'Can-I-modify-Endless-OS',
    '360041082131': 'How-to-tell-if-you-have-Windows',
    '360040650372': 'Endless-OS',
    '115000097483': 'Why-can-t-I-use-apt-get-dpkg-dnf-or-rpm-commands',
    '215071686': 'How-do-I-join-the-Endless-Team',
    '215810983': ('How-much-storage-space-shall-I-set-for-Endless-OS-'
                  'installation-alongside-Windows'),
    '210527403': 'Can-I-use-Microsoft-Word-Excel-or-PowerPoint',
    '208248386': 'What-is-a-user-account',
    '360040652372': 'How-to-check-your-Bios',
    '360040650452': 'Can-I-get-Hack-on-a-computer-that-has-Windows',
    '214986846': 'Is-there-a-recovery-partition-like-Windows-for-Endless-OS',
    '208248476': 'How-do-I-get-more-games-on-my-computer',
    '209763083': ('When-I-plug-the-computer-into-my-TV-I-can-t-see-the-user-'
                  'menu-What-should-I-do'),
    '208248396': 'How-do-I-create-a-new-user-account',
    '360040650552': 'Will-Endless-OS-work-with-my-computer',
    '360041080231': 'Getting-Started',
    '214369366': 'What-changes-are-made-to-my-system-by-the-Installer',
    '212053963': ('How-do-I-erase-my-USB-so-I-can-use-it-again-after-I-ve-'
                  'finished-using-it-for-Endless-OS'),
    '210527383': 'Can-I-run-Windows-applications-on-Endless',
    '209763343': ('I-can-t-see-Endless-on-my-screen-even-though-my-monitor-is-'
                  'turned-on'),
    '360040652192': 'What-is-Error-Code',
    '210527183': ('Can-I-install-Linux-software-and-apps-from-Ubuntu-Fedora-'
                  'and-others-on-Endless'),
    '208248496': 'How-do-I-set-my-own-background-on-the-computer',
    '213585826': 'What-can-I-do-with-an-Endless-USB-Stick',
    '209763473': ('How-can-I-install-a-device-that-is-not-in-your-list-of-'
                  'peripherals'),
    '208248446': 'Can-I-install-and-add-new-software-or-apps',
    '214475943': ('What-information-does-the-Endless-Installer-for-Windows-'
                  'collect'),
    '209763543': 'How-do-I-install-a-printer-to-this-computer',
    '214475283': ('How-do-I-uninstall-Endless-if-I-installed-it-alongside-'
                  'Windows'),
    '210731406': 'Will-my-printer-scanner-or-G-G-dongle-work',
    '208248426': ('How-do-I-find-apps-that-are-currently-installed-on-my-'
                  'computer'),
    '215157086': 'Upgrade-from-Endless-OS--x-to-Endless-OS',
    '212890106': 'How-do-I-install-Endless-OS-alongside-Windows',
    '208920526': 'Can-I-listen-to-my-music',
    '210527323': 'Can-I-view-my-photos',
    '210526863': 'Will-Endless-OS-work-with-my-computer',
    '208247996': 'How-do-I-set-up-my-WiFi',
    '209763173': 'How-can-I-talk-to-people-using-my-computer',
    '208248226': 'How-do-I-know-if-I-m-connected-to-the-internet',
    '210527003': ('Can-I-install-Endless-alongside-an-existing-operating-'
                  'system-like-Windows-or-OSX'),
    '208248506': 'Do-I-need-to-have-internet-for',
    '208907686': 'Which-languages-are-supported-by-Endless-OS',
    '210527043': 'What-is-the-difference-between-the-Basic-and-Full-versions',
    '210527103': ('How-do-I-start-boot-my-computer-from-a-USB-device-or-DVD-'
                  'with-Endless-OS'),
    '209063006': ('Where-can-I-download-the-Endless-OS-ISO-image-files-'
                  'directly'),
    '210654503': 'How-do-I-create-an-Endless-USB-stick-from-Linux',
    '209763423': 'How-do-I-update-Endless-OS',
    '210527046': 'How-do-I-run-Endless-OS-in-a-Virtual-Machine',
    '209763363': ('Why-does-the-computer-seem-to-get-slower-over-time-or-when-'
                  'visiting-a-lot-of-websites'),
    '208248596': 'Does-your-computer-support-Flash-Adobe-Flash',
    '212053683': ('How-do-I-create-a-USB-stick-from-an-image-file-I-have-'
                  'already-downloaded'),
    '209763413': 'What-are-the-shortcut-keys',
    '214711163': 'Which-printers-will-be-supported-by-Endless-OS',
    '210474163': 'How-do-I-block-bad-content-e-g-pornographic-web-pages',
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
