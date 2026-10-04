import json
import os
import random
import time

# Sample sentences for typing tests
PARAGRAPHS = [
    "Python is an interpreted high-level general-purpose programming language.",
    "Developing scalable applications requires a clean architecture and efficient algorithms.",
    "Object oriented programming helps structure software into reusable code blueprints.",
    "Artificial intelligence and machine learning are transforming modern software engineering.",
    "Consistency and daily practice are the keys to mastering typing speed and accuracy.",
]

SCORE_FILE = "scores.json"


def load_scores():
    """Load previous test scores from JSON file."""
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def save_score(score_entry):
    """Save the current test score to JSON file."""
    scores = load_scores()
    scores.append(score_entry)
    # Keep top 5 scores based on Net WPM
    scores = sorted(scores, key=lambda x: x["net_wpm"], reverse=True)[:5]
    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f, indent=4)


def display_leaderboard():
    """Display the top 5 high scores."""
    scores = load_scores()
    print("\n" + "=" * 40)
    print("         TOP 5 LEADERBOARD         ")
    print("=" * 40)
    if not scores:
        print("No scores recorded yet. Be the first!")
    else:
        print(f"{'Rank':<6}{'Name':<12}{'Net WPM':<10}{'Accuracy':<10}")
        print("-" * 40)
        for idx, entry in enumerate(scores, 1):
            print(
                f"{idx:<6}{entry['player']:<12}{entry['net_wpm']:<10.1f}{entry['accuracy']:<10.1f}%"
            )
    print("=" * 40 + "\n")


def calculate_metrics(target_text, typed_text, elapsed_time):
    """Calculate Gross WPM, Accuracy, and Net WPM."""
    minutes = elapsed_time / 60.0

    # standard standard WPM formula: (total characters typed / 5) / time_in_minutes
    gross_wpm = (len(typed_text) / 5) / minutes if minutes > 0 else 0

    # Count correct characters
    correct_chars = sum(
        1
        for t_char, input_char in zip(target_text, typed_text)
        if t_char == input_char
    )

    accuracy = (correct_chars / len(target_text)) * 100 if target_text else 0
    net_wpm = gross_wpm * (accuracy / 100)

    return round(gross_wpm, 1), round(accuracy, 1), round(net_wpm, 1)


def run_typing_test():
    """Execute a single typing test session."""
    player_name = input("Enter your name: ").strip() or "Anonymous"
    target_text = random.choice(PARAGRAPHS)

    print("\n--- GET READY ---")
    print("Type the following sentence as quickly and accurately as you can:\n")
    print(f'"{target_text}"\n')

    input("Press ENTER when you are ready to start...")
    print("\n3... 2... 1... GO!\n")

    start_time = time.time()
    typed_text = input("Your Typing: ").strip()
    end_time = time.time()

    elapsed_time = end_time - start_time

    gross_wpm, accuracy, net_wpm = calculate_metrics(
        target_text, typed_text, elapsed_time
    )

    print("\n" + "*" * 30)
    print("         TEST RESULTS         ")
    print("*" * 30)
    print(f"Time Taken  : {round(elapsed_time, 2)} seconds")
    print(f"Gross Speed : {gross_wpm} WPM")
    print(f"Accuracy    : {accuracy}%")
    print(f"Net Speed   : {net_wpm} WPM")
    print("*" * 30)

    score_entry = {
        "player": player_name,
        "net_wpm": net_wpm,
        "accuracy": accuracy,
        "time": round(elapsed_time, 2),
    }

    save_score(score_entry)


def main():
    """Main menu loop."""
    while True:
        print("\n=== PYTHON TYPING SPEED TEST ===")
        print("1. Start Typing Test")
        print("2. View Leaderboard")
        print("3. Exit")

        choice = input("\nSelect an option (1-3): ").strip()

        if choice == "1":
            run_typing_test()
        elif choice == "2":
            display_leaderboard()
        elif choice == "3":
            print("\nThanks for playing! Goodbye.")
            break
        else:
            print("Invalid selection. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
