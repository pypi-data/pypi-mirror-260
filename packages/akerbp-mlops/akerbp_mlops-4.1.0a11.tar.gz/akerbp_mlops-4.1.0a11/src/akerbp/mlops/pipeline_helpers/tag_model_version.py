import argparse
import logging
import os
import subprocess

import akerbp.mlops.model_manager as mm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--model_name",
        type=str,
        help="Name of model. If not provided, it will be inferred from the mlops_settings.yaml file.",
        default="",
        required=False,
    )
    args = parser.parse_args()
    model_name = args.model_name
    if not model_name:
        from akerbp.mlops.core.config import read_project_settings

        model_names = [s.model_name for s in read_project_settings()]
    else:
        model_names = [model_name]

    logging.disable()
    mm.setup()
    env = os.environ.get("MODEL_ENV")
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], text=True, stderr=subprocess.STDOUT
        ).strip()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error getting commit hash to tag: {e}") from e

    for model_name in model_names:
        try:
            latest_deployed_model = (
                mm.get_model_version_overview(
                    model_name=model_name,
                    env=env,
                    output_logs=False,
                )
                .sort_values(by="uploaded_time", ascending=False)
                .iloc[0]
            )
            version_number = latest_deployed_model.external_id.split("/")[-1]
        except IndexError as e:
            raise Exception(
                f"No version of model {model_name} found in the model registry"
            ) from e

        tag = f"v{version_number}_{model_name}_{env}"
        # Delete tag if it exists
        try:
            subprocess.run(
                ["git", "tag", "-d", tag],
                check=True,
                text=True,
                stderr=subprocess.STDOUT,
            )
            subprocess.run(
                ["git", "push", "origin", f":refs/tags/{tag}"],
                check=True,
                text=True,
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as e:
            logging.warning(f"Error deleting tag: {e}")

        # Create tag
        try:
            subprocess.run(
                ["git", "tag", tag, commit],
                check=True,
                text=True,
                stderr=subprocess.STDOUT,
            )
            subprocess.run(
                ["git", "push", "origin", tag],
                check=True,
                text=True,
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error creating tag: {e}") from e


if __name__ == "__main__":
    main()  # type: ignore
