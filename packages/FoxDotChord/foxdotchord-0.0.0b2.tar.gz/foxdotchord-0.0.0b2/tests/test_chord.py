import pytest
from FoxDot.lib.Root import Root
from FoxDot.lib.Scale import Scale

from FoxDotChord import Chord


@pytest.mark.parametrize(
    ('root', 'scale', 'chord', 'notes'),
    [
        ('C', 'major', 'C', [0, 2, 4]),
        ('D', 'major', 'C', [-1.5, 0.5, 2.5]),
        ('E', 'major', 'C', [-2.5, -0.5, 1.5]),
        ('F', 'major', 'C', [-3, -1, 1]),
        ('G', 'major', 'C', [-4, -2, 0]),
        ('A', 'major', 'C', [-5.5, -3.5, -1.5]),
        ('B', 'major', 'C', [-6.5, -4.5, -2.5]),
        ('C', 'major', 'D', [1, 3, 5]),
        ('D', 'major', 'D', [-0.5, 1.5, 3.5]),
        ('E', 'major', 'D', [-1.5, 0.5, 2.5]),
        ('F', 'major', 'D', [-2, 0, 2]),
        ('G', 'major', 'D', [-3, -1, 1]),
        ('A', 'major', 'D', [-4.5, -2.5, -0.5]),
        ('B', 'major', 'D', [-5.5, -3.5, -1.5]),
        # ('D', [1, 3.5, 5]),
        # ('E', [2, 4, 6]),
        # ('F', [3, 5, 7]),
        # ('G', [4, 6, 8]),
        # ('A', [5, 7, 9]),
        # ('B', [6, 8, 10]),
    ],
)
def test_chord_major(
    root: str,
    scale: str,
    chord: str,
    notes: list[int],
):
    """Tests chord."""
    Root.default = root
    Scale.default = scale
    assert Chord(chord).notes == notes
