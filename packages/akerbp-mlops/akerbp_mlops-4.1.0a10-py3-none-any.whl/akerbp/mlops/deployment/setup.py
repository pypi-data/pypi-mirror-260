# setup.py
import re
from copy import deepcopy
from pathlib import Path

from akerbp.mlops import __version__ as version
from akerbp.mlops.core.config import (
    generate_default_project_settings,
    validate_user_settings,
)
from akerbp.mlops.core.logger import get_logger
from akerbp.mlops.deployment.helpers import replace_string_file, to_folder

logger = get_logger(__name__)


def update_mlops_version_in_pipeline(pipeline_filepath) -> None:
    """Update MLOps settings by overwriting the package version number.
    First, it will go through the pipeline definition and remove any quoatation mark prefix to akerbp.mlops
    (to make it robust against updating from previous versions),
    before it will replace the version number with whatever version the caller has on his/her local machine.

    Args:
        folder_path (Path, optional): Path to folder containing the pipeline file. Defaults to Path(".").
    """
    pattern_package = re.compile(r"mlops_version: \d+\.\d+\.\d+(?:(a|-alpha\.)\d+)?")
    replacement_version = f"Version {version}"
    pattern_version = re.compile(r"Version \S{5,}")
    with pipeline_filepath.open() as f:
        pipeline = f.read()
        new_pipeline = re.sub(
            pattern_version,
            replacement_version,
            re.sub(
                pattern_package,
                f"mlops_version: {version}",
                pipeline,
            ),
        )
    with pipeline_filepath.open("w") as f:
        f.write(new_pipeline)
    if new_pipeline == pipeline:
        logger.warning("No changes to the MLOps version were made in the pipeline file")
    else:
        logger.info("MLOps version successfully updated in pipeline file")


def remove_references_to_old_bash_script(pipeline_filepath) -> None:
    """Remove references to the old bash script in the pipeline file

    Args:
        folder_path (Path, optional): Path to folder containing the pipeline file. Defaults to Path(".").
    """
    replacement_pattern = re.compile("bash deploy_.+.sh")
    with pipeline_filepath.open() as f:
        pipeline = f.read()
        matches = list(re.finditer(replacement_pattern, pipeline))
        if matches:
            new_pipeline = deepcopy(pipeline)
            for match in matches:
                logger.info(f"Removing reference to old bash script {match}")
                match_string = match.group()
                script_name = (
                    match_string.replace("bash", "").replace(".sh", "").strip()
                )
                new_pipeline = new_pipeline.replace(match_string, script_name)
            with pipeline_filepath.open("w") as f:
                f.write(new_pipeline)
            logger.info(
                "References to old bash script successfully removed from pipeline file"
            )
        else:
            logger.info("No references to old bash scripts found")


def generate_pipeline(pipeline_path: Path) -> None:
    """Generate pipeline definition from template

    Args:
        folder_path (Path, optional): Path to folder that should contain the pipeline file. Defaults to Path(".").
    """
    python_version = input(
        "Which python version should be used for the deployment (3.9, 3.10, 3.11, 3.12)?: "
    ).strip()
    pipeline_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Moving main pipeline definition file to {pipeline_path.parent}")
    to_folder(("akerbp.mlops.deployment", "main.yml"), pipeline_path.parent)
    logger.info(
        f"Moving helper action definition files to {pipeline_path.parent.parent}"
    )
    to_folder(("akerbp.mlops.deployment", "actions"), pipeline_path.parent.parent)
    replace_string_file("MLOPS_VERSION_GOES_HERE", version, pipeline_path)
    replace_string_file(
        "PYTHON_VERSION_GOES_HERE",
        python_version,
        pipeline_path.parent.parent
        / "actions/deploy-prediction-service-action/action.yml",
    )
    logger.info("Pipeline definition generated")


def setup_pipeline(folder_path: Path) -> None:
    """
    Set up pipeline file in the given folder.
    Update MLOps package version in the pipeline file if it exists, or generate from template if it doesn't.

    Args:
        folder_path (Path, optional): Path to folder that should contain the pipeline file. Defaults to Path(".").
    """
    pipeline_path = folder_path.resolve() / ".github" / "workflows" / "main.yml"
    if pipeline_path.exists():
        logger.info(f"Update MLOps version in pipeline definition to {version}")
        update_mlops_version_in_pipeline(pipeline_path)
        remove_references_to_old_bash_script(pipeline_path)
    else:
        logger.info(
            "No existing deployment workflow found. Generating pipeline definition from template"
        )
        generate_pipeline(pipeline_path)


if __name__ == "__main__":
    logger = get_logger(name="akerbp.mlops.deployment.setup.py")

    default_path = Path("mlops_settings.yaml").resolve()
    if default_path.exists():
        logger.info("Validate settings file")
        validate_user_settings(default_path)
    else:
        logger.info("Create settings file template")
        generate_default_project_settings(default_path, n_models=1)
    setup_pipeline(default_path.parent)
    logger.info("Done!")
