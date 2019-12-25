import fire
import numpy as np
import requests
import re


def create_tickets(random_seed=np.random.randint((2**32 - 1)), n_tickets=50, n_questions_in_ticket=4, questions_url="https://docs.google.com/document/u/2/export?format=txt&id=1lzrt7C0kPGoks3IvuirrBbBHFl2DGrFfxfC4oXU0dcw"):
    np.random.seed(int(random_seed))
    r = requests.get(questions_url)
    text = r.text
    lectures = [lecture.strip() for lecture in re.split(u"Лекция.+$", text, flags=re.MULTILINE)]
    lectures = lectures[1:]
    
    print(f"Количество лекций:{len(lectures)}")
    questions = [parse_questions(lecture) for lecture in lectures]
    for i, question_set in enumerate(questions, 1):
        print(f"Лекция {i}: {len(question_set)} вопросов")
        for j, question in enumerate(question_set, 1):
            print(f"Вопрос {j}: {question}")

    tickets = generate_tickets(questions, n_questions_in_ticket, n_tickets)
    print_tickets(tickets)    


def parse_questions(lecture):
    return [q.strip() for q in re.split("^\s*[0-9]+.\s", lecture, flags=re.MULTILINE) if q.strip()]


def generate_tickets(questions, n_questions_in_ticket, n_tickets):
    tickets = set([])
    while len(tickets) < n_tickets:
        selected_lectures = np.random.choice(questions, size=n_questions_in_ticket)
        ticket = []
        for lecture in selected_lectures:
            ticket.append(np.random.choice(lecture))
        ticket = tuple(sorted(set(ticket)))
        if len(ticket)==n_questions_in_ticket:
            tickets.add(ticket)
    return tickets


def print_tickets(tickets):
    print("\n\n")
    for i, ticket in enumerate(tickets, 1):
        print(f"Билет №{i}")
        for j, question in enumerate(ticket, 1):
            print(f"{j}. {question}")

        print("\n\n")


if __name__ == "__main__":
    fire.Fire(create_tickets)

