# Third-party notices

All icon artwork is vendored into `assets/icons`, `assets/ui` and
`scripts/logos`, and the same artwork is embedded in the composed panel and
rendered cards under `assets/generated`, so these terms cover those too.
Nothing is hot-linked, so no external host can break the page.

| Count | Source | Licence | Changed here |
| --- | --- | --- | --- |
| 35 | [devicon](https://github.com/devicons/devicon) | MIT | nothing |
| 6 | [Octicons](https://github.com/primer/octicons) | MIT | wrapped in one `<g transform>`, paths untouched |
| 3 | [simple-icons](https://github.com/simple-icons/simple-icons) | CC0-1.0 | root `fill` added, since upstream ships them colourless |
| 3 | [simple-icons](https://github.com/simple-icons/simple-icons) service marks in `scripts/logos` | CC0-1.0 | fill stripped, repainted in the card ink at render time |
| 3 | React Flow, PostHog, Sentry, from each project's own repository | trademark | Sentry given its brand `#362D59` |
| 8 | drawn for this profile | original work, no grant | n/a |

Path data is never altered. Six marks additionally ship a `-dark.svg` twin for
GitHub's dark theme that differs from its light original in colour only.

Rounding path coordinates has silently broken several of these files before, so
do not put this artwork through an SVG minifier.

## devicon

```
The MIT License (MIT)

Copyright (c) 2015 konpa

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

## Octicons

```
MIT License

Copyright (c) 2026 GitHub Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Octicons applies MIT to all files other than GitHub's own logos, which follow
[GitHub's logo guidelines](https://github.com/logos). The six glyphs used here
are general-purpose marks, not GitHub brand logos.

## simple-icons and trademarks

CC0-1.0 is a public domain dedication and requires no attribution, so it is
recorded here for provenance rather than obligation. It does not waive
trademark. All product names, logos and brands remain the property of their
respective owners; they appear here to identify the technologies, which does not
imply endorsement, and the dark variants are not official brand assets.
