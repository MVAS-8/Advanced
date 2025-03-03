import pygame
import chess
import chess.engine

# Ініціалізація Pygame
pygame.init()

# Розміри дошки
WIDTH, HEIGHT = 480, 520  # Додаємо місце для тексту
SQUARE_SIZE = 480 // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Шахи")

# Кольори
WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
BLACK = (0, 0, 0)

# Відповідність між позначенням фігур у `python-chess` та назвами файлів у папці
piece_files = {
    "p": "p_1", "r": "r", "n": "n", "b": "b", "q": "q", "k": "k",  # Чорні
    "P": "pw_1", "R": "Rr", "N": "Nn", "B": "Bb", "Q": "Qq", "K": "Kk"  # Білі
}

# Завантаження зображень фігур
pieces = {}
for symbol, filename in piece_files.items():
    image_path = f"images/{filename}.png"
    try:
        pieces[symbol] = pygame.image.load(image_path)
        pieces[symbol] = pygame.transform.scale(pieces[symbol], (SQUARE_SIZE, SQUARE_SIZE))
    except FileNotFoundError:
        print(f"Помилка: Файл {image_path} не знайдено!")

# Шлях до Stockfish
STOCKFISH_PATH = "/opt/homebrew/bin/stockfish"

# Функція для відображення шахової дошки
def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Функція для відображення фігур на дошці
def draw_pieces(board):
    for row in range(8):
        for col in range(8):
            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)
            if piece:
                piece_img = pieces.get(piece.symbol())
                if piece_img:
                    screen.blit(piece_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Функція для виведення тексту
def draw_text(text):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, BLACK)
    screen.fill(WHITE, (0, 480, 480, 40))  # Очистка нижньої панелі
    screen.blit(text_surface, (10, 485))

# Функція для ходу комп'ютера
def ai_move(board):
    try:
        with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
            result = engine.play(board, chess.engine.Limit(time=0.1))
            board.push(result.move)
    except FileNotFoundError:
        print("Помилка: Stockfish не знайдено! Переконайся, що він встановлений і шлях правильний.")

# Основний цикл гри
board = chess.Board()
selected_square = None
running = True
human_turn = True

def check_game_status(board):
    if board.is_checkmate():
        return "Мат! " + ("Гравець виграв" if board.turn == chess.BLACK else "AI виграв")
    elif board.is_check():
        return "Шах!"
    elif board.is_stalemate():
        return "Пат! Нічия"
    return ""

while running:
    draw_board()
    draw_pieces(board)
    status_text = check_game_status(board)
    draw_text(status_text)
    pygame.display.flip()
    
    if not human_turn and not board.is_game_over():
        ai_move(board)
        human_turn = True
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and human_turn and not board.is_game_over():
            x, y = event.pos
            col = x // SQUARE_SIZE
            row = 7 - (y // SQUARE_SIZE)
            square = chess.square(col, row)
            
            if selected_square is None:
                if board.piece_at(square) and board.piece_at(square).color == chess.WHITE:
                    selected_square = square
            else:
                move = chess.Move(selected_square, square)
                if move in board.legal_moves:
                    board.push(move)
                    human_turn = False
                selected_square = None

pygame.quit()