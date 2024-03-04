import os
import json
from dynaconf import Dynaconf
from dynaconf.utils.boxing import Box
from .file import write_file, read_text, remove_path
from .dict import assign, is_dict


class ObjectCfg:
    def __init__(self, name):
        self.name = name

    @property
    def path(self):
        return os.path.join(os.path.expanduser('~'), f'.{self.name}.json')

    def set(self, data=None):
        if not data:
            remove_path(self.path)
        else:
            write_file(self.path, json.dumps(data))

    def get(self):
        return json.loads(read_text(self.path, default='{}'))

    def update(self, data):
        data = assign(self.get(), data)
        self.set(data)
        return data


class AssignCfg:
    def __init__(self, *objects, prefix=None, dotenv=None):
        self.objects = objects
        self.prefix = prefix
        self.dotenv = dotenv
        self.object_cls = objects[0].__class__

    def generate(self):
        def walk(d, s):
            for k, v in d.items():
                vv = getattr(s, k, empty)
                if isinstance(vv, Box):
                    if is_dict(v):
                        walk(v, vv)
                    else:
                        x = self.object_cls()
                        x.update(vv)
                        d[k] = x
                elif vv is not empty:
                    d[k] = vv

        empty = object()
        options = {}
        if self.prefix:
            options.update(dict(
                envvar_prefix=self.prefix
            ))
        path_dotenv = None
        if self.dotenv:
            path_dotenv = write_file('.env', t=True, s=self.dotenv)
            options.update(dict(
                dotenv_path=path_dotenv
            ))
        settings = Dynaconf(
            **options
        )
        data = assign(*self.objects, cls=self.object_cls)
        walk(data, settings)
        if path_dotenv:
            remove_path(path_dotenv)
        return data
