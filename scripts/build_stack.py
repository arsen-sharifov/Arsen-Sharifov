import json
import math
import pathlib
import re
from dataclasses import dataclass

from frame import SANS, border, esc

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
ICONS = REPO / 'assets' / 'icons'
OUT = REPO / 'assets' / 'generated'

W = 1000
PAD_X = 16
LABEL_COL = 150
COLS = 8
INK_TARGET, MAX_DIM = 44, 58
ICON_BAND = 58
GRID_X0 = PAD_X + LABEL_COL
CELL = (W - GRID_X0 - PAD_X) / COLS
GRID_X = GRID_X0 + CELL / 2
GROUP_PITCH = 96
ICON_DY = 11
CAPTION_DY = 15
LABEL_DY = ICON_DY + ICON_BAND / 2 + 4
TOP, PAD_BOTTOM = 6, 6

@dataclass(frozen=True)
class Theme:
    label: str
    name: str
    band: str
    rule: str


THEMES = {
    '': Theme(label='#3D444D', name='#5A636D', band='#F3F5F8', rule='#D8DEE4'),
    '-dark': Theme(label='#C9D1D9', name='#98A1AC', band='#161B22',
                   rule='#2D333B'),
}

GROUPS = [
    ('Languages', [
        ('languages-frameworks', 'typescript'), ('languages-frameworks', 'javascript'),
        ('languages-frameworks', 'html5'), ('languages-frameworks', 'css3')]),
    ('Frameworks & state', [
        ('languages-frameworks', 'react'), ('languages-frameworks', 'nextjs'),
        ('languages-frameworks', 'redux'), ('languages-frameworks', 'zustand'),
        ('languages-frameworks', 'react-flow'), ('languages-frameworks', 'dnd-kit'),
        ('languages-frameworks', 'i18n')]),
    ('Styling & UI', [
        ('styling-design', 'sass'), ('styling-design', 'tailwindcss'),
        ('styling-design', 'css-modules'), ('styling-design', 'material-ui'),
        ('styling-design', 'ant-design'), ('styling-design', 'storybook'),
        ('styling-design', 'figma'), ('styling-design', 'photoshop')]),
    ('Testing & quality', [
        ('testing-quality', 'playwright'), ('testing-quality', 'vitest'),
        ('testing-quality', 'jest'), ('testing-quality', 'testing-library'),
        ('testing-quality', 'eslint'), ('testing-quality', 'prettier'),
        ('testing-quality', 'sonarqube'), ('styling-design', 'accessibility')]),
    ('Backend & data', [
        ('backend-data', 'nodejs'), ('backend-data', 'rest'),
        ('backend-data', 'graphql'), ('backend-data', 'websocket'),
        ('backend-data', 'supabase'), ('backend-data', 'postgresql'),
        ('backend-data', 'sql')]),
    ('Build & CI', [
        ('tooling-observability', 'vite'), ('tooling-observability', 'webpack'),
        ('tooling-observability', 'github-actions'),
        ('tooling-observability', 'jenkins')]),
    ('Collaboration', [
        ('tooling-observability', 'git'), ('tooling-observability', 'github'),
        ('tooling-observability', 'gitlab'), ('tooling-observability', 'bitbucket'),
        ('tooling-observability', 'jira')]),
    ('Observability', [
        ('tooling-observability', 'sentry'), ('tooling-observability', 'posthog'),
        ('tooling-observability', 'core-web-vitals')]),
    ('Platforms', [
        ('operating-systems', 'windows'), ('operating-systems', 'macos'),
        ('operating-systems', 'linux')]),
]

LABELS = {
    'typescript': 'TypeScript', 'javascript': 'JavaScript', 'html5': 'HTML5',
    'css3': 'CSS3', 'react': 'React', 'nextjs': 'Next.js', 'redux': 'Redux Toolkit',
    'zustand': 'Zustand', 'react-flow': 'React Flow', 'dnd-kit': 'dnd-kit',
    'i18n': 'i18n', 'sass': 'Sass/SCSS', 'tailwindcss': 'Tailwind CSS',
    'css-modules': 'CSS Modules', 'material-ui': 'Material UI',
    'ant-design': 'Ant Design', 'storybook': 'Storybook', 'figma': 'Figma',
    'photoshop': 'Photoshop', 'accessibility': 'Accessibility',
    'playwright': 'Playwright', 'vitest': 'Vitest',
    'jest': 'Jest', 'testing-library': 'React Testing Library', 'eslint': 'ESLint',
    'prettier': 'Prettier', 'sonarqube': 'SonarQube', 'nodejs': 'Node.js',
    'rest': 'REST', 'graphql': 'GraphQL', 'websocket': 'WebSocket',
    'supabase': 'Supabase', 'postgresql': 'PostgreSQL', 'sql': 'SQL',
    'vite': 'Vite',
    'webpack': 'Webpack', 'git': 'Git', 'github': 'GitHub',
    'github-actions': 'GitHub Actions', 'jenkins': 'Jenkins', 'gitlab': 'GitLab',
    'bitbucket': 'Bitbucket', 'jira': 'Jira',
    'sentry': 'Sentry', 'posthog': 'PostHog', 'core-web-vitals': 'Core Web Vitals',
    'windows': 'Windows', 'macos': 'macOS', 'linux': 'Linux',
}

