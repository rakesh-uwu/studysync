
import os
import sys
import time
import datetime
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
from rich.align import Align
from rich.table import Table
from rich.box import ROUNDED

from session import StudySession
from logger import list_sessions, read_session, create_logs_dir
from stats import generate_weekly_stats
from utils import display_banner
from insights import review_due_concepts, display_knowledge_graph, calculate_learning_effectiveness
from animations import show_studying_cat, show_break_cat, show_completion_cat, show_loading_animation, show_home_cat, show_dashboard_cat, show_buddy_cat, show_motivational_cat, show_listening_cat, show_transition_animation

console = Console()

def main_menu():

    create_logs_dir()

    show_home_cat("Welcome to StudySync!", 2)

    display_banner(console)

    while True:
        console.print(Panel(Align.center("[bold cyan]Main Menu[/bold cyan]")))

        show_dashboard_cat("Your StudySync Dashboard", 1)

        display_session_stats_widget()

        display_study_goals()

        options = [
            "[1] [bold]Start Study Session[/bold]",
            "[2] [bold]Start Pomodoro Session[/bold]",
            "[3] View Past Sessions",
            "[4] View Weekly Stats",
            "[5] [bold magenta on white]Learning Insights *[/bold magenta on white]",  
            "[6] [bold magenta on white]Knowledge Graph ^[/bold magenta on white]",  
            "[7] [bold green]Set Study Goals[/bold green]",  
            "[8] [bold yellow on blue]Study Buddy 👥[/bold yellow on blue]",  
            "[9] Exit"
        ]

        menu_panel = Panel(
            "\n".join(options),
            border_style="cyan",
            box=ROUNDED,
            title="[bold]Choose an Option[/bold]"
        )
        console.print(menu_panel)

        time.sleep(0.5)  

        choice = IntPrompt.ask("\nSelect an option", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9"])

        if choice == 1:
            start_session()
        elif choice == 8:
            study_buddy()  
        elif choice == 2:
            start_pomodoro_session()
        elif choice == 3:
            view_past_sessions()
        elif choice == 4:
            view_weekly_stats()
        elif choice == 5:
            view_learning_insights()
        elif choice == 6:
            view_knowledge_graph()
        elif choice == 7:
            set_study_goals()
        elif choice == 8:
            study_buddy()
        elif choice == 9:
            console.print("[bold green]Thank you for using StudySync CLI. Happy studying![/bold green]")
            show_completion_cat("See you next time!", 2)
            sys.exit(0)

def study_buddy():

    console.print(Panel("[bold yellow on blue]Advanced Study Buddy[/bold yellow on blue]"))

    buddy_profile = load_buddy_profile()

    greeting = get_personalized_greeting(buddy_profile)

    from animations import show_buddy_cat

    show_buddy_cat(greeting, 3)

    if buddy_profile.get('sessions', []):
        display_buddy_achievements(buddy_profile)

    console.print("\n[bold]How can your Advanced Study Buddy help you today?[/bold]")

    buddy_options = [
        "[1] Chat with your Study Buddy",
        "[2] Get a pep talk",
        "[3] Study together (virtual company)",
        "[4] Share your thoughts",
        "[5] [bold magenta]Learning Assistant[/bold magenta]",  
        "[6] [bold cyan]Mood Tracker[/bold cyan]",  
        "[7] [bold green]Study Pattern Analysis[/bold green]",  
        "[8] Return to main menu"
    ]

    buddy_panel = Panel(
        "\n".join(buddy_options),
        border_style="yellow",
        box=ROUNDED,
        title="[bold]Advanced Buddy Options[/bold]"
    )
    console.print(buddy_panel)

    choice = IntPrompt.ask("\nSelect an option", choices=["1", "2", "3", "4", "5", "6", "7", "8"])

    if choice == 1:
        chat_with_buddy(buddy_profile)
    elif choice == 2:
        get_pep_talk(buddy_profile)
    elif choice == 3:
        virtual_study_session(buddy_profile)
    elif choice == 4:
        share_thoughts(buddy_profile)
    elif choice == 5:
        learning_assistant(buddy_profile)
    elif choice == 6:
        mood_tracker(buddy_profile)
    elif choice == 7:
        study_pattern_analysis(buddy_profile)
    elif choice == 8:
        return  

def load_buddy_profile():

    import os
    import json
    from datetime import datetime

    profile_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "buddy_profile.json")

    if os.path.exists(profile_path):
        try:
            with open(profile_path, 'r') as f:
                profile = json.load(f)

            profile['last_login'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(profile_path, 'w') as f:
                json.dump(profile, f, indent=4)

            return profile
        except Exception as e:
            console.print(f"[bold red]Error loading profile: {e}[/bold red]")
            return create_new_profile(profile_path)
    else:
        return create_new_profile(profile_path)

def create_new_profile(profile_path):

    import json
    from datetime import datetime

    console.print("\n[bold yellow]Study Buddy:[/bold yellow] I don't think we've met before! What's your name?")
    user_name = Prompt.ask("Your name")

    profile = {
        "name": user_name,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mood_history": [],
        "sessions": [],
        "topics": {},
        "achievements": [],
        "preferences": {
            "study_time_preference": None,
            "favorite_subjects": [],
            "break_reminder": True,
            "encouragement_frequency": "medium"
        }
    }

    try:
        with open(profile_path, 'w') as f:
            json.dump(profile, f, indent=4)
        console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] Nice to meet you, {user_name}! I've created your profile.")
    except Exception as e:
        console.print(f"[bold red]Error creating profile: {e}[/bold red]")

    return profile

def save_buddy_profile(profile):

    import os
    import json

    profile_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "buddy_profile.json")

    try:
        with open(profile_path, 'w') as f:
            json.dump(profile, f, indent=4)
        return True
    except Exception as e:
        console.print(f"[bold red]Error saving profile: {e}[/bold red]")
        return False

def get_personalized_greeting(profile):

    import random
    from datetime import datetime

    current_hour = datetime.now().hour
    user_name = profile.get('name', 'friend')

    if 5 <= current_hour < 12:
        time_greetings = [
            f"Good morning, {user_name}!",
            f"Rise and shine, {user_name}! Ready for a productive day?",
            f"Morning, {user_name}! The early cat catches the knowledge!"
        ]
    elif 12 <= current_hour < 17:
        time_greetings = [
            f"Good afternoon, {user_name}!",
            f"Hello, {user_name}! Hope your day is going well!",
            f"Afternoon greetings, {user_name}! Ready for some studying?"
        ]
    elif 17 <= current_hour < 21:
        time_greetings = [
            f"Good evening, {user_name}!",
            f"Evening, {user_name}! Still got some energy for studying?",
            f"Hi {user_name}! Evening is a great time for focused work!"
        ]
    else:
        time_greetings = [
            f"Hello night owl {user_name}! Late night study session?",
            f"Working late, {user_name}? I'm here to keep you company!",
            f"Night time is quiet time - perfect for deep focus, {user_name}!"
        ]

    if 'last_login' in profile:
        try:
            last_login = datetime.strptime(profile['last_login'], "%Y-%m-%d %H:%M:%S")
            days_since_login = (datetime.now() - last_login).days

            if days_since_login > 7:
                return f"Welcome back, {user_name}! It's been {days_since_login} days. I've missed our study sessions!"
            elif days_since_login > 2:
                return f"Good to see you again, {user_name}! Ready to pick up where we left off?"
        except Exception:
            pass

    if profile.get('mood_history', []):
        last_mood = profile['mood_history'][-1]['mood']
        if last_mood in ['stressed', 'overwhelmed', 'tired']:
            return f"Welcome back, {user_name}. I remember you were feeling {last_mood} last time. How are you doing today?"

    return random.choice(time_greetings)

