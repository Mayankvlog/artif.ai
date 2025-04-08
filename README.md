# ArtifAI - AI Image Generation Platform

ArtifAI is a web application that allows users to generate, manage, and explore AI-created images using OpenAI's DALL-E model.

## Features

- **Image Generation**: Create stunning AI-generated images using text prompts
- **Style Selection**: Choose from various artistic styles (abstract, realistic, anime, etc.)
- **Aspect Ratio Control**: Generate images in different aspect ratios (1:1, 16:9, 9:16)
- **User Accounts**: Secure registration and authentication
- **Personal Gallery**: Save and manage your generated images
- **Favorites**: Mark your favorite creations for easy access
- **Mobile Responsive**: Works on devices of all sizes

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: MySQL with PyMySQL
- **AI Integration**: OpenAI API (DALL-E 3)
- **Frontend**: HTML5, CSS3, JavaScript (with Bootstrap)
- **Authentication**: Flask-Login

## Installation and Setup

### Prerequisites

- Python 3.11 or later (for local setup)
- MySQL database (for production) or SQLite (for development)
- OpenAI API key
- Docker and Docker Compose (optional, for containerized setup)

### Setting Up MySQL Database

1. Create a MySQL database:
   ```sql
   CREATE DATABASE artifai;
   CREATE USER 'artifai_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON artifai.* TO 'artifai_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

2. Create a `.env` file in the root directory by copying the example:
   ```
   cp .env.example .env
   ```
   Then edit the file to include your specific MySQL credentials and OpenAI API key.
   
3. Install the required dependencies:
   ```
   pip install -r requirements-extra.txt
   ```

4. Run the application:
   ```
   python app.py
   ```
   
5. Access the application at `http://localhost:5000`

### Alternative: Running with SQLite (for testing)

If you don't have MySQL installed, you can use SQLite for testing:

1. Create a `.env` file in the root directory with the following variables:
   ```
   SESSION_SECRET=your_session_secret_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   
2. Run the application:
   ```
   python app.py
   ```
   
   The application will create a SQLite database file named `artifai.db` in the project directory.
   
### Running with Docker

1. Make sure you have Docker and Docker Compose installed

2. Copy the .env.example file to .env and set your API key:
   ```
   cp .env.example .env
   ```
   
3. Edit the .env file to include your OpenAI API key

4. Start the application and MySQL database:
   ```
   docker-compose up -d
   ```
   
5. Access the application at http://localhost:5000

6. To stop the containers:
   ```
   docker-compose down
   ```

## Usage

1. Register a new account or login
2. Navigate to the Generator page
3. Enter a text prompt describing the image you want to create
4. Select a style and aspect ratio
5. Click "Generate" and wait for your image to be created
6. View and manage your images in the Gallery

## Environment Variables

- `DATABASE_URL`: MySQL connection string (format: mysql+pymysql://username:password@host/database)
- `MYSQL_HOST`: MySQL server hostname (optional, for direct connection)
- `MYSQL_USER`: MySQL username (optional, for direct connection)
- `MYSQL_PASSWORD`: MySQL password (optional, for direct connection)
- `MYSQL_DATABASE`: MySQL database name (optional, for direct connection)
- `SESSION_SECRET`: Secret key for session management
- `OPENAI_API_KEY`: Your OpenAI API key for DALL-E image generation

## License

[MIT License](LICENSE)

## Credits

Created by [Mayank]