STRUCTURAL = {'xmlns', 'xmlns:xlink', 'width', 'height', 'viewBox', 'role',
              'aria-label', 'aria-hidden', 'class', 'id', 'version',
              'preserveAspectRatio', 'style'}

INK = json.loads((ROOT / 'ink-bounds.json').read_text(encoding='utf-8'))


def place(path: pathlib.Path, prefix: str, key: str, cx: float, cy: float) -> str:
    svg = path.read_text(encoding='utf-8')
    for old in set(re.findall(r'\bid="([^"]+)"', svg)):
        new = f'{prefix}-{old}'
        svg = (svg.replace(f'id="{old}"', f'id="{new}"')
                  .replace(f'url(#{old})', f'url(#{new})')
                  .replace(f'href="#{old}"', f'href="#{new}"'))
    open_tag = svg[svg.index('<svg'): svg.index('>', svg.index('<svg')) + 1]
    inner = svg[svg.index('>', svg.index('<svg')) + 1: svg.rindex('</svg>')]
    carried = ' '.join(
        f'{k}="{v}"' for k, v in re.findall(r'([\w:-]+)="([^"]*)"', open_tag)
        if k not in STRUCTURAL)

    b = INK[key]
    k = INK_TARGET / math.sqrt(b['w'] * b['h'])
    k = min(k, MAX_DIM / max(b['w'], b['h']))
    tx = cx - (b['x'] + b['w'] / 2) * k
    ty = cy - (b['y'] + b['h'] / 2) * k
    return (f'<g transform="translate({tx:.2f},{ty:.2f}) scale({k:.5f})"'
            + (' ' + carried if carried else '') + f'>{inner}</g>')


def render(suffix: str) -> str:
    theme = THEMES[suffix]
    h = TOP + len(GROUPS) * GROUP_PITCH + PAD_BOTTOM
    alt = '; '.join(f'{g}: ' + ', '.join(LABELS[n] for _, n in items)
                    for g, items in GROUPS)

    uid = suffix or '-light'
    p = [(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
          f'viewBox="0 0 {W} {h}" role="img" aria-label="Stack. {esc(alt)}">'),
         '<title>Stack</title>',
         (f'<clipPath id="clip{uid}"><rect width="{W}" height="{h}" rx="10"/>'
          f'</clipPath>'),
         f'<g clip-path="url(#clip{uid})">']

    for r, (title, items) in enumerate(GROUPS):
        base = TOP + r * GROUP_PITCH
        if r % 2 == 0:
            p.append(f'<rect x="0" y="{base}" width="{W}" height="{GROUP_PITCH}" '
                     f'fill="{theme.band}"/>')
        p.append(f'<text x="{PAD_X}" y="{base + LABEL_DY:.0f}" '
                 f'font-family=\'{SANS}\' '
                 f'font-size="12" font-weight="700" letter-spacing="0.8" '
                 f'fill="{theme.label}">{esc(title.upper())}</text>')
        top = base + ICON_DY
        for c, (folder, fname) in enumerate(items):
            cx = GRID_X + CELL * c
            variant = ICONS / folder / f'{fname}{suffix}.svg'
            src = variant if variant.is_file() else ICONS / folder / f'{fname}.svg'
            ink_key = f'{folder}/{fname}' + (suffix if variant.is_file() else '')
            p.append(place(src, f'{fname}{suffix}', ink_key, cx,
                           top + ICON_BAND / 2))
            p.append(f'<text x="{cx:.1f}" y="{top + ICON_BAND + CAPTION_DY}" '
                     f'text-anchor="middle" font-family=\'{SANS}\' font-size="12" '
                     f'fill="{theme.name}">{esc(LABELS[fname])}</text>')

    p.append('</g>')
    p.append(border(W, h, theme.rule))
    p.append('</svg>')
    return ''.join(p)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for stale in OUT.glob('stack*.svg'):
        stale.unlink()
    for suffix in THEMES:
        (OUT / f'stack{suffix}.svg').write_text(render(suffix), encoding='utf-8')
    n = sum(len(items) for _, items in GROUPS)
    widest = max(len(items) for _, items in GROUPS)
    height = TOP + len(GROUPS) * GROUP_PITCH + PAD_BOTTOM
    print(f'rendered: {n} icons, {len(GROUPS)} groups, '
          f'widest {widest}/{COLS}, {W}x{height}')


if __name__ == '__main__':
    main()
