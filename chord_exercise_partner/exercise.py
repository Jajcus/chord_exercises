# -*- coding: utf-8 -*-

"""C.E.P. exercise generator."""

import random

from .notes import (SCALES, chord_name, chord_notes, normalize_scale_root,
                    note_name)
from .progressions import get_progression

LEAD_IN = 2 # bars
DEFAULT_LENGTH = 10 # bars

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII"]

class Exercise:
    """An exercise – a scale and chord progression to play."""
    # pylint: disable=too-few-public-methods
    def __init__(self, length=DEFAULT_LENGTH,
                 root=None, mode="major", harmonization="triads",
                 progression=None):
        random.seed()

        self.length = length

        self.mode = mode
        self.harmonization = harmonization

        if root is not None:
            if isinstance(root, str):
                root = root
            elif isinstance(root, int):
                root = note_name(root)
            else:
                raise TypeError("Root must be int or str")
        else:
            root = random.choice(SCALES[mode])

        root = normalize_scale_root(root, mode)
        self.root = root

        self.scale_name = "{}-{}".format(root, mode)

        self.beats_in_bar = 4
        self.beat_duration = 60.0  # 1/bpm units
        self.bar_duration = self.beat_duration * self.beats_in_bar
        self.whole_note_duration = 60.0 * 4.0

        print("The scale is:", self.scale_name)

        if progression:
            self.progression = get_progression(progression, length)
        else:
            self.progression = [random.randint(0, 6) for i in range(length)]

        roman_numbers = [ROMAN[x] for x in self.progression]
        print("The progression is: {}".format(",".join(roman_numbers)))
        self.chord_names = [chord_name(root, x, mode, harmonization)
                            for x in self.progression]
        #print("Which is: {}".format(",".join(self.chord_names)))

    def chord_notes(self, bar):
        """Return chord notes (relative to C note) at given bar."""
        return chord_notes(self.root,
                           self.progression[bar],
                           self.mode,
                           self.harmonization)
