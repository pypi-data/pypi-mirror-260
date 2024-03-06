from pydantic import BaseModel, ConfigDict, Extra, SerializeAsAny


class TestCaseResponse(BaseModel):
    """Represents the results of running a single test case."""

    id: str
    response: str


class GraderConfig(BaseModel):
    """The basic configuration used to run a grader. Most graders will have additional configuration options derived from this class."""

    grader: str
    config_name: str
    description: str

    model_config = ConfigDict(
        extra="allow",
    )


class FewShotConfig(BaseModel):
    question: str
    correct_answer: str
    user_answer: str
    grade: str
    reason: str


class FactualityGraderConfig(GraderConfig):
    """Configuration for the factuality grader."""

    few_shot_examples: list[FewShotConfig]
    additional_pass_criteria: list[str]
    additional_fail_criteria: list[str]


class GradingSet(BaseModel):
    """Represents a set of test cases that should be graded, and the methods for grading them."""

    responses: list[TestCaseResponse]
    grader_configs: list[SerializeAsAny[GraderConfig]]
