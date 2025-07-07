from typing import List, Dict, Optional
from app.utils.diff_parser import DiffParser


class PromptFormatter:
    """Utility class for formatting prompts for AI analysis"""
    
    @staticmethod
    def create_code_review_prompt(
        diff_content: str,
        pr_title: str,
        pr_description: str = "",
        file_extensions: List[str] = None
    ) -> str:
        """Create a comprehensive code review prompt"""
        
        # Parse the diff to get structured information
        files = DiffParser.parse_diff(diff_content)
        total_additions, total_deletions = DiffParser.get_total_changes(files)
        
        if not file_extensions:
            file_extensions = DiffParser.get_file_extensions(files)
        
        # Build the prompt
        prompt = f"""
# Code Review Request

## Pull Request Information
**Title:** {pr_title}
**Description:** {pr_description or "No description provided"}

## Change Summary
- **Files Modified:** {len(files)}
- **Total Additions:** {total_additions}
- **Total Deletions:** {total_deletions}
- **Languages/Extensions:** {', '.join(file_extensions) if file_extensions else 'Mixed'}

## Code Changes
```diff
{diff_content}
```

## Review Guidelines
Please provide a thorough code review focusing on:

### 1. Code Quality
- Code style and consistency
- Best practices for the identified programming languages
- Code organization and structure
- Naming conventions

### 2. Functionality & Logic
- Correctness of the implementation
- Edge cases and error handling
- Algorithm efficiency
- Business logic accuracy

### 3. Security
- Input validation
- Authentication/authorization
- Data sanitization
- Potential vulnerabilities

### 4. Performance
- Time complexity considerations
- Memory usage
- Database query optimization (if applicable)
- Caching opportunities

### 5. Maintainability
- Code readability
- Documentation and comments
- Test coverage
- Modularity and reusability

### 6. Dependencies & Integration
- New dependencies introduced
- API compatibility
- Breaking changes
- Migration considerations

## Response Format
Please structure your response as a JSON object with the following format:

```json
{{
    "review_summary": "Brief overall assessment (2-3 sentences)",
    "suggestions": [
        "Specific, actionable suggestions for improvement",
        "Focus on the most important issues first"
    ],
    "severity": "low|medium|high",
    "requires_changes": true/false,
    "strengths": [
        "Positive aspects of the code changes"
    ],
    "risks": [
        "Potential risks or concerns"
    ]
}}
```

## Additional Context
- Focus on significant issues rather than minor style preferences
- Provide specific line references when possible
- Consider the impact on existing codebase
- Be constructive and educational in your feedback
"""
        
        return prompt
    
    @staticmethod
    def create_security_focused_prompt(diff_content: str, file_extensions: List[str]) -> str:
        """Create a security-focused review prompt"""
        
        security_checks = {
            'py': ['SQL injection', 'XSS', 'CSRF', 'Input validation', 'Authentication'],
            'js': ['XSS', 'CSRF', 'Input validation', 'Authentication', 'Prototype pollution'],
            'java': ['SQL injection', 'XSS', 'Deserialization', 'Authentication', 'Authorization'],
            'php': ['SQL injection', 'XSS', 'File inclusion', 'Authentication', 'Input validation'],
            'go': ['SQL injection', 'XSS', 'Authentication', 'Memory safety', 'Concurrency issues'],
            'rs': ['Memory safety', 'Authentication', 'Input validation', 'Concurrency issues']
        }
        
        relevant_checks = []
        for ext in file_extensions:
            if ext in security_checks:
                relevant_checks.extend(security_checks[ext])
        
        relevant_checks = list(set(relevant_checks))  # Remove duplicates
        
        prompt = f"""
# Security-Focused Code Review

## Code Changes
```diff
{diff_content}
```

## Security Assessment Required
Please perform a security-focused review of the above code changes.

### Priority Security Checks
Based on the file types ({', '.join(file_extensions)}), pay special attention to:
{chr(10).join(f"- {check}" for check in relevant_checks)}

### General Security Concerns
- Input validation and sanitization
- Authentication and authorization mechanisms
- Data exposure and information leakage
- Injection vulnerabilities (SQL, XSS, Command, etc.)
- Insecure direct object references
- Security misconfigurations
- Cryptographic issues
- Error handling that might leak information

### Response Format
```json
{{
    "security_assessment": "Overall security posture of the changes",
    "vulnerabilities_found": [
        "List of specific security issues identified"
    ],
    "severity": "low|medium|high|critical",
    "recommendations": [
        "Specific security improvements needed"
    ],
    "compliance_notes": "Any compliance considerations (OWASP, etc.)"
}}
```

Focus on actionable security improvements and provide specific remediation steps.
"""
        
        return prompt
    
    @staticmethod
    def create_performance_focused_prompt(diff_content: str, file_extensions: List[str]) -> str:
        """Create a performance-focused review prompt"""
        
        performance_concerns = {
            'py': ['Algorithm complexity', 'Database queries', 'Memory usage', 'I/O operations'],
            'js': ['DOM manipulation', 'Event handling', 'Memory leaks', 'Bundle size'],
            'java': ['Memory allocation', 'Garbage collection', 'Thread safety', 'Database connections'],
            'sql': ['Query optimization', 'Index usage', 'Join performance', 'Data volume'],
            'go': ['Goroutine management', 'Memory allocation', 'Concurrency', 'I/O operations'],
            'rs': ['Memory allocation', 'Concurrency', 'Zero-copy operations', 'Async handling']
        }
        
        relevant_concerns = []
        for ext in file_extensions:
            if ext in performance_concerns:
                relevant_concerns.extend(performance_concerns[ext])
        
        relevant_concerns = list(set(relevant_concerns))
        
        prompt = f"""
# Performance-Focused Code Review

## Code Changes
```diff
{diff_content}
```

## Performance Analysis Required
Please analyze the performance implications of these code changes.

### Key Performance Areas
Based on the file types ({', '.join(file_extensions)}), focus on:
{chr(10).join(f"- {concern}" for concern in relevant_concerns)}

### Performance Checklist
- Time complexity analysis (Big O notation)
- Space complexity considerations
- Database query efficiency
- Caching strategies
- Resource utilization
- Scalability implications
- Bottleneck identification

### Response Format
```json
{{
    "performance_assessment": "Overall performance impact analysis",
    "bottlenecks_identified": [
        "Specific performance bottlenecks found"
    ],
    "optimizations": [
        "Recommended performance improvements"
    ],
    "complexity_analysis": "Time/space complexity assessment",
    "scalability_impact": "How changes affect system scalability"
}}
```

Provide specific, measurable recommendations for performance improvements.
"""
        
        return prompt