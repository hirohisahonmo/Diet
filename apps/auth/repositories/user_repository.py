from sqlalchemy.exc import SQLAlchemyError

from apps.auth.models import User
from apps.extensions import sql_alchemy
from apps.utils.custom_logger import CustomLogger

_logger = CustomLogger.get_logger()


class UserRepository:
    @staticmethod
    def save(user: User) -> None:
        _logger.info("Start")

        try:
            sql_alchemy.session.add(user)
            sql_alchemy.session.commit()
        except SQLAlchemyError as e:
            sql_alchemy.session.rollback()
            _logger.error(e, exc_info=True)
            raise

        _logger.info("End")

    @staticmethod
    def find_by_email(email: str) -> User | None:
        _logger.info(f"Start: {email}")

        user: User | None = User.query.filter_by(email=email).first()

        if not user:
            _logger.info(f"End: User not found - {email}")
            return None

        _logger.info(f"End: User found - {email}")
        return user
