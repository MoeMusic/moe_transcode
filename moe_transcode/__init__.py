"""Transcode plugin."""

import moe
from moe import config

from . import transcode_core
from .transcode_core import *

__all__ = []
__all__.extend(transcode_core.__all__)


@moe.hookimpl
def plugin_registration():
    """Register the core transcode plugin."""
    config.CONFIG.pm.register(transcode_core, "transcode_core")
