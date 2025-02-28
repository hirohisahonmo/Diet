import datetime

from sqlalchemy.orm import validates

from apps.extensions import sql_alchemy
from apps.utils.singleton_logger import SingletonLogger
from apps.utils.validation_helper import ValidationHelper

_logger = SingletonLogger.get_logger()

_MIN_WEIGHT = 0.1
_MAX_WEIGHT = 300.0
_MIN_BODY_FAT = 0.0
_MAX_BODY_FAT = 99.9


class BodyComposition(sql_alchemy.Model):  # type: ignore
    id = sql_alchemy.Column(sql_alchemy.Integer, primary_key=True)
    date = sql_alchemy.Column(sql_alchemy.Date, nullable=False)
    weight = sql_alchemy.Column(sql_alchemy.Float, nullable=False)
    body_fat = sql_alchemy.Column(sql_alchemy.Float, nullable=True)

    user_id = sql_alchemy.Column(
        sql_alchemy.Integer, sql_alchemy.ForeignKey("user.id"), nullable=False
    )

    def __init__(
        self,
        date: datetime.date,
        weight: float,
        body_fat: float | None = None,
        user_id: str | None = None,
    ) -> None:
        self.date = date
        self.weight = weight
        self.body_fat = body_fat
        self.user_id = user_id

    @validates("date")
    def validate_date(
        self, key: str, input_date: datetime.date
    ) -> datetime.date:
        _logger.debug(f"Validating {key}: {key}={input_date}")

        ValidationHelper.validate_not_none(key, input_date)
        ValidationHelper.validate_date(key, input_date)

        _logger.debug(f"Validation passed: {key}={input_date}")
        return input_date

    @validates("weight")
    def validate_weight(self, key: str, weight: float) -> float:
        _logger.debug(f"Validating {key}: {key}={weight}")

        ValidationHelper.validate_not_none(key, weight)
        ValidationHelper.validate_number_range(
            key, weight, _MIN_WEIGHT, _MAX_WEIGHT
        )

        _logger.debug(f"Validation passed: {key}={weight}")
        return weight

    @validates("body_fat")
    def validate_body_fat(self, key: str, body_fat: float) -> float:
        _logger.debug(f"Validating {key}: {key}={body_fat}")

        ValidationHelper.validate_not_none(key, body_fat)
        ValidationHelper.validate_number_range(
            key, body_fat, _MIN_BODY_FAT, _MAX_BODY_FAT
        )

        _logger.debug(f"Validation passed: {key}={body_fat}")
        return body_fat
