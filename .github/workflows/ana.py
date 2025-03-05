import pandas as pd
import matplotlib.pyplot as plt

# Створення таблиці змін категорій
data = {
    "Дата": ["2025-02-01", "2025-02-07", "2025-02-14", "2025-02-21", "2025-02-28"],
    "Нові категорії": [15, 25, 30, 20, 35],
    "Видалені категорії": [5, 10, 8, 12, 9],
    "Змінені назви": [2, 5, 7, 3, 6]
}

df_changes = pd.DataFrame(data)

# Відображення таблиці
print(df_changes)

# Побудова графіка змін
plt.figure(figsize=(10, 5))
plt.plot(df_changes["Дата"], df_changes["Нові категорії"], marker='o', label="Нові категорії")
plt.plot(df_changes["Дата"], df_changes["Видалені категорії"], marker='s', label="Видалені категорії")
plt.plot(df_changes["Дата"], df_changes["Змінені назви"], marker='^', label="Змінені назви")

plt.xlabel("Дата")
plt.ylabel("Кількість змін")
plt.title("Динаміка змін категорій")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)

# Показати графік
plt.show()
