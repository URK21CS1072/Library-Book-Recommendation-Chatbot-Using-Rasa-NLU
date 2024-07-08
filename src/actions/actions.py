import pandas as pd
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from sentence_transformers import SentenceTransformer, util
import numpy as np
from fuzzywuzzy import process

class ActionRecommendBook(Action):
    def name(self) -> str:
        return "action_recommend_book"

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.df = pd.read_csv('D:/RASA/books.csv') 
        self.df['description'] = self.df['description'].fillna('')
        self.description_embeddings = self.model.encode(self.df['description'].tolist(), show_progress_bar=True)

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        genre = next(tracker.get_latest_entity_values("genre"), None)
        author = next(tracker.get_latest_entity_values("author"), None)
        description = tracker.latest_message['text']

        filtered_books = self.df

        if genre:
            genres = self.df['categories'].str.split(',').explode().unique().tolist()
            closest_genre, _ = process.extractOne(genre, genres)
            filtered_books = filtered_books[filtered_books['categories'].str.contains(closest_genre, case=False, na=False)]

        elif author:
            authors = self.df['authors'].unique().tolist()
            closest_author, _ = process.extractOne(author, authors)
            filtered_books = filtered_books[filtered_books['authors'].str.contains(closest_author, case=False, na=False)]

        elif description:
            user_embedding = self.model.encode(description)
            similarities = util.pytorch_cos_sim(user_embedding, self.description_embeddings)[0]
            top_indices = np.argsort(-similarities)[:10].tolist()
            filtered_books = self.df.iloc[top_indices]

        if not filtered_books.empty:
            responses = []
            for _, book in filtered_books.iterrows():
                # Format book title and author in bold using Markdown syntax
                book_title_author = f"**'{book['title']}'** by **{book['authors']}**"
                if len(responses) < 10:  # To ensure only top 10 are added
                    responses.append(book_title_author)
            response = "Here are some recommendations based on your description:\n\n" + "\n".join(responses)
        else:
            response = "I couldn't find any matching books. Please try a different query."

        dispatcher.utter_message(text=response)
        return []


class ActionInquireBookDetails(Action):
    def name(self) -> str:
        return "action_inquire_book_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        title = next(tracker.get_latest_entity_values("title"), None)
        author = next(tracker.get_latest_entity_values("author"), None)
        df = pd.read_csv('D:/RASA/books.csv')  

        if title:
            book_details = df.loc[df['title'].str.contains(title, case=False)]
            if author:
                book_details = book_details[book_details['authors'].str.contains(author, case=False)]
            if not book_details.empty:
                for _, book in book_details.iterrows():
                    # Format the response
                    message = f"**{book['title']}**\n"
                    message += f"![Book Thumbnail]({book['thumbnail']})\n" 
                    message += f"**Published Year:** {book['published_year']}\n"
                    message += f"**Author:** {book['authors']}\n"
                    message += f"**isbn13:** {book['isbn13']}\n"
                    message += f"**isbn10:** {book['isbn10']}\n"
                    message += f"**Average Rating:** {book['average_rating']}\n"
                    message += f"**Ratings Count:** {book['ratings_count']}\n"
                    message += f"**Number of Pages:** {book['num_pages']}\n"
                    message += f"**Description:** {book['description']}\n"

                    dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text="Sorry, I couldn't find that book.")
        else:
            dispatcher.utter_message(text="Please provide the title of the book you want to know about.")
        return []
    

class ActionInquireAuthorDetails(Action):
    def name(self) -> str:
        return "action_inquire_author_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        author_name = next(tracker.get_latest_entity_values("author"), None)
        df = pd.read_csv('D:/RASA/books.csv')  # Adjust the path as necessary

        if author_name:
            # Ensure the 'authors' column does not contain NaN values
            df['authors'] = df['authors'].fillna('Unknown')

            # Filter the DataFrame, safely handling rows where 'authors' might have been NaN
            books_by_author = df[df['authors'].str.contains(author_name, case=False, na=False)]

            if not books_by_author.empty:
                num_books = books_by_author.shape[0]
                average_rating = books_by_author['average_rating'].astype(float).mean()
                genres = books_by_author['categories'].str.split(',').explode().unique().tolist()

                response = f"**{author_name}**\n"
                response += f"**Number of Books Authored:** {num_books}\n"
                response += f"**Average Rating of Authored Books:** {average_rating:.2f}\n"
                response += f"**Genres Authored:** {', '.join(genres)}\n"

                # Providing titles of the author's books
                titles = books_by_author['title'].tolist()
                response += "**Books Authored:** " + ", ".join([f"'{title}'" for title in titles[:10]])  # Limit to first 5 titles for brevity

                dispatcher.utter_message(text=response)
            else:
                dispatcher.utter_message(text=f"I couldn't find any books by {author_name}.")
        else:
            dispatcher.utter_message(text="Please specify the name of the author you're interested in.")

        return []