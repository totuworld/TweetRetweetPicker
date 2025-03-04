import csv
import random
import time
import os

def draw_winners(csv_file, num_winners):
    """
    CSV 파일에서 지정된 수의 당첨자를 무작위로 추첨하고, 시각적 효과와 함께 결과를 출력합니다.
    (두구두구두구 효과와 짠! 하는 결과를 보여주는 방식으로 변경)

    Args:
        csv_file: 당첨자를 추첨할 CSV 파일 경로.
        num_winners: 추첨할 당첨자 수.
    """
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found.")
        return

    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            users = list(reader)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    if not users:
        print("No users found in the CSV file.")
        return

    if num_winners > len(users):
        print(f"Warning: The number of winners ({num_winners}) is greater than the number of users ({len(users)}). Drawing all users.")
        num_winners = len(users)

    print("Drawing winners...")
    time.sleep(1)  # 약간의 시간 지연

    selected_users = []
    for i in range(num_winners):
        print(f"\nDrawing winner {i + 1}...")

        # "두구두구두구" 효과
        print("두구", end="", flush=True)
        time.sleep(0.5)
        print("두구", end="", flush=True)
        time.sleep(0.5)
        print("두구", end="", flush=True)
        time.sleep(0.5)
        print("두구", end="\n", flush=True)
        time.sleep(0.5)

        winner = random.choice(users)
        users.remove(winner)  # 이미 추첨된 사용자를 리스트에서 제거합니다.
        selected_users.append(winner)

        # "짠!" 효과와 함께 결과 출력
        print(f"🎉 짠! Winner {i + 1}: {winner['user_id']} - {winner['nickname']} 🎉")
        time.sleep(0.5)
        

    print("\n🎉🎉🎉 All winners have been drawn! 🎉🎉🎉")
    print("========================")
    for i, user in enumerate(selected_users):
        print(f"{i+1} : {user['user_id']} - {user['nickname']}")
    print("========================")


def main():
    """
    당첨자 추첨을 실행합니다.
    """
    csv_file = 'retweet.csv'  # CSV 파일 경로
    num_winners = 5  # 추첨할 당첨자 수
    draw_winners(csv_file, num_winners)


if __name__ == "__main__":
    main()
