import datetime
import json
import math
import os
import pathlib
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from dataclasses import dataclass
from typing import Any

from frame import SANS, border, esc

GITHUB = 'arsen-sharifov'
CODEWARS = 'Arsen Sharifov'
LEETCODE = 'arsen_sharifov'

TIMEOUT = 30
RETRIES = 4
BACKOFF = 8
REPO_PAUSE = 0.4
SEARCH_PAUSE = 2.5

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent / 'assets' / 'generated'
LOGOS = ROOT / 'logos'

MONO = ('ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,'
        '"Liberation Mono",monospace')

BRAND = {'codewars': '#B1361E', 'leetcode': '#FFA116'}
LANG_COLOUR = {
    'TypeScript': '#3178c6', 'JavaScript': '#f1e05a', 'CSS': '#663399',
    'HTML': '#e34c26', 'PLpgSQL': '#336790', 'Python': '#3572A5',
    'SCSS': '#c6538c', 'Shell': '#89e051', 'Dockerfile': '#384d54',
    'Vue': '#41b883', 'Svelte': '#ff3e00', 'Go': '#00ADD8',
}
LC_COLOUR = {'easy': '#00b8a3', 'medium': '#ffb800', 'hard': '#ff375f'}
KYU_COLOUR = {'white': '#9BA3AB', 'yellow': '#E0AC17', 'blue': '#3C7EBB',
              'purple': '#866CC7', 'black': '#4B5158', 'red': '#CF2B2B'}
FALLBACK = '#8B949E'

W, H, PAD = 320, 240, 18
BAR_Y, BAR_H = 214, 7
LEDE_Y, ROWS_TOP, ROW_STEP = 74, 112, 26


@dataclass(frozen=True)
class Card:
    key: str
    name: str
    domain: str
    rows: tuple[tuple[str, str], ...]
    bar: tuple[tuple[str, float], ...]
    lede: tuple[str, str]


@dataclass(frozen=True)
class Theme:
    ink: str
    muted: str
    rule: str
    track: str
    github: str


THEMES = {
    '': Theme(ink='#1F2328', muted='#6E7781', rule='#D8DEE4',
              track='#EFF2F5', github='#24292F'),
    '-dark': Theme(ink='#E6EDF3', muted='#8B949E', rule='#2D333B',
                   track='#21262D', github='#E6EDF3'),
}

LEETCODE_QUERY = ('query($username: String!) { matchedUser(username: $username) '
                  '{ submitStatsGlobal { acSubmissionNum { difficulty count } } } }')


def _get(url: str, payload: dict | None = None, token: bool = False) -> Any:
    data = json.dumps(payload).encode() if payload else None
    headers = {'User-Agent': 'Mozilla/5.0 profile-card', 'Accept': '*/*'}
    if payload:
        headers['Content-Type'] = 'application/json'
        headers['Referer'] = 'https://leetcode.com'
    if token and (bearer := os.environ.get('GITHUB_TOKEN')):
        headers['Authorization'] = 'Bearer ' + bearer
    request = urllib.request.Request(url, data=data, headers=headers)
    attempt = 1
    while True:
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code not in (403, 429, 502, 503, 504) or attempt == RETRIES:
                raise
            time.sleep(BACKOFF * attempt)
            attempt += 1


def github() -> Card:
    def api(path: str) -> Any:
        return _get('https://api.github.com/' + path, token=True)

    def count(query: str) -> int:
        time.sleep(SEARCH_PAUSE)
        return api('search/' + query)['total_count']

    langs: Counter[str] = Counter()
    for repo in api(f'users/{GITHUB}/repos?per_page=100&type=owner'):
        if repo['fork']:
            continue
        langs.update(api(f'repos/{GITHUB}/{repo["name"]}/languages'))
        time.sleep(REPO_PAUSE)

    prs = count(f'issues?q=author:{GITHUB}+type:pr&per_page=1')
    merged = count(f'issues?q=author:{GITHUB}+type:pr+is:merged&per_page=1')
    top_langs = dict(langs.most_common(5))
    total = sum(top_langs.values()) or 1
    top = next(iter(top_langs), None)
    return Card(
        key='github', name='GitHub', domain='github.com',
        rows=(('commits', f"{count(f'commits?q=author:{GITHUB}&per_page=1'):,}"),
              ('pull requests', f'{prs:,}'),
              ('merged', f'{round(100 * merged / prs) if prs else 0}%'),
              ('issues',
               f"{count(f'issues?q=author:{GITHUB}+type:issue&per_page=1'):,}")),
        bar=tuple((LANG_COLOUR.get(lang, FALLBACK), size)
                  for lang, size in top_langs.items()),
        lede=(top or '—',
              f'{100 * top_langs[top] / total:.1f}% of code' if top else ''))


def codewars() -> Card:
    profile = _get('https://www.codewars.com/api/v1/users/'
                   + urllib.parse.quote(CODEWARS))
    overall = profile.get('ranks', {}).get('overall', {})
    rank = overall.get('name', '—')
    kyu = re.match(r'(\d+)\s*kyu', rank)
    progress = (9 - int(kyu.group(1))) / 8 if kyu else 1.0
    fill = KYU_COLOUR.get(overall.get('color', ''), FALLBACK)
    return Card(
        key='codewars', name='CodeWars', domain='codewars.com',
        rows=(('honor', f"{profile.get('honor', 0):,}"),
              ('kata solved',
               f"{profile.get('codeChallenges', {}).get('totalCompleted', 0):,}"),
              ('score', f"{overall.get('score', 0):,}")),
        bar=((fill, progress), ('none', 1 - progress)),
        lede=(rank, 'overall rank'))


