# Берём список признаков скама из config — он нужен для вывода в конце игры
from config import SCAM_SIGNS
# Берём функцию final_title из answer — она определяет итоговый титул игрока
from answer import final_title


# Функция показывает итоговый экран после окончания игры
# correct — сколько правильных ответов дал игрок
# score — сколько очков он набрал
# lives — сколько жизней осталось
# total — сколько вопросов было всего
def show_results(correct, score, lives, total):
    print("=============================================================")
    print(f"        ИТОГ:                                               ")
    print("=============================================================")
    print(f"Правильных ответов: {correct} из {total}")
    print(f"Итоговый счет:      {score} очков")
    print(f"Оставшиеся жизни:   {lives}")
    print()
    print(final_title(score, total))
    print()
    print("Главные признаки скама:")
    for sign in SCAM_SIGNS:
        print(f" - {sign}")
