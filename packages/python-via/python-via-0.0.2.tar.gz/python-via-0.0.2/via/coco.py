#!/usr/bin/env python3

## Copyright 2024 David Miguel Susano Pinto <pinto@robots.ox.ac.uk>
##
## Licensed under the Apache License, Version 2.0 (the "License"); you
## may not use this file except in compliance with the License.  You
## may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
## implied.  See the License for the specific language governing
## permissions and limitations under the License.

"""Tools to handle COCO data files.

COCO is not a VIA format but ite is very widespread.  See
https://cocodataset.org/#format-data for COCO data format and
https://cocodataset.org/#format-results for COCO results format.

"""


import argparse
import json
import logging
import sys
from typing import List

import via.lisa

_logger = logging.getLogger(__name__)


def is_coco_data(json_obj) -> bool:
    return set(json_obj.keys()) == set(
        ["info", "images", "annotations", "categories", "licenses"]
    )


def main_to_lisa(
    coco_fpath: str,
    *,
    category_type: str,
    items_per_page: int,
    ignore_category: bool,
    filepath_prefix: str,
) -> int:
    """Entry point for the "via.coco to-lisa" program.

    Refer to `python3 -m via.coco to-lisa -h` to description of this
    function arguments.

    """
    with open(coco_fpath) as fh:
        coco = json.load(fh)
    if not is_coco_data(coco):
        logging.error("Not a COCO data file at '%s'", coco_fpath)
        return 1

    lisa = via.lisa.LISA()
    lisa.project_name = coco["info"]["description"]
    lisa.image_filepath_prefix = filepath_prefix

    lisa.define_file_attribute("width", via.lisa.LISALabelAttribute("Width"))
    lisa.define_file_attribute("height", via.lisa.LISALabelAttribute("Height"))

    if not ignore_category:
        attr_lisa_type_to_py_type = {
            "radio": via.lisa.LISARadioAttribute,
            "select": via.lisa.LISASelectAttribute,
        }
        category_attr = attr_lisa_type_to_py_type[category_type](
            aname="Category",
            options={str(x["id"]): x["name"] for x in coco["categories"]},
        )
        lisa.define_region_attribute("category", category_attr)

    for image in coco["images"]:
        img_id = str(image["id"])
        lisa.append_image(img_id, image["file_name"])
        lisa.set_image_attribute(img_id, "width", str(image["width"]))
        lisa.set_image_attribute(img_id, "height", str(image["height"]))

    for annotation in coco["annotations"]:
        img_id = str(annotation["image_id"])
        region_id = str(annotation["id"])
        attr_id = str(annotation["category_id"])

        rect = via.lisa.LISARect(
            x=float(annotation["bbox"][0]),
            y=float(annotation["bbox"][1]),
            w=float(annotation["bbox"][2]),
            h=float(annotation["bbox"][3]),
        )
        lisa.add_region(img_id, region_id, rect)
        if not ignore_category:
            lisa.set_region_attribute(region_id, "category", attr_id)

    if items_per_page < 1:
        lisa.items_per_page = len(coco["images"])
    else:
        lisa.items_per_page = items_per_page

    json.dump(lisa, fp=sys.stdout, default=via.lisa.LISA.json_encoder)
    return 0


def main(argv: List[str]) -> int:
    logging.basicConfig()
    parser = argparse.ArgumentParser(
        prog="via.coco",
        formatter_class=argparse.RawTextHelpFormatter,
        description="Programs to convert between COCO and VIA file formats",
        epilog=(
            "These programs handle only COCO *data* files.  They do not, yet,"
            " handle COCO *results* files (the COCO *results* files only have"
            " the list of detections without the individual image and category"
            " information).\n"
            "\n"
            "These programs only handle COCO files for object detection.  At"
            " least for now."
        ),
    )
    subparsers = parser.add_subparsers(dest="action")

    to_lisa_subparser = subparsers.add_parser(
        "to-lisa",
        help="Convert COCO *data* file into a LISA project",
    )
    to_lisa_subparser.add_argument(
        "--category-type",
        choices=["radio", "select"],
        default="radio",
        help=(
            "Type to display the COCO category in LISA.  'radio' for radio"
            " buttons; 'select' for dropdown list."
        ),
    )
    to_lisa_subparser.add_argument(
        "--items-per-page",
        type=int,
        default=100,
        help=(
            "Number of images to show by default in LISA.  Use a non-positive"
            " number to display all images by default.  This is the 'm'"
            " keyboard shortcut in LISA."
        ),
    )
    to_lisa_subparser.add_argument(
        "--filepath-prefix",
        default="",
        help=(
            "Prefix to the image filepaths.  This is the 'f' keyboard shortcut"
            "in LISA."
        ),
    )
    to_lisa_subparser.add_argument(
        "--ignore-category",
        action="store_true",
        help=(
            "If set, the annotations category is ignored.  Effectively,"
            " this means that it creates a LISA project with only the"
            " regions/bboxes."
        ),
    )
    to_lisa_subparser.add_argument(
        "coco_project", help="Filepath for the COCO data file."
    )

    args = parser.parse_args(argv[1:])
    if args.action == "to-lisa":
        return main_to_lisa(
            args.coco_project,
            category_type=args.category_type,
            items_per_page=args.items_per_page,
            ignore_category=args.ignore_category,
            filepath_prefix=args.filepath_prefix,
        )
    else:
        # We should not get here because `parse_args` should error on
        # unknown actions.
        raise Exception(f"Unknown action {args.action}")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
