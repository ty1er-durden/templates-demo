import os
import jinja2
import jinja2.sandbox

from collections import defaultdict
from platform import system


class Template:
    def __init__(self, template: jinja2.environment.Template = None, **kwargs):
        self.template = template
        self.variables = kwargs

    def render(self, variables: dict = None):
        if variables is None:
            variables = self.variables
        return self.template.render(variables)


class Library(defaultdict):
    def __init__(self, path=None):
        super().__init__(Template)
        # Determine where templates are stored
        self._path = path
        if self._path is None:
            try:
                self._path = os.environ["TEMPLATE_LIBRARY_PATH"]
            except KeyError:
                if system().lower() == "windows":
                    self._path = os.path.join(
                        os.environ["USERPROFILE"], ".templates"
                    )
                else:
                    self._path = os.path.join(os.environ["HOME"], ".templates")
        # Create templates directory if it does not exist
        if not os.path.isdir(self._path):
            os.makedirs(self._path)
        # Jinja2 sandbox
        self._sandbox = jinja2.sandbox.SandboxedEnvironment(
            loader=jinja2.FileSystemLoader(self._path)
        )
        # Load templates
        self.refresh()

    def add(self, name: str, template: str, overwrite: bool = False):
        full_path = os.path.join(self._path, name)
        if not overwrite and (os.path.exists(full_path) or name in self):
            raise ValueError(
                "Specify 'overwrite = True' to replace existing template {n} ({f})".format(
                    n=name, f=full_path
                )
            )
        try:
            Template(template=self._sandbox.from_string(template))
        except Exception as e:
            print("Bad template: {0}".format(e))
        with open(full_path, "w") as f:
            f.write(template)
        self.load_template(name)
        print("Created new template {n} ({f})".format(n=name, f=full_path))

    def load_template(self, name: str):
        self[name] = Template(template=self._sandbox.get_template(name))

    def refresh(self):
        for name in os.listdir(self._path):
            full_path = os.path.join(self._path, name)
            if os.path.isfile(full_path):
                try:
                    self.load_template(name)
                except jinja2.TemplateError as e:
                    if isinstance(e, jinja2.TemplateNotFound):
                        print("Ignored invalid template:".format(e))
                    else:
                        raise

    def remove(self, name: str):
        full_path = os.path.join(self._path, name)
        os.remove(full_path)
        del self[name]
        print("Removed template {n} ({f})".format(n=name, f=full_path))

    def __setitem__(self, key, value):
        if not isinstance(value, Template):
            raise ValueError("Dictionary values must be of type 'Template'")
        super().__setitem__(key, value)


templates = Library()
