# Contributing to AstrOS 🚀

Welcome to the AstrOS community! We're building the AI-integrated operating system, and we're excited to have you join us on this journey.

## 🌟 Our Vision

AstrOS aims to transform how humans interact with computers through natural language and AI-powered automation, while maintaining privacy, security, and the open-source principles that make great OS possible.

---

## 🚀 Quick Start for New Contributors

### Prerequisites

Before you begin, ensure you have:

- **Ubuntu 24.04 LTS** (recommended for development)
- **Python 3.12+** (Ubuntu 24.04 default)
- **Git** and basic command line knowledge
- **Docker** (for containerized development)
- **Build tools**: `sudo apt install build-essential`

### 🛠️ Development Environment Setup

1. **Fork and Clone**
   ```bash
   # Fork the repository on GitHub, then:
   git clone https://github.com/YOUR_USERNAME/astros-core.git
   cd astros-core
   git remote add upstream https://github.com/AstrOS-Project/astros-core.git
   ```

2. **Set Up Development Environment**
   ```bash
   # Option 1: Automated setup (recommended)
   ./scripts/setup-dev.sh
   
   # Option 2: Manual setup
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r requirements/dev.txt
   pre-commit install
   ```

3. **Verify Installation**
   ```bash
   # Run tests to ensure everything works
   pytest tests/
   
   # Start the development agent
   python -m astros.agent --config config/dev.yaml
   ```