def display_buddy_achievements(profile):

    from rich.table import Table

    achievements_table = Table(title="[bold]Your Study Journey[/bold]", box=ROUNDED)
    achievements_table.add_column("Metric", style="cyan")
    achievements_table.add_column("Value", style="yellow")

    total_sessions = len(profile.get('sessions', []))
    total_duration = sum(session.get('duration', 0) for session in profile.get('sessions', []))
    unique_topics = len(profile.get('topics', {}))

    achievements_table.add_row("Total Study Sessions", str(total_sessions))
    achievements_table.add_row("Total Study Time", format_time(total_duration))
    achievements_table.add_row("Topics Explored", str(unique_topics))

    if 'current_streak' in profile:
        achievements_table.add_row("Current Streak", f"{profile['current_streak']} days 🔥")

    if profile.get('achievements', []):
        latest_achievement = profile['achievements'][-1]
        achievements_table.add_row("Latest Achievement", f"🏆 {latest_achievement['title']}")

    console.print(achievements_table)

def chat_with_buddy(profile):

    console.print(Panel("[bold yellow]Chat with your Study Buddy[/bold yellow]"))

    show_dashboard_cat("Let's have a meaningful chat!", 1)

    user_name = profile.get('name', 'friend')

    has_history = False
    if 'chat_history' not in profile:
        profile['chat_history'] = []
    elif len(profile['chat_history']) > 0:
        has_history = True

    standard_topics = [
        "How's your studying going?",
        "What are you learning today?",
        "Are you finding the material interesting?",
        "What's your favorite subject?",
        "Do you prefer studying in the morning or evening?"
    ]

    personalized_topics = []

    if profile.get('topics', {}):

        most_studied = max(profile['topics'].items(), key=lambda x: x[1]['duration'])[0]
        personalized_topics.append(f"How's your progress with {most_studied}?")

    if has_history:

        last_chat = profile['chat_history'][-1]
        personalized_topics.append(f"Last time we talked about {last_chat['topic']}. Want to continue that discussion?")

    if profile.get('preferences', {}).get('favorite_subjects', []):
        fav_subject = profile['preferences']['favorite_subjects'][0]
        personalized_topics.append(f"Tell me more about why you enjoy {fav_subject}?")

    topics = personalized_topics + standard_topics

    console.print("\n[bold]Choose a topic to discuss:[/bold]")
    for i, topic in enumerate(topics, 1):

        if i <= len(personalized_topics):
            console.print(f"[{i}] [bold cyan]{topic}[/bold cyan] 🌟")
        else:
            console.print(f"[{i}] {topic}")

    topic_choice = IntPrompt.ask("Select a topic", choices=[str(i) for i in range(1, len(topics) + 1)])
    selected_topic = topics[topic_choice - 1]

    console.print(f"\n[bold cyan]You:[/bold cyan] {selected_topic}")
    user_response = Prompt.ask("Your response")

    chat_entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "topic": selected_topic,
        "user_response": user_response
    }
    profile['chat_history'].append(chat_entry)

    if "favorite subject" in selected_topic.lower() and user_response:
        if 'favorite_subjects' not in profile['preferences']:
            profile['preferences']['favorite_subjects'] = []

        if user_response not in profile['preferences']['favorite_subjects']:
            profile['preferences']['favorite_subjects'].insert(0, user_response)

            profile['preferences']['favorite_subjects'] = profile['preferences']['favorite_subjects'][:3]

    if "morning or evening" in selected_topic.lower():
        if "morning" in user_response.lower():
            profile['preferences']['study_time_preference'] = "morning"
        elif "evening" in user_response.lower() or "night" in user_response.lower():
            profile['preferences']['study_time_preference'] = "evening"
        elif "afternoon" in user_response.lower():
            profile['preferences']['study_time_preference'] = "afternoon"

    save_buddy_profile(profile)

    buddy_responses = {

        "How's your studying going?": [
            f"That sounds great, {user_name}! Keep up the good work!",
            f"Everyone has those days, {user_name}. Tomorrow will be better!",
            f"Remember to take breaks and stay hydrated, {user_name}!",
            f"I believe in you, {user_name}! You're making progress even when it doesn't feel like it."
        ],
        "What are you learning today?": [
            f"That sounds fascinating, {user_name}! I'd love to hear more about it.",
            f"Wow, that's a complex topic. Breaking it down into smaller parts might help you master it, {user_name}.",
            f"That's an important subject! It will definitely be useful in your future, {user_name}.",
            f"Learning new things is always exciting! How are you finding it so far, {user_name}?"
        ],
        "Are you finding the material interesting?": [
            f"It's great when study material captures your interest, {user_name}!",
            f"Sometimes the most challenging subjects become the most rewarding, {user_name}.",
            f"If you're not finding it interesting, try connecting it to something you care about, {user_name}.",
            f"Your enthusiasm for learning is inspiring, {user_name}!"
        ],
        "What's your favorite subject?": [
            f"That's a great choice, {user_name}! What do you enjoy most about it?",
            f"I can see why you'd like that subject, {user_name}. It has so many fascinating aspects!",
            f"Interesting choice, {user_name}! That subject opens up many opportunities.",
            f"I like that one too! It's so rewarding to study something you're passionate about, {user_name}."
        ],
        "Do you prefer studying in the morning or evening?": [
            f"Morning studying gives you a fresh start to the day, {user_name}!",
            f"Evening studying can be peaceful when the day's distractions are done, {user_name}.",
            f"Finding your optimal study time is so important for productivity, {user_name}.",
            f"Whatever works best for your body clock is the right choice, {user_name}!"
        ]
    }

    for topic in personalized_topics:
        if topic not in buddy_responses:
            if "progress with" in topic:
                subject = topic.split("progress with ")[1].rstrip("?")
                buddy_responses[topic] = [
                    f"I'm glad you're sticking with {subject}, {user_name}! Consistency is key to mastery.",
                    f"Your dedication to {subject} is impressive, {user_name}! How are you feeling about your progress?",
                    f"Learning {subject} takes time. Remember to celebrate small victories along the way, {user_name}!",
                    f"I've noticed you've spent quite a bit of time on {subject}. That kind of focus will definitely pay off, {user_name}!"
                ]
            elif "Last time we talked about" in topic:
                buddy_responses[topic] = [
                    f"I enjoy our ongoing conversations, {user_name}. It helps build a deeper understanding.",
                    f"It's great to revisit topics we've discussed before, {user_name}. It reinforces learning!",
                    f"I remember our last chat clearly, {user_name}. I'm here to continue supporting your learning journey.",
                    f"Continuous dialogue is so valuable for learning, {user_name}. I'm glad we can pick up where we left off!"
                ]
            elif "why you enjoy" in topic:
                subject = topic.split("why you enjoy ")[1].rstrip("?")
                buddy_responses[topic] = [
                    f"Your passion for {subject} really shines through, {user_name}!",
                    f"It's wonderful that you've found a subject that resonates with you, {user_name}.",
                    f"Understanding why we enjoy certain subjects helps us learn more effectively, {user_name}.",
                    f"Your enthusiasm for {subject} is contagious, {user_name}! It makes me curious about it too!"
                ]

    response_set = buddy_responses.get(selected_topic, buddy_responses["What are you learning today?"])

    import random

    keyword_matches = {
        "difficult": 1,  
        "hard": 1,
        "struggling": 1,
        "enjoy": 0,  
        "love": 0,
        "interesting": 0,
        "boring": 2,  
        "tired": 3,  
        "overwhelmed": 3
    }

    response_index = random.randint(0, len(response_set) - 1)

    for keyword, index in keyword_matches.items():
        if keyword in user_response.lower() and index < len(response_set):
            response_index = index
            break

    buddy_response = response_set[response_index]

    console.print(f"\n[bold yellow]Study Buddy is typing...[/bold yellow]")
    time.sleep(1.5)  
    console.print(f"[bold yellow]Study Buddy:[/bold yellow] {buddy_response}")

    follow_up_questions = [
        f"What else would you like to talk about, {user_name}?",
        f"Is there anything specific about your studies that's on your mind, {user_name}?",
        f"Would you like some advice on study techniques for this topic, {user_name}?",
        f"How can I best support your learning journey today, {user_name}?"
    ]

    continue_chat = Prompt.ask("\nWould you like to continue chatting?", choices=["yes", "no"], default="yes")
    if continue_chat.lower() == "yes":

        console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] {random.choice(follow_up_questions)}")
        chat_with_buddy(profile)
    else:

        goodbyes = [
            f"It was nice chatting with you, {user_name}! Let's study hard together next time!",
            f"I enjoyed our conversation, {user_name}! Remember, I'm always here when you need a study companion.",
            f"Until next time, {user_name}! Keep up the great work with your studies!",
            f"Thanks for the chat, {user_name}! I'll be here whenever you need some company during your study sessions."
        ]

        console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] {random.choice(goodbyes)}")
        time.sleep(1)
        study_buddy(profile)  

