import json
import os
from datetime import datetime

FILE_PATH = "books.json"

def load_books():
    """Загружает список книг из JSON-файла."""
    if not os.path.exists(FILE_PATH):
        return []
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, PermissionError):
        print("Ошибка чтения файла. Создан пустой список.")
        return []

def save_books(books):
    """Сохраняет список книг в JSON-файл."""
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

def add_book():
    """Добавляет новую книгу с валидацией."""
    books = load_books()

    author = input("Введите автора: ").strip()
    title = input("Введите название книги: ").strip()

    # Проверка на дубликат
    for book in books:
        if book["author"].lower() == author.lower() and book["title"].lower() == title.lower():
            print("Эта книга уже добавлена.")
            return

    # Валидация оценки
    while True:
        try:
            rating = int(input("Введите оценку (1–5): "))
            if 1 <= rating <= 5:
                break
            else:
                print("Оценка должна быть от 1 до 5.")
        except ValueError:
            print("Введите число.")

    date_read = input("Введите дату прочтения (например, 2025-04-05): ").strip()
    if not date_read:
        date_read = datetime.now().strftime("%Y-%m-%d")

    new_book = {
        "author": author,
        "title": title,
        "rating": rating,
        "date_read": date_read
    }

    books.append(new_book)
    save_books(books)
    print("Книга успешно добавлена!")

def show_all_books():
    """Показывает все книги."""
    books = load_books()
    if not books:
        print("Нет добавленных книг.")
        return

    print("\n" + "="*60)
    for i, book in enumerate(books, 1):
        print(f"{i}. {book['title']} — {book['author']} | Оценка: {book['rating']} | Дата: {book['date_read']}")
    print("="*60)

def show_average_rating():
    """Показывает среднюю оценку."""
    books = load_books()
    if not books:
        print("Нет книг для расчёта.")
        return

    avg = sum(book["rating"] for book in books) / len(books)
    print(f"Средняя оценка: {avg:.2f}")

def show_author_stats():
    """Показывает статистику по авторам."""
    books = load_books()
    if not books:
        print("Нет книг для анализа.")
        return

    stats = {}
    for book in books:
        author = book["author"]
        stats[author] = stats.get(author, 0) + 1

    print("\n Статистика по авторам:")
    for author, count in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {author}: {count} книг(и)")

def delete_book():
    """Удаляет книгу по номеру."""
    books = load_books()
    if not books:
        print("Нет книг для удаления.")
        return

    show_all_books()
    try:
        idx = int(input("Введите номер книги для удаления: ")) - 1
        if 0 <= idx < len(books):
            deleted = books.pop(idx)
            save_books(books)
            print(f"Удалено: {deleted['title']} — {deleted['author']}")
        else:
            print("Неверный номер.")
    except ValueError:
        print("Введите число.")

def main():
    """Главное меню."""
    while True:
        print("\n Трекер прочитанных книг")
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Показать среднюю оценку")
        print("4. Статистика по авторам")
        print("5. Удалить книгу")
        print("6. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            show_all_books()
        elif choice == "3":
            show_average_rating()
        elif choice == "4":
            show_author_stats()
        elif choice == "5":
            delete_book()
        elif choice == "6":
            print("👋 До новых встреч!")
            break
        else:
            print("Выберите число от 1 до 6.")

if __name__ == "__main__":
    main()