import datetime

from rich import print

from ephemeral.model import Task, Tracker


def display_command_start(command: str, tracker: Tracker) -> None:
    """show the command message based on what we're trying to do"""
    # commands on the active task
    if command == "track":
        message = f"[bold blue][+][/] ephemeral is starting a new task"
    elif command == "complete":
        message = f"[bold yellow][?][/] ephemeral is not tracking anything"
        if tracker.current_task is not None:
            message = f"[bold blue][!][/] ephemeral is completing [bold white]{tracker.current_task.task}[/]"
    elif command == "discard":
        message = f"[bold yellow][?][/] ephemeral is not tracking anything"
        if tracker.current_task is not None:
            message = f"[bold red][-][/] ephemeral is discarding [bold white]{tracker.current_task.task}[/]"

    # commands on the history
    elif command == "clear":
        message = f"[bold yellow][?][/] ephemeral has no memory"
        if tracker.current_task is not None or len(tracker.history) > 0:
            message = f"[bold red][!][/] ephemeral is clearing all recorded history"
    elif command == "history":
        message = f"[bold yellow][?][/] ephemeral has no memory"
        if tracker.current_task is not None or len(tracker.history) > 0:
            message = f"[bold green][+][/] ephemeral remembers its history"

    else:
        message = f"[bold red][!] command `{command}` not found[/]"

    print(message)


def display_command_end(command: str, tracker: Tracker) -> None:
    """show a confirmation message at the end of a command"""
    if command == "track":
        message = f"[bold yellow][?][/] ephemeral did not start a task"
        if tracker.current_task is not None:
            message = f"[bold blue][+][/] ephemeral is now tracking [bold white]{tracker.current_task.task}[/]"
    elif command == "complete":
        message = f"[bold green][+][/] ephemeral has remembered this task"
    elif command == "discard":
        message = f"[bold red][-][/] ephemeral has discarded this task"
    elif command == "clear":
        message = f"[bold blue][*][/] ephemeral has forgotten"

    else:
        message = f"[bold red][!] command `{command}` not found[/]"

    print(message)


def show_current_task(tracker: Tracker) -> None:
    if tracker.current_task is not None:
        print(f"[bold green][!][/] tracking [white bold]{tracker.current_task.task}[/]")
    else:
        print("[bold yellow][!][/] no active task found")


def show_history(tracker: Tracker) -> None:
    if tracker.current_task is not None:
        print("[bold green][+][/] active task found")
        history_task(tracker.current_task)
    if not tracker.history:
        print("[bold yellow][?][/] no tasks have been completed")
    else:
        print("[bold green][+][/] completed history found")
        for task in tracker.history[::-1]:
            history_task(task)


def history_task(task: Task) -> None:
    start_dt = _convert_to_datetime(task.start_ts)
    if task.end_ts is not None:
        end_dt = _convert_to_datetime(task.end_ts)
        end_dt_string = f"{end_dt:%Y-%m-%d}"
    else:
        end_dt_string = "now"
    date_string = f"[bold black]{start_dt:%Y-%m-%d} -- {end_dt_string}[/]"
    print(f"    {date_string}: {task.task}")


def _convert_to_datetime(timestamp: int) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(timestamp)
