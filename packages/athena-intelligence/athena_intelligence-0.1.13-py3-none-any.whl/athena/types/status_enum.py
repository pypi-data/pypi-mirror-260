# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class StatusEnum(str, enum.Enum):
    """
    An enumeration.
    """

    PENDING = "pending"
    RESPONDED = "responded"
    ERROR = "error"

    def visit(
        self,
        pending: typing.Callable[[], T_Result],
        responded: typing.Callable[[], T_Result],
        error: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is StatusEnum.PENDING:
            return pending()
        if self is StatusEnum.RESPONDED:
            return responded()
        if self is StatusEnum.ERROR:
            return error()
