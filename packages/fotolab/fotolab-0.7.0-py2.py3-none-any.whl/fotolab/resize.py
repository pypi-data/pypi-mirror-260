# Copyright (C) 2024 Kian-Meng Ang
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""Resize subcommand."""

import argparse
import logging
from pathlib import Path

from PIL import Image

log = logging.getLogger(__name__)


def build_subparser(subparsers) -> None:
    """Build the subparser."""
    resize_parser = subparsers.add_parser("resize", help="resize an image")

    resize_parser.set_defaults(func=run)

    resize_parser.add_argument(
        dest="image_filename",
        help="set the image filename",
        type=str,
        default=None,
        metavar="IMAGE_FILENAME",
    )

    resize_parser.add_argument(
        "-wh",
        "--width",
        dest="width",
        help="set the width of the image (default: '%(default)s')",
        type=int,
        default="600",
        metavar="WIDTH",
    )

    resize_parser.add_argument(
        "-ht",
        "--height",
        dest="height",
        help="set the height of the image (default: '%(default)s')",
        type=int,
        default="277",
        metavar="HEIGHT",
    )


def run(args: argparse.Namespace) -> None:
    """Run resize subcommand.

    Args:
        config (argparse.Namespace): Config from command line arguments

    Returns:
        None
    """
    log.debug(args)

    image_file = Path(args.image_filename)
    original_image = Image.open(args.image_filename)
    resized_image = original_image.copy()
    resized_image = resized_image.resize(
        (args.width, args.height), Image.Resampling.LANCZOS
    )

    if args.overwrite:
        new_filename = image_file.with_name(image_file.name)
    else:
        new_filename = Path(
            args.output_dir,
            image_file.with_name(f"resize_{image_file.name}"),
        )
        new_filename.parent.mkdir(parents=True, exist_ok=True)

    log.info("resizing image: %s", new_filename)
    resized_image.save(new_filename)
