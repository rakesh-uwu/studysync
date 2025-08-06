
import os
import json
import datetime
from pathlib import Path
from rich.console import Console

console = Console()

LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")

def create_logs_dir():

    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
        console.print(f"[green]Created logs directory: {LOGS_DIR}[/green]")

def save_session(session_data):

    create_logs_dir()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = f"{timestamp}.json"
    filepath = os.path.join(LOGS_DIR, filename)

    with open(filepath, 'w') as f:
        json.dump(session_data, f, indent=4)

    return filename

def list_sessions():

    create_logs_dir()

    json_files = [f for f in os.listdir(LOGS_DIR) if f.endswith('.json')]

    json_files.sort(reverse=True)

    return json_files

def read_session(filename):

    filepath = os.path.join(LOGS_DIR, filename)

    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        console.print(f"[bold red]Error reading session file: {e}[/bold red]")
        return None

def export_session(session_data, format_type='txt'):

    create_logs_dir()

    if 'date' in session_data:
        try:
            date_obj = datetime.datetime.strptime(session_data['date'], "%Y-%m-%d %H:%M:%S")
            timestamp = date_obj.strftime("%Y-%m-%d_%H%M")
        except ValueError:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    else:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")

    filename = f"{timestamp}_export.{format_type}"
    filepath = os.path.join(LOGS_DIR, filename)

    if format_type == 'md':
        content = _format_markdown(session_data)
    else:  
        content = _format_text(session_data)

    with open(filepath, 'w') as f:
        f.write(content)

    return filename

def _format_text(session_data):

    lines = [
        "StudySync CLI - Session Summary",
        "=" * 30,
        f"Topic: {session_data.get('topic', 'Unknown')}",
        f"Goal: {session_data.get('goal', 'Unknown')}",
        f"Date: {session_data.get('date', 'Unknown')}",
        f"Duration: {session_data.get('duration', 0)} minutes",
        f"Average Focus Score: {session_data.get('avg_focus', 0):.2f}/5.0",
        "\nFocus Scores by Break:",
        "-" * 30
    ]

    if 'focus_scores' in session_data and session_data['focus_scores']:
        for i, score_data in enumerate(session_data['focus_scores'], 1):
            timestamp = score_data.get('timestamp', 'Unknown')
            score = score_data.get('score', 0)
            lines.append(f"Break {i}: {timestamp} - Focus Score: {score}/5")
    else:
        lines.append("No focus scores recorded.")

    return "\n".join(lines)

def _format_markdown(session_data):

    lines = [
        "# Study Session Summary",
        "",
        f"**Topic:** {session_data.get('topic', 'Unknown')}",
        f"**Goal:** {session_data.get('goal', 'Unknown')}",
        f"**Date:** {session_data.get('date', 'Unknown')}",
        f"**Duration:** {session_data.get('duration', 0)} minutes",
        f"**Average Focus Score:** {session_data.get('avg_focus', 0):.2f}/5.0",
        "",
        "## Focus Scores",
        "",
        "| Break | Timestamp | Focus Score |",
        "| ------- | --------- | ----------- |"
    ]

    if 'focus_scores' in session_data and session_data['focus_scores']:
        for i, score_data in enumerate(session_data['focus_scores'], 1):
            timestamp = score_data.get('timestamp', 'Unknown')
            score = score_data.get('score', 0)
            lines.append(f"| {i} | {timestamp} | {score}/5 |")
    else:
        lines.append("*No focus scores recorded.*")

    return "\n".join(lines)