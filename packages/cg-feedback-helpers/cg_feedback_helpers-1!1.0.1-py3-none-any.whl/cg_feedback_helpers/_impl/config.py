"""Provides the configuration for the implementations of the
:class:`~cg_feedback_helpers._impl.assertions.Asserter` class.
"""

import typing as t
from dataclasses import field, dataclass

from .types import NO_FEEDBACK, Feedback, is_atv2
from .makers import (
    ExistFeedbackMaker, ExpectFeedbackMaker, DefaultExistFeedback,
    DefaultExpectFeedback, ExistFeedbackMakerInput, ExpectFeedbackMakerInput
)
from .writers import Writer, StructuredOutputWriter


def _default_expect_feedback() -> DefaultExpectFeedback:
    def mk_negative(inp: ExpectFeedbackMakerInput) -> Feedback:
        return (
            f'Expected {inp.what} to be {inp.expected}, instead got'
            f' {inp.value}'
        )

    if is_atv2():
        return DefaultExpectFeedback(
            positive=lambda _: NO_FEEDBACK, negative=mk_negative
        )
    return DefaultExpectFeedback(
        positive=lambda inp: f'Got expected {inp.what} {inp.expected}',
        negative=mk_negative,
    )


def _default_not_expect_feedback() -> DefaultExpectFeedback:
    def mk_negative(inp: ExpectFeedbackMakerInput) -> Feedback:
        return f'Expected {inp.what} not to be {inp.expected}'

    if is_atv2():
        return DefaultExpectFeedback(
            positive=lambda _: NO_FEEDBACK, negative=mk_negative
        )
    return DefaultExpectFeedback(
        positive=lambda inp:
        f'Did not get disallowed {inp.what} {inp.expected}',
        negative=mk_negative,
    )


def _default_exist_feedback() -> DefaultExistFeedback:
    def mk_negative(inp: ExistFeedbackMakerInput) -> Feedback:
        return f'Expected {inp.what} {inp.expected} to exist'

    if is_atv2():
        return DefaultExistFeedback(
            positive=lambda _: NO_FEEDBACK, negative=mk_negative
        )
    return DefaultExistFeedback(
        positive=lambda inp: f'Found expected {inp.what} {inp.expected}',
        negative=mk_negative,
    )


def _default_not_exist_feedback() -> DefaultExistFeedback:
    def mk_negative(inp: ExistFeedbackMakerInput) -> Feedback:
        return f'Expected {inp.what} {inp.expected} to not exist'

    if is_atv2():
        return DefaultExistFeedback(
            positive=lambda _: NO_FEEDBACK, negative=mk_negative
        )
    return DefaultExistFeedback(
        positive=lambda inp:
        f'Did not find disallowed {inp.what} {inp.expected}',
        negative=mk_negative,
    )


@dataclass(frozen=True)
class Config:
    """Configuration class used by
    :class:`~cg_feedback_helpers._impl.assertions.Asserter` to determine runtime
    feedback maker functions.

    :param data: The configuration data that can be provided to override
        the default configuration.
    """
    #: The default feedback makers for assertions that compare a value
    #: to another parameter. Used for expectations that should be met.
    expect_feedback: t.Optional[DefaultExpectFeedback] = field(default=None)
    #: The default feedback makers for assertions that compare a value
    #: to another parameter. Used for expectation that should not be met.
    not_expect_feedback: t.Optional[DefaultExpectFeedback] = field(
        default=None
    )
    #: The default feedback makers for assertions that expect something
    #: to exist.
    exist_feedback: t.Optional[DefaultExistFeedback] = field(default=None)
    #: The default feedback makers for assertions that expect something to
    #: not exist.
    not_exist_feedback: t.Optional[DefaultExistFeedback] = field(default=None)

    #: The message to display by default when calling ``emit_success`` on any
    #: :class:`~cg_feedback_helpers._impl.assertions.Asserter` object.
    success_message: str = field(default='Everything was correct! Good job!')

    #: The writer that determines how the output is provided to the user.
    writer: Writer = field(default_factory=StructuredOutputWriter)

    @property
    def is_atv2(self) -> bool:
        """Whether the package is running in ATv2 environment.
        """
        return is_atv2()

    @property
    def expect_feedback_maker(self) -> ExpectFeedbackMaker:
        """A maker object used by 
        :class:`~cg_feedback_helpers._impl.assertions.Asserter` to produce the
        feedback messages for its assertions that expect something to be
        equal, contain, have a property equal to...
        """
        return ExpectFeedbackMaker(
            self.expect_feedback or _default_expect_feedback()
        )

    @property
    def not_expect_feedback_maker(self) -> ExpectFeedbackMaker:
        """A maker object used by 
        :class:`~cg_feedback_helpers._impl.assertions.Asserter` to produce the
        feedback messages for its assertions that expect something to not
        be equal, contain, have a property equal to...
        """
        return ExpectFeedbackMaker(
            self.not_expect_feedback or _default_not_expect_feedback()
        )

    @property
    def exist_feedback_maker(self) -> ExistFeedbackMaker:
        """A maker object used by 
        :class:`~cg_feedback_helpers._impl.assertions.Asserter` to produce the
        feedback messages for its assertions that expect something to
        exist.
        """
        return ExistFeedbackMaker(
            self.exist_feedback or _default_exist_feedback()
        )

    @property
    def not_exist_feedback_maker(self) -> ExistFeedbackMaker:
        """A maker object used by 
        :class:`~cg_feedback_helpers._impl.assertions.Asserter` to produce the
        feedback messages for its assertions that expect something to not
        exist.
        """
        return ExistFeedbackMaker(
            self.not_exist_feedback or _default_not_exist_feedback()
        )
