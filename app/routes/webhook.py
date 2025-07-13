from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import json
import logging
from app.schemas.github import GitHubWebhookPayload
from app.services.github_service import GitHubService
from app.services.openai_service import OpenAIService
from app.core.security import validate_github_webhook
from app.utils.diff_parser import DiffParser
from app.utils.prompt_formatter import PromptFormatter

router = APIRouter()
logger = logging.getLogger(__name__)

github_service = GitHubService()
openai_service = OpenAIService()


@router.post("/webhook")
async def handle_github_webhook(request: Request, background_tasks: BackgroundTasks):
    """Handle GitHub webhook events for pull requests"""
    
    # Get the raw payload
    payload = await request.body()
    
    # Validate the webhook signature
    try:
        validate_github_webhook(request, payload)
    except HTTPException as e:
        logger.error(f"Webhook validation failed: {e.detail}")
        raise e
    
    # Parse the JSON payload
    try:
        webhook_data = json.loads(payload)
    except json.JSONDecodeError:
        logger.error("Invalid JSON payload")
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    # Check if this is a pull request event
    if "pull_request" not in webhook_data:
        logger.info("Not a pull request event, ignoring")
        return JSONResponse(content={"message": "Not a pull request event"}, status_code=200)
    
    # Parse the webhook payload
    try:
        github_payload = GitHubWebhookPayload(**webhook_data)
    except Exception as e:
        logger.error(f"Failed to parse GitHub payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid GitHub payload")
    
    # Only process opened or synchronize events
    if github_payload.action not in ["opened", "synchronize"]:
        logger.info(f"Ignoring PR action: {github_payload.action}")
        return JSONResponse(content={"message": f"Ignoring action: {github_payload.action}"}, status_code=200)
    
    # Add the review task to background tasks
    background_tasks.add_task(
        process_pull_request_review,
        github_payload
    )
    
    return JSONResponse(content={"message": "Pull request review queued"}, status_code=200)


async def process_pull_request_review(github_payload: GitHubWebhookPayload):
    """Process the pull request review in the background"""
    
    try:
        repo_owner = github_payload.repository.owner.login
        repo_name = github_payload.repository.name
        pr_number = github_payload.pull_request.number
        pr_title = github_payload.pull_request.title
        pr_description = github_payload.pull_request.body or ""
        
        logger.info(f"Processing PR review for {repo_owner}/{repo_name}#{pr_number}")
        
        # Fetch the PR diff
        diff_content = await github_service.get_pull_request_diff(
            repo_owner, repo_name, pr_number
        )
        
        if not diff_content:
            logger.error(f"Failed to fetch diff for PR #{pr_number}")
            return
        
        # Parse the diff to get file extensions for context
        parsed_files = DiffParser.parse_diff(diff_content)
        file_extensions = DiffParser.get_file_extensions(parsed_files)
        
        # Create the review prompt
        review_prompt = PromptFormatter.create_code_review_prompt(
            diff_content=diff_content,
            pr_title=pr_title,
            pr_description=pr_description,
            file_extensions=file_extensions
        )
        
        # Get AI analysis
        ai_review = await openai_service.analyze_code_diff(
            diff_content, pr_title, pr_description
        )
        
        if not ai_review:
            logger.error(f"Failed to get AI review for PR #{pr_number}")
            return
        
        # Format the review comment
        review_comment = openai_service.format_review_comment(ai_review)
        
        # Post the review comment
        success = await github_service.post_review_comment(
            repo_owner, repo_name, pr_number, review_comment
        )
        
        if success:
            logger.info(f"Successfully posted review for PR #{pr_number}")
        else:
            logger.error(f"Failed to post review for PR #{pr_number}")
            
    except Exception as e:
        logger.error(f"Error processing PR review: {e}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(content={"status": "healthy"}, status_code=200)


@router.get("/webhook")
async def webhook_info():
    """Provide information about the webhook endpoint"""
    return JSONResponse(content={
        "message": "GitHub PR Reviewer Webhook",
        "endpoint": "/webhook",
        "method": "POST",
        "supported_events": ["pull_request"]
    }, status_code=200)