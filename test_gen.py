from colorama import init, Fore
import tkinter as tk
import os
import asyncio

import platform

size = '500x600'
title = 'Work Checker'

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())



def chatgpt_test(tema, klass, par, slog, num, pred):
    prompt = f'''Составь тест по теме {tema} для {klass}.
    Параметры вопросов: {par} (1 - развернутый ответ, 2 - один вариант ответа, 3 - несколько вариантов).
    Уровень сложности: {slog} (1 - легко, 2 - средне, 3 - сложно).
    Количество вопросов: {num}.
    {pred}'''

    try:
        # Здесь должен быть вызов API
        return "Пример теста: ...\n1. Вопрос 1\n2. Вопрос 2"
    except Exception as e:
        return f'{Fore.RED} Не удалось сгенерировать тест.'


def save_test(tema, klass, par, slog, num, pred):
    def save_data_to_downloads_as_txt(data, filename="data.txt"):
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        filepath = os.path.join(downloads_folder, filename)
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(data)
        return filepath

    otvet = chatgpt_test(tema, klass, par, slog, num, pred)
    if "Не удалось сгенерировать тест" in otvet:
        print("Ошибка при генерации теста.")
        return

    filename = "test.txt"
    file_path = save_data_to_downloads_as_txt(otvet, filename)
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":  # macOS
            os.system(f"open {file_path}")
        else:  # Linux и другие системы
            os.system(f"xdg-open {file_path}")
    except Exception as e:
        print(f"Не удалось открыть файл: {e}")



# GUI
def setup_gui():
    def open_navigation_window():
        navigation_window.deiconify()
        root.withdraw()

    def send_response():
        tema_value = tema.get().strip()
        klass_value = klass.get().strip()
        parametr_value = parametr.get().strip()
        slognost_value = slognost.get().strip()
        num_value = num.get().strip()
        predpochtenia_value = predpochtenia.get().strip()

        if not all([tema_value, klass_value, parametr_value, slognost_value, num_value, predpochtenia_value]):
            tk.Label(navigation_window, text='Заполните все поля!', fg="red").pack(pady=10)
            return

        test_data = chatgpt_test(
            tema_value, klass_value, parametr_value, slognost_value, num_value, predpochtenia_value
        )

        file_path = save_test(test_data)
        tk.Label(navigation_window, text=f"Тест сохранен в {file_path}", fg="green").pack(pady=10)

    root = tk.Tk()
    root.title(title)
    root.geometry('300x400')
    root.resizable(False, False)

    tk.Label(root, text=title, font=("Arial Black", 20), fg="black").pack(pady=20)
    tk.Label(root, text="Сервис для генерации и проверки тестов.").pack(pady=20)
    tk.Button(root, text='Начать', command=open_navigation_window, width=20, height=2).pack(pady=20)

    navigation_window = tk.Toplevel(root)
    navigation_window.title(title)
    navigation_window.geometry('600x700')
    navigation_window.resizable(False, False)
    navigation_window.withdraw()

    tk.Label(navigation_window, text='Введите тему тестов:').pack(pady=10)
    tema = tk.Entry(navigation_window)
    tema.pack(pady=10)

    tk.Label(navigation_window, text='Введите для кого предназначен ваш тест:').pack(pady=10)
    klass = tk.Entry(navigation_window)
    klass.pack(pady=10)

    tk.Label(navigation_window, text='Введите параметры генерации').pack(pady=10)
    tk.Label(navigation_window, text='(1 - развернутый ответ, 2 - один вариант ответа, 3 - несколько вариантов):').pack(
        pady=10)
    parametr = tk.Entry(navigation_window)
    parametr.pack(pady=10)

    tk.Label(navigation_window, text='Введите сложность (1 - легко, 2 - средне, 3 - сложно):').pack(pady=10)
    slognost = tk.Entry(navigation_window)
    slognost.pack(pady=10)

    tk.Label(navigation_window, text='Введите количество вопросов:').pack(pady=10)
    num = tk.Entry(navigation_window)
    num.pack(pady=10)

    tk.Label(navigation_window, text='Введите ваши предпочтения по работе:').pack(pady=10)
    predpochtenia = tk.Entry(navigation_window)
    predpochtenia.pack(pady=10)

    tk.Button(navigation_window, text="Сохранить тест", command=send_response).pack(pady=20)

    root.mainloop()


setup_gui()
