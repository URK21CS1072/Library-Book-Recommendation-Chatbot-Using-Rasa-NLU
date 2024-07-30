# Library-Book-Recommendation-Chatbot-Using-Rasa-NLU

In  response  to  the  growing  demand  for streamlined  library  management,  this  project  introduces  an innovative  system  centered  around  a  friendly  and  intuitive chatbot. The motivation behind this endeavor stems from the need for a cost-effective, personalized recommendation system tailored specifically to local library collections. By harnessing the power of Rasa NLU, a conversational agent was developed to seamlessly assist library visitors in discovering their next favorite read. Through a meticulous integration of Rasa NLU's capabilities,  including  custom  actions  for  book  and  author inquiries and entity extraction for genres and descriptions, the chatbot effectively navigates user queries within the library's context. With a keen focus on precision and user engagement, the system's DIETClassifier ensures accurate intent recognition, facilitating seamless interaction and meaningful responses. The project outcomes underscore the chatbot's ability to understand nuanced requests, provide tailored book recommendations, and enhance  user  experience  within  library  environments.  This initiative serves as a testament to the transformative potential of open-source AI tools in enhancing public service offerings and fostering  greater  accessibility  to  library  resources

# Book Recommendation Chatbot with Rasa

This project is a book recommendation chatbot built using Rasa, an open-source conversational AI framework. The chatbot can recommend books based on genre, author, or description provided by the user. It can also provide detailed information about specific books and authors.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)



## Features

- **Book Recommendation**: Recommends books based on genre, author, or description.
- **Book Details**: Provides detailed information about a specific book.
- **Author Details**: Provides detailed information about a specific author.

## Installation

### Prerequisites

- Python 3.10
- pip (Python package installer)
- Virtual environment tool (optional but recommended)

### Steps

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/book-recommendation-chatbot.git
    cd book-recommendation-chatbot
    ```

2. **Set up a virtual environment** (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Download the pre-trained model**:

    Download the `all-MiniLM-L6-v2` model from [Hugging Face](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) and place it in the `models` directory.

5. **Place the books dataset**:

    Ensure you have a CSV file named `books.csv` containing the book data. Place it in the root directory.

## Usage

### Training the Rasa Model

1. **Activate the virtual environment** (if not already activated):

    ```bash
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2. **Train the Rasa model**:

    ```bash
    python -m rasa train
    ```

### Running the Rasa Server

1. **Run the Rasa server**:

    ```bash
    python -m rasa run --enable-api --cors="*" --port 8098
    ```

### Running the Actions Server

1. **Run the actions server**:

    ```bash
    python -m rasa run actions
    ```
