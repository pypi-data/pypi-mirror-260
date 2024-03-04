# FoxDotChord

[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://taconi.codeberg.page/FoxDotChord)
[![status-badge](https://ci.codeberg.org/api/badges/12671/status.svg)](https://ci.codeberg.org/repos/12671)

Chords for use in FoxDot.

## Instalation

Use the package manager you prefer

```bash
pip install git+https://codeberg.org/taconi/FoxDotChord.git

poetry add  git+https://codeberg.org/taconi/FoxDotChord.git
```

## How to use?

```python
from FoxDotChord import PChord

c0 = PChord['C', 'Am7', 'Dm', 'Em']

t0 >> keys(c0.every(3, 'bubble'), dur=PDur(3, 8))

b0 >> sawbass(c0, amp=1, pan=[0, 1, -1, 0])

d0 >> play('x-o({-=}[--])')
```

<!--
## Contribute
-->