def leetcode() -> Card:
    reply = _get('https://leetcode.com/graphql',
                 {'query': LEETCODE_QUERY, 'variables': {'username': LEETCODE}})
    user = (reply.get('data') or {}).get('matchedUser')
    if not user:
        raise RuntimeError('no such LeetCode user')
    solved = {row['difficulty'].lower(): row['count']
              for row in user['submitStatsGlobal']['acSubmissionNum']}
    return Card(
        key='leetcode', name='LeetCode', domain='leetcode.com',
        rows=tuple((level, f"{solved.get(level, 0):,}")
                   for level in ('easy', 'medium', 'hard')),
        bar=tuple((LC_COLOUR[level], solved.get(level, 0))
                  for level in ('easy', 'medium', 'hard')),
        lede=(f"{solved.get('all', 0):,}", 'problems solved'))


def mark(name: str, x: float, y: float, size: float, colour: str) -> str:
    svg = (LOGOS / f'{name}.svg').read_text(encoding='utf-8')
    inner = ''.join(re.sub(r'\s*fill="[^"]*"', '', path)
                    for path in re.findall(r'<path[^>]*/>', svg))
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({size / 24:.4f})" '
            f'fill="{colour}">{inner}</g>')


def render(card: Card, suffix: str) -> str:
    theme = THEMES[suffix]
    colour = theme.github if card.key == 'github' else BRAND[card.key]
    uid = card.key + (suffix or '-light')
    right = W - PAD

    parts = [(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
              f'viewBox="0 0 {W} {H}" role="img" '
              f'aria-label="{esc(card.name)} activity for {GITHUB}">'),
             (f'<title>{esc(card.name)}: {esc(card.lede[0])} '
              f'{esc(card.lede[1])}</title>'),
             mark(card.key, PAD, 20, 14, colour),
             (f'<text x="{PAD + 21}" y="31.5" font-family=\'{SANS}\' font-size="13" '
              f'font-weight="600" fill="{theme.ink}">{esc(card.name)}</text>'),
             (f'<text x="{right}" y="31.5" font-family=\'{SANS}\' font-size="9.5" '
              f'letter-spacing="0.4" text-anchor="end" fill="{theme.muted}">'
              f'{esc(card.domain)} &#8599;</text>'),
             (f'<text x="{PAD}" y="{LEDE_Y}" font-family=\'{SANS}\'>'
              f'<tspan font-size="20" font-weight="600" fill="{theme.ink}">'
              f'{esc(card.lede[0])}</tspan>'
              f'<tspan dx="7" font-size="11.5" fill="{theme.muted}">'
              f'{esc(card.lede[1])}</tspan></text>')]

    for i, (label, value) in enumerate(card.rows):
        y = ROWS_TOP + ROW_STEP * i
        numeric = all(c.isdigit() or c in ',.%#' for c in value)
        face, size = (MONO, 13) if numeric else (SANS, 12.5)
        parts += [(f'<text x="{PAD}" y="{y:.1f}" font-family=\'{SANS}\' '
                   f'font-size="9.5" letter-spacing="0.8" fill="{theme.muted}">'
                   f'{esc(label.upper())}</text>'),
                  (f'<text x="{right}" y="{y:.1f}" font-family=\'{face}\' '
                   f'font-size="{size}" text-anchor="end" fill="{theme.ink}">'
                   f'{esc(value)}</text>')]

    bar_w = W - PAD * 2
    total = sum(share for _, share in card.bar) or 1
    parts += [(f'<clipPath id="b{uid}"><rect x="{PAD}" y="{BAR_Y}" '
               f'width="{bar_w}" height="{BAR_H}" rx="{BAR_H / 2}"/></clipPath>'),
              (f'<rect x="{PAD}" y="{BAR_Y}" width="{bar_w}" height="{BAR_H}" '
               f'rx="{BAR_H / 2}" fill="{theme.track}"/>'),
              f'<g clip-path="url(#b{uid})">']
    x = float(PAD)
    for fill, share in card.bar:
        segment = bar_w * share / total
        if fill != 'none':
            parts.append(f'<rect x="{x:.2f}" y="{BAR_Y}" '
                         f'width="{math.ceil(segment)}" height="{BAR_H}" '
                         f'fill="{fill}"/>')
        x += segment
    parts += ['</g>', border(W, H, theme.rule), '</svg>']
    return ''.join(parts)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    built = []
    for source in (github, codewars, leetcode):
        try:
            card = source()
        except Exception as error:
            print(f'{source.__name__} unavailable, card left as it was: {error}')
            continue
        for suffix in THEMES:
            (OUT / f'{card.key}{suffix}.svg').write_text(
                render(card, suffix), encoding='utf-8')
        built.append(f'{card.name}: {card.lede[0]} {card.lede[1]}')
    print('rendered:', ', '.join(built) or 'nothing')
    print('stamp:', datetime.datetime.now(datetime.UTC).date().isoformat())


if __name__ == '__main__':
    main()
