import random
import os  

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
}

def play_spin_sound():
    os.system("say Spinning the slots!") 

def play_jackpot_sound():
    os.system("say Jackpot!") 

def check_winnings(columns, lines, bet, symbol_values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            if column[line] != symbol:
                break
        else:
            winnings += bet * symbol_values[symbol]
            winning_lines.append(line + 1)
    return winnings, winning_lines

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, count in symbols.items():
        all_symbols += [symbol] * count

    columns = []
    for _ in range(cols):
        column = random.sample(all_symbols, rows)
        columns.append(column)

    return columns

def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")
        print()

def check_jackpot(slots, winning_lines):
    for line in winning_lines:
        symbol = slots[0][line]
        if all(col[line] == symbol for col in slots) and symbol == "A":
            return True, random.randint(100, 500)
    return False, 0

def deposit():
    while True:
        amount = input("Enter the amount you want to deposit: $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                return amount
            else:
                print("Please enter a valid amount greater than zero.")
        else:
            print("Please enter a valid amount in digits.")

def get_number_of_lines():
    while True:
        lines = input(f"Enter the number of lines to bet on (1 to {MAX_LINES}): ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                return lines
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a valid amount in digits.")

def get_bet():
    while True:
        amount = input("What would you like to bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                return amount
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}.")
        else:
            print("Please enter a number.")

def game(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines
        if total_bet > balance:
            print(f"You do not have enough balance. Your balance is ${balance}, but your total bet is ${total_bet}.")
        else:
            break

    print(f"You are betting ${bet} on {lines} lines. Total bet is ${total_bet}.")
    
    play_spin_sound() 

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)

    jackpot_triggered, jackpot_amount = check_jackpot(slots, winning_lines)
    if jackpot_triggered:
        play_jackpot_sound()  
        print("JACKPOT HIT!")
        print(f"Jackpot Bonus: ${jackpot_amount}")
        winnings += jackpot_amount

    print(f"You won ${winnings}.")
    print(f"Winning lines: {winning_lines}" if winning_lines else "No winning lines this time.")
    
    return winnings - total_bet

def main():
    balance = deposit()
    while True:
        print(f"\nCurrent balance: ${balance}")
        if balance <= 0:
            print("You have no balance left. Please deposit more money to continue playing.")
            break
        
        play = input("Press enter to play (or type 'q' to quit): ")
        if play.lower() == 'q':
            print(f"You left with ${balance}. Thanks for playing!")
            break
        
        balance += game(balance)

main()