import streamlit as st # Библиотека для создания интерактивных веб-приложений
from PIL import Image # Библиотека для работы с изображениями
import pytesseract # Библиотека для распознавания текста на изображениях с использованием Tesseract-OCR
import os # Библиотека для работы с операционной системой и файловой системой
import tempfile # Библиотека для создания временных файлов и директорий

import base64 # Библиотека для кодирования и декодирования данных в формате Base64

# Функция для распознавания текста на изображении
def recognize_text(image, lang='eng'):
    text = pytesseract.image_to_string(image, lang=lang)
    return text

# Функция для сохранения текста в файл
def save_text_to_file(text, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)

# Интерфейс Streamlit
st.title("Распознавание текста на изображениях")
st.header("Загрузите изображение для распознавания текста")

# Выбор языков
languages = st.multiselect(
    "Выберите языки для распознавания текста (удерживайте Ctrl для выбора нескольких)",
    ["eng", "rus", "deu", "fra", "spa"],
    default=["eng", "rus"]
)

# Объединение выбранных языков в строку
lang = "+".join(languages)

# Загрузка изображения
uploaded_file = st.file_uploader("Выберите файл изображения", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Открытие изображения
    image = Image.open(uploaded_file)
    st.image(image, caption='Загруженное изображение', use_column_width=True)
    
    # Распознавание текста
    if st.button("Распознать текст"):
        recognized_text = recognize_text(image, lang=lang)
        
        # Показать распознанный текст
        st.subheader("Распознанный текст")
        st.text_area("Распознанный текст (вы можете отредактировать его):", value=recognized_text, height=300)
        
        # Создание временного файла и запись текста
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
            temp_file.write(recognized_text.encode('utf-8'))
            temp_file_path = temp_file.name
        
        # Отображение кнопки для скачивания файла
        with open(temp_file_path, 'rb') as file:
            st.download_button(
                label="Скачать файл",
                data=file,
                file_name='recognized_text.txt',
                mime='text/plain'
            )

        # Удаление временного файла после использования
        os.remove(temp_file_path)
