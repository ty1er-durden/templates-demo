#!/usr/bin/env python3

from argparse import Action, ArgumentParser
from jinja2 import FileSystemLoader
from jinja2.sandbox import SandboxedEnvironment

import os


class StoreVariables(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        key_value_pairs = dict(
            [value.split("=") for value in values.split(",")]
        )
        setattr(namespace, self.dest, key_value_pairs)


if __name__ == "__main__":

    argparser = ArgumentParser()

    argparser.add_argument(
        "--template", dest="template_file", help="Template file name"
    )
    argparser.add_argument(
        "--output-file",
        dest="output_path",
        help="Full path to export rendered template to",
    )
    argparser.add_argument(
        "--variables",
        required=True,
        dest="variables",
        help="Comma separated list of key-value pairs (e.g. a=1,b=2,...) representing the variables to substitute in to the template",
        action=StoreVariables,
    )

    args = argparser.parse_args()

    sandbox = SandboxedEnvironment(
        loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), "templates")
        )
    )

    template = sandbox.get_template(args.template_file)

    if args.template_file:
        template.stream(variables=args.variables).dump(args.output_path)
    else:
        print(template.render(variables=args.variables))
