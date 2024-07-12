from flask import Flask, jsonify, request

app = Flask(__name__)

# Our list of books
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "1984", "author": "George Orwell"}
]


def find_book_by_id(book_id):
    """Find the book with the given `book_id`. If no such book exists, return None."""
    for book in books:
        if book['id'] == book_id:
            return book
    return None


def validate_book_data(data):
    """Validate book data."""
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

        # Generate new ID for the book
        new_id = max(book['id'] for book in books) + 1
        new_book['id'] = new_id

        # Add new book to the list
        books.append(new_book)

        # Return the new book data to the client
        return jsonify(new_book), 201
    else:
        author = request.args.get('author')
        if author:
            filtered_books = [book for book in books if book.get('author') == author]
            return jsonify(filtered_books)
        return jsonify(books)


@app.route('/api/books/<int:id>', methods=['PUT'])
def handle_book(id):
    # Find the book with the given ID
    book = find_book_by_id(id)

    # If the book wasn't found, return a 404 error
    if book is None:
        return '', 404

    # Update the book with the new data
    new_data = request.get_json()
    if not validate_book_data(new_data):
        return jsonify({"error": "Invalid book data"}), 400

    book.update(new_data)

    # Return the updated book
    return jsonify(book)


@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    # Find the book with the given ID
    book = find_book_by_id(id)

    # If the book wasn't found, return a 404 error
    if book is None:
        return '', 404

    # Remove the book from the list
    books.remove(book)

    # Return the deleted book
    return jsonify(book)


if __name__ == '__main__':
    app.run(debug=True)
