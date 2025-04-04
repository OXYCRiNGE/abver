import re
import pandas as pd

def extract_features(abbreviation: str) -> dict:
    """
    Извлекает признаки из строки-аббревиатуры.
    
    Признаки:
      - vowel_count: количество гласных (Г).
      - consonant_count: количество согласных (С).
      - max_consecutive_vowels: максимальное количество подряд идущих гласных.
      - max_consecutive_consonants: максимальное количество подряд идущих согласных.
      - pattern_vowel_consonant: количество сочетаний ГC (гласная, затем согласная).
      - pattern_consonant_vowel: количество сочетаний СГ (согласная, затем гласная).
      - pattern_vowel_consonant_vowel: количество сочетаний ГСГ.
      - pattern_consonant_vowel_consonant: количество сочетаний СГС.
      - vowel_consonant_ratio: отношение гласных к согласным (если согласных нет, возвращается 0).
      - first_letter_type: "Г", если первая буква гласная, или "С", если согласная.
      - last_letter_type: "Г", если последняя буква гласная, или "С", если согласная.
    """
    # Набор гласных букв русского языка
    vowels = "АЕЁИОУЫЭЮЯаеёиоуыэюя"
    
    features = {}
    
    # Подсчет гласных и согласных (учитываются только буквы)
    vowel_count = sum(1 for c in abbreviation if c in vowels)
    consonant_count = sum(1 for c in abbreviation if c.isalpha() and c not in vowels)
    features['vowel_count'] = vowel_count
    features['consonant_count'] = consonant_count
    
    # Подсчет максимальной последовательности гласных и согласных
    max_consecutive_vowels = 0
    max_consecutive_consonants = 0
    current_vowels = 0
    current_consonants = 0
    for c in abbreviation:
        if c in vowels:
            current_vowels += 1
            max_consecutive_vowels = max(max_consecutive_vowels, current_vowels)
            current_consonants = 0
        elif c.isalpha():
            current_consonants += 1
            max_consecutive_consonants = max(max_consecutive_consonants, current_consonants)
            current_vowels = 0
        else:
            current_vowels = 0
            current_consonants = 0
    features['max_consecutive_vowels'] = max_consecutive_vowels
    features['max_consecutive_consonants'] = max_consecutive_consonants
    
    # Сначала считаем двухбуквенные сочетания по всей строке
    pattern_vowel_consonant = 0  # ГС: гласная, затем согласная
    pattern_consonant_vowel = 0  # СГ: согласная, затем гласная
    for i in range(len(abbreviation) - 1):
        if abbreviation[i] in vowels and abbreviation[i+1].isalpha() and abbreviation[i+1] not in vowels:
            pattern_vowel_consonant += 1
        if abbreviation[i].isalpha() and abbreviation[i] not in vowels and abbreviation[i+1] in vowels:
            pattern_consonant_vowel += 1

    # Считаем 3-буквенные сочетания
    pattern_vowel_consonant_vowel = 0  # ГСГ: гласная, согласная, гласная
    pattern_consonant_vowel_consonant = 0  # СГС: согласная, гласная, согласная
    for i in range(len(abbreviation) - 2):
        if (abbreviation[i] in vowels and 
            abbreviation[i+1].isalpha() and abbreviation[i+1] not in vowels and 
            abbreviation[i+2] in vowels):
            pattern_vowel_consonant_vowel += 1
        if (abbreviation[i].isalpha() and abbreviation[i] not in vowels and 
            abbreviation[i+1] in vowels and 
            abbreviation[i+2].isalpha() and abbreviation[i+2] not in vowels):
            pattern_consonant_vowel_consonant += 1

    # Приоритет: если найдены 3-буквенные сочетания, то соответствующие 2-буквенные должны быть не меньше их количества
    pattern_vowel_consonant = max(pattern_vowel_consonant, pattern_vowel_consonant_vowel)
    pattern_consonant_vowel = max(pattern_consonant_vowel, pattern_consonant_vowel_consonant)
    
    features['pattern_vowel_consonant'] = pattern_vowel_consonant
    features['pattern_consonant_vowel'] = pattern_consonant_vowel
    features['pattern_vowel_consonant_vowel'] = pattern_vowel_consonant_vowel
    features['pattern_consonant_vowel_consonant'] = pattern_consonant_vowel_consonant
    
    # Отношение гласных к согласным: если согласных нет, возвращаем 0
    features['vowel_consonant_ratio'] = (vowel_count / consonant_count) if consonant_count != 0 else 0
    
    # Определяем тип первой и последней буквы (если буква, то "Г" для гласной и "С" для согласной)
    if abbreviation:
        first_letter_type = "Г" if abbreviation[0] in vowels else "С" if abbreviation[0].isalpha() else ""
        last_letter_type = "Г" if abbreviation[-1] in vowels else "С" if abbreviation[-1].isalpha() else ""
    else:
        first_letter_type = ""
        last_letter_type = ""
    features['first_letter_type'] = first_letter_type
    features['last_letter_type'] = last_letter_type
    
    return features

# Загрузка листа "Соответствуют" из файла output.xlsx
df_matching = pd.read_excel("output.xlsx", sheet_name="Соответствуют")

# Применяем функцию extract_features к каждой аббревиатуре в столбце "Аббревиатура"
features_df = df_matching["Аббревиатура"].apply(lambda x: pd.Series(extract_features(str(x))))

# Объединяем исходный DataFrame с новыми признаками
df_with_features = pd.concat([df_matching, features_df], axis=1)

# Сохраняем результат в новый Excel-файл
output_file = "output_with_features.xlsx"
df_with_features.to_excel(output_file, index=False)

print(f"Новые признаки успешно выделены и сохранены в файл {output_file}")
