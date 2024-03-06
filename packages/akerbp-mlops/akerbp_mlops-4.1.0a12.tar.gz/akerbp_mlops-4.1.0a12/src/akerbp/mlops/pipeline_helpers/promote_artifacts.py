import argparse
import os

import akerbp.mlops.model_manager as mm


def main():
    parser = argparse.ArgumentParser(
        description="Promote artifacts to specified target environment"
    )
    parser.add_argument(
        "-n",
        "--model_name",
        type=str,
        help="Name of the model to promote. If not provided, it is inferred from the mlops_settings.yaml file.",
        required=False,
    )
    args = parser.parse_args()
    model_name = args.model_name
    if model_name is None:
        from akerbp.mlops.core.config import read_project_settings

        model_names = [s.model_name for s in read_project_settings()]
    else:
        model_names = [model_name]
    env = os.environ.get("MODEL_ENV", None)
    if env is None:
        raise Exception("Environment variabel 'MODEL_ENV' is not set")

    if env == "dev":
        target_env = "test"
    elif env == "test":
        target_env = "prod"
    else:
        raise Exception(
            "Cannot infer target env from environment variable 'MODEL_ENV'={env}"
        )

    mm.setup()
    for model_name in model_names:
        mm.promote_model(
            model_name=model_name,
            promote_to=target_env,
            confirm=False,
        )


if __name__ == "__main__":
    main()  # type: ignore
