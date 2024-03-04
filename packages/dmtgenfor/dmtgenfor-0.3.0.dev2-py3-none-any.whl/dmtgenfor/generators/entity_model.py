
from typing import Set

from dmtgen.common.blueprint_attribute import BlueprintAttribute
from dmtgen.common.package import Blueprint, Package
from inflection import humanize
from .hdf5_model import create_hdf5_save,create_hdf5_load,create_save_order
from .common import to_type_name,to_field_name,to_module_name


types = {"number": "real(dp)", "double": "real(dp)", "string": "character(:)", "char": "character",
            "integer": "integer", "short": "short", "boolean": "logical"}

default_values = {"number": "0.0", "boolean": ".false.", "integer": "0"}

def create_model(blueprint: Blueprint, config: dict):
    """Create entity model from blueprint"""
    model = {}
    if config is None:
        config = {}
    name = blueprint.name
    model["name"] = name
    name = blueprint.name
    ftype = to_type_name(name)
    module = to_module_name(blueprint)
    model["name"] = name
    model["type"] = ftype
    model["module"] = module
    model["path"] = blueprint.get_path()
    model["description"] = blueprint.description
    model["file_basename"] = name.lower()
    attributes = []
    model["attributes"]=attributes
    attribute_deps = set()
    has_name = False
    for attribute in blueprint.all_attributes.values():
        attributes.append(__to_attribute_dict(blueprint, attribute, attribute_deps,config))
        if attribute.name == "name":
            has_name = True

    model["has_name"] = has_name
    model["hdf5_save_order"]= create_save_order(blueprint)

    model["dependencies"]= [__create_dependency(dep) for dep in attribute_deps]
    return model


def __create_dependency(dep: Blueprint):
    return {"name": dep.name, "type": to_type_name(dep.name), "module": to_module_name(dep)}

def __to_attribute_dict(blueprint: Blueprint,attribute: BlueprintAttribute, attribute_deps: Set[Blueprint], config: dict):
    if attribute.is_primitive:
        atype = __map(attribute.type, types)
    else:
        pkg: Package = blueprint.parent
        bp = pkg.get_blueprint(attribute.type)
        atype = to_type_name(bp.name)
        attribute_deps.add(bp)

    type_init = __attribute_init(attribute,atype, config)
    if len(attribute.description)==0:
        attribute.description = humanize(attribute.name)

    return {
        "name": attribute.name,
        "fieldname": to_field_name(attribute.name),
        "is_required": not attribute.is_optional,
        "type" : atype,
        "is_primitive" : attribute.is_primitive,
        "save_hdf5": create_hdf5_save(blueprint,attribute),
        "load_hdf5": create_hdf5_load(blueprint,attribute),
        "is_array" : attribute.is_array,
        "type_init" : type_init,
        "has_default_init" : __has_default_init(attribute),
        "is_destroyable" : __is_destroyable(attribute),
        "description" : attribute.description
    }

def __is_destroyable(attribute: BlueprintAttribute):
    # Rules based on SIMOS
    if attribute.is_blueprint:
        return True
    if attribute.is_string:
        return True
    if attribute.is_array:
        return not attribute.is_fixed_array()
    return False

def __has_default_init(attribute: BlueprintAttribute):
    # From SIMOS
    if attribute.is_array:
        return False
    if attribute.is_blueprint:
        return attribute.is_contained and attribute.is_required
    return False

def __attribute_init(attribute: BlueprintAttribute,atype, config: dict):
    field_name = to_field_name(attribute.name)
    if attribute.is_primitive:
        is_string = attribute.is_string
        if is_string:
            if config.get("use_string", False):
                return "type(String), public :: " + field_name
            else:
                return "character(:), allocatable, public :: " + field_name
        else:
            if attribute.is_array:
                dims=attribute.content["dimensions"]
                if "*" in dims:
                    return atype + ", allocatable, public :: " + field_name + "(:)"
                else:
                    return atype + ", dimension(" + dims + "), public :: " + field_name
            else:
                type_init = atype + ", public :: " + field_name
                default = __find_default_value(attribute)
                if default:
                    type_init += " = " + str(default)
            if attribute.is_array:
                type_init += "(:)"
            return type_init
    else:
        if attribute.is_array:

            return "type(" + atype + "), allocatable, public :: " + field_name + "(:)"
        elif attribute.is_optional:
            return "type(" + atype + "), allocatable, public :: " + field_name
        else:
            return "type(" + atype + "), public :: " + field_name

def __map(key, values):
    converted = values[key]
    if not converted:
        raise ValueError("Unkown type " + key)
    return converted

def __find_default_value(attribute: BlueprintAttribute):
    default_value = attribute.get("default")
    if default_value is not None:
        return __convert_default(attribute,default_value)
    return default_value

def __convert_default(attribute: BlueprintAttribute, default_value):
    # converts json value to fortran value
    if isinstance(default_value,str):
        if default_value == '' or default_value == '""':
            return '""'
        elif attribute.is_integer:
            return int(default_value)
        elif attribute.is_number:
            return float(default_value)
        elif attribute.is_boolean:
            conversion = {
                "false": ".false.",
                "true": ".true.",
            }
            return conversion.get(default_value, default_value)
        else:
            return "'" + default_value + "'"
