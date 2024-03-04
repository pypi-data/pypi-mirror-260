# from inflection import underscore
from dmtgen.common.package import Blueprint

def to_type_name(name: str):
    """Convert blueprint name to type name"""
     #TODO return underscore(name)+"_t"
    return name

def to_field_name(name: str):
    """Convert attribute name to field name"""
    #TODO: return underscore(name)
    return name

def to_module_name(blueprint: Blueprint):
    """Convert to module name"""
    #TODO return underscore(blueprint.name)+"_mod"
    path=blueprint.get_path().replace("/","_")
    return f"class_{path}"
