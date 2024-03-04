""" " A basic SIMOS Attribute"""
from __future__ import annotations
from typing import Dict
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .blueprint import Blueprint

class BlueprintAttribute:
    """ " A basic SIMOS Attribute"""

    def __init__(self, content: Dict, parent_blueprint: Blueprint) -> None:
        self.content = content
        name = content["name"]
        if len(name)==0:
            raise ValueError("Attribute has no name")
        self.name = name
        if "description" not in content:
            content["description"] = ""
        self.description = content["description"].replace('"',"'")
        dims=content.get("dimensions")
        if dims:
            self.dimensions = dims.split(",")
        else:
            self.dimensions = []

        atype = content["attributeType"]
        self.parent = parent_blueprint
        package = parent_blueprint.parent
        self.type = package.resolve_type(atype)
        self.is_primitive = atype in ['boolean', 'number', 'string', 'integer']
        self.is_enum = self.content.get("enumType",None) is not None
        self.is_blueprint = not (self.is_primitive or self.is_enum)
        self.is_optional = self.content.get("optional",True)
        self.is_array = len(self.dimensions)>0
        self.is_contained = content.get("contained",True)

    @property
    def is_string(self) -> bool:
        """Is this a string"""
        return self.type == "string"

    @property
    def is_boolean(self) -> bool:
        """Is this a boolean"""
        return self.type == "boolean"

    @property
    def is_integer(self) -> bool:
        """Is this an integer"""
        return self.type == "integer"

    @property
    def is_number(self) -> bool:
        """Is this a number"""
        return self.type == "number"

    @property
    def is_required(self) -> bool:
        """Is a required relation"""
        return not self.is_optional

    def is_fixed_array(self) -> bool:
        """Is this a fixed array"""
        return self.is_array and "*" not in self.dimensions

    def is_variable_array(self) -> bool:
        """Is this a variable array"""
        return self.is_array and "*" in self.dimensions

    def get(self, key, default=None):
        """Return the content value or an optional default"""
        return self.content.get(key,default)

    def as_dict(self) -> Dict:
        """Return the attribute as a dictionary"""
        return dict(self.content)
