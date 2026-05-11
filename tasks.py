import datetime
from greeting import speak

# Nee daily tasks ikkade add cheyyi
TASKS = [
    "Check emails",
    "Apply to 3 jobs on Naukri",
    "Complete JARVIS Day 2 feature",
    "DSA practice — 1 problem",
]

def show_tasks():
    today = datetime.datetime.now().strftime("%A, %B %d")
    print(f"\n--- Today's Tasks ({today}) ---")

    task_text = f"You have {len(TASKS)} tasks today. "
    for i, task in enumerate(TASKS, 1):
        print(f"  {i}. {task}")
        task_text += f"Task {i}: {task}. "

    speak(task_text)

if __name__ == "__main__":
    show_tasks()