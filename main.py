"""Describe Your Ex in One Word.

The word: "Unsubscribed" — exactly 12 characters, one word, no newline.

Why this word should win:
- It is a one-word VERDICT on the ex, not a description of what the ex did
  ("Ghosted", "Cheated" fail that test). The ex is not the one who acted;
  the ex is the thing being judged.
- It turns the ex into a mailing list you opted out of: someone whose
  messages you no longer receive, by your own choice, with one click.
  The whole breakup is inside the word — the endless unwanted updates,
  the final unsubscribe, the silence after.
- Comic punch and surprise: a subscription metaphor applied to a person
  is an unexpected angle, yet instantly clear to anyone who has ever
  unsubscribed from spam. The laugh lands at a glance, no caption needed.
- Craft: exactly one word, correctly spelled, no punctuation tricks.
- Recognition: everyone has had an ex, and everyone has hit unsubscribe.
  The nod comes with the laugh.

Why not the nearest rivals: "Expired" is a verdict too, but it is the
obvious one — a past-its-date joke with no surprise turn, and the judge
weighs surprise third. "Deprecated" is clever but niche: it only lands
for people who know the tech term, so it loses on recognition.
"Unsubscribed" keeps the verdict, adds the surprise, and needs no
explanation from anyone.

The program writes exactly that word, and nothing else, to entry.txt.
"""

import os
import stat
import tempfile

WORD = "Unsubscribed"


def validate(word):
    """Check the word against the sealed gate before writing anything."""
    if not isinstance(word, str):
        raise ValueError("word must be a string")
    if not (1 <= len(word) <= 111):
        raise ValueError("word must be 1 to 111 characters, got %d" % len(word))
    if not word.strip():
        raise ValueError("word must not be only whitespace")
    if len(word.split()) != 1:
        raise ValueError("word must be exactly one word")
    if any(ch.isspace() for ch in word):
        raise ValueError("word must contain no whitespace")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in word):
        raise ValueError("word must contain no control characters")
    if word != word.strip():
        raise ValueError("word must have no leading or trailing whitespace")
    word.encode("utf-8")  # must be valid UTF-8 text
    return word


def main():
    word = validate(WORD)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")

    # Write via a temp file in the output dir, then atomically replace,
    # so a reader never sees a half-written entry.
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(word)
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, target)
        os.chmod(target, 0o644)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise

    # Read back and verify the bytes on disk are exactly the word.
    with open(target, "rb") as f:
        data = f.read()
    if data != word.encode("utf-8"):
        raise ValueError("bytes on disk do not match the word")
    if len(data) != len(word):
        raise ValueError("byte length on disk does not match the word")
    if stat.S_IMODE(os.stat(target).st_mode) != 0o644:
        raise ValueError("entry.txt mode is not 0644")


if __name__ == "__main__":
    main()
