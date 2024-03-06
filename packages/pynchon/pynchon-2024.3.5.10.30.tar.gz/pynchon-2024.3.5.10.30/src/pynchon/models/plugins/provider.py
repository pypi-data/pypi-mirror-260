""" pynchon.models.plugins.provider """

from fleks import tagging

from . import validators

from pynchon import api, cli, events  # noqa
from pynchon.util import lme, typing  # noqa

from .cli import CliPlugin  # noqa

LOGGER = lme.get_logger(__name__)


@tagging.tags(cli_label="Provider")
class Provider(CliPlugin):
    """ProviderPlugin provides context-information,
    but little other functionality


    """

    cli_label = "Provider"
    contribute_plan_apply = False
    priority = 2
    __class_validators__ = [
        validators.require_conf_key,
        # validators.warn_config_kls,
    ]
