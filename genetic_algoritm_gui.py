import tkinter as tk
from tkinter import ttk
import numpy as np

# Создаем основное окно приложения
root = tk.Tk()
root.title("Генетический алгоритм")  # Устанавливаем заголовок окна
root.geometry("1000x600")  # Устанавливаем размер окна


# Функция для вычисления значения целевой функции
# Цель - минимизировать эту функцию
def target_function(x):
    # Здесь вычисляется значение целевой функции для каждого вектора x
    return 3 * (x[0] - 4) ** 2 + 5 * (x[1] + 3) ** 2 + 7 * (2 * x[2] + 1) ** 2


# Функция для реализации генетического алгоритма
def genetic_algorithm():
    try:
        # Получаем параметры из полей ввода (с вероятностью мутации, размером популяции и т.д.)
        mutation_rate = float(mutation_entry.get())
        pop_size = int(pop_size_entry.get())
        generations = int(generations_entry.get())
        min_gene = float(min_gene_entry.get())
        max_gene = float(max_gene_entry.get())
    except ValueError:
        # Если произошла ошибка преобразования, выводим сообщение об ошибке
        result_label["text"] = "Ошибка ввода параметров"
        return

    # Очищаем таблицу перед запуском нового алгоритма
    for row in tree.get_children():
        tree.delete(row)

    # Создаем начальное поколение (случайные значения в пределах от min_gene до max_gene)
    population = np.random.uniform(min_gene, max_gene, (pop_size, 3))
    best_solution = None
    best_score = float("inf")  # Изначально ставим лучшее значение функции на максимум

    # Основной цикл по поколениям
    for generation in range(generations):
        # Вычисляем значение функции для каждого индивида в популяции
        scores = np.array([target_function(individual) for individual in population])

        # Находим лучшего индивида в текущем поколении
        best_idx = np.argmin(scores)
        if scores[best_idx] < best_score:
            best_score = scores[best_idx]
            best_solution = population[best_idx]  # Обновляем лучшее решение

        # Обновляем текстовое поле с результатом лучшего найденного решения
        result_label["text"] = (
            f"Лучшее решение: x1={best_solution[0]:.2f}, "
            f"x2={best_solution[1]:.2f}, x3={best_solution[2]:.2f}\n"
            f"Значение функции: {best_score:.2f}"
        )

        # Обновляем таблицу с информацией о текущем поколении
        for i, (individual, score) in enumerate(zip(population, scores)):
            tree.insert("", "end", values=(i + 1, f"{score:.2f}",
                                           f"{individual[0]:.2f}",
                                           f"{individual[1]:.2f}",
                                           f"{individual[2]:.2f}"))

        # Отбор: выбираем половину популяции с наименьшими значениями функции (наиболее приспособленных)
        selected = population[scores.argsort()[:pop_size // 2]]

        # Создание нового поколения через кроссовер и мутацию
        offspring = []
        while len(offspring) < pop_size:
            # Случайно выбираем двух родителей из отобранных индивидов
            parents = selected[np.random.choice(len(selected), 2, replace=False)]
            # Кроссовер: создаем потомка как среднее значение генов родителей
            child = np.mean(parents, axis=0)
            # Мутация: случайно изменяем потомка с заданной вероятностью мутации
            if np.random.rand() < mutation_rate / 100:
                child += np.random.uniform(-1, 1, child.shape)  # Добавляем случайное изменение
            offspring.append(child)  # Добавляем потомка в новое поколение
        population = np.array(offspring)  # Обновляем популяцию


# Создаем интерфейсные элементы (левая часть окна)
# Поля ввода для параметров генетического алгоритма
ttk.Label(root, text="Вероятность мутации, %:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
mutation_entry = ttk.Entry(root)
mutation_entry.insert(0, "20")  # Устанавливаем значение по умолчанию
mutation_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(root, text="Количество хромосом:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
pop_size_entry = ttk.Entry(root)
pop_size_entry.insert(0, "50")  # Значение по умолчанию для популяции
pop_size_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(root, text="Количество поколений:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
generations_entry = ttk.Entry(root)
generations_entry.insert(0, "100")  # Значение по умолчанию для числа поколений
generations_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(root, text="Минимальное значение гена:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
min_gene_entry = ttk.Entry(root)
min_gene_entry.insert(0, "-50")  # Минимально возможное значение гена
min_gene_entry.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(root, text="Максимальное значение гена:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
max_gene_entry = ttk.Entry(root)
max_gene_entry.insert(0, "50")  # Максимально возможное значение гена
max_gene_entry.grid(row=4, column=1, padx=5, pady=5)

# Кнопка для запуска алгоритма
run_button = ttk.Button(root, text="Рассчитать", command=genetic_algorithm)
run_button.grid(row=5, column=0, columnspan=2, pady=10)

# Метка для вывода результатов (лучшего решения)
result_label = ttk.Label(root, text="Лучшее решение: ")
result_label.grid(row=6, column=0, columnspan=2, pady=10)

# Правая часть интерфейса - таблица для отображения текущего поколения
columns = ("Номер", "Результат", "Ген 1", "Ген 2", "Ген 3")
tree = ttk.Treeview(root, columns=columns, show="headings", height=20)
tree.grid(row=0, column=3, rowspan=7, padx=10, pady=5, sticky="nsew")

# Настройка заголовков таблицы
for col in columns:
    tree.heading(col, text=col)  # Устанавливаем текст заголовка
    tree.column(col, width=100)  # Устанавливаем ширину столбца

# Устанавливаем пропорции для правильного масштабирования окна
root.grid_columnconfigure(3, weight=1)
root.grid_rowconfigure(7, weight=1)

# Запуск основного цикла приложения
root.mainloop()
