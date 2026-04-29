import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

# --- Конфигурация ---
QUOTES_FILE = "quotes.json"
DEFAULT_QUOTES = [
    {"text": "Жизнь — это то, что происходит, пока ты строишь другие планы.", "author": "Джон Леннон", "theme": "Жизнь"},
    {"text": "Будь тем изменением, которое ты хочешь видеть в мире.", "author": "Махатма Ганди", "theme": "Мотивация"},
    {"text": "Единственный способ делать великие дела — любить то, что ты делаешь.", "author": "Стив Джобс", "theme": "Работа"}
]

class QuoteGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных цитат")
        self.root.geometry("600x500")
        
        self.quotes = self.load_quotes()
        self.history = []
        
        self.create_widgets()
        self.update_history_display()

    def load_quotes(self):
        """Загрузка цитат из файла JSON или использование стандартных"""
        if os.path.exists(QUOTES_FILE):
            with open(QUOTES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return DEFAULT_QUOTES

    def save_quotes(self):
        """Сохранение цитат в файл JSON"""
        with open(QUOTES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.quotes, f, ensure_ascii=False, indent=4)

    def generate_quote(self):
        """Генерация случайной цитаты и добавление в историю"""
        if not self.quotes:
            messagebox.showwarning("Нет цитат", "Список цитат пуст. Добавьте новые цитаты.")
            return

        quote = random.choice(self.quotes)
        self.history.append(quote)
        self.update_history_display()
        
        # Отображение текущей цитаты
        self.quote_text_label.config(text=quote["text"])
        self.author_label.config(text=f"— {quote['author']}")

    def update_history_display(self):
        """Обновление списка истории с учетом фильтрации"""
        self.history_listbox.delete(0, tk.END)
        
        filtered_history = self.history.copy()
        
        # Фильтрация по автору
        author_filter = self.author_filter_var.get()
        if author_filter:
            filtered_history = [q for q in filtered_history if q["author"] == author_filter]
        
        # Фильтрация по теме
        theme_filter = self.theme_filter_var.get()
        if theme_filter:
            filtered_history = [q for q in filtered_history if q["theme"] == theme_filter]
        
        for q in filtered_history:
            display_text = f'"{q["text"]}" — {q["author"]}'
            self.history_listbox.insert(tk.END, display_text)

    def add_quote(self):
        """Добавление новой цитаты с проверкой ввода"""
        text = self.new_quote_entry.get("1.0", tk.END).strip()
        author = self.new_author_entry.get().strip()
        theme = self.new_theme_entry.get().strip()

        # Проверка на пустые строки
        if not text or not author or not theme:
            messagebox.showerror("Ошибка ввода", "Все поля (текст, автор, тема) должны быть заполнены.")
            return

        new_quote = {"text": text, "author": author, "theme": theme}
        self.quotes.append(new_quote)
        self.save_quotes()
        
        # Обновление фильтров для новых авторов/тем
        self.update_filters()
        
        messagebox.showinfo("Успех", "Цитата успешно добавлена!")
        
    def update_filters(self):
        """Обновление выпадающих списков фильтрации"""
        authors = sorted(list(set([q["author"] for q in self.quotes])))
        themes = sorted(list(set([q["theme"] for q in self.quotes])))
        
        menu = self.author_filter_option['menu']
        menu.delete(0, 'end')
        for author in authors:
            menu.add_command(label=author, command=lambda value=author: self.author_filter_var.set(value))
            
        menu = self.theme_filter_option['menu']
        menu.delete(0, 'end')
        for theme in themes:
            menu.add_command(label=theme, command=lambda value=theme: self.theme_filter_var.set(value))

    def create_widgets(self):
        # --- Основная цитата ---
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10)

        self.quote_text_label = tk.Label(main_frame, text="Нажмите кнопку для генерации цитаты", wraplength=500, font=('Arial', 12))
        self.quote_text_label.pack()

        self.author_label = tk.Label(main_frame, text="", font=('Arial', 10, 'italic'))
        self.author_label.pack(pady=5)

        tk.Button(main_frame, text="Сгенерировать цитату", command=self.generate_quote).pack(pady=10)

         # --- История ---
        history_frame = tk.LabelFrame(self.root, text="История сгенерированных цитат")
        history_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

         # Фильтры
         filter_frame = tk.Frame(history_frame)
         filter_frame.pack(fill=tk.X, pady=5)

         # Фильтр по автору
         tk.Label(filter_frame, text="Фильтр по автору:").pack(side=tk.LEFT)
         self.author_filter_var = tk.StringVar()
         self.author_filter_option = ttk.OptionMenu(filter_frame, self.author_filter_var, "", command=self.update_history_display)
         self.author_filter_option.pack(side=tk.LEFT, padx=5)
         
         # Фильтр по теме
         tk.Label(filter_frame, text="Фильтр по теме:").pack(side=tk.LEFT, padx=(20, 0))
         self.theme_filter_var = tk.StringVar()
         self.theme_filter_option = ttk.OptionMenu(filter_frame, self.theme_filter_var, "", command=self.update_history_display)
         self.theme_filter_option.pack(side=tk.LEFT, padx=5)
         
         # Заполнение фильтров при старте
         self.update_filters()
         
         # Список истории
         list_frame = tk.Frame(history_frame)
         list_frame.pack(fill=tk.BOTH, expand=True)
         
         scrollbar = tk.Scrollbar(list_frame)
         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
         
         self.history_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=10)
         self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
         scrollbar.config(command=self.history_listbox.yview)

          # --- Добавление новой цитаты ---
          add_frame = tk.LabelFrame(self.root, text="Добавить новую цитату")
          add_frame.pack(padx=10, pady=10, fill=tk.X)
          
          tk.Label(add_frame, text="Текст:").grid(row=0, column=0, sticky='w')
          self.new_quote_entry = tk.Text(add_frame, height=3, width=50)
          self.new_quote_entry.grid(row=1, column=0, columnspan=2, pady=5)
          
          tk.Label(add_frame, text="Автор:").grid(row=2, column=0, sticky='w')
          self.new_author_entry = tk.Entry(add_frame)
          self.new_author_entry.grid(row=3, column=0, pady=5)
          
          tk.Label(add_frame, text="Тема:").grid(row=2, column=1, sticky='w')
          self.new_theme_entry = tk.Entry(add_frame)
          self.new_theme_entry.grid(row=3, column=1, pady=5)
          
          tk.Button(add_frame, text="Добавить цитату", command=self.add_quote).grid(row=4, column=0, columnspan=2)


if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGeneratorApp(root)
    root.mainloop()
