from flask import Flask, jsonify, request

app = Flask(__name__)

# Нашият списък с книги
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "1984", "author": "George Orwell"}
]


def find_book_by_id(book_id):
    """ Find the book with the id `book_id`.
    If there is no book with this id, return None. """
    for book in books:
        if book['id'] == book_id:
            return book
    return None


@app.route('/api/books', methods=['GET', 'POST'])
def handle_books():
    if request.method == 'POST':
        # Получаване на данните за новата книга от клиента
        new_book = request.get_json()

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
    book.update(new_data)

    # Връщане на обновената книга
    return jsonify(book)


if __name__ == '__main__':
    app.run(debug=True)
