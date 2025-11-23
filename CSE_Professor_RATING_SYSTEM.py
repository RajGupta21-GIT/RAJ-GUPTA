# Professor Review and Analysis System


import json
import os
import tempfile
import matplotlib.pyplot as plt
import numpy as np

plt.ion() 

DATA_FILE = "professors.json"
professors = {}


def load_data():
    global professors
   
    professors = {}

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(professors, f, indent=4)
    except Exception as e:
        print(f"Error clearing data file: {e}")

def save_data():
    
    dir_name = os.path.dirname(os.path.abspath(DATA_FILE))
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            delete=False,
            dir=dir_name,
            encoding="utf-8"
        ) as tmp:
            json.dump(professors, tmp, indent=4)
            temp_name = tmp.name
        os.replace(temp_name, DATA_FILE)
    except Exception as e:
        print(f"Error saving data: {e}")


def add_professor():
    name = input("Enter professor's name to add: ").strip()
    if name in professors:
        print("Professor already exists.")
    else:
        professors[name] = {"ratings": [], "subject": None}
        save_data()
        print(f"Professor {name} added.")

def rate_professor():
    name = input("Enter professor's name to rate: ").strip()
    if name not in professors:
        print("Professor not found. Please add professor first.")
        return
    if professors[name]["subject"] is None:
        subject = input(f"Enter the subject {name} teaches: ").strip()
        professors[name]["subject"] = subject
    try:
        teaching = float(input("Rate Teaching (0-5): "))
        evaluation = float(input("Rate Evaluation (0-5): "))
        internals = float(input("Rate Internals (0-5): "))
        behavior = float(input("Rate Behavior (0-5): "))
        for val, label in zip(
            [teaching, evaluation, internals, behavior],
            ["Teaching", "Evaluation", "Internals", "Behavior"]
        ):
            if val < 0 or val > 5:
                print(f"{label} rating must be between 0 and 5.")
                return
        overall = (teaching + evaluation + internals + behavior) / 4
        professors[name]["ratings"].append({
            "teaching": teaching,
            "evaluation": evaluation,
            "internals": internals,
            "behavior": behavior,
            "overall": overall
        })
        save_data()
        print(f"Ratings added for Professor {name}, Overall: {overall:.2f}")
    except ValueError:
        print("Invalid input. Please enter numbers for all ratings.")

def edit_rating():
    name = input("Enter professor's name to edit rating: ").strip()
    if name not in professors or len(professors[name]["ratings"]) == 0:
        print("Professor not found or no ratings exist.")
        return
    print(f"Current subject taught by {name}: {professors[name]['subject'] or 'Unknown'}")
    new_subject = input("Enter new subject taught (leave blank to keep unchanged): ").strip()
    if new_subject:
        professors[name]["subject"] = new_subject
        print(f"Subject updated to: {new_subject}")

    print(f"Current ratings for {name}:")
    for i, r in enumerate(professors[name]["ratings"], 1):
        print(
            f"  {i}: Teaching={r['teaching']}, "
            f"Evaluation={r['evaluation']}, "
            f"Internals={r['internals']}, "
            f"Behavior={r['behavior']}, "
            f"Overall={r['overall']:.2f}"
        )
    try:
        index = int(
            input(f"Enter rating position to edit (1 to {len(professors[name]['ratings'])}): ")
        ) - 1
        if 0 <= index < len(professors[name]["ratings"]):
            teaching = float(input("Rate Teaching (0-5): "))
            evaluation = float(input("Rate Evaluation (0-5): "))
            internals = float(input("Rate Internals (0-5): "))
            behavior = float(input("Rate Behavior (0-5): "))
            for val, label in zip(
                [teaching, evaluation, internals, behavior],
                ["Teaching", "Evaluation", "Internals", "Behavior"]
            ):
                if val < 0 or val > 5:
                    print(f"{label} rating must be between 0 and 5.")
                    return
            overall = (teaching + evaluation + internals + behavior) / 4
            professors[name]["ratings"][index] = {
                "teaching": teaching,
                "evaluation": evaluation,
                "internals": internals,
                "behavior": behavior,
                "overall": overall
            }
            save_data()
            print("Rating updated.")
        else:
            print("Invalid rating position.")
    except ValueError:
        print("Invalid input. Please enter valid numbers.")

