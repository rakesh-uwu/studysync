
import os
import json
import datetime
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

from logger import create_logs_dir, LOGS_DIR

console = Console()

INSIGHTS_DIR = os.path.join(os.path.dirname(LOGS_DIR), "insights")

SR_INTERVALS = [1, 3, 7, 14, 30, 90]  

class Concept(BaseModel):

    content: str
    topic: str
    created_at: str
    last_reviewed: Optional[str] = None
    next_review: Optional[str] = None
    review_count: int = 0
    retention_level: int = 0  

class TopicInsights(BaseModel):

    topic: str
    concepts: List[Concept] = Field(default_factory=list)
    related_topics: List[str] = Field(default_factory=list)
    last_studied: Optional[str] = None

def create_insights_dir():

    if not os.path.exists(INSIGHTS_DIR):
        os.makedirs(INSIGHTS_DIR)
        console.print(f"[green]Created insights directory: {INSIGHTS_DIR}[/green]")

def get_topic_insights_file(topic):

    safe_topic = "".join(c if c.isalnum() else "_" for c in topic)
    return os.path.join(INSIGHTS_DIR, f"{safe_topic}.json")

def load_topic_insights(topic):

    create_insights_dir()

    file_path = get_topic_insights_file(topic)

    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return TopicInsights(**data)
        except (json.JSONDecodeError, FileNotFoundError):
            pass

    return TopicInsights(topic=topic)

def save_topic_insights(insights):

    create_insights_dir()

    file_path = get_topic_insights_file(insights.topic)

    with open(file_path, 'w') as f:
        json.dump(insights.dict(), f, indent=4)

def capture_concepts(topic, goal):

    console.print(Panel("[bold cyan]Capture Key Concepts[/bold cyan]"))
    console.print("[yellow]What are 1-3 key concepts you learned in this session?[/yellow]")
    console.print("[dim](Press Enter with empty input when done)[/dim]")

    concepts = []
    for i in range(1, 4):
        concept = Prompt.ask(f"[bold]Concept {i}[/bold]", default="")
        if not concept:
            break

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        next_review = (datetime.datetime.now() + 
                      datetime.timedelta(days=SR_INTERVALS[0])).strftime("%Y-%m-%d")

        concepts.append(Concept(
            content=concept,
            topic=topic,
            created_at=now,
            next_review=next_review,
            review_count=0,
            retention_level=0
        ))

    if concepts:
        insights = load_topic_insights(topic)
        insights.concepts.extend(concepts)
        insights.last_studied = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_topic_insights(insights)

        console.print(f"[green]Saved {len(concepts)} concepts for future review![/green]")

    return concepts

def check_concepts_for_review(topic):

    insights = load_topic_insights(topic)

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    due_concepts = []

    for concept in insights.concepts:
        if concept.next_review and concept.next_review <= today:
            due_concepts.append(concept)

    return due_concepts

def review_due_concepts(topic):

    due_concepts = check_concepts_for_review(topic)

    if not due_concepts:
        return False

    console.print(Panel(f"[bold cyan]Concept Review for {topic}[/bold cyan]"))
    console.print(f"[yellow]You have {len(due_concepts)} concepts due for review.[/yellow]")

    insights = load_topic_insights(topic)
    updated = False

    for i, concept in enumerate(due_concepts, 1):
        console.print(f"\n[bold]Concept {i}/{len(due_concepts)}:[/bold]")
        console.print(Panel(concept.content))

        remembered = Prompt.ask(
            "Did you remember this concept?", 
            choices=["y", "n"], 
            default="y"
        ).lower() == "y"

        for j, c in enumerate(insights.concepts):
            if c.content == concept.content and c.created_at == concept.created_at:
                if remembered:
                    c.retention_level = min(5, c.retention_level + 1)
                else:
                    c.retention_level = max(0, c.retention_level - 1)

                c.review_count += 1
                c.last_reviewed = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                interval_idx = min(c.retention_level, len(SR_INTERVALS) - 1)
                next_review = (datetime.datetime.now() + 
                              datetime.timedelta(days=SR_INTERVALS[interval_idx]))
                c.next_review = next_review.strftime("%Y-%m-%d")

                insights.concepts[j] = c
                updated = True
                break

    if updated:
        save_topic_insights(insights)
        console.print("\n[green]Concept review completed and saved![/green]")

    return True

def display_knowledge_graph():

    create_insights_dir()

    insight_files = [f for f in os.listdir(INSIGHTS_DIR) if f.endswith('.json')]

    if not insight_files:
        console.print("[yellow]No insights found to generate knowledge graph.[/yellow]")
        return

    topics = {}
    for file in insight_files:
        try:
            with open(os.path.join(INSIGHTS_DIR, file), 'r') as f:
                data = json.load(f)
                insights = TopicInsights(**data)
                topics[insights.topic] = insights.related_topics
        except (json.JSONDecodeError, FileNotFoundError):
            continue

    if not topics:
        console.print("[yellow]No valid insights found to generate knowledge graph.[/yellow]")
        return

    console.print(Panel("[bold cyan]Knowledge Graph[/bold cyan]"))

    for topic, related in topics.items():
        console.print(f"[bold green]{topic}[/bold green]")
        if related:
            for i, rel in enumerate(related):
                prefix = "└── " if i == len(related) - 1 else "├── "
                console.print(f"  {prefix}[blue]{rel}[/blue]")
        else:
            console.print("  └── [dim](No related topics yet)[/dim]")
        console.print("")

def add_related_topic(topic, related_topic):

    insights = load_topic_insights(topic)

    if related_topic not in insights.related_topics:
        insights.related_topics.append(related_topic)
        save_topic_insights(insights)

        related_insights = load_topic_insights(related_topic)
        if topic not in related_insights.related_topics:
            related_insights.related_topics.append(topic)
            save_topic_insights(related_insights)

def calculate_learning_effectiveness(topic):

    insights = load_topic_insights(topic)

    if not insights.concepts:
        return 0

    total_retention = sum(c.retention_level for c in insights.concepts)
    max_retention = 5 * len(insights.concepts)  

    effectiveness = (total_retention / max_retention) * 100 if max_retention > 0 else 0

    return round(effectiveness, 2)