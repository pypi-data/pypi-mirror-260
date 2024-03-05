# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Scipp contributors (https://github.com/scipp)

# flake8: noqa
import importlib.metadata

try:
    __version__ = importlib.metadata.version(__package__ or __name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"

from . import typing
from .base import (
    Group,
    NexusStructureError,
    NXobject,
    base_definitions,
    create_class,
    create_field,
)
from .field import Attrs, Field
from .file import File
from .nexus_classes import *
from .nxtransformations import compute_positions, zip_pixel_offsets
