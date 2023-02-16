from pathlib import Path

from cookiecutter.exceptions import FailedHookException, OutputDirExistsException
from cookiecutter.main import cookiecutter
from termcolor import cprint, colored

from ltou.cli import run_command
from ltou.model import Context

script_dir = Path(__file__).parent


def generate_project(context: Context) -> None:
    """
    Generate actual project with given context.

    :param context: builder_context
    """
    try:
        cprint(f"Generating project in {script_dir}")
        cookiecutter(
            template=f"{script_dir}/template",
            extra_context=context.dict(),
            default_config=Context().dict(),
            no_input=True,
            overwrite_if_exists=context.force,
        )
    except (FailedHookException, OutputDirExistsException) as exc:
        if isinstance(exc, OutputDirExistsException):
            cprint("==> Directory with such name already exists!", "red")
        return
    else:
        prompt_with_underline = colored(f"{script_dir}/README.md", color="cyan", attrs=["underline"])
        cprint(
            f"🍺 Done. Now Run. 👀You can read information about usage in {prompt_with_underline}"
        )
        cprint("🧵Now Run:")
        cprint(f"  cd {context.project_name}", color="green")
        cprint(f"  charm .", color="green")


def main() -> None:
    """Starting entry."""
    run_command(generate_project)


if __name__ == "__main__":
    main()
