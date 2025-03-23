import random
import os

def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')

def print_board(board):
    """2행 5열 보드를 출력 (빈칸 0은 공백으로 표시)"""
    for i in range(2):
        row = board[5*i:5*i+5]
        print(" ".join(str(x) if x != 0 else " " for x in row))
    print()

def board_to_permutation(board):
    """보드를 읽은 순서(좌측 상단부터 우측 하단)로 하되, 빈칸(0)은 제외한 순열 반환"""
    return [x for x in board if x != 0]

def inversion_count(perm):
    """주어진 순열의 inversion count 계산"""
    inv = 0
    for i in range(len(perm)):
        for j in range(i+1, len(perm)):
            if perm[i] > perm[j]:
                inv += 1
    return inv

def find_empty(board):
    """보드에서 빈칸(0)의 인덱스 반환"""
    return board.index(0)

def possible_moves(board):
    """현재 보드에서 빈칸이 이동할 수 있는 방향과 그 위치(인덱스)를 사전으로 반환"""
    idx = find_empty(board)
    r, c = divmod(idx, 5)
    moves = {}
    if r > 0:
        moves["up"] = idx - 5
    if r < 1:  # 2행이므로 r가 0일 때만 아래로 이동 가능
        moves["down"] = idx + 5
    if c > 0:
        moves["left"] = idx - 1
    if c < 4:
        moves["right"] = idx + 1
    return moves

def move_tile(board, direction):
    """입력된 방향대로 빈칸과 인접 타일을 교환하여 이동"""
    idx = find_empty(board)
    moves = possible_moves(board)
    if direction not in moves:
        return False
    target = moves[direction]
    board[idx], board[target] = board[target], board[idx]
    return True

def is_solved(board):
    """해결 상태: [1,2,3,4,5,6,7,8,9,0]"""
    return board == [1,2,3,4,5,6,7,8,9,0]

def generate_random_board():
    """0부터 9까지 숫자를 랜덤하게 섞어, 빈칸(0)을 제외한 순열의 inversion count가 짝수인 해결 가능한 보드를 반환"""
    board = list(range(10))
    random.shuffle(board)
    def is_solvable(b):
        perm = board_to_permutation(b)
        return inversion_count(perm) % 2 == 0
    while not is_solvable(board):
        random.shuffle(board)
    return board

def main():
    # 초기 보드는 랜덤 생성
    board = generate_random_board()
    goal = [1,2,3,4,5,6,7,8,9,0]

    while True:
        clear_screen()
        print("현재 보드:")
        print_board(board)
        perm = board_to_permutation(board)
        inv = inversion_count(perm)
        print("현재 순열 (빈칸 제외):", perm)
        print("현재 inversion count:", inv, "(짝수)" if inv % 2 == 0 else "(홀수)")
        if is_solved(board):
            print("퍼즐이 해결되었습니다!")
            break
        moves = possible_moves(board)
        print("가능한 이동:", list(moves.keys()))
        direction = input("이동할 방향을 입력하세요 (up, down, left, right): ").strip().lower()
        if direction not in moves:
            input("잘못된 이동입니다. Enter를 눌러 다시 시도하세요...")
            continue
        # 이동 유형에 따른 안내 메시지
        if direction in ["up", "down"]:
            move_type = "수직 이동 (5-cycle 적용: 5-cycle은 4개의 전치로 분해되어 parity 보존)"
        else:
            move_type = "수평 이동 (단순 swap: 빈칸은 순열에 포함되지 않아 parity 변화 없음)"
        print("선택한 이동:", direction, "-", move_type)
        old_inv = inv
        move_tile(board, direction)
        new_perm = board_to_permutation(board)
        new_inv = inversion_count(new_perm)
        print("\n이동 후 보드:")
        print_board(board)
        print("이동 후 순열:", new_perm)
        print("이동 후 inversion count:", new_inv, "(짝수)" if new_inv % 2 == 0 else "(홀수)")
        if old_inv == new_inv:
            print("-> 순열의 parity는 유지되었습니다.")
        else:
            print("-> 경고: 순열의 parity가 변경되었습니다!")
        input("\n다음 이동을 위해 Enter를 누르세요...")

if __name__ == "__main__":
    main()
