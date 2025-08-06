
import os
import json
import datetime
from collections import defaultdict
from rich.console import Console
from rich.table import Table

from logger import list_sessions, read_session, LOGS_DIR

console = Console()

def generate_weekly_stats():

    session_files = list_sessions()

    if not session_files:
        return False

    sessions = []
    for filename in session_files:
        session_data = read_session(filename)
        if session_data:
            sessions.append(session_data)

    if not sessions:
        return False

    days_data = _group_sessions_by_day(sessions)

    _display_weekly_overview(days_data)

    _display_focus_trend(days_data)

    return True

def _group_sessions_by_day(sessions):

    days_data = defaultdict(lambda: {
        'sessions': 0,
        'total_duration': 0,
        'focus_scores': [],
        'avg_focus': 0
    })

    today = datetime.datetime.now().date()

    for session in sessions:
        try:

            session_date = datetime.datetime.strptime(
                session.get('date', ''), 
                "%Y-%m-%d %H:%M:%S"
            ).date()

            days_ago = (today - session_date).days
            if days_ago > 7:
                continue

            day_name = session_date.strftime("%A")

            days_data[day_name]['sessions'] += 1
            days_data[day_name]['total_duration'] += session.get('duration', 0)

            if 'focus_scores' in session:
                for score_data in session['focus_scores']:
                    days_data[day_name]['focus_scores'].append(score_data.get('score', 0))
        except (ValueError, KeyError):

            continue

    for day, data in days_data.items():
        if data['focus_scores']:
            data['avg_focus'] = sum(data['focus_scores']) / len(data['focus_scores'])

    return days_data

def _display_weekly_overview(days_data):

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Day")
    table.add_column("Sessions")
    table.add_column("Total Duration (min)")
    table.add_column("Avg Focus Score")

    days_order = [
        "Monday", "Tuesday", "Wednesday", "Thursday", 
        "Friday", "Saturday", "Sunday"
    ]

    for day in days_order:
        if day in days_data:
            data = days_data[day]
            avg_focus = f"{data['avg_focus']:.2f}/5.0" if data['avg_focus'] else "N/A"
            table.add_row(
                day,
                str(data['sessions']),
                str(data['total_duration']),
                avg_focus
            )
        else:
            table.add_row(day, "0", "0", "N/A")

    console.print("\n[bold]Weekly Overview:[/bold]")
    console.print(table)

def _display_focus_trend(days_data):

    days_order = [
        "Monday", "Tuesday", "Wednesday", "Thursday", 
        "Friday", "Saturday", "Sunday"
    ]

    focus_scores = []
    for day in days_order:
        if day in days_data and days_data[day]['avg_focus']:
            focus_scores.append(days_data[day]['avg_focus'])
        else:
            focus_scores.append(0)

    console.print("\n[bold]Weekly Focus Trend:[/bold]")
    _display_ascii_chart(days_order, focus_scores)

def _display_ascii_chart(labels, values):

    max_value = 5  
    chart_width = 20

    for i, (label, value) in enumerate(zip(labels, values)):

        bar_length = int((value / max_value) * chart_width) if value > 0 else 0

        if value >= 4:
            color = "green"
        elif value >= 3:
            color = "yellow"
        elif value > 0:
            color = "red"
        else:
            color = "white"

        bar = f"[{color}]{'█' * bar_length}[/{color}]"

        day_abbr = label[:3]
        console.print(f"{day_abbr}: {bar} {value:.2f}/5.0" if value > 0 else f"{day_abbr}: {bar} N/A")