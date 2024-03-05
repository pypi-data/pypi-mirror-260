import sys
import click
from clisync import CliSync

# from .client import group


def main():
    group = CliSync(classes=['Object'], 
                    module='clisyncdemo.objects', 
                    requires_decorator=False)
    controlled_group = CliSync(classes=['ObjectControlled'],
                                module='clisyncdemo.objects'
                               )

    cli = click.CommandCollection(sources=[group, controlled_group])
    # Standalone mode is False so that the errors can be caught by the runs
    cli(standalone_mode=False)
    sys.exit()

if __name__ == "__main__":
    main()
