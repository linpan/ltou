import subprocess
import json
import os
import shutil
from termcolor import cprint, colored
import subprocess
from pathlib import Path
from typing import NoReturn

from termcolor import cprint

CONDITIONAL_MANIFEST = "conditional_files.json"
REPLACE_MANIFEST = "replaceable_files.json"


def delete_resource(resource):
    print(resource)
    if os.path.isfile(resource):
        os.remove(resource)
    elif os.path.isdir(resource):
        shutil.rmtree(resource)


def delete_resource_for_disabled_features() -> NoReturn:
    with open(CONDITIONAL_MANIFEST) as manifest_fd:
        manifest = json.load(manifest_fd)
        for feature_name, feature in manifest.items():
            if feature["enabled"].lower() != "true":
                text = f'{colored("Removing", color="red")} resources for disabled feature ' \
                       f'{colored(feature_name, color="magenta", attrs=["underline"])}...'
                print(text)
                for resource in feature["resources"]:
                    delete_resource(resource)

    delete_resource(CONDITIONAL_MANIFEST)
    cprint("✨ 🍰 ✨cleanup complete!", color="green")


def replace_resource() -> NoReturn:
    print(
        "⭐ Placing {} nicely in your {} ⭐".format(
            colored("resources", color="green"), colored("new project", color="blue")
        )
    )
    with open(REPLACE_MANIFEST) as replace_manifest:
        manifest = json.load(replace_manifest)
        for target, replaces in manifest.items():
            target_path = Path(target)
            print(target_path, replaces)
            delete_resource(target_path)
            for src_file in map(Path, replaces):
                print(src_file, src_file.exists())
                if src_file.exists():
                    shutil.move(src_file, target_path)
    delete_resource(REPLACE_MANIFEST)
    print(
        "Resources are happy to be where {}.".format(
            colored("they are needed the most", color="green", attrs=["underline"])
        )
    )


def init_repo():

    subprocess.run(["git", "init"], stdout=subprocess.PIPE)
    cprint("Git repository initialized.", "green")
    subprocess.run(["git", "add", "."], stdout=subprocess.PIPE)
    cprint("Added files to index.", "green")
    subprocess.run(["poetry", "install", "-n"])
    subprocess.run(["poetry", "run", "pre-commit", "install"])
    cprint("pre-commit installed.", "green")
    subprocess.run(["poetry", "run", "pre-commit", "run", "-a"])
    subprocess.run(["git", "add", "."], stdout=subprocess.PIPE)
    subprocess.run(["git", "commit", "-m", "Initial commit"], stdout=subprocess.PIPE)
    cprint("✨ 🍰 ✨Initiating complete!", color="green")


if __name__ == "__main__":
    delete_resource_for_disabled_features()
    replace_resource()
