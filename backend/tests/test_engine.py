"""Hand-verified end-to-end error maps, one per behaviour.

Each case states the target, the transcript, and the exact expected outcome a human
graded by reading the two strings.
"""
from app.engine import analyze
from app.engine.errormap import (
    INSERTION,
    OMISSION,
    REPETITION,
    SELF_CORRECTION,
    ST_OMISSION,
    ST_SUBSTITUTION,
    SUBSTITUTION,
)


def test_perfect_read_ignores_diacritics():
    em = analyze("ذهب الولد إلى المدرسة", "ذَهَبَ الوَلَدُ إلى المَدرَسَةِ")
    assert em.accuracy_pct == 100.0
    assert em.correct_words == 4 and em.total_target_words == 4
    assert em.miscues == [] and em.counts == {}


def test_single_substitution():
    # الولد (the boy) misread as الورد (the rose): ل/ر swap, a valid word -> preserved.
    em = analyze("ذهب الولد إلى المدرسة", "ذهب الورد إلى المدرسة")
    assert em.accuracy_pct == 75.0
    assert em.counts == {SUBSTITUTION: 1}
    sub = em.miscues[0]
    assert sub.type == SUBSTITUTION and sub.target_index == 1
    assert sub.target_word == "الولد" and sub.spoken_word == "الورد"
    assert em.words[1].status == ST_SUBSTITUTION and em.words[1].spoken == "الورد"


def test_omission():
    em = analyze("قطتي الصغيرة تحب اللعب", "قطتي الصغيرة تحب")
    assert em.accuracy_pct == 75.0
    assert em.counts == {OMISSION: 1}
    assert em.miscues[0].type == OMISSION and em.miscues[0].target_index == 3
    assert em.words[3].status == ST_OMISSION and em.words[3].spoken is None


def test_insertion_does_not_lower_accuracy():
    # An unrelated extra word; both target words are still read correctly.
    em = analyze("القط نائم", "القط الكبير نائم")
    assert em.accuracy_pct == 100.0
    assert em.counts == {INSERTION: 1}
    assert em.extras[0].type == INSERTION and em.extras[0].word == "الكبير"


def test_repetition():
    em = analyze("البيت كبير", "البيت البيت كبير")
    assert em.accuracy_pct == 100.0          # the word was ultimately read correctly
    assert em.counts == {REPETITION: 1}
    assert em.extras[0].type == REPETITION


def test_self_correction():
    # Child says المزرعة (farm), then corrects to المدرسة (school).
    em = analyze("ذهب إلى المدرسة", "ذهب إلى المزرعة المدرسة")
    assert em.accuracy_pct == 100.0
    assert em.counts == {SELF_CORRECTION: 1}
    assert em.extras[0].type == SELF_CORRECTION
    assert "المدرسة" in em.extras[0].word or em.miscues[0].note  # note records the fix


def test_phase0_faithfulness_scenario():
    # The exact Phase 0 result: real-word subs survive, the emphatic non-word was
    # normalized by Aura back to المدرسة (so the engine sees only 2 substitutions).
    em = analyze("ذهب الولد إلى المدرسة في الصباح",
                 "ذهب الورد إلى المدرسة في المساء")
    assert em.counts == {SUBSTITUTION: 2}
    assert em.accuracy_pct == 66.7            # 4 of 6 correct
    subs = {m.target_word for m in em.miscues}
    assert subs == {"الولد", "الصباح"}


def test_empty_transcript_all_omissions():
    em = analyze("ذهب الولد إلى المدرسة", "")
    assert em.accuracy_pct == 0.0
    assert em.correct_words == 0
    assert em.counts == {OMISSION: 4}
    assert all(w.status == ST_OMISSION for w in em.words)


def test_wpm_and_wcpm_from_duration():
    em = analyze("واحد اثنان ثلاثة اربعة خمسة",
                 "واحد اثنان ثلاثة اربعة خمسة", duration_sec=30.0)
    assert em.wpm == 10.0                      # 5 words / 0.5 min
    assert em.wcpm == 10.0                      # all correct
    assert em.timestamps_available is False
    assert em.hesitations == []


def test_hesitation_detection_from_timestamps():
    ts = [
        {"word": "القط", "start": 0.0, "end": 0.5},
        {"word": "جلس", "start": 2.0, "end": 2.5},   # 1.5s pause before this
        {"word": "هنا", "start": 2.6, "end": 3.0},
    ]
    em = analyze("القط جلس هنا", "القط جلس هنا", word_timestamps=ts)
    assert em.timestamps_available is True
    assert em.duration_sec == 3.0              # derived from timestamps
    assert len(em.hesitations) == 1
    assert em.hesitations[0].before_word == "جلس"
    assert em.hesitations[0].gap_sec == 1.5


def test_error_map_is_json_serializable():
    import json
    em = analyze("ذهب الولد", "ذهب الورد")
    json.dumps(em.to_dict())                   # must not raise
