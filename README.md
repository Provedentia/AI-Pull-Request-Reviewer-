# GitHub PR Reviewer

An AI-powered Pull Request reviewer that automatically analyzes code changes and provides intelligent feedback using OpenAI's GPT models.

## Features

- 🤖 **AI-Powered Reviews**: Leverages OpenAI's GPT models for intelligent code analysis
- 🔍 **Comprehensive Analysis**: Reviews code quality, security, performance, and maintainability
- 🚀 **Easy Deployment**: Ready for deployment on Render, Railway, or any Docker-compatible platform
- 🔒 **Secure**: Webhook signature verification and secure API handling
- 📊 **Detailed Feedback**: Provides structured feedback with suggestions and risk assessment
- 🎯 **Focused Reviews**: Tailored analysis based on file types and programming languages

## Project Structure

```
PR-reviewer/
├── app/
│   ├── main.py                 # FastAPI application entrypoint
│   ├── core/
│   │   ├── config.py          # Configuration management
│   │   ├── logging.py         # Logging setup
│   │   └── security.py        # Security utilities
│   ├── routes/
│   │   └── webhook.py         # GitHub webhook handler
│   ├── services/
│   │   ├── github_service.py  # GitHub API interactions
│   │   └── openai_service.py  # OpenAI API interactions
│   ├── schemas/
│   │   ├── github.py          # GitHub data models
│   │   └── openai.py          # OpenAI data models
│   └── utils/
│       ├── diff_parser.py     # Git diff parsing utilities
│       └── prompt_formatter.py # AI prompt formatting
├── requirements.txt           # Python dependencies
├── Dockerfile                # Docker configuration
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Prerequisites

- Python 3.11 or higher
- GitHub Personal Access Token with repository access
- OpenAI API Key
- A publicly accessible URL for webhook delivery (use ngrok for local testing)

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd PR-reviewer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit the `.env` file with your actual values:

```env
# GitHub Configuration
GITHUB_TOKEN=your_github_personal_access_token_here
GITHUB_WEBHOOK_SECRET=your_webhook_secret_here

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Server Configuration
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### 4. Run the Application

```bash
python -m app.main
```

The API will be available at `http://localhost:8000`

## GitHub Integration

### 1. Create a GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with the following permissions:
   - `repo` (Full control of private repositories)
   - `pull_requests` (Read/write access to pull requests)

### 2. Set Up Webhook

1. Navigate to your repository's Settings → Webhooks
2. Click "Add webhook"
3. Configure the webhook:
   - **Payload URL**: `https://your-domain.com/api/v1/webhook`
   - **Content type**: `application/json`
   - **Secret**: Use the same value as `GITHUB_WEBHOOK_SECRET` in your `.env`
   - **Events**: Select "Pull requests"

### 3. Testing with ngrok (Local Development)

For local testing, use ngrok to expose your local server:

```bash
# Install ngrok (if not already installed)
# Visit https://ngrok.com/ for installation instructions

# Start your local server
python -m app.main

# In another terminal, expose port 8000
ngrok http 8000
```

Use the ngrok URL (e.g., `https://abc123.ngrok.io/api/v1/webhook`) as your webhook URL in GitHub.

## API Endpoints

### Webhook Endpoint
- **POST** `/api/v1/webhook` - Receives GitHub webhook events

### Health Check
- **GET** `/health` - Health check endpoint
- **GET** `/api/v1/health` - Health check with API versioning

### Documentation
- **GET** `/docs` - Interactive API documentation (development only)
- **GET** `/redoc` - Alternative API documentation (development only)

## Deployment

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t pr-reviewer .
```

2. Run the container:
```bash
docker run -p 8000:8000 --env-file .env pr-reviewer
```

### Render Deployment

1. Connect your repository to Render
2. Use the following configuration:
   - **Environment**: Docker
   - **Dockerfile Path**: `./Dockerfile`
   - **Port**: 8000
3. Add environment variables in Render's dashboard

### Railway Deployment

1. Connect your repository to Railway
2. Railway will automatically detect the Dockerfile
3. Add environment variables in Railway's dashboard
4. Deploy!

### Environment Variables for Production

Ensure these environment variables are set in your production environment:

```env
GITHUB_TOKEN=your_production_github_token
GITHUB_WEBHOOK_SECRET=your_production_webhook_secret
OPENAI_API_KEY=your_production_openai_key
OPENAI_MODEL=gpt-4
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=production
LOG_LEVEL=INFO
```

## How It Works

1. **Webhook Receipt**: GitHub sends a webhook when a PR is opened or updated
2. **Signature Verification**: The webhook signature is verified for security
3. **Diff Retrieval**: The PR diff is fetched using the GitHub API
4. **AI Analysis**: The diff is analyzed using OpenAI's GPT model
5. **Review Posting**: A structured review comment is posted back to the PR

## Configuration

### OpenAI Models

The application supports various OpenAI models:
- `gpt-4` (recommended for best results)
- `gpt-3.5-turbo` (faster, more cost-effective)

### Review Focus Areas

The AI reviewer analyzes:
- **Code Quality**: Style, consistency, best practices
- **Security**: Potential vulnerabilities and security issues
- **Performance**: Efficiency and optimization opportunities
- **Maintainability**: Code readability and structure
- **Functionality**: Logic correctness and edge cases

## Troubleshooting

### Common Issues

1. **Webhook not receiving events**
   - Check that the webhook URL is correct and accessible
   - Verify the webhook secret matches your environment variable
   - Check GitHub's webhook delivery logs

2. **Authentication errors**
   - Ensure your GitHub token has the required permissions
   - Verify your OpenAI API key is valid and has sufficient credits

3. **Review not posted**
   - Check the application logs for error messages
   - Verify the GitHub token has write access to the repository

### Logs

The application logs important events and errors. Check the logs for troubleshooting:

```bash
# If running locally
python -m app.main

# If running with Docker
docker logs <container-id>
```

## Security Considerations

- Webhook signatures are verified to ensure requests come from GitHub
- Secrets are stored in environment variables, not in code
- The application runs as a non-root user in Docker
- CORS is configured appropriately for the deployment environment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the application logs
3. Open an issue on GitHub with relevant details

---

**Note**: This application uses OpenAI's API, which incurs costs based on usage. Monitor your API usage and set appropriate limits to control costs.