def get_pep_talk(profile):

    console.print(Panel("[bold yellow]Personalized Pep Talk from your Study Buddy[/bold yellow]"))

    user_name = profile.get('name', 'friend')

    if 'pep_talks' not in profile:
        profile['pep_talks'] = {
            'count': 0,
            'last_used': None,
            'favorite_messages': []
        }

    profile['pep_talks']['count'] += 1
    profile['pep_talks']['last_used'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    from animations import show_motivational_cat

    standard_pep_talks = [
        f"You're doing amazing, {user_name}! Every minute of study is an investment in your future.",
        f"Remember why you started, {user_name}. Your dedication will pay off in ways you can't even imagine yet.",
        f"It's okay to struggle - that's how we grow. I believe in your ability to overcome any challenge, {user_name}.",
        f"You've got this, {user_name}! Break down big tasks into small steps and celebrate each victory.",
        f"Your brain is getting stronger with every study session, {user_name}. I'm proud of your commitment!",
        f"Studying alone doesn't mean you're alone, {user_name}. I'm here cheering you on every step of the way!",
        f"When you feel like giving up, {user_name}, remember how far you've already come. Progress isn't always visible day to day.",
        f"You're not just studying, {user_name} - you're building your future, one concept at a time.",
        f"It's normal to feel overwhelmed sometimes, {user_name}. Take a deep breath, refocus, and keep going at your pace.",
        f"The fact that you're here studying shows incredible strength and determination, {user_name}. That's something to be proud of!"
    ]

    personalized_pep_talks = []

    if profile.get('preferences', {}).get('study_time_preference') == 'morning':
        personalized_pep_talks.append(f"Your morning study sessions show real dedication, {user_name}! Early birds catch the knowledge worm!")
    elif profile.get('preferences', {}).get('study_time_preference') == 'evening':
        personalized_pep_talks.append(f"Your evening study routine is impressive, {user_name}! The quiet hours can be so productive.")
    elif profile.get('preferences', {}).get('study_time_preference') == 'afternoon':
        personalized_pep_talks.append(f"Afternoon studying works well for you, {user_name}! That's when your brain is warmed up and ready!")

    if profile.get('preferences', {}).get('favorite_subjects', []):
        fav_subject = profile['preferences']['favorite_subjects'][0]
        personalized_pep_talks.append(f"Your passion for {fav_subject} will take you far, {user_name}! Experts are just beginners who never gave up.")

    if profile.get('sessions', []):
        session_count = len(profile['sessions'])
        personalized_pep_talks.append(f"Wow, {user_name}! You've completed {session_count} study sessions. That's impressive dedication!")

    all_pep_talks = personalized_pep_talks + standard_pep_talks

    import random
    if personalized_pep_talks and random.random() < 0.7:  
        selected_talk = random.choice(personalized_pep_talks)
    else:
        selected_talk = random.choice(all_pep_talks)

    show_motivational_cat(user_name, selected_talk, 3)

    helpful = Prompt.ask("\nWas this message helpful?", choices=["very", "somewhat", "not really"], default="somewhat")

    if helpful == "very" and selected_talk not in profile.get('pep_talks', {}).get('favorite_messages', []):
        if 'favorite_messages' not in profile['pep_talks']:
            profile['pep_talks']['favorite_messages'] = []

        profile['pep_talks']['favorite_messages'].append(selected_talk)

        profile['pep_talks']['favorite_messages'] = profile['pep_talks']['favorite_messages'][-5:]
        console.print("[italic]I'll remember you liked this message![/italic]")

    save_buddy_profile(profile)

    another = Prompt.ask("\nWould you like another pep talk?", choices=["yes", "no"], default="yes")
    if another.lower() == "yes":
        get_pep_talk(profile)
    else:

        if profile.get('pep_talks', {}).get('favorite_messages', []) and random.random() < 0.7:  
            farewell = random.choice(profile['pep_talks']['favorite_messages'])
            console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] One more for the road: {farewell}")
        else:
            farewells = [
                f"You're going to do amazing, {user_name}! I believe in you!",
                f"Go show those books who's boss, {user_name}!",
                f"Your potential is limitless, {user_name}. Now go unleash it!",
                f"Remember, {user_name}, every expert was once a beginner. Keep going!"
            ]
            console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] {random.choice(farewells)}")

        time.sleep(1)
        study_buddy(profile)  

