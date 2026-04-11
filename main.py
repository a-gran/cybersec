import data
import random

LIVES = 3
POINTS = 10


def show_rules():
    print("=" * 50)
    print("   КИБЕРДЕТЕКТИВ: Распознай скам!")
    print("=" * 50)
    print()
    print("Тебе будут показаны сообщения из интернета.")
    print("Определи: это СКАМ или безопасное сообщение?")
    print()
    print(f"Жизни: {LIVES}  |  За правильный ответ: {POINTS} очков")
    print()
    print("  1 — это СКАМ")
    print("  2 — безопасное сообщение")
    print()
    input("Нажми Enter, чтобы начать... ")


def get_choice():
    while True:
        answer = input("Твой ответ (1 или 2): ").strip()
        if answer == "1":
            return True
        elif answer == "2":
            return False
        else:
            print("Введи 1 или 2.")


def final_title(score, total):
    percent = score / (total * POINTS)
    if percent >= 0.8:
        return "КИБЕРДЕТЕКТИВ — отличный результат!"
    elif percent >= 0.5:
        return "ОСТОРОЖНЫЙ ПОЛЬЗОВАТЕЛЬ — неплохо, но есть куда расти."
    else:
        return "НОВИЧОК — не расстраивайся, теперь ты знаешь больше!"


def play():
    show_rules()

    shuffled = data.cases[:]
    random.shuffle(shuffled)

    lives = LIVES
    score = 0
    correct = 0

    for i, case in enumerate(shuffled, 1):
        print()
        print("=" * 50)
        print(f"Вопрос {i}/{len(shuffled)}  |  Жизни: {lives}  |  Счёт: {score}")
        print("=" * 50)
        print()
        print("Сообщение:")
        print(f"  {case['text']}")
        print()

        player = get_choice()

        if player == case["is_scam"]:
            print("ПРАВИЛЬНО!")
            score += POINTS
            correct += 1
        else:
            lives -= 1
            print("НЕПРАВИЛЬНО!")

        print()
        print("Объяснение:", case["explanation"])
        print()

        if lives == 0:
            print("Жизни закончились! Игра окончена.")
            break

        input("Нажми Enter, чтобы продолжить... ")

    print()
    print("=" * 50)
    print("           ИТОГ")
    print("=" * 50)
    print(f"Правильных ответов: {correct} из {len(shuffled)}")
    print(f"Итоговый счёт:      {score} очков")
    print(f"Оставшиеся жизни:   {lives}")
    print()
    print(final_title(score, len(shuffled)))
    print()
    print("Главные признаки скама:")
    print("  - просят пароль или код подтверждения")
    print("  - слишком выгодное предложение (бесплатный приз)")
    print("  - искусственная срочность (только сейчас!)")
    print("  - подозрительные ссылки на незнакомые сайты")
    print("  - просят данные карты или CVV")
    print()


play()
