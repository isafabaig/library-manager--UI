import streamlit as st
import json
import os

data_file = 'library.json'

def load_library():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

def save_library(library):
    with open(data_file, 'w') as file:
        json.dump(library, file, indent=4)

def add_book(title, author, year, genre, read):
    library = load_library()
    new_book = {
        'title': title,
        'author': author,
        'year': year,
        'genre': genre,
        'read': read
    }
    library.append(new_book)
    save_library(library)

def remove_book(title):
    library = load_library()
    updated_library = [book for book in library if book['title'].lower() != title.lower()]
    save_library(updated_library)

def search_books(search_by, search_term):
    library = load_library()
    return [book for book in library if search_term.lower() in book[search_by].lower()]

def display_statistics():
    library = load_library()
    total_books = len(library)
    read_books = sum(1 for book in library if book['read'])
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
    return total_books, percentage_read

# Streamlit UI
st.title("📚 Book Library Manager")
st.caption("Built with ❤️ using Python & Streamlit")

menu = ["Add Book", "Remove Book", "Search Library", "View All Books", "Statistics"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.text_input("Year")
    genre = st.text_input("Genre")
    read = st.checkbox("Have you read this book?")
    if st.button("Add Book"):
        add_book(title, author, year, genre, read)
        st.success(f"'{title}' has been added to the library!")

elif choice == "Remove Book":
    st.subheader("❌ Remove a Book")
    title = st.text_input("Enter book title to remove")
    if st.button("Remove Book"):
        remove_book(title)
        st.warning(f"'{title}' has been removed from the library!")

elif choice == "Search Library":
    st.subheader("🔍 Search Books")
    search_by = st.selectbox("Search by", ["title", "author"])
    search_term = st.text_input("Enter search term")
    if st.button("Search"):
        results = search_books(search_by, search_term)
        if results:
            for book in results:
                st.write(f"📖 {book['title']} by {book['author']} ({book['year']}, {book['genre']})")
        else:
            st.warning("No books found!")

elif choice == "View All Books":
    st.subheader("📚 Library Collection")
    library = load_library()
    if library:
        for book in library:
            st.write(f"📖 {book['title']} by {book['author']} ({book['year']}, {book['genre']}) - {'✅ Read' if book['read'] else '❌ Unread'}")
    else:
        st.info("Library is empty!")

elif choice == "Statistics":
    st.subheader("📊 Library Statistics")
    total_books, percentage_read = display_statistics()
    st.write(f"Total Books: {total_books}")
    st.write(f"Books Read: {percentage_read:.2f}%")

st.sidebar.write("💡 **Manage your library effortlessly!**")