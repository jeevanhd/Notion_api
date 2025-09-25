# 🚀 Notion Integration API

A powerful FastAPI-based service that allows you to save topics and content directly to your Notion database through a RESTful API interface.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Notion API](https://img.shields.io/badge/Notion_API-2022--06--28-black.svg)](https://developers.notion.com)

## 📋 Table of Contents

- [Features](#✨ Features)
- [Project Structure](#📁 Project Structure)
- [Prerequisites](#🔧 Prerequisites)
- [Installation](#📦 Installation)
- [Configuration](#️-configuration)
- [Usage](#-usage)
  - [FastAPI Web Server](#fastapi-web-server)
  - [Command Line Interface](#command-line-interface)
- [API Endpoints](#-api-endpoints)
- [Examples](#-examples)
- [Development](#️-development)
- [Troubleshooting](#-troubleshooting)
## ✨ Features

- 🔗 **Notion Integration**: Direct integration with Notion API v2022-06-28
- 🌐 **REST API**: FastAPI-powered web service with automatic OpenAPI documentation
- 🛡️ **Input Validation**: Comprehensive request validation using Pydantic models
- ❌ **Error Handling**: Robust error handling with proper HTTP status codes
- 📖 **Interactive Docs**: Auto-generated Swagger UI and ReDoc documentation
- 🖥️ **CLI Support**: Command-line interface for direct script usage
- 🔒 **Environment Variables**: Secure configuration using environment variables
- 📊 **Health Monitoring**: Built-in health check and API info endpoints

## 📁 Project Structure

```txt
notion/
├── notion_api.py           # FastAPI web server
├── notion_service.py       # Core Notion integration logic
├── .env                    # Environment variables (create this)
├── .gitignore             # Git ignore rules
├── readme.md              # This documentation
└── __pycache__/           # Python cache (auto-generated)
```

## 🔧 Prerequisites

- **Python 3.11+**
- **Notion Account** with API access
- **Notion Integration** set up in your workspace

### Setting up Notion Integration

1. Go to [Notion Developers](https://developers.notion.com/)
2. Click "Create new integration"
3. Name your integration (e.g., "Topic Saver")
4. Select your workspace
5. Copy the **Internal Integration Token**
6. Create a database in Notion and copy its **Database ID**

## 📦 Installation

1. **Clone or download the project**

```bash
cd notion
```

1. **Install required packages**

```bash
pip install fastapi uvicorn python-dotenv requests pydantic
```

1. **Create environment file**

```bash
# Create .env file
touch .env
```

## ⚙️ Configuration

Create a `.env` file in the project root with your Notion credentials:

```env
# Notion API Configuration
NOTION_TOKEN=your_notion_integration_token_here
DATABASE_ID=your_notion_database_id_here
```

### How to get these values

**NOTION_TOKEN**:

- Go to your Notion integration settings
- Copy the "Internal Integration Token"

**DATABASE_ID**:

- Open your Notion database
- Copy the ID from URL: `https://notion.so/workspace/DATABASE_ID?v=...`
- Or use the share menu → "Copy link" and extract the ID

## 🚀 Usage

### FastAPI Web Server

Start the API server:

```bash
# Development mode with auto-reload
python -m uvicorn notion_api:app --reload

# Production mode
python -m uvicorn notion_api:app --host 0.0.0.0 --port 8000
```

The server will start at: `http://localhost:8000`

**Access Documentation**:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

### Command Line Interface

Use the script directly from command line:

```bash
python notion_service.py "Topic Name" "Topic Content"
```

**Example:**

```bash
python notion_service.py "Python Basics" "Python is a high-level programming language known for its simplicity and readability."
```

## 🌐 API Endpoints

### General Endpoints

| Method | Endpoint  | Description     | Response                                                               |
| ------ | --------- | --------------- | ---------------------------------------------------------------------- |
| GET    | `/`       | Welcome message | `{"message": "Welcome to Notion Integration API", "status": "active"}` |
| GET    | `/health` | Health check    | `{"status": "healthy", "service": "notion-integration-api"}`           |
| GET    | `/info`   | API information | API details and available endpoints                                    |

### Topic Endpoints

| Method | Endpoint      | Description          | Request Body                              | Response               |
| ------ | ------------- | -------------------- | ----------------------------------------- | ---------------------- |
| POST   | `/save_topic` | Save topic to Notion | `{"name": "string", "content": "string"}` | Success/Error response |

### Request/Response Models

**Topic Request:**

```json
{
  "name": "string (1-2000 chars, required)",
  "content": "string (min 1 char, required)"
}
```

**Success Response:**

```json
{
  "success": true,
  "message": "Page created successfully!",
  "page_id": "abc123-def456-ghi789",
  "url": "https://www.notion.so/workspace/page-title-abc123"
}
```

**Error Response:**

```json
{
  "success": false,
  "message": "Error description",
  "error_type": "NetworkError|UnexpectedError"
}
```

## 💡 Examples

### Using cURL

```bash
# Save a topic
curl -X POST "http://localhost:8000/save_topic" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "FastAPI Tutorial",
    "content": "FastAPI is a modern, fast web framework for building APIs with Python 3.7+"
  }'
```

### Using Python requests

```python
import requests

response = requests.post(
    "http://localhost:8000/save_topic",
    json={
        "name": "Machine Learning Basics",
        "content": "Machine Learning is a subset of AI that focuses on algorithms that learn from data."
    }
)

if response.status_code == 200:
    result = response.json()
    print(f"✅ {result['message']}")
    if result.get('url'):
        print(f"🔗 Page URL: {result['url']}")
else:
    print(f"❌ Error: {response.text}")
```

### Using JavaScript fetch

```javascript
const response = await fetch("http://localhost:8000/save_topic", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    name: "Web Development",
    content:
      "Modern web development involves HTML, CSS, JavaScript, and frameworks like React or Vue.",
  }),
});

const result = await response.json();
console.log(result);
```

## 🛠️ Development

### Project Dependencies

- **FastAPI**: Web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **Pydantic**: Data validation using Python type annotations
- **Requests**: HTTP library for Notion API calls
- **Python-dotenv**: Load environment variables from .env file

### Code Structure

- **`notion_service.py`**: Core business logic for Notion API integration
- **`notion_api.py`**: FastAPI web server with REST endpoints
- **`.env`**: Configuration file (not tracked in git)
- **`.gitignore`**: Excludes sensitive files and cache

### Adding New Features

1. **New endpoints**: Add them in `notion_api.py`
2. **New Notion operations**: Add them in `notion_service.py`
3. **New models**: Define Pydantic models in `notion_api.py`

## 🔍 Troubleshooting

### Common Issues

1. **❌ "Missing Notion token or Database id"**

- Check your `.env` file exists and contains valid credentials
- Ensure no extra spaces in your token/database ID

1. **❌ "401 Unauthorized"**

- Verify your Notion integration token is correct
- Ensure the integration has access to your database

1. **❌ "404 Not Found"**

- Check your database ID is correct
- Make sure the database exists in your Notion workspace

1. **❌ "Network error occurred"**

- Check your internet connection
  -N Verify Notion API is accessible

### Debug Mode

Add debug prints in `notion_service.py`:

```python
print(f"Token: {NOTION_TOKEN[:10]}...")  # First 10 chars only
print(f"Database ID: {DATABASE_ID}")
print(f"Request data: {data}")
```

### Logs

Check FastAPI logs when running with `--reload`:

```bash
python -m uvicorn notion_api:app --reload --log-level debug
```

## 🔐 Security Notes

- **Never commit `.env` file** to version control
- **Keep your Notion token secure** - treat it like a password
- **Use environment variables** in production deployments
- **Consider adding API authentication** for production use

## 📝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Commit your changes: `git commit -m 'Add some feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#🔍 Troubleshooting) section
2. Review [Notion API Documentation](https://developers.notion.com/reference)
3. Check [FastAPI Documentation](https://fastapi.tiangolo.com/)
4. Create an issue in this repository
