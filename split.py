import os
import pandas as pd
import json

# Создаём папку для JSON-файлов, если её ещё нет
output_dir = 'json_output'
os.makedirs(output_dir, exist_ok=True)

# Загрузка датасета из листа "Соответствуют" файла output_with_features.xlsx
df = pd.read_excel("output.xlsx", sheet_name="Соответствуют")

# Перемешиваем строки датасета
df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Размер мини‑DataFrame: 1000 строк
chunk_size = 1000
num_chunks = (len(df_shuffled) + chunk_size - 1) // chunk_size  # Округление вверх

# Обработка каждого чанка и сохранение в отдельный JSON файл внутри папки output_dir
for i in range(num_chunks):
    # Выбираем строки от i*chunk_size до (i+1)*chunk_size
    chunk = df_shuffled.iloc[i*chunk_size:(i+1)*chunk_size]
    
    # Формируем список словарей в требуемом формате:
    records = [
        {
            "origin": row["Аббревиатура"],
            "transcription": "",
            "type": "Аббревиатура"
        }
        for _, row in chunk.iterrows()
    ]
    
    # Имя файла с номером чанка
    filename = os.path.join(output_dir, f"output_chunk_{i+1}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=4)

print("Датасет перемешан, разбит на чанки по 1000 строк и сохранён в папке 'json_output'.")
