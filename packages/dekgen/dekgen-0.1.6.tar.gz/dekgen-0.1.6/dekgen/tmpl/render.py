import os
from dektools.yaml import yaml
from dektools.dict import dict_merge
from dektools.attr import object_path_update
from dektools.typer import multi_options_to_dict
from .template import TemplateWide


class RenderTemplate(TemplateWide):
    file_ignore_tpl = [f"../{x}" for x in TemplateWide.file_ignore_tpl]
    file_ignore_override = [f"../{x}" for x in TemplateWide.file_ignore_override]
    file_ignore = [f"../{x}" for x in TemplateWide.file_ignore]


def render_dir(dest, src, file_list=None, set_list=None):
    data = {}
    path_values = os.path.join(src, 'values.yaml')
    if os.path.isfile(path_values):
        data = dict(Values=yaml.load(path_values))
    if file_list:
        for f in file_list:
            strict = True
            if f.startswith('?'):
                f = f[1:]
                strict = False
            if not strict and not os.path.isfile(f):
                continue
            dict_merge(data, dict(Values=yaml.load(f)))
    if set_list:
        object_path_update(data, multi_options_to_dict(set_list))
    RenderTemplate(data).render_dir(dest, os.path.join(src, 'templates'))
