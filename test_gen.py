from colorama import init, Fore
import tkinter as tk
from tkinter import messagebox
import asyncio
from g4f.client import Client
import platform

size = '500x600'
title = 'Work Checker'

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def chatgpt_test(tema, klass, par, slog, num, pred):
    prompt = f'''Составь тест по теме {tema} для  {klass}.
            Параметры вопросов: {par} (1 - развернутый ответ, 2 - один вариант ответа, 3 - несколько вариантов).
            Уровень сложности: {slog} (1 - легко, 2 - средне, 3 - сложно).
            Количество вопросов: {num}.
            Каждый вопрос должен быть четко сформулирован, а для вопросов с вариантами ответа должны быть предложены как минимум 4 варианта, из которых один (или несколько) правильные.
            Если требуется развернутый ответ, сформулируй задание так, чтобы оно побуждало учеников объяснять, анализировать или описывать с примерами.
            Добавь примечание, где указано, какова правильность ответа (особенно для вариантов с выбором ответа).
            Внимание без указания правильного ответа!!! Фотмат теста: В самом верху написано тема без слова тема, далее идут задания каждое пронумеровано. 
            ВСЕ!! больше ничего не надо.{pred}'''

    client = Client()
    user_message = {"role": "user", "content": prompt}

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[user_message],
            temperature=0.7,
            max_tokens=200000,
            top_p=1.0,
            frequency_penalty=0.2,
            presence_penalty=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f'{Fore.RED} Не удалось сгенерировать тест.'
def proverka(test, otvet):
    prompt = f'''Проверь тест и выставь оценку по пятибалльной шкале.

        Тест: 
        {test}

        Ответы пользователя: 
        {otvet}
        Формат вывода строго определен: написано только колличество набраных баллов, оценка и все если все правильно, если есть ошибки то вывод правильного варианта ответа и обьяснение почему.
        Алгоритм проверки:
        1. Определи правильные ответы и сравни с ответами пользователя.
        2. Рассчитай итоговую оценку:
           - Оцени тест по пятибалльной шкале:
             5 (отлично) — 90-100% правильных ответов.
             4 (хорошо) — 75-89% правильных.
             3 (удовлетворительно) — 50-74%.
             2 (плохо) — меньше 50%.
        3. Для развернутых ответов оцени полноту, соответствие заданию и пояснения.
        Внимание напиши только колличество баллов и оценку, если есть ошибки добавь пояснение. И все!!! Больше ничего не надо!
        '''

    client = Client()
    user_message = {"role": "user", "content": prompt}

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[user_message],
            temperature=0.7,
            max_tokens=2000,
            top_p=1.0,
            frequency_penalty=0.2,
            presence_penalty=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f'{Fore.RED} Не удалось проверить тест.'

def setup_gui():
    def generate_test():
        tema_value = tema.get().strip()
        klass_value = klass.get().strip()
        parametr_value = parametr.get().strip()
        slognost_value = slognost.get().strip()
        num_value = num.get().strip()
        predpochtenia_value = predpochtenia.get().strip()

        if not all([tema_value, klass_value, parametr_value, slognost_value, num_value]):
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        test_text.set(chatgpt_test(tema_value, klass_value, parametr_value, slognost_value, num_value, predpochtenia_value))
        show_test_page()

    def check_answers():
        user_answers = [entry.get() for entry in answer_entries]
        result = proverka(test_text.get(), user_answers)
        result_label.config(text=result)
        show_result_page()

    def reset_app():
        test_text.set("")
        for entry in answer_entries:
            entry.destroy()
        answer_entries.clear()
        show_main_page()

    def show_main_page():
        main_page.pack(fill="both", expand=True)
        test_page.pack_forget()
        result_page.pack_forget()

    def show_test_page():
        main_page.pack_forget()
        test_page.pack(fill="both", expand=True)

        for widget in answers_frame.winfo_children():
            widget.destroy()

        questions = test_text.get().split("\n")[1:]
        for i, question in enumerate(questions, start=1):
            tk.Label(answers_frame, text=question).grid(row=i, column=0, sticky="w", pady=5)
            entry = tk.Entry(answers_frame)
            entry.grid(row=i, column=1, pady=5)
            answer_entries.append(entry)

    def show_result_page():
        test_page.pack_forget()
        result_page.pack(fill="both", expand=True)

    root = tk.Tk()
    root.title("Work Checker")
    root.geometry("900x1000")

    test_text = tk.StringVar()
    answer_entries = []

    main_page = tk.Frame(root)
    tk.Label(main_page, text="Work Checker", font=("Arial Black", 20)).pack(pady=20)

    tk.Label(main_page, text="Тема теста:").pack()
    tema = tk.Entry(main_page)
    tema.pack(pady=5)

    tk.Label(main_page, text="Класс:").pack()
    klass = tk.Entry(main_page)
    klass.pack(pady=5)

    tk.Label(main_page, text="Параметры вопросов (1/2/3):").pack()
    parametr = tk.Entry(main_page)
    parametr.pack(pady=5)

    tk.Label(main_page, text="Сложность (1/2/3):").pack()
    slognost = tk.Entry(main_page)
    slognost.pack(pady=5)

    tk.Label(main_page, text="Количество вопросов:").pack()
    num = tk.Entry(main_page)
    num.pack(pady=5)

    tk.Label(main_page, text="Дополнительные пожелания:").pack()
    predpochtenia = tk.Entry(main_page)
    predpochtenia.pack(pady=5)

    tk.Button(main_page, text="Сохранить тест", command=generate_test).pack(pady=20)

    test_page = tk.Frame(root)
    tk.Label(test_page, textvariable=test_text, justify="left", wraplength=500).pack(pady=20)

    answers_frame = tk.Frame(test_page)
    answers_frame.pack()

    tk.Button(test_page, text="Проверить тест", command=check_answers).pack(pady=20)

    result_page = tk.Frame(root)
    result_label = tk.Label(result_page, text="", font=("Arial", 14))
    result_label.pack(pady=20)

    tk.Button(result_page, text="Начать сначала", command=reset_app).pack(pady=20)

    show_main_page()
    root.mainloop()

setup_gui()
