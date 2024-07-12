from flask import Flask, jsonify, request

app = Flask(__name__)

# Нашият списък с книги
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "1984", "author": "George Orwell"}
]


def find_book_by_id(book_id):
    """Намира книга с даденото `book_id`.
    Ако няма книга с това id, връща None."""
    for book in books:
        if book['id'] == book_id:
            return book
    return None


def validate_book_data(data):
    """Валидация на данните за книгата"""
    if "title" not in data or "author" not in data:
        return False
    return True


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed"}), 405


@app.route('/api/books', methods=['GET', 'POST'])
def handle_books():
    if request.method == 'POST':
        new_book = request.get_json()
        if not validate_book_data(new_book):
            return jsonify({"error": "Invalid book data"}), 400

        # Генериране на ново ID за книгата
        new_id = max(book['id'] for book in books) + 1
        new_book['id'] = new_id

        # Добавяне на новата книга към нашия списък
        books.append(new_book)

        # Връщане на данните за новата книга на клиента
        return jsonify(new_book), 201
    else:
        # Обработка на GET заявката
        return jsonify(books)


@app.route('/api/books/<int:id>', methods=['PUT'])
def handle_book(id):
    # Намиране на книгата с даденото ID
    book = find_book_by_id(id)

    # Ако книгата не е намерена, връщане на грешка 404
    if book is None:
        return '', 404

    # Обновяване на книгата с новите данни
    new_data = request.get_json()
    if not validate_book_data(new_data):
        return jsonify({"error": "Invalid book data"}), 400

    book.update(new_data)

    # Връщане на обновената книга
    return jsonify(book)


@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    # Намиране на книгата с даденото ID
    book = find_book_by_id(id)

    # Ако книгата не е намерена, връщане на грешка 404
    if book is None:
        return '', 404

    # Премахване на книгата от списъка
    books.remove(book)

    # Връщане на изтритата книга
    return jsonify(book)


if __name__ == '__main__':
    app.run(debug=True)
