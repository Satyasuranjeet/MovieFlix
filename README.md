# 🎬 MovieFlix

MovieFlix is a modern web application that allows users to search and watch movies across different categories. Built with React and Flask, it provides a seamless experience for discovering and streaming movie content.

![MovieFlix Screenshot](https://i.ibb.co/N2rZsZVQ/image.png)

## ✨ Features

- 🔍 Real-time movie search functionality
- 🎯 Category-based filtering
- 🎨 Modern, responsive UI design
- 🎥 Integrated video player
- ⬇️ Movie download capability
- 🚀 Server health monitoring
- 📱 Mobile-friendly interface

## 🛠️ Tech Stack

### Frontend
- React.js
- Tailwind CSS
- Lucide React Icons
- Modern React Hooks
- Responsive Design Components

### Backend
- Flask (Python)
- YouTube Data API v3
- CORS support
- Environment variable configuration
- Logging system

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Node.js (v14 or higher)
- Python (v3.8 or higher)
- npm or yarn
- pip (Python package manager)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/movieflix.git
cd movieflix
```

### 2. Backend Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Unix/macOS
venv\Scripts\activate     # For Windows
```

2. Install Python dependencies:
```bash
pip install flask flask-cors google-api-python-client python-dotenv
```

3. Create a `.env` file in the backend directory:
```env
YOUTUBE_API_KEY=your_youtube_api_key_here
```

4. Start the Flask server:
```bash
python app.py
```

### 3. Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Start the development server:
```bash
npm start
# or
yarn start
```

## 🎯 Usage

1. **Search Movies**: Enter a movie title in the search bar or select a category from the dropdown menu.

2. **Watch Movies**: Click on any movie card to open the video player modal.

3. **Download Movies**: Use the download button on each movie card to save movies locally.

4. **Browse Categories**: Use the category dropdown to filter movies by genre:
   - Comedy
   - Action
   - Animation
   - Cartoon
   - Sci-Fi
   - Fantasy
   - History

## 🔧 API Endpoints

### `GET /health`
- Check server status and uptime
- Response includes server status and YouTube API connection status

### `GET /search_movie`
- Search for movies by name or category
- Query parameters:
  - `name`: Movie title to search for
  - `category`: Movie category/genre

### `GET /popular_movies`
- Get a list of popular movies
- No parameters required

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- YouTube Data API for providing movie content
- React and Flask communities for excellent documentation
- All contributors who have helped to improve this project

## 📞 Support

For support, email support@movieflix.com or create an issue in the GitHub repository.

## 🔒 Security

Please note that this application is for educational purposes only. Make sure to comply with YouTube's terms of service when using the application.

---

Made with ❤️ by Satya Suranjeet Jena
