import logging
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Example list of books
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    # Add more books as needed
]


# Function to find a book by ID
def find_book_by_id(book_id):
    for book in books:
        if book['id'] == book_id:
            return book
    return None


# Route to handle GET and POST requests for /api/books
@app.route('/api/books', methods=['GET', 'POST'])
def handle_books():
    if request.method == 'POST':
        new_book = request.get_json()
        if not validate_book_data(new_book):
            app.logger.warning('Invalid book data received')
            return jsonify({"error": "Invalid book data"}), 400

        new_id = max(book['id'] for book in books) + 1 if books else 1
        new_book['id'] = new_id
        books.append(new_book)
        app.logger.info(f'Added new book: {new_book}')
        return jsonify(new_book), 201
    else:
        # Handle pagination
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        start_index = (page - 1) * limit
        end_index = start_index + limit
        paginated_books = books[start_index:end_index]

        app.logger.info(f'Returning books from index {start_index} to {end_index}')
        return jsonify(paginated_books)


# Route to handle GET, PUT, and DELETE requests for /api/books/<id>
@app.route('/api/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_book(id):
    book = find_book_by_id(id)
    if request.method == 'GET':
        if book is None:
            app.logger.warning(f'Book with ID {id} not found')
            return '', 404
        app.logger.info(f'Retrieved book: {book}')
        return jsonify(book)

    if request.method == 'PUT':
        if book is None:
            app.logger.warning(f'Book with ID {id} not found')
            return '', 404
        new_data = request.get_json()
        book.update(new_data)
        app.logger.info(f'Updated book with ID {id}: {book}')
        return jsonify(book)

    if request.method == 'DELETE':
        if book is None:
            app.logger.warning(f'Book with ID {id} not found')
            return '', 404
        books.remove(book)
        app.logger.info(f'Deleted book with ID {id}')
        return jsonify(book)


# Function to validate book data
def validate_book_data(data):
    return 'title' in data and 'author' in data


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    app.logger.error('404 Not Found error')
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    app.logger.error('405 Method Not Allowed error')
    return jsonify({"error": "Method Not Allowed"}), 405


if __name__ == "__main__":
    app.run(debug=True)
