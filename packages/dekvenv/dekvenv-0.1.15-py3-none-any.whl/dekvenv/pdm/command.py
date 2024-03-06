import sys
import typer
from typing_extensions import Annotated
from dektools.shell import shell_wrapper
from dektools.file import remove_path, write_file, read_text

app = typer.Typer(add_completion=False)


@app.command()
def config(
        update: Annotated[bool, typer.Option("--update/--no-update")] = False,
        cache: Annotated[bool, typer.Option("--cache/--no-cache")] = True,
        redirect: Annotated[bool, typer.Option("--redirect/--no-redirect")] = False,
):
    shell_wrapper(f"pdm config check_update {'true' if update else 'false'}")
    shell_wrapper(f"pdm config install.cache {'on' if cache else 'off'}")

    # disable mirror redirect
    from unearth import collector
    path_target = collector.__file__
    contents = (
        "        headers={",
        "        allow_redirects=False, headers={"
    )
    write_file(path_target, read_text(path_target).replace(*contents[::-1 if redirect else 1]))


@app.command(
    context_settings=dict(resilient_parsing=True)
)
def install():
    argv = sys.argv[sys.argv.index(install.__name__) + 1:]
    shell_wrapper(f'pdm install {" ".join(argv)}')


@app.command()
def clear():
    from .core import get_pdm_cache_dir
    shell_wrapper(f'pdm cache clear')
    remove_path(get_pdm_cache_dir())


@app.command()
def clear_hash():
    from .core import get_pdm_cache_dir_hash
    remove_path(get_pdm_cache_dir_hash())
