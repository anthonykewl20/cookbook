"""The one authoritative description of a brief's exact field shape.

A brief is what the prep cook (press/prep.py) writes, the printer (press/print.py) reads,
and the taster (press/taste.py) reads beside the page. The producer and every consumer used
to keep their own hand-written copy of the six list-field names, which is the same
two-copies-of-one-promise shape the rest of this shop is built to catch. They all derive
their exact-field validation from here now, so a shape that drifts in one place is refused by
the others rather than silently established.

Import-safe by construction: this module declares only data. It opens no files, touches no
network, and runs nothing at import time, so importing it has no side effects whether the
caller is run directly (``python3 press/prep.py``) or loaded as a module. ``BRIEF_LIST_FIELDS``
is the exact ordered set of the six list-valued fields; ``BRIEF_FIELDS`` is the exact set of
all eight fields a brief must carry.
"""

# The six list-valued fields, in the canonical order prep.py asks the model for them.
BRIEF_LIST_FIELDS = (
    "must_cover",
    "must_not_cover",
    "must_not_contradict",
    "known_holes",
    "traps",
    "hooks",
)

# Every field a brief carries, as an exact set: the two scalars plus the six lists.
BRIEF_FIELDS = ("chapter", "title", *BRIEF_LIST_FIELDS)