def display_professors():
    if not professors:
        print("No professors available.")
        return
    for name, data in professors.items():
        subject = data.get("subject") or "Unknown"
        ratings = data.get("ratings", [])
        if ratings:
            avg_teaching = sum(r["teaching"] for r in ratings) / len(ratings)
            avg_evaluation = sum(r["evaluation"] for r in ratings) / len(ratings)
            avg_internals = sum(r["internals"] for r in ratings) / len(ratings)
            avg_behavior = sum(r["behavior"] for r in ratings) / len(ratings)
            avg_overall = sum(r["overall"] for r in ratings) / len(ratings)
        else:
            avg_teaching = avg_evaluation = avg_internals = avg_behavior = avg_overall = 0
        print(f"\nProfessor: {name} (Subject: {subject})")
        print(f"Total Ratings: {len(ratings)}")
        print(
            f"Avg Teaching: {avg_teaching:.2f}, "
            f"Eval: {avg_evaluation:.2f}, "
            f"Internals: {avg_internals:.2f}, "
            f"Behavior: {avg_behavior:.2f}, "
            f"Overall: {avg_overall:.2f}"
        )
        print("All Ratings:")
        for r in ratings:
            print(
                f"  Teaching={r['teaching']}, "
                f"Evaluation={r['evaluation']}, "
                f"Internals={r['internals']}, "
                f"Behavior={r['behavior']}, "
                f"Overall={r['overall']:.2f}"
            )

def plot_ratings_graph():
    if not professors:
        print("No professors to display.")
        return
    labels = []
    averages = []
    for name, data in professors.items():
        ratings = data.get("ratings", [])
        if ratings:
            avg_overall = sum(r["overall"] for r in ratings) / len(ratings)
        else:
            avg_overall = 0
        subject = data.get("subject") or "Unknown"
        labels.append(f"{name}\n({subject})")
        averages.append(avg_overall)
    plt.figure(figsize=(12, 6))
    plt.bar(labels, averages, color='skyblue')
    plt.xlabel('Professors (Subject)')
    plt.ylabel('Average Overall Rating')
    plt.title('Professor Overall Ratings')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 5)
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(2)  
    plt.close()   

def compare_professors():
    if len(professors) < 2:
        print("Not enough professors added to compare.")
        return
    name1 = input("Enter first professor's name to compare: ").strip()
    name2 = input("Enter second professor's name to compare: ").strip()
    if name1 not in professors or name2 not in professors:
        print("One or both professors not found.")
        return
    data1 = professors[name1]
    data2 = professors[name2]

    def avg_metric(data, metric):
        ratings = data.get("ratings", [])
        return sum(r[metric] for r in ratings) / len(ratings) if ratings else 0

    metrics = ["teaching", "evaluation", "internals", "behavior", "overall"]
    avg1 = [avg_metric(data1, m) for m in metrics]
    avg2 = [avg_metric(data2, m) for m in metrics]

    print(f"\nComparison between {name1} and {name2}:")
    for m, v1, v2 in zip(metrics, avg1, avg2):
        print(f"{m.capitalize()}: {name1}={v1:.2f}, {name2}={v2:.2f}")

    labels = ['Teaching', 'Evaluation', 'Internals', 'Behavior', 'Overall']
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width / 2, avg1, width, label=name1, color='lightcoral')
    bars2 = ax.bar(x + width / 2, avg2, width, label=name2, color='lightseagreen')

    ax.set_ylabel('Average Rating')
    ax.set_title('Professor Ratings Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 5)
    ax.legend()

    def autolabel(bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f'{height:.2f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center',
                va='bottom'
            )

    autolabel(bars1)
    autolabel(bars2)

    plt.tight_layout()
    plt.show(block=False)
    plt.pause(2)
    plt.close()   

def main():
    load_data()

    commands = {
        "add": add_professor,
        "rate": rate_professor,
        "edit": edit_rating,
        "show": display_professors,
        "graph": plot_ratings_graph,
        "compare": compare_professors,
        "exit": None,
        "quit": None,
    }

    print("Welcome to Professor Review System!")
    print("Commands:")
    print("  add      - Add a professor")
    print("  rate     - Rate a professor (includes multiple matrices and subject)")
    print("  edit     - Edit a professor's rating (all matrices)")
    print("  show     - Display all professors and detailed ratings")
    print("  graph    - Show professor overall rating graph")
    print("  compare  - Compare two professors on all rating matrices")
    print("  exit     - Exit the program")

    while True:
        user_input = input("\nEnter command: ").strip().lower()

        if user_input in ("exit", "quit"):
            print("Exiting... Goodbye!")
            break
        elif user_input in commands:
            commands[user_input]()
        else:
            print("Unknown command. Please enter one of the listed commands.")


if __name__ == "__main__":
    main()
