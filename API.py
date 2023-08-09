import csv
import requests

url = "https://www.googleapis.com/books/v1/volumes?q=python&startIndex=0&maxResults=40"

try:
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    books = data.get("items", [])
    filtered_books = []

    for book in books:
        volume_info = book.get("volumeInfo", {})
        title = volume_info.get("title", "")
        authors = volume_info.get("authors", [])
        publisher = volume_info.get("publisher", "")
        published_date = volume_info.get("publishedDate", "")
        average_rating = volume_info.get("averageRating", 0)
        ratings_count = volume_info.get("ratingsCount", 0)
        language = volume_info.get("language", "")
        genres = volume_info.get("categories", [])
        industry_identifiers = volume_info.get("industryIdentifiers", [])
        isbn_10 = next((identifier["identifier"] for identifier in industry_identifiers if identifier["type"] == "ISBN_10"), "")
        isbn_13 = next((identifier["identifier"] for identifier in industry_identifiers if identifier["type"] == "ISBN_13"), "")
        description = volume_info.get("description", "")
        cover_image_url = volume_info.get("imageLinks", {}).get("thumbnail", "")

        page_count = volume_info.get("pageCount", 0)

        if (
            title
            and isinstance(page_count, int)
            and page_count > 0
            and published_date and published_date[:4].isdigit() and int(published_date[:4]) > 2010
            and float(average_rating) >= 4.0
        ):
            filtered_books.append(
                {
                    "Title": title,
                    "Authors": ", ".join(authors),
                    "Publisher": publisher,
                    "Published Date": published_date,
                    "Average Rating": average_rating,
                    "Ratings Count": ratings_count,
                    "Language": language,
                    "Genres": ", ".join(genres),
                    "ISBN-10": isbn_10,
                    "ISBN-13": isbn_13,
                    "Description": description,
                    "Page Count": page_count,
                    "Cover Image URL": cover_image_url,
                }
            )

    sorted_books = sorted(filtered_books, key=lambda x: x["Average Rating"], reverse=True)

    print("Top 5 Books:")
    for book in sorted_books[:5]:
        print(f'Title: {book["Title"]}')
        print(f'Authors: {book["Authors"]}')
        print(f'Publisher: {book["Publisher"]}')
        print(f'Published Date: {book["Published Date"]}')
        print(f'Average Rating: {book["Average Rating"]}')
        print(f'Ratings Count: {book["Ratings Count"]}')
        print(f'Language: {book["Language"]}')
        print(f'Genres: {book["Genres"]}')
        print(f'ISBN-10: {book["ISBN-10"]}')
        print(f'ISBN-13: {book["ISBN-13"]}')
        print(f'Description: {book["Description"]}')
        print(f'Page Count: {book["Page Count"]}')
        print(f'Cover Image URL: {book["Cover Image URL"]}')
        print("---------------------------")

    csv_file = "books.csv"

    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "Title",
                "Authors",
                "Publisher",
                "Published Date",
                "Average Rating",
                "Ratings Count",
                "Language",
                "Genres",
                "ISBN-10",
                "ISBN-13",
                "Description",
                "Page Count",
                "Cover Image URL",
            ],
        )
        writer.writeheader()
        writer.writerows(sorted_books)

    print(f"Data saved to {csv_file} successfully.")

except requests.exceptions.RequestException as e:
    print("Request Error:", e)

except ValueError as e:
    print("Invalid JSON response:", e)

except Exception as e:
    print("An error occurred:", e)