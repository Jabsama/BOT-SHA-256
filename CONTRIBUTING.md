# Contributing to VoltageGPU Bot

Thank you for your interest in contributing to VoltageGPU Bot! 🚀

## 📋 Table of Contents
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Convention](#commit-convention)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)
- [Issue Reporting](#issue-reporting)

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/BOT-SHA-256.git
   cd BOT-SHA-256
   ```
3. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+ 
- pip or poetry
- Git

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install flake8 pytest black

# Copy environment template
cp .env.example .env
# Edit .env with your test API keys
```

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific bot in test mode
python final_optimized_bot.py --test

# Lint code
flake8 .

# Format code
black .
```

## 📝 Coding Standards

### Python Style
- Follow **PEP 8** guidelines
- Use **Black** for code formatting
- Maximum line length: **127 characters**
- Use **type hints** where possible

### Code Structure
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module docstring explaining purpose
"""

import os
import sys
# ... other imports

class BotClass:
    """Class docstring"""
    
    def __init__(self):
        """Initialize with clear docstring"""
        pass
        
    def method_name(self, param: str) -> bool:
        """Method docstring with parameters and return type"""
        pass
```

### Documentation
- **Docstrings** for all classes and methods
- **Comments** for complex logic
- **Type hints** for function parameters and returns
- **README updates** for new features

## 🔄 Commit Convention

We use **Conventional Commits** format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```bash
feat(twitter): add multi-account support
fix(telegram): resolve message encoding issue
docs(readme): update installation instructions
style(bot): format code with black
test(api): add VoltageGPU API tests
```

## 🔀 Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Ensure all tests pass**:
   ```bash
   python -m pytest
   flake8 .
   ```
4. **Update CHANGELOG.md** if applicable
5. **Create Pull Request** with:
   - Clear title and description
   - Reference related issues
   - Screenshots/demos if UI changes

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tests pass locally
- [ ] Added new tests for functionality
- [ ] Tested in different environments

## Screenshots (if applicable)
Add screenshots or GIFs demonstrating the changes
```

## 🧪 Testing

### Test Structure
```
tests/
├── test_bots.py          # Bot functionality tests
├── test_api.py           # API integration tests
├── test_config.py        # Configuration tests
└── fixtures/             # Test data
```

### Writing Tests
```python
import pytest
from unittest.mock import Mock, patch

def test_bot_initialization():
    """Test bot initializes correctly"""
    bot = FinalOptimizedBot(test_mode=True)
    assert bot.test_mode is True

@patch('requests.get')
def test_api_call(mock_get):
    """Test API calls with mocking"""
    mock_get.return_value.json.return_value = {'status': 'ok'}
    # Test implementation
```

### Test Categories
- **Unit tests**: Individual functions/methods
- **Integration tests**: API interactions
- **End-to-end tests**: Full bot workflows
- **Performance tests**: Load and timing tests

## 🐛 Issue Reporting

### Before Creating an Issue
1. **Search existing issues** for duplicates
2. **Check documentation** and FAQ
3. **Test with latest version**
4. **Reproduce the issue** consistently

### Issue Types
- **Bug Report**: Use the bug report template
- **Feature Request**: Use the feature request template
- **Question**: Use discussions for general questions

### Good Issue Examples
```markdown
**Bug**: Bot crashes when posting to Reddit
- Clear reproduction steps
- Expected vs actual behavior
- Environment details
- Error logs

**Feature**: Add Discord support
- Use case description
- Implementation suggestions
- Alternatives considered
```

## 🏗️ Development Branches

- **`master`**: Stable release branch
- **`develop`**: Development integration branch
- **`feature/*`**: Feature development branches
- **`hotfix/*`**: Critical bug fixes

### Workflow
```bash
# Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/new-feature

# Work on feature
git add .
git commit -m "feat: add new feature"

# Push and create PR to develop
git push origin feature/new-feature
```

## 📦 Release Process

1. **Version bump** in relevant files
2. **Update CHANGELOG.md**
3. **Create release tag**:
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```
4. **GitHub Release** with release notes

## 🤝 Code of Conduct

- **Be respectful** and inclusive
- **Help others** learn and grow
- **Focus on constructive feedback**
- **Respect different perspectives**

## 📞 Getting Help

- **GitHub Discussions**: General questions
- **GitHub Issues**: Bug reports and feature requests
- **Documentation**: Check existing guides first

## 🎉 Recognition

Contributors will be:
- **Listed in CONTRIBUTORS.md**
- **Mentioned in release notes**
- **Credited in documentation**

Thank you for contributing to VoltageGPU Bot! 🚀💰
