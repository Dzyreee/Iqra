"""Reference-checked tests for the faraid calculator.

Each expected dict maps heir -> total class fraction. Values are taken from standard
faraid tables. Every test also asserts the shares sum to exactly 1 (except the
spouse-only bayt al-mal edge case).
"""
from fractions import Fraction as F

import pytest

from app.faraid import Heirs, compute_inheritance


def shares_map(dist):
    return {s.heir: s.fraction for s in dist.shares}


# (id, Heirs, expected {heir: fraction}, expected kind)
CASES = [
    # --- simple fixed shares + agnatic residue ---
    ("wife+son", Heirs(wives=1, sons=1), {"wife": F(1, 8), "son": F(7, 8)}, "normal"),
    ("husband+son+daughter", Heirs(husband=True, sons=1, daughters=1),
     {"husband": F(1, 4), "son": F(1, 2), "daughter": F(1, 4)}, "normal"),
    ("mother+son", Heirs(mother=True, sons=1), {"mother": F(1, 6), "son": F(5, 6)}, "normal"),
    ("2wives+son", Heirs(wives=2, sons=1), {"wife": F(1, 8), "son": F(7, 8)}, "normal"),

    # --- daughters as Quranic sharers (no son) + father as agnate ---
    ("daughter+mother+father", Heirs(daughters=1, mother=True, father=True),
     {"daughter": F(1, 2), "mother": F(1, 6), "father": F(1, 3)}, "normal"),
    ("2daughters+father+mother", Heirs(daughters=2, father=True, mother=True),
     {"daughter": F(2, 3), "father": F(1, 6), "mother": F(1, 6)}, "normal"),
    ("father+mother", Heirs(father=True, mother=True),
     {"father": F(2, 3), "mother": F(1, 3)}, "normal"),
    ("father_only", Heirs(father=True), {"father": F(1)}, "normal"),

    # --- Umariyyatan / Gharrawayn (spouse + mother + father, no descendants) ---
    ("husband+father+mother", Heirs(husband=True, father=True, mother=True),
     {"husband": F(1, 2), "mother": F(1, 6), "father": F(1, 3)}, "normal"),
    ("wife+father+mother", Heirs(wives=1, father=True, mother=True),
     {"wife": F(1, 4), "mother": F(1, 4), "father": F(1, 2)}, "normal"),

    # --- 'AWL (fixed shares exceed unity) ---
    # husband 1/4 + 2 daughters 2/3 + mother 1/6 = 13/12 -> 'awl to /13
    ("awl_husband+2daughters+mother", Heirs(husband=True, daughters=2, mother=True),
     {"husband": F(3, 13), "daughter": F(8, 13), "mother": F(2, 13)}, "awl"),
    # wife 1/8 + 2 daughters 2/3 + father 1/6 + mother 1/6 = 27/24 -> 'awl to /27
    ("awl_wife+2daughters+father+mother",
     Heirs(wives=1, daughters=2, father=True, mother=True),
     {"wife": F(3, 27), "daughter": F(16, 27), "father": F(4, 27), "mother": F(4, 27)}, "awl"),

    # --- RADD (surplus, no agnate; spouse excluded from radd) ---
    ("radd_mother+daughter", Heirs(mother=True, daughters=1),
     {"daughter": F(3, 4), "mother": F(1, 4)}, "radd"),
    ("radd_wife+daughter", Heirs(wives=1, daughters=1),
     {"wife": F(1, 8), "daughter": F(7, 8)}, "radd"),
    ("radd_daughter_only", Heirs(daughters=1), {"daughter": F(1)}, "radd"),
    ("radd_mother_only", Heirs(mother=True), {"mother": F(1)}, "radd"),
]


@pytest.mark.parametrize("name,heirs,expected,kind", CASES, ids=[c[0] for c in CASES])
def test_reference_cases(name, heirs, expected, kind):
    dist = compute_inheritance(heirs)
    assert shares_map(dist) == expected, dist.render()
    assert dist.kind == kind
    assert dist.total() == F(1)


def test_husband_only_goes_to_bayt_al_mal():
    dist = compute_inheritance(Heirs(husband=True))
    assert shares_map(dist) == {"husband": F(1, 2)}
    assert "bayt al-mal" in (dist.note or "")
    assert dist.total() == F(1, 2)  # remainder is not distributed


def test_per_individual_split_2to1():
    dist = compute_inheritance(Heirs(sons=2, daughters=1))  # residue 1 split 2:2:1
    by = {s.heir: s for s in dist.shares}
    assert by["son"].each == F(2, 5)
    assert by["daughter"].each == F(1, 5)
    assert dist.total() == F(1)


def test_multiple_wives_split_equally():
    dist = compute_inheritance(Heirs(wives=4, sons=1))
    wife = next(s for s in dist.shares if s.heir == "wife")
    assert wife.fraction == F(1, 8)
    assert wife.each == F(1, 32)


def test_display_base_is_common_denominator():
    dist = compute_inheritance(Heirs(husband=True, sons=1, daughters=1))
    assert dist.base == 4
    ratios = {s.heir: s.as_ratio(dist.base) for s in dist.shares}
    assert ratios == {"husband": "1/4", "son": "2/4", "daughter": "1/4"}


@pytest.mark.parametrize("bad", [
    Heirs(),                       # no heirs
    Heirs(husband=True, wives=1),  # both spouses
    Heirs(wives=5),                # too many wives
    Heirs(sons=-1),                # negative
])
def test_validation_errors(bad):
    with pytest.raises(ValueError):
        compute_inheritance(bad)
