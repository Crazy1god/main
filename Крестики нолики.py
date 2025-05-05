def  print_board(board):
    """Функция отражающего текущего игрового поля"""
    print("\n")
    for row in board:
        print(" | ".join(row))
        print(" - " * 4)
    print("\n")

def check_winner(broard):
    """Функция проверки состояние игры"""
    for row in broard:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            return row[0]

    for col in range(3):
        if broard[0][col] == broard[1][col] == broard[2][col] and broard[0][col] != ' ':
            return broard[0][col]

    if broard[0][0] == broard[1][1] == broard[2][2] and broard[0][0] != ' ':
        return broard[0][0]
    if broard[0][2] == broard[1][1] == broard[2][0] and broard[0][2] != ' ':
        return broard[0][2]

    if all(cell != ' ' for row in broard for cell in row):
        return 'N'

    return None

def is_valid_input(move):
    """Проверка корректности ввода пользователем"""
    try:
        x, y = map(int, move.split())
        return  0 <= x <= 3 and 0 <= y < 3
    except ValueError:
        return False

def main():
    """Основная функция для включение игры"""
    board = [[' ' for _ in range(4)]for _ in range(3)]
    current_pleyer = 'X'

    while True:
        print_board(board)
        move = input(f"Игрок {current_pleyer}, введите ваши координаты (строка и столбец через пробел)")

        if not is_valid_input(move):
            print("Некорректный ввод. Пожалуйста, введите координаты в формате 'строка столбец'.")
            continue

        x, y = map(int, move.split())

        if board[x][y] != ' ':
            print("Эта клетка уже занята. Попробуйте снова.")
            continue

        board[x][y] = current_pleyer
        winner = check_winner(board)

        if winner:
            print_board(board)
            if winner == 'N':
                print("Игра завершилась ничьей!")
            else:
                print(f"Игрок {winner} выиграл!")
            break

        current_pleyer = 'O' if current_pleyer == 'X' else 'X'

if __name__ == "__main__":
    main()