from fpdf import FPDF
import csv


def number_from_ticket(ticket: str) -> int:
    return int(ticket[2:6])


def draw_tickets(prizes_file: str = 'prizes.csv', start: int = 1) -> None:
    with open(prizes_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        data = list(reader)
    for i in range(start, len(data)):
        ticket = input(f"{i}-th winning ticket: ")
        if ticket == "exit":
            break
        else:
            data[i][2] = ticket
    with open(prizes_file, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def make_pdf(prizes_file: str = 'prizes.csv', pdf_path: str = 'winning_tickets.pdf') -> None:
    # Make pdf of winning tickets using pypdf2
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Winning tickets", ln=True, align="C")
    with open(prizes_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        data = list(reader)
    for row in data:
        pdf.cell(200, 10, txt=number_from_ticket(row[2]), ln=True, align="C")
    pdf.output(pdf_path)
    print(f"Winning tickets saved to {pdf_path}")


def check_ticket(prizes_file: str = 'prizes.csv') -> None:
    # load csv
    with open(prizes_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        data = list(reader)
    while True:
        ticket = input("Enter the ticket number: ")
        if ticket == "exit":
            break
        for row in data:
            if row[2] == ticket:
                print(f"Ticket {number_from_ticket(ticket)} won {row[0]}: {row[1]}")
                break
        else:
            print(f"Ticket {number_from_ticket(ticket)} did not win")


def generate_prizes(mode, prizes_file='prizes.csv'):
    # generate prizes file
    if mode == 'c':
        # create prizes file
        with open(prizes_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['index', 'prize', 'ticket'])
            i = 1
            while True:
                prize = input('Enter the prize: ')
                if prize == 'exit':
                    break
                writer.writerow([i, prize, None])
                i += 1

    elif mode == 'a':
        # edit prizes file
        with open(prizes_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            reader = csv.reader(file)
            i = file.readlines()[-1].split(',')[0]
            while True:
                prize = input('Enter the prize: ')
                if prize == 'exit':
                    break
                i += 1
                writer.writerow([i, prize])

    elif mode == 'e':
        # edit prizes file
        with open(prizes_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)
        while True:
            i = input('Enter the index: ')
            if i == 'exit':
                break
            prize = input('Enter the prize: ')
            for row in data:
                if row[0] == i:
                    row[1] = prize
        with open(prizes_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    else:
        print('Invalid mode')
        return