def virtual_study_session(profile):

    console.print(Panel("[bold yellow]Advanced Virtual Study Session with Buddy[/bold yellow]"))

    user_name = profile.get('name', 'friend')

    if 'sessions' not in profile:
        profile['sessions'] = []

    if 'topics' not in profile:
        profile['topics'] = {}

    suggested_topics = []

    if profile['topics']:

        sorted_topics = sorted(profile['topics'].items(), key=lambda x: (x[1].get('frequency', 0), x[1].get('last_studied', '')), reverse=True)
        suggested_topics = [topic for topic, _ in sorted_topics[:3]]

    if suggested_topics:
        console.print("\n[bold cyan]Based on your history, you might want to study:[/bold cyan]")
        for i, topic in enumerate(suggested_topics, 1):
            console.print(f"[{i}] {topic}")

        use_suggestion = Prompt.ask("Would you like to choose one of these topics?", choices=["yes", "no"], default="yes")

        if use_suggestion.lower() == "yes":
            suggestion_choice = IntPrompt.ask("Select a topic number", choices=[str(i) for i in range(1, len(suggested_topics) + 1)])
            topic = suggested_topics[suggestion_choice - 1]
        else:
            topic = Prompt.ask("[bold]What are you studying?[/bold]")
    else:
        topic = Prompt.ask("[bold]What are you studying?[/bold]")

    suggested_duration = 25  

    if topic in profile['topics'] and 'avg_duration' in profile['topics'][topic]:
        suggested_duration = profile['topics'][topic]['avg_duration']

    while True:
        try:
            duration = IntPrompt.ask(
                f"[bold]How long would you like to study together?[/bold] (in minutes, suggested: {suggested_duration})", 
                default=suggested_duration
            )
            if duration <= 0:
                console.print("[bold red]Duration must be positive![/bold red]")
                continue
            break
        except ValueError:
            console.print("[bold red]Please enter a valid number![/bold red]")

    difficulty = Prompt.ask(
        "[bold]How challenging is this topic for you?[/bold]", 
        choices=["easy", "moderate", "difficult"], 
        default="moderate"
    )

    show_studying_cat(f"Let's study {topic} together, {user_name}!", 2)

    console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] I'll be studying alongside you for the next {duration} minutes, {user_name}.")

    if difficulty == "difficult":
        console.print(f"[bold yellow]Study Buddy:[/bold yellow] This might be challenging, {user_name}, but I believe in you! We'll tackle it together. Remember to break it down into smaller parts.")
    elif difficulty == "easy":
        console.print(f"[bold yellow]Study Buddy:[/bold yellow] Great! Since this is easier for you, {user_name}, let's aim for deep understanding rather than just completion.")
    else:
        console.print(f"[bold yellow]Study Buddy:[/bold yellow] Let's focus together, {user_name}! I'll check in occasionally with some encouragement.")

    from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn

    start_time = datetime.datetime.now()

    easy_encouragements = [
        f"You're cruising through this, {user_name}! Great job!",
        f"Since this is easier for you, try explaining the concepts to solidify your understanding, {user_name}.",
        f"You're making this look easy, {user_name}! Keep up the good pace!",
        f"Excellent progress, {user_name}! Try challenging yourself with some advanced concepts.",
        f"You've got a good grasp on this, {user_name}. Keep building on that foundation!"
    ]

    moderate_encouragements = [
        f"You're doing great, {user_name}! Keep it up!",
        f"I'm right here studying with you, {user_name}!",
        f"Need a quick stretch, {user_name}? It helps with focus.",
        f"Remember to hydrate, {user_name}!",
        f"You're making excellent progress, {user_name}!",
        f"I'm impressed by your focus, {user_name}!",
        f"We're in this together, {user_name}!",
        f"Your dedication is inspiring, {user_name}!",
        f"Just a bit more, you've got this, {user_name}!",
        f"I'm enjoying studying with you, {user_name}!"
    ]

    difficult_encouragements = [
        f"Each step forward is a victory, {user_name}, no matter how small!",
        f"Difficult material builds stronger neural connections, {user_name}. You're literally getting smarter!",
        f"It's okay to struggle, {user_name}. That's how we grow!",
        f"Take a deep breath, {user_name}. Break it down into smaller pieces.",
        f"You can do this, {user_name}! Persistence beats resistance.",
        f"Remember why you started, {user_name}. Your future self will thank you!",
        f"Every expert was once a beginner, {user_name}. Keep going!",
        f"I believe in you, {user_name}! This challenge is making you stronger."
    ]

    if difficulty == "easy":
        encouragements = easy_encouragements
    elif difficulty == "difficult":
        encouragements = difficult_encouragements
    else:
        encouragements = moderate_encouragements

    if profile.get('preferences', {}).get('favorite_subjects', []) and topic in profile['preferences']['favorite_subjects']:
        encouragements.append(f"I know {topic} is one of your favorites, {user_name}! Your enthusiasm makes learning more effective!")

    if profile.get('stats', {}).get('current_streak', 0) > 2:
        streak = profile['stats']['current_streak']
        encouragements.append(f"You're on a {streak}-day study streak, {user_name}! That's impressive consistency!")

    with Progress(
        TextColumn("[bold blue]{task.description}[/bold blue]"),
        BarColumn(),
        TextColumn("{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
    ) as progress:
        task_description = f"Studying {topic} together"
        task = progress.add_task(task_description, total=duration * 60)

        import random
        seconds_passed = 0

        while not progress.finished:
            progress.update(task, advance=1)
            seconds_passed += 1

            if seconds_passed % random.randint(180, 300) == 0 and seconds_passed > 0:
                encouragement = random.choice(encouragements)
                progress.stop()
                console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] {encouragement}")
                time.sleep(2)  
                progress.start()

            time.sleep(1)

    end_time = datetime.datetime.now()
    duration_seconds = (end_time - start_time).total_seconds()
    from utils import format_time
    duration_formatted = format_time(int(duration_seconds))
    actual_minutes = int(duration_seconds / 60)

    if 'study_sessions' not in profile:
        profile['study_sessions'] = []

    session_data = {
        'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'topic': topic,
        'planned_duration': minutes,
        'actual_duration': actual_minutes,
        'difficulty': difficulty,
        'feeling': None  
    }

    if 'stats' not in profile:
        profile['stats'] = {}
    if 'total_study_minutes' not in profile['stats']:
        profile['stats']['total_study_minutes'] = 0
    profile['stats']['total_study_minutes'] += actual_minutes

    if 'topic_frequency' not in profile['stats']:
        profile['stats']['topic_frequency'] = {}
    if topic not in profile['stats']['topic_frequency']:
        profile['stats']['topic_frequency'][topic] = 0
    profile['stats']['topic_frequency'][topic] += 1

    console.print("\n[bold green]Virtual Study Session Complete![/bold green]")
    console.print(f"[bold]Topic:[/bold] {topic}")
    console.print(f"[bold]Time spent studying together:[/bold] {duration_formatted}")

    if profile['stats']['topic_frequency'][topic] == 3:
        console.print(f"[bold magenta]🏆 Achievement Unlocked: {topic} Enthusiast - Studied this topic 3 times![/bold magenta]")
    elif profile['stats']['total_study_minutes'] >= 60 and profile.get('stats', {}).get('total_study_minutes_milestone', 0) < 60:
        console.print("[bold magenta]🏆 Achievement Unlocked: Hour Power - Studied for over an hour total![/bold magenta]")
        profile['stats']['total_study_minutes_milestone'] = 60

    console.print("\n[bold yellow]Study Buddy:[/bold yellow] Great job on our study session! How do you feel?")
    feeling = Prompt.ask("How do you feel after the session?", choices=["Great", "Good", "Okay", "Tired"], default="Good")

    session_data['feeling'] = feeling.lower()
    profile['study_sessions'].append(session_data)

    save_buddy_profile(profile)

    if feeling.lower() == "great":
        console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] That's awesome, {user_name}! Your enthusiasm is contagious!")

        if profile['stats']['topic_frequency'][topic] > 1:
            console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] I've noticed you really enjoy studying {topic}. Your dedication is impressive!")
    elif feeling.lower() == "good":
        console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] I'm glad to hear that, {user_name}! Steady progress is the key to success.")

        if len(profile['stats']['topic_frequency']) > 1 and random.random() < 0.7:
            other_topics = [t for t in profile['stats']['topic_frequency'].keys() if t != topic]
            if other_topics:
                suggested_topic = random.choice(other_topics)
                console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] Since you're interested in {topic}, you might also enjoy studying {suggested_topic} next time!")
    elif feeling.lower() == "okay":
        console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] That's alright, {user_name}. Every study session counts, even the challenging ones.")

        if difficulty == "difficult":
            console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] {topic} can be challenging! Breaking it into smaller parts might help next time.")
        elif profile.get('stats', {}).get('total_study_minutes', 0) > 30:
            console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] You've already put in {profile['stats']['total_study_minutes']} minutes of study time overall. That's something to be proud of!")
    else:  
        console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] Rest is important too, {user_name}! Take care of yourself and we'll study again when you're refreshed.")

        self_care_tips = [
            "Remember to drink water and stretch between study sessions.",
            "A short walk can help refresh your mind before your next study session.",
            "Sometimes a 20-minute power nap can help restore your energy.",
            "Don't forget to eat nutritious snacks to fuel your brain!"
        ]
        console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] {random.choice(self_care_tips)}")

    today = datetime.datetime.now().date()
    if 'last_study_date' not in profile['stats']:
        profile['stats']['last_study_date'] = today.isoformat()
        profile['stats']['current_streak'] = 1
    else:
        last_date = datetime.date.fromisoformat(profile['stats']['last_study_date'])
        delta = (today - last_date).days

        if delta == 0:  
            pass  
        elif delta == 1:  
            profile['stats']['current_streak'] = profile['stats'].get('current_streak', 0) + 1
            profile['stats']['last_study_date'] = today.isoformat()

            if profile['stats']['current_streak'] in [3, 5, 7, 10, 14, 21, 30]:
                console.print(f"\n[bold magenta]🔥 {profile['stats']['current_streak']} Day Streak! Amazing consistency, {user_name}![/bold magenta]")
        else:  
            profile['stats']['current_streak'] = 1
            profile['stats']['last_study_date'] = today.isoformat()

    save_buddy_profile(profile)

    if len(profile.get('study_sessions', [])) > 3:

        topic_counts = profile['stats']['topic_frequency']
        most_studied = max(topic_counts.items(), key=lambda x: x[1])[0] if topic_counts else None

        console.print("\n[bold cyan]Based on your study patterns:[/bold cyan]")

        if most_studied and most_studied != topic:
            console.print(f"- You've studied {most_studied} the most ({topic_counts[most_studied]} times)")

        if profile.get('stats', {}).get('current_streak', 0) > 1:
            console.print(f"- You're on a {profile['stats']['current_streak']}-day study streak! 🔥")

        if profile.get('stats', {}).get('total_study_minutes', 0) > 0:
            console.print(f"- Total study time: {profile['stats']['total_study_minutes']} minutes")

    if len(profile.get('study_sessions', [])) > 2:

        recent_sessions = profile.get('study_sessions', [])[-2:]
        recent_topics = [s['topic'] for s in recent_sessions]
        other_topics = [t for t in profile['stats']['topic_frequency'].keys() if t not in recent_topics]

        if other_topics and random.random() < 0.7:  
            suggested_topic = random.choice(other_topics)
            console.print(f"\n[italic]Would you like to study again? Perhaps revisit {suggested_topic}?[/italic]")
        else:
            console.print("\nWould you like to study together again?")
    else:
        console.print("\nWould you like to study together again?")

    again = Prompt.ask("Enter your choice", choices=["yes", "no"], default="yes")
    if again.lower() == "yes":
        virtual_study_session()
    else:
        console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] It was great studying with you, {user_name}! Let's do it again soon.")
        time.sleep(1)
        study_buddy()  

