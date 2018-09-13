from enum import Enum


class GPIO:
    class Mode(Enum):
        PULL_UP_INPUT_MODE = 0
        INPUT_BINDING_MODE = 1
        PUSH_PULL_OUTPUT_MODE = 2
        PWM_OUTPUT_MODE = 3
        OPEN_DRAIN_OUTPUT_MODE = 4
