from typing import Optional

from rich import print
import typer
from typing_extensions import Annotated

from ephemeral import __version__
from ephemeral.model import Task, Tracker
from ephemeral.view import (
    display_command_end,
    display_command_start,
    show_current_task,
    show_history,
)

app = typer.Typer()
tracker = Tracker.load()


def version_callback(value: bool):
    # TODO mmoran 2024-03-02
    # we're not getting this callback with `ephemeral --version` despite
    # our structure being the same as the `typer` docs
    if value:
        print(f"[white bold][?][/] {__package__} {__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[
        Optional[bool],
        typer.Option("--version", callback=version_callback, is_eager=True),
    ] = None,
) -> None:
    """A simple task tracker with a forgetful history"""
    if ctx.invoked_subcommand is not None:
        return

    show_current_task(tracker)


@app.command()
def track() -> None:
    """start tracking a new task, or replace your current task"""
    display_command_start("track", tracker)
    if tracker.current_task is not None:
        show_current_task(tracker)
        # TODO mmoran 2024-03-02
        # we should ask if the user wants to save, and if they don't, if
        # they want to discard. if they say no to both, then we can't start a new task
        _ = typer.confirm("    would you like to complete your current task?", abort=True)
        complete()

    _ = typer.confirm("    would you like to start tracking a new task?", abort=True)
    new_task = typer.prompt("    what would you like to track?")
    tracker.update(Task(new_task))
    display_command_end("track", tracker)
    tracker.save()


@app.command()
def complete() -> None:
    """finish a task and save it in the history"""
    display_command_start("complete", tracker)

    if tracker.current_task is not None:
        tracker.update(new_task=None)  # this saves current task to history by default
        display_command_end("complete", tracker)
        tracker.save()


@app.command()
def discard() -> None:
    """discard the currently-active task"""
    display_command_start("discard", tracker)

    if tracker.current_task is not None:
        tracker.clear(task=True, history=False)
        display_command_end("discard", tracker)
        tracker.save()


@app.command()
def history() -> None:
    """display record of completed tasks"""
    display_command_start("history", tracker)
    show_history(tracker)


@app.command()
def clear() -> None:
    """delete all persisted state"""
    display_command_start("clear", tracker)
    if tracker.current_task is not None or len(tracker.history) > 0:
        print("    you have saved history")
        _ = typer.confirm("    would you like to continue?", abort=True)
    if tracker.current_task is not None:
        print("    Clearing the current task...")
    if len(tracker.history) > 0:
        print(f"    Clearing the saved history ({len(tracker.history)} tasks)...")
    tracker.clear(task=True, history=True)
    display_command_end("clear", tracker)
    tracker.save()


if __name__ == "__main__":
    app()