def share_thoughts():

    profile = load_buddy_profile()
    user_name = profile.get('name', 'friend')

    console.print(Panel(f"[bold yellow]Share Your Thoughts with Study Buddy[/bold yellow]"))
    console.print(f"Sometimes it helps to express what's on your mind, {user_name}. I'm here to listen and support you.")

    from animations import show_listening_cat

    show_listening_cat(user_name, 2)

    if 'thought_sharing' not in profile:
        profile['thought_sharing'] = {'count': 0, 'topics': [], 'last_sentiment': None}

    if profile['thought_sharing']['count'] == 0:
        prompt_message = f"What's on your mind today, {user_name}?"
    else:

        returning_prompts = [
            f"What's on your mind today, {user_name}?",
            f"How are you feeling about your studies today, {user_name}?",
            f"Anything specific you'd like to talk about today, {user_name}?",
            f"I'm here for you again, {user_name}. What would you like to share?"
        ]
        prompt_message = random.choice(returning_prompts)

    console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] {prompt_message}")
    thoughts = Prompt.ask("Share your thoughts (or type 'skip' to go back)")

    if thoughts.lower() == "skip":
        study_buddy()  
        return

    profile['thought_sharing']['count'] += 1

    positive_words = ['good', 'great', 'happy', 'excited', 'love', 'enjoy', 'success', 'accomplished', 'proud']
    negative_words = ['bad', 'sad', 'anxious', 'worried', 'stress', 'difficult', 'hard', 'struggle', 'overwhelm', 'confus']
    neutral_words = ['okay', 'fine', 'alright', 'so-so', 'neutral', 'average']

    positive_count = sum(1 for word in positive_words if word in thoughts.lower())
    negative_count = sum(1 for word in negative_words if word in thoughts.lower())
    neutral_count = sum(1 for word in neutral_words if word in thoughts.lower())

    if positive_count > negative_count:
        sentiment = 'positive'
    elif negative_count > positive_count:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    profile['thought_sharing']['last_sentiment'] = sentiment

    positive_responses = [
        f"I'm so glad to hear that positivity in your voice, {user_name}! Your optimism is inspiring.",
        f"That's wonderful to hear, {user_name}! Holding onto that positive energy will help you in your studies.",
        f"Your positive outlook is one of your strengths, {user_name}. It will take you far!",
        f"I love hearing you so upbeat, {user_name}! That energy is contagious."
    ]

    neutral_responses = [
        f"Thank you for sharing that with me, {user_name}. It takes courage to express your thoughts.",
        f"I appreciate you opening up, {user_name}. Remember that your feelings are valid.",
        f"It sounds like you've been thinking deeply about this, {user_name}. That's a strength.",
        f"I'm glad you felt comfortable sharing that with me, {user_name}. You're not alone in your journey.",
        f"Thank you for trusting me with your thoughts, {user_name}. That's what study buddies are for!"
    ]

    negative_responses = [
        f"I hear that you're facing some challenges, {user_name}. Remember that difficult moments are often opportunities for growth.",
        f"It's okay to feel this way, {user_name}. Acknowledging these feelings is the first step toward working through them.",
        f"Thank you for being honest about how you're feeling, {user_name}. Would it help to break down what's troubling you into smaller pieces?",
        f"I'm here for you during the tough times too, {user_name}. Sometimes just expressing these feelings can help lighten the load."
    ]

    console.print("\n[bold yellow]Study Buddy is thinking...[/bold yellow]")
    time.sleep(1.5)  

    if sentiment == 'positive':
        response = random.choice(positive_responses)
    elif sentiment == 'negative':
        response = random.choice(negative_responses)
    else:
        response = random.choice(neutral_responses)

    console.print(f"[bold yellow]Study Buddy:[/bold yellow] {response}")

    study_topics = ['math', 'science', 'history', 'english', 'language', 'programming', 'physics', 'chemistry', 'biology', 
                   'literature', 'writing', 'reading', 'exam', 'test', 'assignment', 'project', 'homework']

    mentioned_topics = [topic for topic in study_topics if topic in thoughts.lower()]

    if mentioned_topics:
        if 'topics' not in profile['thought_sharing']:
            profile['thought_sharing']['topics'] = []
        profile['thought_sharing']['topics'].extend(mentioned_topics)

        profile['thought_sharing']['topics'] = list(set(profile['thought_sharing']['topics']))

    save_buddy_profile(profile)

    if sentiment == 'negative':
        console.print("\n[bold yellow]Study Buddy:[/bold yellow] Would you like some specific advice or just want to talk more about how you're feeling?")
        follow_up = Prompt.ask("Choose an option", choices=["Get advice", "Talk more", "Go back"], default="Get advice")

        if follow_up == "Talk more":
            console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] I'm here for you, {user_name}. Please tell me more.")
            more_thoughts = Prompt.ask("Share more of your thoughts")
            console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] Thank you for continuing to share, {user_name}. Remember that challenges are temporary, and I believe in your ability to overcome them.")
            time.sleep(1)
            share_thoughts()  
        elif follow_up == "Get advice":

            advice_topics = [
                "Study motivation",
                "Dealing with stress",
                "Improving focus",
                "Time management",
                "Self-care during studying"
            ]

            if mentioned_topics:
                for topic in mentioned_topics:
                    if topic in ['stress', 'anxious', 'worried', 'overwhelm']:
                        advice_topics.insert(0, "Managing study anxiety")  
                    elif topic in ['focus', 'concentrate', 'distract']:
                        advice_topics.insert(0, "Concentration techniques")  
    else:  
        console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] Would you like to share anything else or get some advice, {user_name}?")
        follow_up = Prompt.ask("Choose an option", choices=["Share more", "Get advice", "Go back"], default="Go back")

        if follow_up == "Share more":
            share_thoughts()  
            return
        elif follow_up == "Get advice":

            advice_topics = [
                "Study motivation",
                "Dealing with stress",
                "Improving focus",
                "Time management",
                "Self-care during studying"
        ]

        if profile.get('stats', {}).get('current_streak', 0) > 3:
            advice_topics.append("Maintaining study streaks")

        if profile.get('stats', {}).get('total_study_minutes', 0) > 60:
            advice_topics.append("Advancing your study techniques")

        if profile.get('thought_sharing', {}).get('count', 0) > 3:
            advice_topics.append("Journaling for academic success")

        console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] What kind of advice would you like, {user_name}?")

        for i, topic in enumerate(advice_topics, 1):
            console.print(f"[{i}] {topic}")

        topic_choice = IntPrompt.ask("Select a topic", choices=[str(i) for i in range(1, len(advice_topics) + 1)])
        selected_topic = advice_topics[topic_choice - 1]

        advice = {
            "Study motivation": f"Remember your 'why', {user_name} - the reason you started studying this subject. Connect your current task to your bigger goals. Also, try the 5-minute rule: commit to just 5 minutes of study, and often you'll find yourself continuing naturally.",

            "Dealing with stress": f"Take deep breaths when you feel overwhelmed, {user_name}. Break large tasks into smaller, manageable chunks. Remember that perfect understanding isn't always necessary - progress matters more than perfection.",

            "Improving focus": f"Try the Pomodoro technique, {user_name} - 25 minutes of focused study followed by a 5-minute break. Remove distractions from your environment, and consider using background sounds like white noise or lo-fi music.",

            "Time management": f"Prioritize tasks using the Eisenhower matrix (urgent/important), {user_name}. Schedule specific study blocks in your day rather than vague intentions to study. Remember to include buffer time between tasks.",

            "Self-care during studying": f"Stay hydrated and keep healthy snacks nearby, {user_name}. Take short movement breaks to refresh your mind. Ensure you're getting enough sleep - it's when your brain consolidates what you've learned.",

            "Managing study anxiety": f"Study anxiety is common, {user_name}. Try breaking down what's causing your anxiety into specific concerns. Is it a particular subject? A deadline? Once identified, we can address each concern specifically. Writing down your worries on paper can help get them out of your head.",

            "Concentration techniques": f"For better concentration, {user_name}, try the 'environment reset' technique: change your study location when focus wanes. Also, use noise-cancelling headphones or background sounds that mask distractions. Before starting, write down exactly what you plan to accomplish in the next 30 minutes.",

            "Maintaining study streaks": f"You're on an impressive {profile.get('stats', {}).get('current_streak', 0)}-day streak, {user_name}! To maintain momentum, try studying at the same time each day to build a habit. Even just 10 minutes counts - consistency matters more than duration.",

            "Advancing your study techniques": f"Since you've logged over an hour of study time, {user_name}, you might benefit from advanced techniques like spaced repetition or the Feynman Technique. Spaced repetition involves reviewing material at increasing intervals, while the Feynman Technique involves explaining concepts in simple terms as if teaching someone else.",

            "Journaling for academic success": f"You've shared your thoughts with me {profile['thought_sharing'].get('count', 0)} times now, {user_name}. Consider keeping a learning journal where you reflect on what you've learned, questions you have, and connections to other subjects. This reflection deepens understanding and retention."
        }

        if selected_topic == "Study motivation" and profile.get('stats', {}).get('topic_frequency', {}):
            favorite_subject = max(profile['stats']['topic_frequency'].items(), key=lambda x: x[1])[0] if profile['stats']['topic_frequency'] else None
            if favorite_subject:
                advice["Study motivation"] += f"\n\nI've noticed you enjoy studying {favorite_subject}! Try connecting other subjects to this interest to boost your motivation."

        elif selected_topic == "Time management" and profile.get('study_sessions', []):
            avg_duration = sum(s.get('actual_duration', 0) for s in profile['study_sessions']) / len(profile['study_sessions'])
            advice["Time management"] += f"\n\nBased on your history, your average study session is about {int(avg_duration)} minutes. Consider planning your tasks in {int(avg_duration)}-minute blocks to match your natural rhythm."

        console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] Here's some advice on {selected_topic}:")
        console.print(f"\n[italic cyan]{advice[selected_topic]}[/italic cyan]")

        tips = {
            "Study motivation": "🌟 Tip: Create a visual progress tracker for your studies. Seeing your progress can be highly motivating!",
            "Dealing with stress": "🧘 Tip: Try the 4-7-8 breathing technique: Inhale for 4 seconds, hold for 7, exhale for 8.",
            "Improving focus": "🎧 Tip: Studies show that certain types of music, like instrumental or nature sounds, can enhance focus for some people.",
            "Time management": "⏱️ Tip: The 2-minute rule: If a task takes less than 2 minutes, do it immediately rather than scheduling it.",
            "Self-care during studying": "👁️ Tip: Follow the 20-20-20 rule to reduce eye strain: Every 20 minutes, look at something 20 feet away for 20 seconds."
        }

        if selected_topic in tips:
            console.print(f"\n[bold green]{tips[selected_topic]}[/bold green]")

        if 'advice_history' not in profile:
            profile['advice_history'] = []

        profile['advice_history'].append({
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            'topic': selected_topic
        })
        save_buddy_profile(profile)

        time.sleep(1)
        console.print(f"\n[bold yellow]Study Buddy:[/bold yellow] I hope that helps, {user_name}! Remember, you're doing great.")

    time.sleep(1)
    study_buddy()

