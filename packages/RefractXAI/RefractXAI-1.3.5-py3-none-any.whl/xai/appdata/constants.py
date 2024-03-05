from typing import Final
class ProblemType:
    BINARY_CLASSIFICATION: Final = 'Binary Classification'
    MULTICLASS_CLASSIFICATION: Final = 'Multiclass Classification'
    MULTI_LABEL_CLASSIFICATION: Final = 'Multilabel Classification'
    REGRESSION: Final = 'Regression'

class Log:
    file_name = "logs/refract-explainer.log"
    file_size = 20000000
    backup_count = 10
    logger_level = 60
    interal_logger_level = 60
