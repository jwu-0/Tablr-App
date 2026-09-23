"""Unit tests for the scoring model.

Named `scoring_test.py` rather than `scoring.test.py`: a dot in a
module name is not importable inside a Python package. It stays
colocated with the code it tests.

These run without a database, a server, or fixtures — that is the whole
point of keeping `scoring.py` pure. Grow this file alongside the real
implementation; every weighting change should show up here as a diff in
expected numbers.
"""

from app.domains.matching.scoring import (
    MAX_SCORE,
    MIN_SCORE,
    MatchInput,
    MatchWeights,
    score_pair,
)


def _profile(
    profile_id: str,
    *,
    age: int | None = None,
    tags: frozenset[str] = frozenset(),
    cuisines: frozenset[str] = frozenset(),
    distance_km: float | None = None,
) -> MatchInput:
    """Build a `MatchInput` with everything defaulted but the id."""
    return MatchInput(
        profile_id=profile_id,
        age=age,
        tag_slugs=tags,
        cuisine_slugs=cuisines,
        distance_km=distance_km,
    )


def test_score_pair_is_within_bounds() -> None:
    a = _profile("a", age=20, tags=frozenset({"ramen"}))
    b = _profile("b", age=21, tags=frozenset({"ramen"}))
    assert MIN_SCORE <= score_pair(a, b) <= MAX_SCORE


def test_score_pair_is_symmetric() -> None:
    a = _profile("a", age=19, tags=frozenset({"tacos", "late-night"}))
    b = _profile("b", age=23, tags=frozenset({"tacos"}))
    assert score_pair(a, b) == score_pair(b, a)


def test_zero_weights_do_not_divide_by_zero() -> None:
    weights = MatchWeights(
        shared_tags=0.0,
        shared_cuisines=0.0,
        age_proximity=0.0,
        distance=0.0,
    )
    assert score_pair(_profile("a"), _profile("b"), weights) == MIN_SCORE


# TODO(slice-5): once the scorers are implemented, assert that
#   - identical profiles score higher than disjoint ones
#   - a missing age scores neutral rather than zero
#   - distance decays monotonically
