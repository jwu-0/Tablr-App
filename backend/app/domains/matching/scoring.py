"""Match scoring — pure functions. No database, network, or clock.

This is the IP. Keeping it pure means it can be unit-tested
exhaustively, tuned offline against recorded inputs, and reasoned about
without a running system. Nothing in this module may import SQLAlchemy,
FastAPI, or `app.config`.

Every scorer returns an integer in `MIN_SCORE..MAX_SCORE`.

STUB: each scorer returns `MIN_SCORE`. Slice 5 implements them — see
TABLR_PLAN.md.
"""

from dataclasses import dataclass, field

MIN_SCORE = 0
MAX_SCORE = 100


@dataclass(frozen=True, slots=True)
class MatchInput:
    """Everything scoring may see about one side of a match.

    Deliberately not a database row: the caller projects rows into this,
    so schema churn cannot leak into the scoring model.

    Attributes:
        profile_id: Identifier, carried for traceability only. Never
            score on it.
        age: Years, or None when the profile has no date of birth.
        tag_slugs: Canonical interest tag slugs.
        cuisine_slugs: Canonical cuisine slugs.
        distance_km: Kilometres from a shared reference point, rather
            than raw coordinates — scoring never sees a location.
    """

    profile_id: str
    age: int | None = None
    tag_slugs: frozenset[str] = field(default_factory=frozenset)
    cuisine_slugs: frozenset[str] = field(default_factory=frozenset)
    distance_km: float | None = None


@dataclass(frozen=True, slots=True)
class MatchWeights:
    """How much each signal counts.

    The weights need not sum to 1; `score_pair` normalises by their
    total. Tuning these is the main lever on match quality, so change
    them together with the expected numbers in `scoring_test.py`.
    """

    shared_tags: float = 0.4
    shared_cuisines: float = 0.35
    age_proximity: float = 0.15
    distance: float = 0.10


DEFAULT_WEIGHTS = MatchWeights()


def score_shared_tags(a: MatchInput, b: MatchInput) -> int:
    """Score overlap in interest tags.

    TODO(slice-5): Jaccard overlap, weighting rare tags above common
    ones so "likes food" counts for less than "plays go".
    """
    _ = (a, b)
    return MIN_SCORE


def score_shared_cuisines(a: MatchInput, b: MatchInput) -> int:
    """Score overlap in cuisine preferences.

    TODO(slice-5).
    """
    _ = (a, b)
    return MIN_SCORE


def score_age_proximity(a: MatchInput, b: MatchInput) -> int:
    """Score closeness in age.

    TODO(slice-5). An unknown age must score neutral, not zero —
    otherwise an incomplete profile is silently penalised.
    """
    _ = (a, b)
    return MIN_SCORE


def score_distance(a: MatchInput, b: MatchInput) -> int:
    """Score closeness in space.

    TODO(slice-5). Decay monotonically with distance, and score an
    unknown distance neutral rather than zero.
    """
    _ = (a, b)
    return MIN_SCORE


def score_pair(
    a: MatchInput,
    b: MatchInput,
    weights: MatchWeights = DEFAULT_WEIGHTS,
) -> int:
    """Combine every signal into the number shown as "84% match".

    Returns:
        A weighted average of the individual scorers, clamped to
        `MIN_SCORE..MAX_SCORE`. Returns `MIN_SCORE` when every weight is
        zero, rather than dividing by zero.
    """
    parts = (
        (score_shared_tags(a, b), weights.shared_tags),
        (score_shared_cuisines(a, b), weights.shared_cuisines),
        (score_age_proximity(a, b), weights.age_proximity),
        (score_distance(a, b), weights.distance),
    )
    total_weight = sum(w for _, w in parts)
    if total_weight == 0:
        return MIN_SCORE
    raw = sum(score * w for score, w in parts) / total_weight
    return max(MIN_SCORE, min(MAX_SCORE, round(raw)))