def display_session_stats_widget():

    sessions = list_sessions()

    total_sessions = len(sessions)
    total_minutes = 0
    current_streak = 0
    last_date = None
    topics_studied = set()
    achievements = []

    session_dates = []
    for filename in sessions:
        session_data = read_session(filename)
        if session_data and 'date' in session_data:
            session_dates.append(session_data['date'])
            total_minutes += session_data.get('duration', 0)

            if 'topic' in session_data:
                topics_studied.add(session_data['topic'])

    session_dates.sort(reverse=True)

    from datetime import datetime, timedelta

    if session_dates:
        try:

            try:
                last_date = datetime.strptime(session_dates[0], "%Y-%m-%d")
            except ValueError:

                last_date = datetime.strptime(session_dates[0], "%Y-%m-%d %H:%M:%S")

            current_date = datetime.now().date()
            last_session_date = last_date.date()

            if current_date == last_session_date or current_date - last_session_date == timedelta(days=1):
                current_streak = 1

                for i in range(1, len(session_dates)):
                    try:
                        try:
                            date = datetime.strptime(session_dates[i], "%Y-%m-%d").date()
                        except ValueError:
                            date = datetime.strptime(session_dates[i], "%Y-%m-%d %H:%M:%S").date()

                        if last_session_date - date == timedelta(days=current_streak):
                            current_streak += 1
                        else:
                            break
                    except ValueError:

                        continue
        except Exception:

            pass

    if total_sessions >= 10:
            achievements.append("+ Study Master: Completed 10+ sessions")
    if total_minutes >= 500:
        achievements.append("* Time Wizard: Studied for 500+ minutes")
    if current_streak >= 3:
        achievements.append("^ Consistency King: 3+ day streak")
    if len(topics_studied) >= 3:
        achievements.append("^ Knowledge Explorer: Studied 3+ topics")

    stats_table = Table(box=ROUNDED, border_style="cyan", show_header=False)
    stats_table.add_column("Stat", style="bold cyan")
    stats_table.add_column("Value")

    stats_table.add_row("📊 Total Sessions", f"[bold]{total_sessions}[/bold]")
    stats_table.add_row("⏱️ Total Study Time", f"[bold]{total_minutes}[/bold] minutes")
    stats_table.add_row("🔥 Current Streak", f"[bold]{current_streak}[/bold] days")
    stats_table.add_row("📚 Topics Studied", f"[bold]{len(topics_studied)}[/bold]")

    if last_date:
        try:
            stats_table.add_row("📅 Last Session", f"[bold]{last_date.strftime('%Y-%m-%d')}[/bold]")
        except Exception:

            stats_table.add_row("📅 Last Session", f"[bold]Recently[/bold]")

    stats_panel = Panel(
        Align.center(stats_table),
        title="[bold]Your Study Stats[/bold]",
        border_style="green",
        box=ROUNDED
    )

    console.print(stats_panel)

    if achievements:
        achievements_panel = Panel(
            "\n".join(achievements),
            title="[bold]🏆 Achievements Unlocked[/bold]",
            border_style="yellow",
            box=ROUNDED
        )
        console.print(achievements_panel)

def display_study_goals():

    import os
    import json
    from datetime import datetime

    goals_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "goals.json")

    if not os.path.exists(goals_file):
        return

    try:
        with open(goals_file, "r") as f:
            goals_data = json.load(f)

        if not goals_data or not goals_data.get("goals"):
            return

        current_date = datetime.now().date()

        goals_table = Table(box=ROUNDED)
        goals_table.add_column("Goal", style="bold cyan")
        goals_table.add_column("Target", style="bold")
        goals_table.add_column("Deadline", style="bold")
        goals_table.add_column("Progress", style="bold")

        sessions = list_sessions()
        total_minutes = 0
        topics_studied = set()
        session_count = len(sessions)

        for filename in sessions:
            session_data = read_session(filename)
            if session_data:
                total_minutes += session_data.get('duration', 0)
                if 'topic' in session_data:
                    topics_studied.add(session_data['topic'])

        for goal in goals_data["goals"]:
            goal_type = goal.get("type")
            target = goal.get("target")
            deadline = goal.get("deadline")

            progress = "0%"
            progress_style = "red"

            if goal_type == "minutes":
                if target > 0:
                    percent = min(100, int((total_minutes / target) * 100))
                    progress = f"{percent}%"
                    if percent >= 100:
                        progress_style = "green"
                    elif percent >= 50:
                        progress_style = "yellow"
            elif goal_type == "sessions":
                if target > 0:
                    percent = min(100, int((session_count / target) * 100))
                    progress = f"{percent}%"
                    if percent >= 100:
                        progress_style = "green"
                    elif percent >= 50:
                        progress_style = "yellow"
            elif goal_type == "topics":
                if target > 0:
                    percent = min(100, int((len(topics_studied) / target) * 100))
                    progress = f"{percent}%"
                    if percent >= 100:
                        progress_style = "green"
                    elif percent >= 50:
                        progress_style = "yellow"

            if goal_type == "minutes":
                display_type = "Study Time"
                display_target = f"{target} minutes"
            elif goal_type == "sessions":
                display_type = "Complete Sessions"
                display_target = f"{target} sessions"
            elif goal_type == "topics":
                display_type = "Study Topics"
                display_target = f"{target} topics"
            else:
                display_type = goal_type
                display_target = str(target)

            goals_table.add_row(
                display_type,
                display_target,
                deadline,
                f"[{progress_style}]{progress}[/{progress_style}]"
            )

        goals_panel = Panel(
            Align.center(goals_table),
            title="[bold]📋 Your Study Goals[/bold]",
            border_style="blue",
            box=ROUNDED
        )

        console.print(goals_panel)
    except Exception as e:

        pass

