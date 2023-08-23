import tkinter as tk
import json
from difflib import get_close_matches

def load_knowledge_base(knowledge_base: str) -> dict:
    with open(knowledge_base, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

def process_input(entry, text_area, knowledge_base):
    user_input = entry.get()
    text_area.insert(tk.END, "You: " + user_input + "\n")
    entry.delete(0, tk.END)

    if user_input.lower() == "quit":
        root.quit()

    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        text_area.insert(tk.END, "Bot: " + answer + "\n")
    else:
        text_area.insert(tk.END, "Bot: Sorry, I do not understand. Can you teach me?\n")

        def save_new_answer():
            new_answer = entry.get()
            if new_answer.lower() != "skip":
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base("knowledge_base.json", knowledge_base)
                text_area.insert(tk.END, "Bot: Thank you for teaching me!\n")

        save_button = tk.Button(root, text="Save", command=save_new_answer)
        save_button.pack()

root = tk.Tk()
root.title("Chatbot")

knowledge_base = load_knowledge_base("knowledge_base.json")

text_area = tk.Text(root, wrap=tk.WORD)
text_area.pack(expand=True, fill="both")

entry = tk.Entry(root)
entry.pack(expand=True, fill="both")
entry.bind("<Return>", lambda event: process_input(entry, text_area, knowledge_base))

root.mainloop()
