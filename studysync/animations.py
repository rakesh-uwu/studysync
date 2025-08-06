
import time
import random
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

console = Console()

CAT_FRAMES = [
    """
    /\_/\
   ( o.o )
    > ^ <
    """,
    """
    /\_/\
   ( o.o )
    > ~ <
    """,
    """
    /\_/\
   ( ^.^ )
    > ^ <
    """
]

STUDYING_CAT_FRAMES = [
    """
    /\_/\
   ( o.o )  
    > ^ <
    """,
    """
    /\_/\
   ( o.o ) 
    > ~ <
    """,
    """
    /\_/\
   ( ^.^ )  
    > ^ <
    """
]

BREAK_CAT_FRAMES = [
    """
    /\_/\
   ( o.o )  
    > ^ <
    """,
    """
    /\_/\
   ( -.- ) 
    > ~ <
    """,
    """
    /\_/\
   ( ^.^ )  
    > ^ <
    """
]

def animate_cat(frames=None, duration=3, fps=5, message="", border_style="cyan", title=""):

    if frames is None:
        frames = CAT_FRAMES

    total_frames = int(duration * fps)
    frame_duration = 1 / fps

    try:
        for i in range(total_frames):
            console.clear()
            frame = frames[i % len(frames)]

            if message:
                content = f"{frame}\n\n{message}"
            else:
                content = frame

            panel = Panel(content, border_style=border_style)
            if title:
                panel.title = f"[bold {border_style}]{title}[/bold {border_style}]"

            console.print(Align.center(panel))
            time.sleep(frame_duration)
    except KeyboardInterrupt:
        pass

def show_studying_cat(message="Studying hard...", duration=3):

    animate_cat(STUDYING_CAT_FRAMES, duration, 2, message, border_style="green", title="Study Mode")

def show_break_cat(message="Break time!", duration=3):

    animate_cat(BREAK_CAT_FRAMES, duration, 2, message, border_style="yellow", title="Break Time")

def show_completion_cat(message="Great job!", duration=3):

    celebration_frames = []
    for frame in CAT_FRAMES:

        confetti = ""
        for _ in range(10):
            x = random.randint(0, 20)
            y = random.randint(0, 5)
            symbol = random.choice(["+", "*", ".", "o", "*"])
            confetti += f"\033[{y};{x}H{symbol}"

        celebration_frames.append(f"{confetti}{frame}")

    animate_cat(celebration_frames, duration, 3, message, border_style="magenta", title="Celebration")

def show_loading_animation(message="Loading...", duration=2):

    frames = [
        f"[bold cyan]{message}[/bold cyan] [dim]|[/dim]",
        f"[bold cyan]{message}[/bold cyan] [dim]/[/dim]",
        f"[bold cyan]{message}[/bold cyan] [dim]-[/dim]",
        f"[bold cyan]{message}[/bold cyan] [dim]\\[/dim]"
    ]

    total_frames = int(duration * 4)  

    try:
        for i in range(total_frames):
            console.clear()
            frame = CAT_FRAMES[i % len(CAT_FRAMES)]
            spinner = frames[i % len(frames)]

            content = f"{frame}\n\n{spinner}"
            panel = Panel(content, border_style="blue", title="[bold blue]Loading[/bold blue]")
            console.print(Align.center(panel))
            time.sleep(0.25)  
    except KeyboardInterrupt:
        pass

HOME_CAT_FRAMES = [
    """
    /\_/\
   ( o.o )  
    > ^ <
    """,
    
    """
    /\_/\
   ( ^.^ )  
    > ~ <
    """,

    """
    /\_/\
   ( o.o )  
    > ^ <
    """
]

def show_home_cat(message="Welcome to StudySync!", duration=3):

    animate_cat(HOME_CAT_FRAMES, duration, 2, message, border_style="cyan", title="Home")

DASHBOARD_CAT_FRAMES = [
    """
    /\_/\
   ( o.o )  
    > ^ <
    """,
    
    """
    /\_/\
   ( ^.^ )  
    > ~ <
    """,

    """
    /\_/\
   ( o.o )  
    > ^ <
    """,

]

def show_dashboard_cat(message="Your Dashboard", duration=3):

    animate_cat(DASHBOARD_CAT_FRAMES, duration, 2, message, border_style="green", title="Dashboard")

def show_transition_animation(from_screen="", to_screen="", duration=1.5):

    frames = [
        """
        /\_/\
       ( o.o )  
        > ^ <
        """,
        
        """
        /\_/\
       ( ^.^ )  
        > ~ <
        """,

         """
         /\_/\
        ( o.o )  
         > ^ <
         """,

    ]

    if from_screen and to_screen:
        message = f"[bold]Transitioning from [cyan]{from_screen}[/cyan] to [green]{to_screen}[/green]...[/bold]"
    elif to_screen:
        message = f"[bold]Going to [green]{to_screen}[/green]...[/bold]"
    else:
        message = "[bold]Loading next screen...[/bold]"

    animate_cat(frames, duration, 8, message, border_style="blue", title="Transition")

BUDDY_CAT_FRAMES = [
    """
    /\_/\
   ( o.o )  
    > ^ <
    """,
    """
    /\_/\
   ( o.o ) 
    > ~ <
    """,
    """
    /\_/\
   ( ^.^ )  
    > ^ <
    """
]

def create_motivational_cat_frames(user_name):

    return [
        f"""
        /\_/\
       ( o.o )  
        > ^ <
        
        Keep going, {user_name}! You're doing great!
        """,
        
        f"""
        /\_/\
       ( ^.^ )  
        > ~ <
        
        You've got this, {user_name}! Stay focused!
        """,
        
        f"""
        /\_/\
       ( o.o )  
        > ^ <
        
        Almost there, {user_name}! Don't give up!
        """,
        
        f"""
        /\_/\
       ( ^.^ )  
        > ^ <
        
        Excellent work, {user_name}! Keep that momentum!
        """
    ]

LISTENING_CAT_FRAMES = [
    """
    /\_/\
   ( o.o )  
    > ^ <
    """,
    
    """
    /\_/\
   ( o.o ) 
    > ~ <
    """,
    
    """
    /\_/\
   ( ^.^ )  
    > ^ <
    """,
    
    """
    /\_/\
   ( o.o )  
    > ^ <
    """,

]

def show_buddy_cat(greeting, duration=3):

    animate_cat(BUDDY_CAT_FRAMES, duration, 2, greeting, border_style="yellow", title="Study Buddy")

def show_motivational_cat(user_name, message, duration=3):

    frames = create_motivational_cat_frames(user_name)
    animate_cat(frames, duration, 2, message, border_style="magenta", title="Motivation")

def show_listening_cat(user_name, duration=2):

    listening_messages = [
        f"I'm here to listen, {user_name}...",
        f"Your thoughts matter, {user_name}...",
        f"Feel free to share, {user_name}...",
        f"I'm all ears, {user_name}..."
    ]

    import random
    message = random.choice(listening_messages)
    animate_cat(LISTENING_CAT_FRAMES, duration, 2, message, border_style="cyan", title="Listening")