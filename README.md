# GitHub PR Reviewer

An AI-powered Pull Request reviewer that automatically analyzes code changes and provides intelligent feedback using OpenAI's GPT models.

## What This Project Does

This application acts as an automated code reviewer for GitHub pull requests. When a developer opens or updates a pull request, the system:

1. **Receives notifications** from GitHub via webhooks
2. **Analyzes the code changes** using AI (OpenAI's GPT models)
3. **Posts intelligent reviews** directly to the pull request with feedback on code quality, security, performance, and maintainability

Think of it as having an experienced developer automatically review every pull request in your repository, providing consistent, thorough feedback 24/7.

## Why Use This?

- **Consistent Reviews**: Every PR gets the same level of thorough analysis
- **Immediate Feedback**: Reviews are posted as soon as a PR is opened or updated
- **Educational**: Helps developers learn best practices through detailed feedback
- **Security-Focused**: Automatically identifies potential security vulnerabilities
- **Time-Saving**: Reduces the manual review burden on senior developers
- **Quality Assurance**: Catches common issues before they reach production

## How It Works

```
GitHub PR → Webhook → AI Analysis → Review Comment Posted
```

1. **Developer opens/updates a PR** on GitHub
2. **GitHub sends a webhook** to this application
3. **The app fetches the code diff** using GitHub's API
4. **AI analyzes the changes** for quality, security, and best practices
5. **A structured review is posted** back to the PR with specific feedback

## Review Focus Areas

The AI reviewer analyzes code changes across multiple dimensions:

- **Code Quality**: Style consistency, best practices, and maintainability
- **Security**: Potential vulnerabilities and security anti-patterns
- **Performance**: Efficiency concerns and optimization opportunities
- **Functionality**: Logic correctness and edge case handling
- **Documentation**: Code clarity and commenting

## Technology Stack

- **FastAPI**: Modern Python web framework for the API
- **GitHub API**: For fetching pull request data and posting reviews
- **OpenAI API**: For AI-powered code analysis
- **Docker**: For containerized deployment
- **Webhooks**: For real-time GitHub event notifications

## Example Review Output

When the AI analyzes a pull request, it provides structured feedback like:

```
## Code Review Summary

### Overall Assessment
This pull request introduces a new authentication feature with generally good code quality, but there are some security and performance considerations that should be addressed.

### Key Findings
- **Security**: Password validation could be stronger (line 42)
- **Performance**: Consider caching user lookups (line 67)
- **Code Quality**: Good use of type hints and error handling
- **Maintainability**: Functions are well-structured and documented

### Specific Recommendations
1. Add rate limiting to the login endpoint
2. Use environment variables for sensitive configuration
3. Consider adding unit tests for the new authentication logic
```

## Requirements

To run this application, you'll need:

- **GitHub Personal Access Token** (with repository and pull request permissions)
- **OpenAI API Key** (for AI-powered analysis)
- **Python 3.11+** environment
- **Public URL** for receiving GitHub webhooks

## Getting Started

1. **Set up your tokens**: Get a GitHub Personal Access Token and OpenAI API key
2. **Deploy the application**: Use Docker, Render, Railway, or run locally
3. **Configure webhooks**: Point your GitHub repository to your deployed app
4. **Start reviewing**: Open a pull request and watch the AI provide feedback

The application is designed to be deployed once and then work automatically for all pull requests in your configured repositories.

## Architecture & Design

This application follows a **webhook-driven architecture**:

- **Event-Driven**: Responds to GitHub events in real-time
- **Stateless**: No database required, processes each PR independently  
- **Modular**: Separate services for GitHub API, OpenAI API, and webhook handling
- **Secure**: Webhook signature verification and proper secret management
- **Scalable**: Can handle multiple repositories and high PR volumes

### Key Design Decisions

- **FastAPI**: Chosen for its async capabilities and automatic API documentation
- **Structured Prompts**: AI prompts are carefully crafted to provide consistent, actionable feedback
- **Diff-Based Analysis**: Only analyzes changed code, not entire files, for efficiency
- **Fail-Safe**: Errors don't break the PR workflow - they're logged but don't block development

## Use Cases

- **Small Teams**: Get expert-level reviews even with limited senior developer availability
- **Large Organizations**: Ensure consistent code quality standards across teams
- **Open Source Projects**: Provide helpful feedback to contributors automatically
- **Learning Environments**: Help junior developers learn best practices through detailed feedback
- **Code Quality Gates**: Catch common issues before manual review

---

## Detailed Setup Instructions

<details>
<summary>Click to expand full setup and deployment guide</summary>

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

</details>

## Important Considerations

### Cost Management
This application uses OpenAI's API, which incurs costs based on usage. Each PR review typically costs $0.01-$0.10 depending on the size of the changes and the model used (GPT-4 vs GPT-3.5-turbo).

### Privacy & Security
- Code is sent to OpenAI for analysis - ensure this complies with your organization's policies
- Webhook signatures are verified to prevent unauthorized access
- All sensitive configuration is stored in environment variables

### Limitations
- Only analyzes code changes (diffs), not entire file context
- Quality depends on the AI model's capabilities and training data
- May not catch all issues that human reviewers would identify
- Best used as a complement to, not replacement for, human code review

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

MIT License - see LICENSE file for details.