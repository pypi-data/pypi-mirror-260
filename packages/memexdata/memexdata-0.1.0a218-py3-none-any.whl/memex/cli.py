import click
from memex.bootstrap import bootstrap_project


@click.command()
@click.argument("project_path", type=click.Path(exists=True))
def load_project(project_path: str):
    """Load a project into Memex."""
    bootstrap_project(project_path)


@click.group()
def main() -> None:
    """Memex CLI."""
    pass


main.add_command(load_project)

if __name__ == "__main__":
    main()
