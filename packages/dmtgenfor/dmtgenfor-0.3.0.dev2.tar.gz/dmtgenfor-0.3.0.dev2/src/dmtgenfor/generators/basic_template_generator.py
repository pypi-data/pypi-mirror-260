"""Basic generator, one template, one output file"""

import codecs
from pathlib import Path
from typing import Dict
from dmtgen import TemplateBasedGenerator
from dmtgen.package_generator import PackageGenerator
from dmtgen.common.package import Package
from dmtgen.common.blueprint_attribute import BlueprintAttribute
from inflection import underscore,humanize
from .graph import Graph
class BasicTemplateGenerator(TemplateBasedGenerator):
    """Basic generator, one template, one output file"""

    types = {"number": "real(dp)", "double": "real(dp)", "string": "character(:)", "char": "character",
            "integer": "integer", "short": "short", "boolean": "logical"}

    default_values = {"number": "0.0", "boolean": ".false.", "integer": "0"}

    def generate(self, package_generator: PackageGenerator, template, outputfile: Path, config: Dict):
        """Basic generator, one template, one output file"""
        model = {}
        package_name = package_generator.package_name
        model["package_name"] = package_name
        model["lib_name"] = config.get("lib_name",f'{package_name}-for')
        model["description"] = package_name + " - Generated types"
        model["version"] = config.get("version","0.0.0")
        etypes = {}

        pkg: Package = package_generator.root_package

        dependencies = {}

        for blueprint in pkg.blueprints:
            etype = {}
            name = blueprint.name
            ftype = underscore(name)+"_t"
            etype["name"] = name
            etype["type"] = ftype
            etype["path"] = blueprint.get_path()
            etype["description"] = blueprint.description
            etype["file_basename"] = name.lower()
            attributes = []
            etype["attributes"]=attributes
            attribute_deps = set()
            for attribute in blueprint.all_attributes.values():
                attributes.append(self.__to_attribute_dict(attribute, pkg, attribute_deps))
            dependencies[name]=attribute_deps
            etypes[name]=etype

        model["types"] = self.__sort(etypes, dependencies)

        with codecs.open(outputfile, "w", "utf-8") as file:
            file.write(template.render(model))

    def __to_attribute_dict(self,attribute: BlueprintAttribute, pkg: Package, attribute_deps):
        fieldname =underscore(attribute.name)

        if attribute.is_primitive:
            atype = self.__map(attribute.type, self.types)
            # integer :: index
            # character(:), allocatable :: name
            allocatable = attribute.is_array or attribute.is_string()
            if allocatable:
                type_init = atype + ", allocatable :: " + fieldname
            else:
                type_init = atype + " :: " + fieldname
                default = self.__find_default_value(attribute)
                if default:
                    type_init += " = " + str(default)
            if attribute.is_array:
                type_init += "(:)"
        else:
            bp=pkg.get_blueprint(attribute.type)
            attribute_deps.add(bp.name)
            atype = underscore(bp.name)+"_t"
            if attribute.is_array:
                type_init = "type(" + atype + "), allocatable :: " + fieldname + "(:)"
            elif attribute.optional:
                type_init = "type(" + atype + "), allocatable :: " + fieldname
            else:
                type_init = "type(" + atype + ") :: " + fieldname

        if len(attribute.description)==0:
            attribute.description = humanize(attribute.name)

        return {
            "name": attribute.name,
            "fieldname": fieldname,
            "is_required": not attribute.optional,
            "type" : atype,
            "is_primitive" : attribute.is_primitive,
            "is_array" : attribute.is_array,
            "type_init" : type_init,
            "description" : attribute.description
        }

    def __sort(self, etypes, dependencies):
        vertices = [x["name"] for x in etypes.values()]
        graph = Graph(vertices)
        for etype in etypes.values():
            name = etype["name"]
            for dep in dependencies[name]:
                graph.addEdge(dep,name)
        sorted_types = list()
        sorted_names = graph.sort()
        for name in sorted_names:
            sorted_types.append(etypes[name])
        return sorted_types

    def __map(self, key, values):
        converted = values[key]
        if not converted:
            raise Exception("Unkown type " + key)
        return converted

    def __find_default_value(self, attribute: BlueprintAttribute):
        default_value = attribute.get("default")
        if default_value is not None:
            return self.__convert_default(attribute,default_value)
        return default_value

    def __convert_default(self,attribute: BlueprintAttribute, default_value):
        # converts json value to fortran value
        if isinstance(default_value,str):
            if default_value == '' or default_value == '""':
                return '""'
            elif attribute.type == 'integer':
                return int(default_value)
            elif attribute.type == 'number':
                return float(default_value)
            elif attribute.type == 'boolean':
                conversion = {
                    "false": ".false.",
                    "true": ".true.",
                }
                return conversion.get(default_value, default_value)
            else:
                return "'" + default_value + "'"

    @staticmethod
    def first_to_upper(string):
        """ Make sure the first letter is uppercase """
        return string[:1].upper() + string[1:]
