#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Code generator for fortran runtime library
'''

from distutils.dir_util import copy_tree
from pathlib import Path
from typing import Dict

from dmtgen import BaseGenerator, TemplateBasedGenerator,NoneGenerator

from .entity_generator import EntityGenerator
from .basic_template_generator import BasicTemplateGenerator


class RuntimeGenerator(BaseGenerator):
    """ Generates a fortran runtime library to access the entities as plain objects """

    # @override
    def get_template_generator(self, template: Path, config: Dict) -> TemplateBasedGenerator:
        """ Override in subclasses """
        if template.name == "types_mod.f90.jinja":
            return EntityGenerator()
        if config.get("simos", False):
            return NoneGenerator()
        return BasicTemplateGenerator()

    def copy_templates(self, template_root: Path, output_dir: Path):
        """Copy template folder to output folder"""
        if self.source_only:
            src_dir = template_root / "src"
            dest_dir = output_dir
            copy_tree(str(src_dir), str(dest_dir))
        else:
            copy_tree(str(template_root), str(output_dir))
