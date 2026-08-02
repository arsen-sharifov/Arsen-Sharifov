SANS = '-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif'

FRAME_CYCLE = ('#3178c6', '#41b883', '#f1e05a', '#e34c26', '#663399',
               '#c6538c', '#00ADD8', '#ff3e00')
FRAME_PERIOD = 24


def esc(s: object) -> str:
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def border(width: float, height: float, rule: str) -> str:
    cycle = ';'.join((*FRAME_CYCLE, FRAME_CYCLE[0]))
    return ('<style>@media (prefers-reduced-motion:reduce)'
            '{.frame{display:none}}</style>'
            f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" '
            f'rx="10" fill="none" stroke="{rule}"/>'
            f'<rect class="frame" x="0.5" y="0.5" width="{width - 1}" '
            f'height="{height - 1}" rx="10" fill="none" '
            f'stroke="{FRAME_CYCLE[0]}" stroke-width="1.5">'
            f'<animate attributeName="stroke" values="{cycle}" '
            f'dur="{FRAME_PERIOD}s" repeatCount="indefinite"/></rect>')
