import pandas as pd
import numpy as np


from tomodachi_core.tomodachi.utils import expected_types

# TODO: Possible to re-write as decorator (for, say, Preprocess)
def validate(df: pd.DataFrame, rules_map: dict[str, str] = expected_types):
    """
    Проверяет, соответствует ли DataFrame ожидаемой структуре и сохраняет его в файл.

    :df: DataFrame для проверки
    :param output_path: Путь для сохранения файла
    """
    
    # Checks and maps the types of Pandas column
    for col, expected_type in rules_map.items():
        if col not in df.columns:
            # print(f"Ошибка: отсутствует столбец '{col}'")
            return False
        
        actual_type = df[col].dtype

        # TODO: Rewrite using pattern match and that dictionay
        # For now: keep the code
        # Проверяем datetime
        if expected_type.startswith("datetime") and not np.issubdtype(actual_type, np.datetime64):
            print(f"Ошибка: '{col}' должен быть datetime, но имеет тип {actual_type}")
            return False
        
        # Проверяем числа (float или int)
        if expected_type == "float64" and not np.issubdtype(actual_type, np.floating):
            # print(f"Ошибка: '{col}' должен быть float64, но имеет тип {actual_type}")
            return False
        
        if expected_type == "int64" and not np.issubdtype(actual_type, np.integer):
            # print(f"Ошибка: '{col}' должен быть int64, но имеет тип {actual_type}")
            return False
        
        # Проверяем строки (object)
        if expected_type == "object" and not np.issubdtype(actual_type, np.object_):
            # print(f"Ошибка: '{col}' должен быть строкой (object), но имеет тип {actual_type}")
            return False

    # print("DataFrame соответствует ожидаемой структуре.")
    return True