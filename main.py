import re
import pandas as pd

# Регулярное выражение для проверки:
# - Первая и последняя буква – заглавные.
# - Минимум два заглавных символа в строке.
# - Строка состоит только из русских букв.
check_pattern = re.compile(
    r'^(?=(?:.*[А-ЯЁ]){2,})[А-ЯЁ][А-ЯЁа-яё]*[А-ЯЁ]$'
)

def clean_abbreviation(text: str) -> str:
    """
    Удаляет из строки все символы, кроме букв (латиница и кириллица),
    цифр и пробельных символов.
    """
    return re.sub(r'[^A-Za-zА-Яа-яЁё0-9\s]', '', text)

# Читаем исходный Excel-файл
df = pd.read_excel(r"dataset\\result_abbreviation_data (3).xlsx")

matching = []
non_matching = []

for abbr in df["Аббревиатура"]:
    # Приводим значение к строке и очищаем от спецсимволов
    abbr_str = str(abbr)
    cleaned = clean_abbreviation(abbr_str)
    
    # Если в строке есть пробелы, разделяем на отдельные токены
    tokens = cleaned.split()
    
    for token in tokens:
        # Убираем токены длиной больше 6 символов
        if len(token) > 6:
            continue
        
        # Проверяем, удовлетворяет ли токен регулярным правилам
        if check_pattern.match(token):
            matching.append(token)
        else:
            non_matching.append(token)

# Удаляем дубликаты, преобразуя списки в DataFrame
df_matching = pd.DataFrame(sorted(set(matching)), columns=["Аббревиатура"])
df_non_matching = pd.DataFrame(sorted(set(non_matching)), columns=["Аббревиатура"])

# Записываем результаты в Excel с разными листами
output_file = "output.xlsx"
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    df_matching.to_excel(writer, sheet_name="Соответствуют", index=False)
    df_non_matching.to_excel(writer, sheet_name="Не соответствуют", index=False)

print(f"Результаты записаны в файл {output_file}")
