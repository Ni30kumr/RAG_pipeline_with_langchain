# RAG-based User Bot System

This project implements a Retrieval-Augmented Generation (RAG) based user bot system using FastAPI, SQLAlchemy, and Pinecone. It allows users to create accounts, upload PDFs, and query a bot trained on their uploaded documents.

## Features

- User registration and authentication
- PDF document upload for each user
- Custom bot creation for each user based on their uploaded documents
- Query interface for user-specific bots
- User search functionality
- User deletion with associated data cleanup

## Technologies Used

- FastAPI: For creating the API endpoints
- SQLAlchemy: For database operations
- Pinecone: For vector storage and similarity search
- LangChain: For creating the RAG pipeline
- HuggingFace Transformers: For embeddings
- MySQL: As the relational database

## Project Structure

- `main.py`: The main FastAPI application
- `user_manager.py`: Contains the UserManager class with user-related operations
- `database.py`: Database connection and session management
- `models.py`: SQLAlchemy models for the database
- `lang_data.py`: Functions for creating and managing Pinecone indexes
- `query.py`: Functions for creating the RAG chain and querying the bot

## Setup and Installation

1. Clone the repository:
2. Install the required dependencies:
3. Set up your MySQL database and update the `URL_DATABASE` in `database.py` with your credentials.
4. Set up your Pinecone account and add your API key to a `.env` file:
## API Endpoints

- POST `/users/`: Create a new user
- POST `/users/{user_id}/setup_bot`: Upload a PDF and set up a bot for a user
- POST `/users/{user_id}/query`: Query a user's bot
- GET `/users/search`: Search for users by username or email
- POST `/users/delete`: Delete a user and their associated data

## Usage

1. Create a new user using the `/users/` endpoint.
2. Upload a PDF and set up a bot for the user using the `/users/{user_id}/setup_bot` endpoint.
3. Query the bot using the `/users/{user_id}/query` endpoint.
4. Search for users using the `/users/search` endpoint.
5. Delete a user and their data using the `/users/delete` endpoint.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
