import click
import auth
import sys
import os

# Get the directory of the current file (thunder.py), then go up two levels to the root
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(current_dir, "..", "..")

# Add the src directory to sys.path
# src_dir = os.path.join(root_dir, 'src')
sys.path.append(root_dir)

# Now you can import your modules
from thunder_helper import Task


class DefaultCommandGroup(click.Group):
    def resolve_command(self, ctx, args):
        try:
            # Try to resolve the command normally
            return super(DefaultCommandGroup, self).resolve_command(ctx, args)
        except click.exceptions.UsageError:
            # If no command is found, default to 'run' and include the args
            return "run", run, args


@click.group(
    cls=DefaultCommandGroup,
    help="This CLI is the interface between you and the Thunder network.",
)
def cli():
    pass


@cli.command(
    help="Runs a specified task on the Thunder network. This is the default behavior of the thunder command. Please see thundergpu.net for detailed documentation."
)
@click.option("--ngpus", default=1, help="Specify the number of GPUs to use.")
@click.argument("args", nargs=-1)
def run(ngpus, args):
    """
    Executes a task on the Thunder network.

    Args:
        ngpus: The number of GPUs to use for the task.
        args: Additional arguments to pass to the task.
    """
    id_token, refresh_token, uid = auth.validate_auth()

    if not id_token or not refresh_token:
        click.echo("Please log in to begin using the Thunder network.")
        id_token, refresh_token, uid = auth.login()

        if not id_token or not refresh_token:
            click.echo("Authentication failed. Unable to proceed.")
            return

    # Create an instance of Task with required arguments
    task = Task(ngpus, args, uid)

    # Initialize the session with the current auth token
    if not task.get_password(id_token):
        click.echo("Failed to retrieve password for session.")
        return

    # Execute the task
    if not task.execute_task(id_token, args):
        click.echo("Failed to execute the task.")
        return

    # Close the session
    if not task.close_session(id_token):
        click.echo("Failed to close the session.")


@cli.command(help="Logs in to the Thunder network.")
def login():
    """
    Authenticates a user for access to the Thunder network. Please use the same login credentials as the Thunder console (console.thundergpu.net).
    """
    auth.login()


@cli.command(help="Logs out from the Thunder network.")
def logout():
    """
    Logs the current user out of the Thunder network.
    """
    auth.logout()


if __name__ == "__main__":
    cli()
