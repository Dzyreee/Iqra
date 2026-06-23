"""Edit-distance alignment op sequence (deterministic)."""
from app.engine.align import DEL, INS, MATCH, SUB, align


def kinds(ops):
    return [o.kind for o in ops]


def test_all_match():
    assert kinds(align(["ا", "ب", "ج"], ["ا", "ب", "ج"])) == [MATCH, MATCH, MATCH]


def test_substitution():
    ops = align(["ا", "ب", "ج"], ["ا", "خ", "ج"])
    assert kinds(ops) == [MATCH, SUB, MATCH]
    assert ops[1].t_index == 1 and ops[1].h_index == 1


def test_omission_is_del():
    ops = align(["ا", "ب", "ج"], ["ا", "ج"])
    assert kinds(ops) == [MATCH, DEL, MATCH]
    assert ops[1].t_index == 1 and ops[1].h_index is None


def test_insertion_is_ins():
    ops = align(["ا", "ج"], ["ا", "ب", "ج"])
    assert kinds(ops) == [MATCH, INS, MATCH]
    assert ops[1].t_index is None and ops[1].h_index == 1


def test_empty_hyp_all_del():
    assert kinds(align(["ا", "ب"], [])) == [DEL, DEL]


def test_empty_target_all_ins():
    assert kinds(align([], ["ا", "ب"])) == [INS, INS]
