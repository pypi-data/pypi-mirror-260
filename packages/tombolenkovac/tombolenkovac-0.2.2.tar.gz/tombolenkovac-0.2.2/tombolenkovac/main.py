# Make CLI app
#
# It should be runned as "tombolenkovac --gen", "tombolenkovac --draw" or "tombolenkovac --check"
#
# The "tombolenkovac --gen" command should generate a set of tickets and save them to a directory. Also save ticket numbers to a file.
#
# The "tombolenkovac --draw" command should draw winning tickets and save it to a file. Also generate a table of winning tickets as pdf.
#
# The "tombolenkovac --check" command should check if the ticket is winning or not.
#
# The "tombolenkovac --clean" command should clean the directory.
#
# The "tombolenkovac --version" command should print the version of the app.
#
# The "tombolenkovac --help" command should print the help message.


import argparse
import sys
import tombolenkovac.generate as generate
import tombolenkovac.draw as draw

def main() -> None:
    parser = argparse.ArgumentParser(description='Tombolenkovac')
    parser.add_argument('--gen', action='store_true', help='Generate tickets')
    parser.add_argument('--draw', action='store_true', help='Draw winning tickets')
    parser.add_argument('--check', action='store_true', help='Check if the ticket is winning')
    parser.add_argument('--clean', action='store_true', help='Clean the directory')
    parser.add_argument('--version', action='version', version='%(prog)s 0.2.2')
    parser.add_argument('--prizes', action='store_true', help='Create prizes file')
    parser.add_argument('--prize-path', type=str, help='Path to the prizes file', default='prizes.csv')
    parser.add_argument('--pdf-path', type=str, help='Path to the pdf file', default='winning_tickets.pdf')

    args = parser.parse_args()

    if args.gen:
        year = int(input('Enter the year: '))
        start = int(input('Enter the start number: '))
        stop = int(input('Enter the stop number: '))
        style = input('Enter the style: ')
        generate.make_tickets(year, start, stop, style)

    elif args.clean:
        generate.clean()

    elif args.draw:
        start = int(input('Enter the number of first drawn prize (blank from 1): ').strip() or 1)
        draw.draw_tickets(args.prize_path, start)
        draw.make_pdf(args.prize_path, args.pdf_path)

    elif args.check:
        draw.check_ticket('prizes.csv', args.prize_path)

    elif args.prizes:
        mode = input('Enter the mode (c for create, a for append, e for edit, default create): ') or 'c'
        draw.generate_prizes(mode, args.prize_path)

    else:
        print('No command given, try --help for help.')
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    main()
