# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Collection of first-party plugins.

This module exists to isolate tensorboard.program from the potentially
heavyweight build dependencies for first-party plugins. This way people
doing custom builds of TensorBoard have the option to only pay for the
dependencies they want.

This module also grants the flexibility to those doing custom builds, to
automatically inherit the centrally-maintained list of standard plugins,
for less repetition.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os

import pkg_resources

from tensorboard.backend import experimental_plugin
from tensorboard.compat import tf
from tensorboard.plugins import base_plugin
from tensorboard.plugins.audio import audio_plugin
from tensorboard.plugins.beholder import beholder_plugin_loader
from tensorboard.plugins.core import core_plugin
from tensorboard.plugins.custom_scalar import custom_scalars_plugin
from tensorboard.plugins.debugger import debugger_plugin_loader
from tensorboard.plugins.debugger_v2 import debugger_v2_plugin
from tensorboard.plugins.distribution import distributions_plugin
from tensorboard.plugins.graph import graphs_plugin
from tensorboard.plugins.histogram import histograms_plugin
from tensorboard.plugins.hparams import hparams_plugin
from tensorboard.plugins.image import images_plugin
from tensorboard.plugins.pr_curve import pr_curves_plugin
from tensorboard.plugins.profile_redirect import profile_redirect_plugin
from tensorboard.plugins.scalar import scalars_plugin
from tensorboard.plugins.text import text_plugin
from tensorboard.plugins.mesh import mesh_plugin
from tensorboard.webapp.plugins.text import text_v2_plugin

logger = logging.getLogger(__name__)


class ExperimentalDebuggerV2Plugin(
    debugger_v2_plugin.DebuggerV2Plugin, experimental_plugin.ExperimentalPlugin
):
    """Debugger v2 plugin marked as experimental."""

    pass


class ExperimentalTextV2Plugin(
    text_v2_plugin.TextV2Plugin, experimental_plugin.ExperimentalPlugin
):
    """Angular Text Plugin marked as experimental."""

    pass


# Ordering matters. The order in which these lines appear determines the
# ordering of tabs in TensorBoard's GUI.
_PLUGINS = [
    core_plugin.CorePluginLoader,
    scalars_plugin.ScalarsPlugin,
    custom_scalars_plugin.CustomScalarsPlugin,
    ExperimentalDebuggerV2Plugin,
    images_plugin.ImagesPlugin,
    audio_plugin.AudioPlugin,
    debugger_plugin_loader.DebuggerPluginLoader,
    graphs_plugin.GraphsPlugin,
    distributions_plugin.DistributionsPlugin,
    histograms_plugin.HistogramsPlugin,
    text_plugin.TextPlugin,
    pr_curves_plugin.PrCurvesPlugin,
    profile_redirect_plugin.ProfileRedirectPluginLoader,
    beholder_plugin_loader.BeholderPluginLoader,
    hparams_plugin.HParamsPlugin,
    mesh_plugin.MeshPlugin,
    ExperimentalTextV2Plugin,
]


def get_plugins():
    """Returns a list specifying TensorBoard's default first-party plugins.

    Plugins are specified in this list either via a TBLoader instance to load the
    plugin, or the TBPlugin class itself which will be loaded using a BasicLoader.

    This list can be passed to the `tensorboard.program.TensorBoard` API.

    Returns:
      The list of default plugins.

    :rtype: list[Type[base_plugin.TBLoader] | Type[base_plugin.TBPlugin]]
    """

    return _PLUGINS[:]


def get_dynamic_plugins():
    """Returns a list specifying TensorBoard's dynamically loaded plugins.

    A dynamic TensorBoard plugin is specified using entry_points [1] and it is
    the robust way to integrate plugins into TensorBoard.

    This list can be passed to the `tensorboard.program.TensorBoard` API.

    Returns:
      The list of dynamic plugins.

    :rtype: list[Type[base_plugin.TBLoader] | Type[base_plugin.TBPlugin]]

    [1]: https://packaging.python.org/specifications/entry-points/
    """
    return [
        entry_point.load()
        for entry_point in pkg_resources.iter_entry_points(
            "tensorboard_plugins"
        )
    ]
