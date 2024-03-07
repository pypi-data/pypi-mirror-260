import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont
from PyPDF2 import PdfMerger
import os
import pkg_resources



# Dimensions of A4 paper in mm
A4_WIDTH = 210
A4_HEIGHT = 297

# Margin in mm
MARGIN = 10

# Grid dimensions
GRID_WIDTH = 5
GRID_HEIGHT = 5

DPI = 500

MM_TO_INCH = 0.0393701

YEAR = 2024

# Calculate the available width and height for the grid
available_width = A4_WIDTH - 2 * MARGIN
available_height = A4_HEIGHT - 2 * MARGIN

# Calculate cell dimensions
cell_width = available_width / GRID_WIDTH
cell_height = available_height / GRID_HEIGHT

def ean_gen(year: int, start: int, stop: int) -> list[str]:
    ean = []
    for i in range(start, stop + 1):
        ean.append(str(year)[2:] + str(i).zfill(4) + "0")

    return ean


def generate_ean(ean: list[str]) -> None:
    for i in ean:
        # EAN8 without checksum
        code = barcode.EAN8(i, writer=ImageWriter())
        code.save(f'barcode_{i}')


def create_ticket(ean: str, style: str, year:int=YEAR) -> Image:
    image = Image.new('RGB', (int(cell_width * DPI * MM_TO_INCH), int(cell_height * DPI * MM_TO_INCH)), color = (255, 255, 255))
    # Code
    code = Image.open(f'barcode_{ean}.png')
    code = code.resize((int(cell_width * DPI * MM_TO_INCH), int(code.height * (cell_width * DPI * MM_TO_INCH) / code.width)))
    image.paste(code, (0, int(cell_height * DPI * MM_TO_INCH) - code.height))

    # Style
    if os.path.exists(f"{style}.png"):
        top = Image.open(f"{style}.png")
        top = top.resize((int(cell_width * DPI * MM_TO_INCH), int(top.height * (cell_width * DPI * MM_TO_INCH) / top.width)))
        image.paste(top, (0, 0))

    # Text
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("OpenSans-Bold.ttf", 100)

    # Los number
    los = f'Los {int(ean[2:6])}'
    los_width = draw.textlength(los, font=font)
    draw.text((int((cell_width * DPI * MM_TO_INCH - los_width) // 2), 125), los, fill='black', font=font)

    # Logo
    try:
        logo_path = pkg_resources.resource_filename('Tombolenkovac', 'data/logo.png')
    except ModuleNotFoundError:
        location = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        logo_path = os.path.join(location, 'data/logo.png')
    logo = Image.open(logo_path)
    logo = logo.resize((200, 200))
    image.paste(logo, ((int(cell_width * DPI * MM_TO_INCH) // 2 - 310), 350))

    # {year - 1995}. ples MFF UK
    font = ImageFont.truetype("OpenSans-Bold.ttf", 100)
    ples = f'{year - 1995}. ples'
    draw.text((int(cell_width * DPI * MM_TO_INCH) // 2 - 75, 310), ples, fill='black', font=font)
    ples = 'MFF UK'
    draw.text((int(cell_width * DPI * MM_TO_INCH) // 2 - 75, 440), ples, fill='black', font=font)

    return image


def make_A4(year: int, start: int, stop: int, style: str) -> None:
    ean = ean_gen(year, start, stop)
    generate_ean(ean)
    
    # Make A4 grid of tickets
    tickets = []
    for i in ean:
        tickets.append(create_ticket(i, style, year))

    # Create A4 grid
    tickets_grid = Image.new('RGB', (int(A4_WIDTH * DPI * MM_TO_INCH), int(A4_HEIGHT * DPI * MM_TO_INCH)), color = (255, 255, 255))
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            index = i * GRID_WIDTH + j
            if index >= len(tickets):
                break
            tickets_grid.paste(tickets[index], (int(MARGIN * DPI * MM_TO_INCH + j * cell_width * DPI * MM_TO_INCH), int(MARGIN * DPI * MM_TO_INCH + i * cell_height * DPI * MM_TO_INCH)))

    # Add dotted lines to the grid
    draw = ImageDraw.Draw(tickets_grid)
    dotted_color = (150, 150, 150)  # Light gray color
    for i in range(0, GRID_WIDTH + 1):
        for j in range(int(MARGIN * DPI * MM_TO_INCH), int((MARGIN + GRID_HEIGHT * cell_height) * DPI * MM_TO_INCH), 10):
            draw.line([(int((MARGIN + i * cell_width) * DPI * MM_TO_INCH), j), (int((MARGIN + i * cell_width) * DPI * MM_TO_INCH), j+5)], fill=dotted_color)

    for i in range(0, GRID_HEIGHT + 1):
        for j in range(int(MARGIN * DPI * MM_TO_INCH), int((MARGIN + GRID_WIDTH * cell_width) * DPI * MM_TO_INCH), 10):
            draw.line([(j, int((MARGIN + i * cell_height) * DPI * MM_TO_INCH)), (j+5, int((MARGIN + i * cell_height) * DPI * MM_TO_INCH))], fill=dotted_color)
    # Save it as pdf
    tickets_grid.save(f'tickets_{year}_{start}_{stop}.pdf')


def make_tickets(year: int, start: int, stop: int, style: str) -> None:
    # On one page there are 25 tickets
    for i in range(start, stop, 25):
        make_A4(year, i, min(i + 24, stop), style)
        print(f"Page {i // 25 + 1} out of {stop // 25} done")

    concatenate()

    clean()


def concatenate() -> None:
    # Concatenate all the pdfs
    files = os.listdir()
    pdfs = []
    for file in files:
        if file.startswith('tickets_'):
            pdfs.append(file)
    pdfs.sort(key=lambda x: int(x.split('_')[2]))

    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write('tombolenky.pdf')
    merger.close()


def clean() -> None:
    # delete all barcodes in the folder
    files = os.listdir()
    for file in files:
        if file.startswith('barcode_'):
            os.remove(file)
        if file.startswith('ticket_'):
            os.remove(file)
        if file.startswith('tickets_'):
            os.remove(file)
