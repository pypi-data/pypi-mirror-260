import copy
import os

from cerebrium import utils
from cerebrium.constants import INTERNAL_FILES
from cerebrium.datatypes import CerebriumConfig, CerebriumDependencies
from cerebrium.utils.logging import cerebrium_log


def update_config_from_files(
    config: CerebriumConfig, warning_message: bool = False, archive_files: bool = False
) -> bool:
    """Update the config object with the contents of the files"""

    has_changed = False
    dependencies = copy.deepcopy(config.dependencies).to_dict()
    if os.path.exists("requirements.txt"):
        utils.requirements.update_from_file(
            "requirements.txt", dependencies, "pip", False
        )

    if os.path.exists("pkglist.txt"):
        utils.requirements.update_from_file("pkglist.txt", dependencies, "apt", False)

    if os.path.exists("conda_pkglist.txt"):
        utils.requirements.update_from_file(
            "conda_pkglist.txt", dependencies, "conda", False
        )

    # update the config file with the new dependencies
    if config.dependencies.to_dict() != dependencies:
        has_changed = True

    if has_changed and warning_message:
        files = [e for e in INTERNAL_FILES if os.path.exists(e)]
        cerebrium_log(
            level="WARNING",
            message=f"The dependencies in your config file have been updated with the contents of the {files} file{'s' if len(files)>1 else ''}.",
        )

    config.dependencies = CerebriumDependencies(
        pip=dependencies.get("pip", {}),
        apt=dependencies.get("apt", {}),
        conda=dependencies.get("conda", {}),
    )

    if archive_files:
        internal_files = [
            "requirements.txt",
            "pkglist.txt",
            "conda_pkglist.txt",
        ]
        for file in internal_files:
            archive_file(file)

    return has_changed


def archive_file(file_name: str):
    if os.path.exists(f"{file_name}.old"):
        os.remove(f"{file_name}.old")
    if os.path.exists(file_name):
        os.rename(file_name, f"{file_name}.old")
