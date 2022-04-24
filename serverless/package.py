import shutil
import os
from samcli.yamlhelper import yaml_parse
from samcli.commands._utils.options import DEFAULT_BUILD_DIR


def package():
    template_file = "template.yaml"
    template_dict = get_template_data(template_file)
    for resource_logical_id in template_dict.get("Resources", {}).keys():
        path = os.path.join(os.getcwd(), DEFAULT_BUILD_DIR, resource_logical_id)
        shutil.make_archive(
            "artifacts/" + resource_logical_id, format="zip", root_dir=path
        )


def get_template_data(template_file):
    with open(template_file, "r") as handle:
        template_str = handle.read()
    return yaml_parse(template_str)


if __name__ == "__main__":
    package()
