from mbodied.models.rt1.action import RT1Action
from mbodied.models.rt1.agent import RT1Agent
from mbodied.models.octo.action import OctoAction
from mbodied.models.octo.agent import OctoAgent
from mbodied.models.teleop import TeleOpAgent
from mbodied.models.replay import ReplayAgent
from mbodied.models.rtdiffusion.agent import RTDiffusion
from mbodied.spaces.common import EEF_ACTION_SPACE
from mbodied.spaces.common import BASIC_VISION_LANGUAGE_OBSERVATION_SPACE as VLA_SPACE

REGISTRY = {
    "rt1": {
        "agent": RT1Agent,
        "action": RT1Action,
        "variants": ["rt1main", "rt1simreal", "rt1multirobot", "rt1x"]
    },
    "octo": {
        "agent": OctoAgent,
        "action": OctoAction,
        "observation": VLA_SPACE,
        "variants": ["octo-small", "octo-base"]
    },
    "teleop": {
        "agent": TeleOpAgent,
        "action": OctoAction,
        "weight_keys": []
    },
    "replay": {
        "agent": ReplayAgent,
        "action": OctoAction,
        "weight_keys": []
    },
    "rtdiffusion": {
        "agent": RTDiffusion,
        "action": RT1Action,
        "weight_keys": ["rtdiffusion"]
    }
}