def set_study_goals():

    import os
    import json
    from datetime import datetime, timedelta

    console.print(Panel(Align.center("[bold cyan]Set Study Goals[/bold cyan]")))

    goals_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "goals.json")

    goals_data = {"goals": []}
    if os.path.exists(goals_file):
        try:
            with open(goals_file, "r") as f:
                goals_data = json.load(f)
        except:
            pass

    if goals_data.get("goals"):
        console.print("[bold]Current Goals:[/bold]")
        for i, goal in enumerate(goals_data["goals"], 1):
            goal_type = goal.get("type")
            target = goal.get("target")
            deadline = goal.get("deadline")

            if goal_type == "minutes":
                display_type = "Study Time"
                display_target = f"{target} minutes"
            elif goal_type == "sessions":
                display_type = "Complete Sessions"
                display_target = f"{target} sessions"
            elif goal_type == "topics":
                display_type = "Study Topics"
                display_target = f"{target} topics"
            else:
                display_type = goal_type
                display_target = str(target)

            console.print(f"[{i}] {display_type}: {display_target} by {deadline}")

    console.print("\n[bold]Goal Management:[/bold]")
    console.print("[1] Add a new goal")
    console.print("[2] Remove a goal")
    console.print("[3] Clear all goals")
    console.print("[4] Return to main menu")

    choice = IntPrompt.ask("\nSelect an option", choices=["1", "2", "3", "4"])

    if choice == 1:

        console.print("\n[bold]Select Goal Type:[/bold]")
        console.print("[1] Study Time (minutes)")
        console.print("[2] Complete Sessions")
        console.print("[3] Study Topics")

        goal_type_choice = IntPrompt.ask("Select goal type", choices=["1", "2", "3"])

        if goal_type_choice == 1:
            goal_type = "minutes"
            target = IntPrompt.ask("Target study minutes", default=500)
        elif goal_type_choice == 2:
            goal_type = "sessions"
            target = IntPrompt.ask("Target number of sessions", default=10)
        elif goal_type_choice == 3:
            goal_type = "topics"
            target = IntPrompt.ask("Target number of topics", default=3)

        default_deadline = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        deadline = Prompt.ask("Deadline (YYYY-MM-DD)", default=default_deadline)

        new_goal = {
            "type": goal_type,
            "target": target,
            "deadline": deadline
        }

        goals_data.setdefault("goals", []).append(new_goal)

        with open(goals_file, "w") as f:
            json.dump(goals_data, f, indent=2)

        console.print("[bold green]Goal added successfully![/bold green]")

    elif choice == 2:

        if not goals_data.get("goals"):
            console.print("[yellow]No goals to remove.[/yellow]")
        else:
            goal_index = IntPrompt.ask(
                "Enter the number of the goal to remove", 
                choices=[str(i) for i in range(1, len(goals_data["goals"]) + 1)]
            )

            goals_data["goals"].pop(int(goal_index) - 1)

            with open(goals_file, "w") as f:
                json.dump(goals_data, f, indent=2)

            console.print("[bold green]Goal removed successfully![/bold green]")

    elif choice == 3:

        from rich.prompt import Confirm

        if Confirm.ask("Are you sure you want to clear all goals?", default=False):
            goals_data["goals"] = []

            with open(goals_file, "w") as f:
                json.dump(goals_data, f, indent=2)

            console.print("[bold green]All goals cleared![/bold green]")

    time.sleep(1)

def start_session():

    console.print(Panel("[bold cyan]Start Study Session[/bold cyan]"))

    topic = Prompt.ask("[bold]Topic[/bold] (e.g., 'Physics - Chapter 2')")
    goal = Prompt.ask("[bold]Goal[/bold] (What do you aim to accomplish?)")

    while True:
        try:
            duration = IntPrompt.ask("[bold]Total Duration[/bold] (in minutes)", default=60)
            if duration <= 0:
                console.print("[bold red]Duration must be positive![/bold red]")
                continue
            break
        except ValueError:
            console.print("[bold red]Please enter a valid number![/bold red]")

    while True:
        try:
            break_interval = IntPrompt.ask("[bold]Break Interval[/bold] (in minutes)", default=25)
            if break_interval <= 0 or break_interval > duration:
                console.print("[bold red]Break interval must be positive and less than total duration![/bold red]")
                continue
            break
        except ValueError:
            console.print("[bold red]Please enter a valid number![/bold red]")

    from rich.prompt import Confirm
    capture_concepts = Confirm.ask("Would you like to capture key concepts during breaks?", default=True)

    session = StudySession(topic, goal, duration, break_interval, capture_concepts)
    session.start()

