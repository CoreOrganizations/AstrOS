# Pull Request Template

## 🎯 Pull Request Summary

### 📝 Description
Briefly describe what this PR does and why it's needed.

### 🔗 Related Issues
- Closes #[issue number]
- Related to #[issue number]
- Depends on #[PR number]

### 🏷️ Type of Change
- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to change)
- [ ] 📚 Documentation update
- [ ] 🎨 Code style/formatting change
- [ ] ♻️ Refactoring (no functional changes)
- [ ] 🔧 Chore (dependencies, build config, etc.)
- [ ] 🧪 Tests (adding or updating tests)

---

## 🔄 Changes Made

### 🛠️ Technical Changes
List the main technical changes made:
- [ ] Modified core agent functionality
- [ ] Added new plugin capabilities
- [ ] Updated UI components
- [ ] Changed database schema
- [ ] Updated API endpoints
- [ ] Modified system integration
- [ ] Other: [specify]

### 📁 Files Changed
List the main files/directories modified:
- `src/astros/core/` - [brief description of changes]
- `plugins/example-plugin/` - [brief description of changes]
- `docs/` - [brief description of changes]

---

## 🧪 Testing

### ✅ Testing Done
- [ ] All existing tests pass
- [ ] Added new tests for new functionality
- [ ] Manually tested the changes
- [ ] Tested on Ubuntu 22.04 LTS
- [ ] Tested on Ubuntu 24.04 LTS
- [ ] Plugin functionality tested
- [ ] UI changes tested in GNOME
- [ ] Voice commands tested (if applicable)
- [ ] Edge cases tested

### 🧪 Test Commands Run
```bash
# List the commands you ran to test your changes
pytest tests/
python -m astros.agent --config config/dev.yaml
# Add other test commands here
```

### 🎯 Test Coverage
- [ ] Test coverage maintained or improved
- [ ] All new code has tests
- [ ] Integration tests pass

---

## 🖼️ Screenshots/Demo (if applicable)

### Before
[Screenshot or description of before state]

### After  
[Screenshot or description of after state]

### Demo Video/GIF
[Link to demo video or attach GIF showing the feature in action]

---

## 📋 Code Quality Checklist

### 🐍 Python Standards
- [ ] Code follows Black formatting (88 character limit)
- [ ] Passes Ruff linting checks
- [ ] Type hints added for all functions
- [ ] MyPy type checking passes
- [ ] Imports sorted with isort

### 📝 Documentation
- [ ] Docstrings added for new functions/classes
- [ ] README updated if needed
- [ ] API documentation updated
- [ ] Plugin documentation updated (if applicable)
- [ ] User-facing changes documented

### 🔒 Security
- [ ] No hardcoded secrets or API keys
- [ ] Input validation implemented
- [ ] Error handling doesn't expose sensitive info
- [ ] Follows security best practices
- [ ] No new security vulnerabilities introduced

---

## 🌍 Compatibility & Performance

### 🖥️ Platform Compatibility
- [ ] Works on Ubuntu 22.04 LTS
- [ ] Works on Ubuntu 24.04 LTS  
- [ ] Works with Python 3.12+
- [ ] Compatible with current plugin API
- [ ] No breaking changes to existing features

### ⚡ Performance Impact
- [ ] No significant performance regression
- [ ] Memory usage is reasonable
- [ ] Startup time not significantly impacted
- [ ] Plugin loading time acceptable

### 🔌 Plugin Ecosystem
- [ ] Existing plugins still work
- [ ] Plugin API changes are backwards compatible
- [ ] New plugin capabilities documented

---

## 🚀 Deployment Considerations

### 🏗️ Build & Release
- [ ] CI/CD pipeline passes
- [ ] ISO build not broken (if applicable)
- [ ] No new runtime dependencies added (or documented)
- [ ] Version numbers updated appropriately

### 📦 Distribution
- [ ] Package metadata updated
- [ ] Release notes content provided
- [ ] Migration guide needed (if breaking changes)
- [ ] User announcement planned

---

## 👥 Review Guidelines

### 🎯 Focus Areas for Reviewers
Please pay special attention to:
- [ ] Security implications
- [ ] Performance impact
- [ ] User experience
- [ ] API design
- [ ] Code architecture
- [ ] Test coverage
- [ ] Documentation accuracy

### ❓ Questions for Reviewers
- [Any specific questions you have for reviewers]
- [Areas where you'd like particular feedback]
- [Specific concerns or trade-offs made]

### 🤝 Collaboration
- [ ] I'm open to feedback and changes
- [ ] I'm available for follow-up questions
- [ ] I can make requested modifications promptly

---

## 📚 Additional Context

### 🎯 Design Decisions
Explain any significant design decisions made and the reasoning:

### 🔄 Alternative Approaches
Were there other ways to implement this? Why did you choose this approach?

### 🚧 Known Limitations
Are there any known limitations or TODOs for future work?

### 🔮 Future Considerations
How does this change impact future development?

---

## 🏁 Definition of Done

This PR is ready to merge when:
- [ ] All CI checks pass
- [ ] At least one maintainer has approved
- [ ] All review feedback has been addressed
- [ ] Documentation is updated
- [ ] Tests are passing
- [ ] No merge conflicts
- [ ] Security review completed (if needed)

---

## 🙏 Additional Notes

[Any additional information, context, or notes for reviewers]

---

### 📋 Maintainer Checklist (for maintainer use)
- [ ] PR follows contribution guidelines
- [ ] Code quality standards met
- [ ] Security review completed
- [ ] Breaking change impact assessed
- [ ] Documentation review completed
- [ ] Ready to merge
