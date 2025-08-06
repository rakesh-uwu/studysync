
import time
import datetime
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn
from rich.prompt import IntPrompt
from rich.align import Align

from logger import save_session
from utils import format_time
from animations import show_studying_cat, show_break_cat, show_completion_cat

console = Console()

class StudySession:

    def __init__(self, topic, goal, duration, break_interval, capture_concepts=False):

        self.topic = topic
        self.goal = goal
        self.duration = duration  
        self.break_interval = break_interval  
        self.capture_concepts = capture_concepts
        self.start_time = None
        self.end_time = None
        self.focus_scores = []

    def start(self):

        self.start_time = datetime.datetime.now()
        console.print(f"\n[bold green]Starting study session: {self.topic}[/bold green]")
        console.print(Align.center(f"[bold]Goal:[/bold] {self.goal}"))
        console.print(Align.center(f"[bold]Total Duration:[/bold] {self.duration} minutes"))
        console.print(Align.center(f"[bold]Break Interval:[/bold] {self.break_interval} minutes\n"))

        show_studying_cat("Let's focus!", 2)

        total_seconds = self.duration * 60
        interval_seconds = self.break_interval * 60
        num_intervals = total_seconds // interval_seconds
        remaining_seconds = total_seconds % interval_seconds

        for interval in range(1, num_intervals + 1):
            self._run_interval(interval, interval_seconds)
            if interval < num_intervals or remaining_seconds > 0:
                self._take_break(interval)

        if remaining_seconds > 0:
            self._run_interval(num_intervals + 1, remaining_seconds)

        self.end_time = datetime.datetime.now()
        self._show_summary()

    def _run_interval(self, interval_num, seconds):

        console.print(f"[bold cyan]Study Interval {interval_num}[/bold cyan]")

        with Progress(
            TextColumn("[bold blue]{task.description}[/bold blue]"),
            BarColumn(),
            TextColumn("{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task(f"Studying: {self.topic}", total=seconds)

            while not progress.finished:
                progress.update(task, advance=1)
                time.sleep(1)

    def _take_break(self, interval_num):

        console.print("\n[bold yellow]Break Time![/bold yellow]")

        show_break_cat("Time to relax!", 2)

        from utils import get_motivational_quote
        quote = get_motivational_quote()
        console.print(Panel(f"[italic cyan]\"{quote}\"[/italic cyan]", border_style="yellow"))

        while True:
            try:
                focus_score = IntPrompt.ask(
                    "How focused were you in the last session?", 
                    choices=["1", "2", "3", "4", "5"]
                )
                break
            except ValueError:
                console.print("[bold red]Please enter a number between 1 and 5![/bold red]")

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.focus_scores.append({
            "timestamp": timestamp,
            "score": focus_score,
            "interval": interval_num
        })

        console.print(f"Focus score of {focus_score}/5 recorded.")

        if self.capture_concepts:
            from insights import capture_key_concepts
            console.print("\n[bold cyan]Learning Insights[/bold cyan]")
            console.print("Let's capture what you've learned in this study interval.")
            capture_key_concepts(self.topic)

        console.print("Take a short break and prepare for the next interval...\n")

        with Progress() as progress:
            break_task = progress.add_task("Break time remaining", total=30)
            for _ in range(30):
                progress.update(break_task, advance=1)
                time.sleep(1)

    def _show_summary(self):

        from rich.table import Table

        duration_seconds = (self.end_time - self.start_time).total_seconds()
        duration_formatted = format_time(int(duration_seconds))

        if self.focus_scores:
            avg_focus = sum(score["score"] for score in self.focus_scores) / len(self.focus_scores)
        else:
            avg_focus = 0

        console.print("\n" + "=" * 50)
        console.print("[bold green]Session Complete![/bold green]")
        console.print(f"[bold]Topic:[/bold] {self.topic}")
        console.print(f"[bold]Goal:[/bold] {self.goal}")
        console.print(f"[bold]Total Study Time:[/bold] {duration_formatted}")
        console.print(f"[bold]Average Focus Score:[/bold] {avg_focus:.2f}/5.0")

        if self.focus_scores:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Break")
            table.add_column("Timestamp")
            table.add_column("Focus Score")

            for i, score_data in enumerate(self.focus_scores, 1):
                timestamp = score_data["timestamp"]
                score = score_data["score"]
                table.add_row(str(i), timestamp, f"{score}/5")

            console.print("\n[bold]Focus Scores by Break:[/bold]")
            console.print(table)

        session_data = {
            "topic": self.topic,
            "goal": self.goal,
            "date": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration": self.duration,
            "break_interval": self.break_interval,
            "actual_duration_seconds": int(duration_seconds),
            "focus_scores": self.focus_scores,
            "avg_focus": avg_focus
        }

        filename = save_session(session_data)
        console.print(f"\n[bold]Session saved:[/bold] {filename}")
        console.print("=" * 50)

        show_completion_cat("Great job! You completed your study session!", 3)