def start_pomodoro_session():

    from utils import PomodoroTimer
    from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn
    from rich.prompt import Confirm
    from rich.table import Table

    console.print(Panel("[bold cyan]Start Pomodoro Study Session[/bold cyan]"))

    topic = Prompt.ask("[bold]Topic[/bold] (e.g., 'Physics - Chapter 2')")
    goal = Prompt.ask("[bold]Goal[/bold] (What do you aim to accomplish?)")

    console.print("\n[bold]Pomodoro Settings[/bold] (Leave blank for defaults)")

    while True:
        try:
            work_minutes = IntPrompt.ask("[bold]Work interval[/bold] (in minutes)", default=25)
            if work_minutes <= 0:
                console.print("[bold red]Duration must be positive![/bold red]")
                continue
            break
        except ValueError:
            console.print("[bold red]Please enter a valid number![/bold red]")

    while True:
        try:
            short_break = IntPrompt.ask("[bold]Short break[/bold] (in minutes)", default=5)
            if short_break <= 0:
                console.print("[bold red]Duration must be positive![/bold red]")
                continue
            break
        except ValueError:
            console.print("[bold red]Please enter a valid number![/bold red]")

    while True:
        try:
            long_break = IntPrompt.ask("[bold]Long break[/bold] (in minutes)", default=15)
            if long_break <= 0:
                console.print("[bold red]Duration must be positive![/bold red]")
                continue
            break
        except ValueError:
            console.print("[bold red]Please enter a valid number![/bold red]")

    while True:
        try:
            intervals = IntPrompt.ask("[bold]Work intervals before long break[/bold]", default=4)
            if intervals <= 0:
                console.print("[bold red]Number must be positive![/bold red]")
                continue
            break
        except ValueError:
            console.print("[bold red]Please enter a valid number![/bold red]")

    while True:
        try:
            total_intervals = IntPrompt.ask("[bold]Total work intervals to complete[/bold]", default=8)
            if total_intervals <= 0:
                console.print("[bold red]Number must be positive![/bold red]")
                continue
            break
        except ValueError:
            console.print("[bold red]Please enter a valid number![/bold red]")

    capture_concepts = Confirm.ask("Would you like to capture key concepts during long breaks?", default=True)

    pomodoro = PomodoroTimer(work_minutes, short_break, long_break, intervals)

    start_time = datetime.datetime.now()
    focus_scores = []

    console.print(f"\n[bold green]Starting Pomodoro session: {topic}[/bold green]")
    console.print(Align.center(f"[bold]Goal:[/bold] {goal}"))
    console.print(Align.center(f"[bold]Work interval:[/bold] {work_minutes} minutes"))
    console.print(Align.center(f"[bold]Short break:[/bold] {short_break} minutes"))
    console.print(Align.center(f"[bold]Long break:[/bold] {long_break} minutes"))
    console.print(Align.center(f"[bold]Total work intervals:[/bold] {total_intervals}\n"))

    show_studying_cat("Let's focus with Pomodoro!", 2)

    completed_work_intervals = 0

    while completed_work_intervals < total_intervals:

        interval_type, duration_minutes = pomodoro.get_next_interval_type()

        if interval_type == 'work':
            completed_work_intervals += 1
            console.print(f"\n[bold cyan]Work Interval {completed_work_intervals}/{total_intervals}[/bold cyan]")
            show_studying_cat(f"Focus time! Interval {completed_work_intervals}/{total_intervals}", 1)
        elif interval_type == 'short_break':
            console.print("\n[bold yellow]Short Break![/bold yellow]")
            show_break_cat("Quick break!", 1)
        else:  
            console.print("\n[bold green]Long Break![/bold green]")
            show_break_cat("Time for a longer break!", 1)

            from utils import get_motivational_quote
            quote = get_motivational_quote()
            console.print(Panel(f"[italic cyan]\"{quote}\"[/italic cyan]", border_style="yellow"))

        with Progress(
            TextColumn("[bold blue]{task.description}[/bold blue]"),
            BarColumn(),
            TextColumn("{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
        ) as progress:
            task_description = f"{'Working' if interval_type == 'work' else 'Break'}: {topic}"
            task = progress.add_task(task_description, total=duration_minutes * 60)

            while not progress.finished:
                progress.update(task, advance=1)
                time.sleep(1)

        pomodoro.complete_current_interval()

        if interval_type == 'work':
            while True:
                try:
                    focus_score = IntPrompt.ask(
                        "How focused were you in this work interval?", 
                        choices=["1", "2", "3", "4", "5"]
                    )
                    break
                except ValueError:
                    console.print("[bold red]Please enter a number between 1 and 5![/bold red]")

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            focus_scores.append({
                "timestamp": timestamp,
                "score": focus_score,
                "interval": completed_work_intervals
            })

            console.print(f"Focus score of {focus_score}/5 recorded.")

        if interval_type == 'long_break' and capture_concepts:
            from insights import capture_concepts
            console.print("\n[bold cyan]Learning Insights[/bold cyan]")
            console.print("Let's capture what you've learned so far.")
            capture_concepts(topic, goal)

    end_time = datetime.datetime.now()
    duration_seconds = (end_time - start_time).total_seconds()
    duration_formatted = format_time(int(duration_seconds))

    if focus_scores:
        avg_focus = sum(score["score"] for score in focus_scores) / len(focus_scores)
    else:
        avg_focus = 0

    console.print("\n" + "=" * 50)
    console.print("[bold green]Pomodoro Session Complete![/bold green]")
    console.print(f"[bold]Topic:[/bold] {topic}")
    console.print(f"[bold]Goal:[/bold] {goal}")
    console.print(f"[bold]Total Study Time:[/bold] {duration_formatted}")
    console.print(f"[bold]Completed Work Intervals:[/bold] {completed_work_intervals}")
    console.print(f"[bold]Average Focus Score:[/bold] {avg_focus:.2f}/5.0")

    if focus_scores:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Interval")
        table.add_column("Timestamp")
        table.add_column("Focus Score")

        for i, score_data in enumerate(focus_scores, 1):
            timestamp = score_data["timestamp"]
            score = score_data["score"]
            table.add_row(str(i), timestamp, f"{score}/5")

        console.print("\n[bold]Focus Scores by Interval:[/bold]")
        console.print(table)

    session_data = {
        "topic": topic,
        "goal": goal,
        "date": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "duration": int(duration_seconds / 60),  
        "session_type": "pomodoro",
        "work_interval": work_minutes,
        "short_break": short_break,
        "long_break": long_break,
        "completed_intervals": completed_work_intervals,
        "actual_duration_seconds": int(duration_seconds),
        "focus_scores": focus_scores,
        "avg_focus": avg_focus
    }

    from logger import save_session
    filename = save_session(session_data)
    console.print(f"\n[bold]Session saved:[/bold] {filename}")
    console.print("=" * 50)

    show_completion_cat("Great job! You completed your Pomodoro session!", 3)

def view_past_sessions():

    console.print(Panel("[bold cyan]View Past Sessions[/bold cyan]"))

    sessions = list_sessions()

    if not sessions:
        console.print("[yellow]No saved sessions found.[/yellow]")
        return

    console.print("[bold]Saved Sessions:[/bold]")
    for i, session_file in enumerate(sessions, 1):
        console.print(f"[{i}] {session_file}")

    while True:
        try:
            choice = IntPrompt.ask(
                "\nSelect a session to view (0 to return to main menu)", 
                default=0
            )

            if choice == 0:
                return

            if 1 <= choice <= len(sessions):
                session_data = read_session(sessions[choice - 1])
                if session_data:
                    display_session_summary(session_data)
                break
            else:
                console.print("[bold red]Invalid selection![/bold red]")
        except ValueError:
            console.print("[bold red]Please enter a valid number![/bold red]")

def display_session_summary(session_data):

    from rich.table import Table

    console.print(Panel(f"[bold cyan]Session Summary: {session_data.get('topic', 'Unknown')}[/bold cyan]"))

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Property")
    table.add_column("Value")

    table.add_row("Topic", session_data.get('topic', 'Unknown'))
    table.add_row("Goal", session_data.get('goal', 'Unknown'))
    table.add_row("Date", session_data.get('date', 'Unknown'))
    table.add_row("Total Duration", f"{session_data.get('duration', 0)} minutes")
    table.add_row("Average Focus Score", f"{session_data.get('avg_focus', 0):.2f}/5.0")

    console.print(table)

    if 'focus_scores' in session_data and session_data['focus_scores']:
        focus_table = Table(show_header=True, header_style="bold magenta")
        focus_table.add_column("Break")
        focus_table.add_column("Timestamp")
        focus_table.add_column("Focus Score")

        for i, score_data in enumerate(session_data['focus_scores'], 1):
            timestamp = score_data.get('timestamp', 'Unknown')
            score = score_data.get('score', 0)
            focus_table.add_row(str(i), timestamp, f"{score}/5")

        console.print("\n[bold]Focus Scores by Break:[/bold]")
        console.print(focus_table)

    Prompt.ask("\nPress Enter to return to the list")

def view_weekly_stats():

    console.print(Panel(Align.center("[bold cyan]Weekly Stats[/bold cyan]")))

    show_loading_animation("Generating stats", 1)

    stats = generate_weekly_stats()
    if not stats:
        console.print("[yellow]Not enough data to generate weekly stats.[/yellow]")

    Prompt.ask("\nPress Enter to return to the main menu")

def view_learning_insights():

    console.print(Panel(Align.center("[bold cyan]Learning Insights[/bold cyan]")))

    sessions = list_sessions()
    topics = set()

    for filename in sessions:
        session_data = read_session(filename)
        if session_data and 'topic' in session_data:
            topics.add(session_data['topic'])

    if not topics:
        console.print("[yellow]No study sessions found. Start a session first![/yellow]")
        return

    console.print("\n[bold]Your Study Topics:[/bold]")

    from rich.table import Table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Session")
    table.add_column("Topic")
    table.add_column("Learning Effectiveness")

    for i, topic in enumerate(sorted(topics), 1):
        effectiveness = calculate_learning_effectiveness(topic)

        if effectiveness >= 80:
            color = "green"
        elif effectiveness >= 60:
            color = "yellow"
        elif effectiveness > 0:
            color = "red"
        else:
            color = "white"

        table.add_row(
            str(i),
            topic,
            f"[{color}]{effectiveness}%[/{color}]"
        )

    console.print(table)

    choice = IntPrompt.ask(
        "\nSelect a topic to review concepts (0 to return)", 
        default=0
    )

    if choice == 0:
        return

    if 1 <= choice <= len(topics):
        selected_topic = sorted(topics)[choice - 1]
        reviewed = review_due_concepts(selected_topic)

        if not reviewed:
            console.print(f"[yellow]No concepts due for review for '{selected_topic}'.[/yellow]")
            time.sleep(1)

def view_knowledge_graph():

    console.print(Panel(Align.center("[bold cyan]Knowledge Graph[/bold cyan]")))

    show_loading_animation("Generating knowledge graph", 1)

    display_knowledge_graph()

    Prompt.ask("\nPress Enter to return to the main menu")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Program interrupted. Exiting...[/bold yellow]")
        sys.exit(0)