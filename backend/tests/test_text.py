"""Tokenization + normalization (the comparison layer)."""
from app.engine.text import normalize_word, tokenize


def test_strips_diacritics_and_punctuation():
    toks = tokenize("ذَهَبَ، الوَلَدُ!")
    assert [t.norm for t in toks] == ["ذهب", "الولد"]
    assert [t.raw for t in toks] == ["ذَهَبَ،", "الوَلَدُ!"]  # raw is preserved for display


def test_alef_and_maqsura_unified():
    # أ/إ/آ -> ا ; ى -> ي  (so إلى and الي compare equal)
    assert normalize_word("إلى") == normalize_word("الي")
    assert normalize_word("أحمد") == normalize_word("احمد")


def test_taa_marbuta_and_emphatics_preserved():
    # These distinctions ARE reading errors we must keep (Phase 0 finding).
    assert normalize_word("مدرسة") != normalize_word("مدرسه")   # ة vs ه kept distinct
    assert normalize_word("صار") != normalize_word("سار")       # ص vs س kept distinct


def test_pure_punctuation_dropped():
    assert tokenize("؟ ! ،") == []
    assert len(tokenize("القط . نائم")) == 2
