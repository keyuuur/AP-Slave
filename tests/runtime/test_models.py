from __future__ import annotations

from copy import deepcopy

import pytest
from pydantic import ValidationError

from ap_slave_runtime.models import ManualPromoEvaluation

from tests.runtime.factories import request_payload


def test_decimal_string_round_trip_is_reproducible() -> None:
    first = ManualPromoEvaluation.model_validate(request_payload())
    serialized = first.model_dump_json()
    second = ManualPromoEvaluation.model_validate_json(serialized)

    assert second.model_dump(mode="json") == first.model_dump(mode="json")
    assert second.promotion.boost_percent.as_tuple() == first.promotion.boost_percent.as_tuple()
    assert second.candidates[0].market_identity.line.as_tuple() == (
        first.candidates[0].market_identity.line.as_tuple()
    )


def test_recommendation_grade_decimal_rejects_binary_float() -> None:
    payload = request_payload()
    payload["promotion"]["boost_percent"] = 30.0

    with pytest.raises(ValidationError, match="decimal"):
        ManualPromoEvaluation.model_validate(payload)


def test_utc_fields_reject_non_utc_offsets() -> None:
    payload = request_payload()
    payload["created_at_utc"] = "2026-07-13T23:00:00-05:00"

    with pytest.raises(ValidationError, match="UTC"):
        ManualPromoEvaluation.model_validate(payload)


@pytest.mark.parametrize(
    "unsupported_shape",
    ["odds_boost", "payout_boost", "bonus_bet", "insured_bet", "parlay_boost", "other"],
)
def test_named_unsupported_promo_shapes_reach_the_engine_contract(
    unsupported_shape: str,
) -> None:
    payload = deepcopy(request_payload())
    payload["promotion"]["boost_type"] = unsupported_shape
    payload["promotion"]["boost_percent"] = None

    parsed = ManualPromoEvaluation.model_validate(payload)

    assert parsed.promotion.boost_type == unsupported_shape
