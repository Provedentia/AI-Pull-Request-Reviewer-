import re
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class DiffParser:
    """Utility class for parsing git diffs and extracting relevant information"""
    
    @staticmethod
    def parse_diff(diff_content: str) -> List[Dict]:
        """Parse a git diff and extract file changes"""
        files = []
        current_file = None
        
        lines = diff_content.split('\n')
        
        for line in lines:
            if line.startswith('diff --git'):
                # Start of a new file
                if current_file:
                    files.append(current_file)
                
                # Extract file paths
                match = re.search(r'diff --git a/(.*) b/(.*)', line)
                if match:
                    current_file = {
                        'old_path': match.group(1),
                        'new_path': match.group(2),
                        'changes': [],
                        'additions': 0,
                        'deletions': 0
                    }
            
            elif line.startswith('+++') or line.startswith('---'):
                # File path indicators
                continue
            
            elif line.startswith('@@'):
                # Hunk header
                if current_file:
                    hunk_info = DiffParser._parse_hunk_header(line)
                    current_file['changes'].append({
                        'type': 'hunk',
                        'info': hunk_info,
                        'lines': []
                    })
            
            elif current_file and current_file['changes']:
                # Code lines
                last_change = current_file['changes'][-1]
                if line.startswith('+'):
                    last_change['lines'].append({
                        'type': 'addition',
                        'content': line[1:]
                    })
                    current_file['additions'] += 1
                elif line.startswith('-'):
                    last_change['lines'].append({
                        'type': 'deletion',
                        'content': line[1:]
                    })
                    current_file['deletions'] += 1
                elif line.startswith(' '):
                    last_change['lines'].append({
                        'type': 'context',
                        'content': line[1:]
                    })
        
        # Don't forget the last file
        if current_file:
            files.append(current_file)
        
        return files
    
    @staticmethod
    def _parse_hunk_header(line: str) -> Dict:
        """Parse a hunk header line like @@ -1,4 +1,6 @@"""
        match = re.search(r'@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@', line)
        if match:
            return {
                'old_start': int(match.group(1)),
                'old_count': int(match.group(2)) if match.group(2) else 1,
                'new_start': int(match.group(3)),
                'new_count': int(match.group(4)) if match.group(4) else 1
            }
        return {}
    
    @staticmethod
    def get_file_extensions(files: List[Dict]) -> List[str]:
        """Get unique file extensions from the diff"""
        extensions = set()
        for file in files:
            path = file.get('new_path', file.get('old_path', ''))
            if '.' in path:
                ext = path.split('.')[-1].lower()
                extensions.add(ext)
        return list(extensions)
    
    @staticmethod
    def get_total_changes(files: List[Dict]) -> Tuple[int, int]:
        """Get total additions and deletions"""
        total_additions = sum(f.get('additions', 0) for f in files)
        total_deletions = sum(f.get('deletions', 0) for f in files)
        return total_additions, total_deletions
    
    @staticmethod
    def filter_significant_changes(files: List[Dict], min_changes: int = 5) -> List[Dict]:
        """Filter files with significant changes"""
        return [
            f for f in files 
            if (f.get('additions', 0) + f.get('deletions', 0)) >= min_changes
        ]
    
    @staticmethod
    def extract_context_lines(files: List[Dict], context_lines: int = 3) -> Dict:
        """Extract context around changes for better analysis"""
        context_data = {}
        
        for file in files:
            file_path = file.get('new_path', file.get('old_path', ''))
            context_data[file_path] = []
            
            for change in file.get('changes', []):
                if change['type'] == 'hunk':
                    hunk_context = {
                        'hunk_info': change['info'],
                        'relevant_lines': []
                    }
                    
                    lines = change.get('lines', [])
                    for i, line in enumerate(lines):
                        if line['type'] in ['addition', 'deletion']:
                            # Get context around this change
                            start = max(0, i - context_lines)
                            end = min(len(lines), i + context_lines + 1)
                            
                            context_lines_data = lines[start:end]
                            hunk_context['relevant_lines'].extend(context_lines_data)
                    
                    if hunk_context['relevant_lines']:
                        context_data[file_path].append(hunk_context)
        
        return context_data