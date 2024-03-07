import click

from src.nextflow_file import Nextflow_File


@click.command()
@click.argument('main_workflow_path')
@click.option('--author', 'author', required=False, help='Author name, extracted otherwise')
@click.option('--name', 'name', required=False, help='Workflow name, extracted otherwise')
@click.option('--output-dir', default='./results', help='Where the results will be written')
@click.option(
    '--no-duplicate',
    'duplicate',
    required=False,
    default=True,
    is_flag=True,
    help=''
    'When processes and subworkflows are duplicated in the workflows by the \'include as\' option, '
    'this option will duplicate the procedures in the graph output.',
)
@click.option(
    '--graph-in-dot-only',
    'render_graphs',
    required=False,
    default=True,
    is_flag=True,
    help='Generate the graph output only in dot format, not png (faster).',
)
def cli_command(main_workflow_path, **kwargs):
    return cli(main_workflow_path, **kwargs)


def cli(main_workflow_path, render_graphs: bool, **kwargs):
    """
    The path to main file, subworkflows and modules must be in direct subdir of this file,
    in folders with eponymous names.
    """

    w = Nextflow_File(address=main_workflow_path, **kwargs)
    w.initialise()
    w.generate_all_graphs(render_graphs=render_graphs)


if __name__ == '__main__':
    cli_command()
