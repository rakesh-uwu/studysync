
from rich.console import Console
from rich.panel import Panel

def format_time(seconds):

    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def display_banner(console):

    banner = """
    ╔═══════════════════════════════════════════╗
    ║             STUDY SYNC                    ║
    ╚═══════════════════════════════════════════╝
    """

    console.print(banner, style="cyan")

def get_color_for_focus_score(score):

    if score >= 4.5:
        return "bright_green"
    elif score >= 3.5:
        return "green"
    elif score >= 2.5:
        return "yellow"
    elif score >= 1.5:
        return "orange_red1"
    else:
        return "red"

def get_motivational_quote():

    quotes = [
        "The expert in anything was once a beginner. — Helen Hayes",
        "The beautiful thing about learning is that no one can take it away from you. — B.B. King",
        "Education is the passport to the future. — Malcolm X",
        "The more that you read, the more things you will know. — Dr. Seuss",
        "Learning is never done without errors and defeat. — Vladimir Lenin",
        "The mind is not a vessel to be filled, but a fire to be kindled. — Plutarch",
        "Study hard what interests you the most in the most undisciplined way possible. — Richard Feynman",
        "The cure for boredom is curiosity. There is no cure for curiosity. — Dorothy Parker",
        "Learning is not attained by chance, it must be sought with ardor and attended to with diligence. — Abigail Adams",
        "The more I read, the more I acquire, the more certain I am that I know nothing. — Voltaire"
    ]

    import random
    return random.choice(quotes)

class PomodoroTimer:

    def __init__(self, work_minutes=25, short_break_minutes=5, long_break_minutes=15, long_break_interval=4):

        self.work_minutes = work_minutes
        self.short_break_minutes = short_break_minutes
        self.long_break_minutes = long_break_minutes
        self.long_break_interval = long_break_interval
        self.completed_intervals = 0

    def get_next_interval_type(self):

        if self.completed_intervals % (self.long_break_interval * 2 - 1) == 0 and self.completed_intervals > 0:
            return 'long_break', self.long_break_minutes
        elif self.completed_intervals % 2 == 0:
            return 'work', self.work_minutes
        else:
            return 'short_break', self.short_break_minutes

    def complete_current_interval(self):

        self.completed_intervals += 1

    def get_session_progress(self):

        work_intervals = (self.completed_intervals + 1) // 2
        return {
            'completed_work_intervals': work_intervals,
            'completed_breaks': self.completed_intervals // 2,
            'total_work_minutes': work_intervals * self.work_minutes
        }