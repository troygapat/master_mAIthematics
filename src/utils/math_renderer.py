"""Math rendering utilities for LaTeX"""

import re
from typing import List, Tuple


class MathRenderer:
    """Helper class for rendering mathematical content"""
    
    @staticmethod
    def contains_latex(text: str) -> bool:
        """
        Check if text contains LaTeX math expressions
        
        Args:
            text: Text to check
        
        Returns:
            True if LaTeX found
        """
        # Look for common LaTeX patterns
        patterns = [
            r'\$\$.*?\$\$',  # Display math
            r'\$.*?\$',      # Inline math
            r'\\[a-zA-Z]+',  # LaTeX commands
            r'\\\(.*?\\\)',  # Inline math alternative
            r'\\\[.*?\\\]',  # Display math alternative
        ]
        
        for pattern in patterns:
            if re.search(pattern, text, re.DOTALL):
                return True
        
        return False
    
    @staticmethod
    def extract_latex_expressions(text: str) -> List[Tuple[str, str]]:
        """
        Extract LaTeX expressions from text
        
        Args:
            text: Text containing LaTeX
        
        Returns:
            List of tuples (expression, type) where type is 'inline' or 'display'
        """
        expressions = []
        
        # Display math $$...$$
        display_pattern = r'\$\$(.*?)\$\$'
        for match in re.finditer(display_pattern, text, re.DOTALL):
            expressions.append((match.group(1), 'display'))
        
        # Inline math $...$
        inline_pattern = r'\$(?!\$)(.*?)(?<!\$)\$'
        for match in re.finditer(inline_pattern, text):
            expressions.append((match.group(1), 'inline'))
        
        return expressions
    
    @staticmethod
    def format_for_streamlit(text: str) -> str:
        """
        Format text with LaTeX for Streamlit display
        Streamlit natively supports LaTeX with $ and $$ delimiters
        
        Args:
            text: Text with LaTeX
        
        Returns:
            Formatted text (no changes needed for Streamlit)
        """
        return text
    
    @staticmethod
    def wrap_inline_math(text: str) -> str:
        """
        Ensure inline math is properly wrapped
        
        Args:
            text: Text with potential math expressions
        
        Returns:
            Text with properly wrapped math
        """
        # This is a simple heuristic - wrap common math patterns
        # Example: x^2 -> $x^2$
        
        # Common math patterns without delimiters
        patterns = [
            (r'(?<!\$)\b([a-z])\^(\d+)(?!\$)', r'$\1^\2$'),  # x^2
            (r'(?<!\$)\\frac\{([^}]+)\}\{([^}]+)\}(?!\$)', r'$\\frac{\1}{\2}$'),  # \frac{a}{b}
        ]
        
        for pattern, replacement in patterns:
            text = re.sub(pattern, replacement, text)
        
        return text
    
    @staticmethod
    def escape_latex_special_chars(text: str, in_math_mode: bool = False) -> str:
        """
        Escape special LaTeX characters
        
        Args:
            text: Text to escape
            in_math_mode: Whether text is in math mode
        
        Returns:
            Escaped text
        """
        if in_math_mode:
            # In math mode, most special chars are okay
            return text
        
        # Outside math mode, escape special chars
        special_chars = {
            '&': r'\&',
            '%': r'\%',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
            '\\': r'\textbackslash{}',
        }
        
        for char, escaped in special_chars.items():
            text = text.replace(char, escaped)
        
        return text
    
    @staticmethod
    def format_equation(equation: str, numbered: bool = False) -> str:
        """
        Format an equation for display
        
        Args:
            equation: Equation string
            numbered: Whether to number the equation
        
        Returns:
            Formatted equation
        """
        if not equation.startswith('$'):
            equation = f"$${equation}$$"
        
        return equation
    
    @staticmethod
    def format_problem_solution(problem: str, solution: str,
                               show_solution: bool = False) -> str:
        """
        Format a problem and its solution
        
        Args:
            problem: Problem text
            solution: Solution text
            show_solution: Whether to show the solution
        
        Returns:
            Formatted text
        """
        formatted = f"**Problem:**\n\n{problem}\n\n"
        
        if show_solution:
            formatted += f"**Solution:**\n\n{solution}"
        else:
            formatted += "*Solution hidden - click to reveal*"
        
        return formatted


# Streamlit-specific helper functions
def render_math_message(message: str, role: str = "student") -> str:
    """
    Render a message with math support for Streamlit
    
    Args:
        message: Message content
        role: Message role (student or tutor)
    
    Returns:
        Formatted message
    """
    # Streamlit handles LaTeX natively, just return the message
    return message


def create_problem_card(problem_number: int, problem_text: str,
                       difficulty: str = "medium") -> str:
    """
    Create a formatted problem card
    
    Args:
        problem_number: Problem number
        problem_text: Problem text
        difficulty: Difficulty level
    
    Returns:
        Formatted problem card HTML/Markdown
    """
    difficulty_emoji = {
        "easy": "🟢",
        "medium": "🟡",
        "hard": "🔴",
        "challenge": "⭐"
    }
    
    emoji = difficulty_emoji.get(difficulty, "⚪")
    
    return f"""
### {emoji} Problem {problem_number}

{problem_text}

---
"""

