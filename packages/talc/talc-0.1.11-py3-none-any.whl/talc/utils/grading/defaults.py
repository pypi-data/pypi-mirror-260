from talc.grading import GradingSet, GraderConfig, FactualityGraderConfig, FewShotConfig

DEFAULT_FACTUALITY_GRADER_CONFIG = FactualityGraderConfig(
    grader="FactualityGrader",
    config_name="DefaultFactualityGraderConfig",
    description="The default configuration for the factuality grader.",
    few_shot_examples=[
        FewShotConfig(
            question="What command is used to install the Python SDK for modelscope?",
            correct_answer="The Python SDK for modelscope can be installed using `pip install modelscope` command.",
            user_answer="pip install modelscope",
            grade="PASS",
            reason="The user answer specifies the correct command.",
        ),
        FewShotConfig(
            question="What command is used to install the Python SDK for modelscope?",
            correct_answer="The Python SDK for modelscope can be installed using `pip install modelscope` command.",
            user_answer="It's possible to use pip to install modelscope.",
            grade="FAIL",
            reason="The user answer is not specific about the command that needs to be run.",
        ),
    ],
    additional_pass_criteria=[
        "It's ok if the user response includes extra information as long as it does not contradict the reference answer.",
        "If the question is misleading, it's acceptable to respond with the following message: 'I am not able to provide an answer based on the information available to me. Please consult with your manager, Director of Sales Training, or MSL for further assistance.'",
    ],
    additional_fail_criteria=[],
)

DEFAULT_SOURCE_CONTENT_FACTUALITY_GRADER_CONFIG = FactualityGraderConfig(
    grader="SourceContentFactualityGrader",
    config_name="DefaultSourceContentFactualityGraderConfig",
    description="The default configuration for the source content factuality grader.",
    few_shot_examples=[
        FewShotConfig(
            question="What command is used to install the Python SDK for modelscope?",
            correct_answer="The Python SDK for modelscope can be installed using `pip install modelscope` command.",
            user_answer="pip install modelscope",
            grade="PASS",
            reason="The user answer specifies the correct command.",
        ),
        FewShotConfig(
            question="What command is used to install the Python SDK for modelscope?",
            correct_answer="The Python SDK for modelscope can be installed using `pip install modelscope` command.",
            user_answer="It's possible to use pip to install modelscope.",
            grade="FAIL",
            reason="The user answer is not specific about the command that needs to be run.",
        ),
    ],
    additional_pass_criteria=[
        "It's ok if the user response includes extra information as long as it does not contradict the source contents.",
        "If the question is misleading, it's acceptable to respond with the following message: 'I am not able to provide an answer based on the information available to me. Please consult with your manager, Director of Sales Training, or MSL for further assistance.'",
    ],
    additional_fail_criteria=[],
)

DEFAULT_GRADER_CONFIG = [
    DEFAULT_FACTUALITY_GRADER_CONFIG,
    DEFAULT_SOURCE_CONTENT_FACTUALITY_GRADER_CONFIG,
]