4. **Join Our Community**
   - 💬 [Discord Server](https://discord.gg/astros) - Real-time chat and support
   - 🌐 [Matrix Room](https://matrix.to/#/#astros:matrix.org) - Open protocol chat
   - 📋 [GitHub Discussions](https://github.com/orgs/AstrOS-Project/discussions) - Long-form discussions

---

## 🤝 How to Contribute

### 🎯 Ways to Make an Impact

We welcome contributions of all sizes and types:

<table>
<tr>
<td width="50%">

#### 🐛 **Report Bugs & Issues**
- Use our [bug report template](.github/ISSUE_TEMPLATE/bug_report.md)
- Include system info (Ubuntu version, Python version)
- Provide clear reproduction steps
- Check existing issues to avoid duplicates

#### 💡 **Suggest Features**
- Use our [feature request template](.github/ISSUE_TEMPLATE/feature_request.md)
- Explain the use case and expected behavior
- Consider implementation complexity
- Engage in discussion with maintainers

</td>
<td width="50%">

#### 🔧 **Code Contributions**
- **Core Development**: Python agent and system integration
- **Plugin Development**: AI-powered automation plugins  
- **UI/UX**: GNOME Shell extensions, desktop interfaces
- **Documentation**: Guides, tutorials, API references
- **Testing**: Unit tests, integration tests, manual QA

#### 🎨 **Non-Code Contributions**
- **Documentation**: Writing and improving docs
- **Design**: UI/UX design, logos, graphics
- **Community**: Answering questions, mentoring newcomers
- **Translation**: Localization for international users

</td>
</tr>
</table>

### 🎪 Finding Your First Contribution

1. **Browse Good First Issues**: Look for [`good first issue`](https://github.com/search?q=org%3AAstrOS-Project+label%3A%22good+first+issue%22&type=issues) labels
2. **Check Help Wanted**: Issues labeled [`help wanted`](https://github.com/search?q=org%3AAstrOS-Project+label%3A%22help+wanted%22&type=issues) need contributors
3. **Plugin Ideas**: Check our [plugin wishlist](https://github.com/AstrOS-Project/astros-plugins/discussions)
4. **Documentation Gaps**: Help us improve our [documentation](https://github.com/AstrOS-Project/astros-docs)

---

## 🔄 Development Workflow

### Step 1: Choose Your Contribution

Before starting work:
- **Comment on the issue** to let others know you're working on it
- **Ask questions** if anything is unclear
- **Check for existing work** to avoid duplication
- **Discuss approach** for complex features

### Step 2: Create a Branch

```bash
# Always work from the latest develop branch
git checkout develop
git pull upstream develop

# Create a descriptive feature branch
git checkout -b feature/voice-command-processing
# or
git checkout -b fix/plugin-loading-error
# or  
git checkout -b docs/api-reference-update
```

### Step 3: Make Your Changes

Follow our coding standards and best practices:

#### 🐍 **Python Code Standards**
- **Formatter**: Black (line length: 88)
- **Linter**: Ruff with AstrOS configuration
- **Type Checker**: MyPy in strict mode
- **Import Sorting**: isort with Black compatibility

```bash
# Run code quality checks
black src/ tests/
ruff check src/ tests/
mypy src/
pytest tests/ --cov=src
```

#### 📝 **Commit Message Format**
We use [Conventional Commits](https://conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix  
- `docs`: Documentation changes
- `style`: Code style (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

**Scopes:**
- `core`: Core agent functionality
- `plugins`: Plugin system
- `ui`: User interface components
- `iso`: Ubuntu ISO building
- `docs`: Documentation
- `security`: Security-related changes

**Examples:**
```bash
git commit -m "feat(core): add natural language file search capability"
git commit -m "fix(plugins): resolve race condition in plugin loader"
git commit -m "docs(api): update plugin development guide with examples"
```

### Step 4: Test Your Changes

```bash
# Run full test suite
pytest tests/ -v

# Test specific components
pytest tests/core/ -v
pytest tests/plugins/ -v

# Run integration tests
pytest tests/integration/ -v --slow

# Test Ubuntu ISO build (if applicable)
./scripts/test-iso-build.sh
```

### Step 5: Create Pull Request

```bash
# Push your branch
git push origin feature/your-feature-name

# Create PR through GitHub UI or CLI
gh pr create --title "feat(core): add voice command processing" --body "Description of changes"
```

#### 📋 **Pull Request Guidelines**

- **Use our PR template** - it's automatically loaded
- **Link related issues** using "Closes #123" or "Fixes #456"  
- **Provide clear description** of what changed and why
- **Include screenshots/videos** for UI changes
- **Mark as draft** if work is still in progress
- **Request review** from relevant maintainers

---

## 🧩 Plugin Development

Creating plugins is one of the best ways to contribute! Plugins extend AstrOS with new AI-powered capabilities.

### 🏗️ Plugin Architecture

```python
# Basic plugin structure
from astros.plugin import BasePlugin, plugin_handler
from astros.types import Intent, Response

class MyAwesomePlugin(BasePlugin):
    """Plugin that does something awesome with AI."""
    
    name = "awesome-plugin"
    version = "1.0.0"
    description = "Does something awesome with user files"
    author = "Your Name <your.email@example.com>"
    
    # Plugin capabilities
    handles = ["file_organization", "smart_search"]
    requires_ai = True
    requires_permissions = ["file_system"]
    
    @plugin_handler("organize_files")
    async def organize_files(self, intent: Intent) -> Response:
        """Organize files based on natural language request."""
        # Your awesome AI-powered logic here
        return Response(
            success=True,
            message="Files organized successfully!",
            data={"files_moved": 42}
        )
    
    async def initialize(self):
        """Plugin initialization code."""
        self.logger.info("Awesome plugin initialized!")
    
    async def shutdown(self):
        """Cleanup when plugin is unloaded."""
        self.logger.info("Awesome plugin shutting down")
```

### 🎯 Plugin Development Guidelines

1. **Single Responsibility**: Each plugin should have one clear purpose
2. **Minimal Dependencies**: Keep external dependencies light and well-justified
3. **Error Handling**: Handle failures gracefully with proper logging
4. **Privacy Aware**: Respect user privacy settings and data preferences
5. **Documentation**: Include clear README with usage examples
6. **Testing**: Write tests for your plugin functionality

### 🏃‍♂️ Quick Plugin Setup

```bash
# Generate plugin scaffold
python scripts/create-plugin.py --name awesome-plugin --author "Your Name"

# This creates:
plugins/awesome-plugin/
├── plugin.yaml          # Plugin metadata
├── src/
│   ├── __init__.py
│   └── main.py         # Plugin implementation
├── tests/
│   └── test_plugin.py  # Plugin tests
├── README.md           # Plugin documentation  
└── requirements.txt    # Plugin dependencies
```

---

## 📊 Code Quality Standards

### 🎯 Quality Requirements

- **Test Coverage**: Maintain 80%+ code coverage
- **Type Hints**: All functions must have proper type annotations
- **Documentation**: All public APIs must have docstrings
- **Error Handling**: Proper exception handling with logging
- **Security**: Never commit API keys or sensitive data

### 🔍 Code Review Process

1. **Automated Checks**: All PRs must pass CI checks
2. **Peer Review**: At least one maintainer review required
3. **Testing**: New features must include tests
4. **Documentation**: User-facing changes need doc updates
5. **Backwards Compatibility**: Maintain API compatibility

### 🛡️ Security Guidelines

- **Never commit secrets**: Use environment variables or secure storage
- **Validate inputs**: All user inputs must be sanitized
- **Principle of least privilege**: Request minimal permissions needed
- **Security reviews**: Security-sensitive code gets extra review
- **Dependency scanning**: Regular vulnerability scans on dependencies

---

## 🏆 Recognition & Rewards

We believe in recognizing our contributors!

### 🌟 Contributor Benefits

- **Hall of Fame**: Featured on our website and README
- **Release Notes**: Major contributors mentioned in releases  
- **Swag**: AstrOS stickers, t-shirts, and exclusive merchandise
- **Conference Opportunities**: Speaking slots at open-source events
- **Early Access**: Beta features and insider updates
- **Direct Impact**: Shape the future of AI-powered computing

### 🎖️ Path to Maintainership

Active contributors can become maintainers with additional privileges:

**Requirements:**
- **Consistent Contributions**: Regular, high-quality contributions over 6+ months
- **Community Engagement**: Help other contributors and users
- **Technical Expertise**: Deep understanding of codebase and architecture
- **Leadership Skills**: Demonstrate initiative and mentorship abilities

**Benefits:**
- **Review Permissions**: Help review and merge pull requests  
- **Release Management**: Participate in release planning and execution
- **Project Direction**: Influence roadmap and architectural decisions
- **Direct Commit Access**: For trusted long-term contributors

---

## 🌍 Community Guidelines

### 💝 Our Values

- **🤝 Inclusivity**: Welcome contributors of all backgrounds and skill levels
- **💬 Respect**: Treat everyone with kindness and professionalism  
- **🚀 Innovation**: Embrace new ideas and creative solutions
- **🔍 Quality**: Strive for excellence in everything we build
- **🔒 Privacy**: Protect user privacy and data rights
- **🌐 Openness**: Transparent development and decision making

### 📋 Code of Conduct

We follow the [Contributor Covenant](CODE_OF_CONDUCT.md). In summary:

- **Be welcoming and inclusive** to people of all backgrounds
- **Be respectful** in all interactions
- **Be constructive** when giving feedback
- **Focus on what's best** for the community and users
- **Show empathy** towards other community members

### 🚨 Reporting Issues

If you experience or witness unacceptable behavior:
- **Contact maintainers**: Email conduct@astros.org
- **Private reporting**: All reports are handled confidentially
- **No retaliation**: We protect reporters from retaliation
- **Fair process**: All reports are investigated fairly and promptly

---

## 📚 Resources & Learning

### 🎓 Getting Started Resources

- **[Development Guide](docs/development.md)** - Detailed development setup
- **[Plugin Tutorial](docs/plugin-development.md)** - Step-by-step plugin creation
- **[API Reference](docs/api/)** - Complete API documentation
- **[Architecture Overview](docs/architecture.md)** - System design and components

### 🔗 External Resources

- **Python**: [Python.org](https://python.org) - Official Python documentation
- **Ubuntu**: [Ubuntu.com](https://ubuntu.com) - Ubuntu Linux documentation  
- **AI/ML**: [Hugging Face](https://huggingface.co) - AI model hub and resources
- **Open Source**: [Open Source Guides](https://opensource.guide) - Best practices

### 📹 Video Tutorials

- **[AstrOS Development Playlist](https://youtube.com/playlist?list=...)** - YouTube tutorials
- **[Plugin Development Workshop](https://youtube.com/watch?v=...)** - Live coding session
- **[Community Calls](https://youtube.com/playlist?list=...)** - Monthly community updates

---

## ❓ Getting Help

### 💬 Community Support

- **Discord**: [Join our server](https://discord.gg/astros) for real-time help
- **Matrix**: [Join our room](https://matrix.to/#/#astros:matrix.org) for open protocol chat
- **GitHub Discussions**: [Ask questions](https://github.com/orgs/AstrOS-Project/discussions) in our discussions
- **Stack Overflow**: Use the `astros` tag for technical questions

### 🆘 Troubleshooting

**Common Issues:**
- **Build failures**: Check our [troubleshooting guide](docs/troubleshooting.md)
- **Development setup**: Follow our [development guide](docs/development.md)  
- **Plugin development**: See our [plugin tutorial](docs/plugin-development.md)
- **Ubuntu issues**: Check [Ubuntu documentation](https://ubuntu.com/support)

**Getting Unstuck:**
1. Check existing [GitHub issues](https://github.com/AstrOS-Project/astros-core/issues)
2. Search our [documentation](https://docs.astros.org)
3. Ask in [Discord](https://discord.gg/astros) or [Matrix](https://matrix.to/#/#astros:matrix.org)
4. Create a [GitHub discussion](https://github.com/orgs/AstrOS-Project/discussions)

---

## 🙏 Thank You!

Contributing to open source can be challenging, but it's incredibly rewarding. You're not just writing code – you're helping build the future of human-computer interaction.

Every contribution matters, whether it's:
- 🐛 Fixing a small bug
- 📝 Improving documentation  
- 💡 Suggesting new features
- 🤝 Helping other contributors
- 🎉 Spreading the word about AstrOS

**Welcome to the AstrOS community! Let's build something amazing together.** 🚀

---

<div align="center">

### Ready to contribute?

**[🔍 Find an Issue](https://github.com/search?q=org%3AAstrOS-Project+label%3A%22good+first+issue%22&type=issues)** • **[💬 Join Discord](https://discord.gg/astros)** • **[📖 Read the Docs](https://docs.astros.org)**

*Made with ❤️ by the AstrOS community*

</div>
