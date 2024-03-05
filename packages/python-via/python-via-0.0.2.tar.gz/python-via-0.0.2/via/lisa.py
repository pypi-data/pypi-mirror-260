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

"""LISA
"""

import dataclasses
import time
import uuid
from dataclasses import dataclass
from typing import Dict, Tuple, Union

# @dataclass
# class LISACheckboxAttribute:
#     pass


@dataclass
class LISALabelAttribute:
    aname: str


@dataclass
class LISARadioAttribute:
    aname: str  # The displayed string
    options: Dict[str, str]  # Map key to displayed string


@dataclass
class LISASelectAttribute(LISARadioAttribute):
    pass


@dataclass
class LISATextAttribute:
    aname: str  # The displayed string


LISAAttribute = Union[
    # LISACheckboxAttribute,
    LISALabelAttribute,
    LISARadioAttribute,
    LISASelectAttribute,
    LISATextAttribute,
]


# This map is used to fill the atype field when exporting to JSON.
_lisa_attr_type_to_json = {
    # LISACheckboxAttribute: "checkbox",
    LISALabelAttribute: "label",
    LISARadioAttribute: "radio",
    LISASelectAttribute: "select",
    LISATextAttribute: "text",
}


@dataclass
class LISAPoint:
    x: float
    y: float


@dataclass
class LISARect:
    x: float
    y: float
    w: float
    h: float


LISAShape = Union[LISAPoint, LISARect]


class LISA:
    def __init__(self):
        self._project = {
            "created_timestamp": time.time_ns() // 10**6,
            "file_format_version": "0.0.3",
            "project_id": str(uuid.uuid1()),
            "project_name": "",
            "shared_fid": "__FILE_ID__",
            "shared_rev": "__FILE_REV_ID__",
            "shared_rev_timestamp": "__FILE_REV_TIMESTAMP__",
        }
        self._config = {
            "navigation_from": 0,
            "file_src_prefix": "",
            "item_height_in_pixel": 1024,
            "item_per_page": -1,
            "show_attributes": {"file": [], "region": []},
            "navigation_to": 1,
            "float_precision": 4,
        }
        self._files = []
        self._file_attributes: Dict[str, LISAAttribute] = {}
        self._region_attributes: Dict[str, LISAAttribute] = {}
        self._img_key_to_idx: Dict[str, int] = {}
        self._region_key_to_idx: Dict[str, Tuple[str, int]] = {}

    def define_file_attribute(
        self, attr_key: str, attr: LISAAttribute, show=True
    ) -> None:
        if attr_key in self._file_attributes:
            raise ValueError(
                f"A file attribute '{attr_key}' is already defined"
            )
        self._file_attributes[attr_key] = dataclasses.replace(attr)
        if show:
            self._config["show_attributes"]["file"].append(attr_key)

    def define_region_attribute(
        self, attr_key: str, attr: LISAAttribute, show=True
    ) -> None:
        if attr_key in self._region_attributes:
            raise ValueError(
                f"A region attribute '{attr_key}' is already defined"
            )
        self._region_attributes[attr_key] = dataclasses.replace(attr)
        if show:
            self._config["show_attributes"]["region"].append(attr_key)

    # TODO: option to append image with attributes and region
    def append_image(self, img_id: str, fpath: str) -> None:
        """Append an image to the project.

        This method is named `append` and not `add` (see `add-region`)
        because the order of the images matter and this appends.

        """
        if img_id in self._img_key_to_idx:
            raise ValueError()
        self._files.append(
            {
                "fid": img_id,
                "src": fpath,
                "fdata": {},
                "regions": [],
                "rdata": [],
            }
        )
        self._img_key_to_idx[img_id] = len(self._files) - 1

    # TODO: add option to add region with attributes
    def add_region(
        self, img_id: str, region_id: str, shape: LISAShape
    ) -> None:
        """Add a region to an image.

        This method is named `add` and not `append` (see
        `append_image`) because the order of the regions does not
        matter.

        """
        # not append because the order sholdn't mater
        if img_id not in self._img_key_to_idx:
            raise ValueError()
        if region_id in self._region_key_to_idx:
            raise ValueError()

        img = self._files[self._img_key_to_idx[img_id]]
        if isinstance(shape, LISAPoint):
            xshape = [shape.x, shape.y]
        elif isinstance(shape, LISARect):
            xshape = [shape.x, shape.y, shape.w, shape.h]
        else:
            raise TypeError()
        img["regions"].append(xshape)
        img["rdata"].append({})

        self._region_key_to_idx[region_id] = (img_id, len(img["regions"]) - 1)

    def set_image_attribute(
        self, img_id: str, attr_key: str, attr_value: str
    ) -> None:
        # TODO: validate value?
        self._files[self._img_key_to_idx[img_id]]["fdata"][
            attr_key
        ] = attr_value

    def set_region_attribute(
        self, region_id: str, attr_key: str, attr_value: str
    ) -> None:
        if region_id not in self._region_key_to_idx:
            raise ValueError()
        if attr_key not in self._region_attributes:
            raise ValueError()

        img_id, region_idx = self._region_key_to_idx[region_id]
        img = self._files[self._img_key_to_idx[img_id]]
        img["rdata"][region_idx][attr_key] = attr_value

    @property
    def project_name(self) -> str:
        return self._project["project_name"]

    @project_name.setter
    def project_name(self, name: str) -> None:
        self._project["project_name"] = name

    @property
    def image_filepath_prefix(self) -> str:
        return self._config["file_src_prefix"]

    @image_filepath_prefix.setter
    def image_filepath_prefix(self, prefix: str) -> None:
        self._config["file_src_prefix"] = prefix

    @property
    def items_per_page(self) -> int:
        return self._config["item_per_page"]

    @items_per_page.setter
    def items_per_page(self, n: int) -> int:
        self._config["item_per_page"] = n
        self._config["navigation_to"] = self._config["navigation_to"] + n

    @staticmethod
    def json_encoder(py_obj):
        """Return a JSON encodable version of the LISA project.

        This is meant to be used like so:

            json.dump(lisa_project, ..., default=LISA.json_encoder)

        The object returned includes references to the input object
        internals.  `json.dump` should then serialise it in chunks
        avoiding higher memory usage.

        """
        if isinstance(py_obj, LISA):
            # pylint: disable=protected-access
            return {
                "attributes": {
                    "file": py_obj._file_attributes,
                    "region": py_obj._region_attributes,
                },
                "config": py_obj._config,
                "files": py_obj._files,
                "project": py_obj._project,
            }

        elif isinstance(py_obj, LISAAttribute):
            json_obj = {"atype": _lisa_attr_type_to_json[type(py_obj)]}
            json_obj.update(dataclasses.asdict(py_obj))
            return json_obj

        else:
            raise TypeError(
                "Not a LISA object to encode (got a '%s')"
                % type(py_obj).__name__
            )
