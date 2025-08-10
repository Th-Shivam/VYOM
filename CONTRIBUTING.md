# 🤝 Contributing to VYOM

<div align="center">

![VYOM Logo](https://img.shields.io/badge/VYOM-Virtual%20Yet%20Omnipotent%20Machine-blue?style=for-the-badge&logo=robot)

**Welcome to VYOM – Virtual Yet Omnipotent Machine!** 🚀

*We're thrilled that you're interested in contributing.*

[![GSSoC'25](https://img.shields.io/badge/GSSoC-2025-orange?style=flat-square)](https://gssoc.girlscript.tech/)
[![Contributors Welcome](https://img.shields.io/badge/Contributors-Welcome-brightgreen?style=flat-square)](#)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=flat-square)](#)

</div>

Whether it's fixing a bug 🐛, adding a feature ✨, improving documentation 📚, or suggesting an enhancement 💡 — **every contribution counts!**

---

## 📦 Setting Up VYOM Locally

### Prerequisites
- Python 3.8+ installed on your system
- Git version control
- A GitHub account

### Quick Start Guide

1. **Fork & Clone**
   ```bash
   # Fork this repository to your GitHub account first
   git clone https://github.com/th-shivam/VYOM.git
   cd VYOM
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate Environment**
   
   **Windows:**
   ```cmd
   .venv\Scripts\activate
   ```
   
   **Mac/Linux:**
   ```bash
   source .venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Environment Configuration**
   ```bash
   # Create environment file from template
   cp .env.example .env
   # Add your API keys to .env file
   ```

6. **Launch VYOM**
   ```bash
   python main.py
   ```

> 🎉 **Congratulations!** VYOM is now running locally on your machine.

---

## 🛠️ How to Contribute

### Step-by-Step Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-awesome-feature
   # or
   git checkout -b fix/bug-description
   ```

2. **Develop & Test**
   - Make your changes
   - Test thoroughly locally
   - Ensure code follows our guidelines

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add voice command for media control"
   ```
   
   > 💡 **Tip:** Use [conventional commits](https://conventionalcommits.org/) format!

4. **Push & Create PR**
   ```bash
   git push origin feature/your-awesome-feature
   ```
   
   Then open a Pull Request to the `main` branch on GitHub.

---

## 🧾 Contribution Guidelines

### Code Standards
- ✅ Follow **PEP8** Python style guide
- ✅ Keep code **modular** and **well-documented**
- ✅ Add **meaningful comments** for complex logic
- ✅ Include **type hints** where appropriate

### Documentation
- 📝 Update `README.md` if your changes affect usage
- 📝 Add docstrings for new functions/classes
- 📝 Update relevant documentation files

### Pull Request Requirements
- 🔗 Link related issues in your PR description
- ✅ Ensure all tests pass
- 📋 Provide clear description of changes
- 🖼️ Include screenshots for UI changes

---

## 🐞 Reporting Issues

Found a bug? We want to hear about it! 

### Before Reporting
1. 🔍 **Search existing issues** to avoid duplicates
2. 📋 **Check FAQ** and documentation first

### When Creating an Issue
Please include:

| Information | Description |
|-------------|-------------|
| **Clear Title** | Brief, descriptive summary |
| **Description** | Detailed explanation of the issue |
| **Reproduction Steps** | Step-by-step guide to reproduce |
| **Expected Behavior** | What should happen |
| **Actual Behavior** | What actually happens |
| **Environment** | OS, Python version, dependencies |
| **Logs/Screenshots** | Any relevant error messages or visuals |

### Issue Templates
- 🐛 **Bug Report** - For reporting bugs
- ✨ **Feature Request** - For suggesting new features
- 📚 **Documentation** - For documentation improvements

---

## 🌟 Areas You Can Contribute To

<div align="center">

| Category | Description | Difficulty |
|----------|-------------|------------|
| 🎤 **Voice Commands** | Enhance voice recognition & new commands | `Beginner-Intermediate` |
| 🌐 **Web Automation** | Browser automation & web scraping modules | `Intermediate` |
| 🎨 **GUI Development** | User interface improvements & new features | `Intermediate-Advanced` |
| 📱 **Mobile App** | Companion mobile application development | `Advanced` |
| 📄 **Documentation** | Improve docs, tutorials, and guides | `Beginner` |
| ⚡ **Performance** | Code optimization & efficiency improvements | `Intermediate-Advanced` |

</div>

### 🔰 Good First Issues
Look for issues labeled with `good first issue` - these are perfect for newcomers!

---

## 🙌 Code of Conduct

We are committed to providing a **welcoming** and **inclusive** environment for all contributors.

### Our Standards
- ✅ Be respectful and inclusive
- ✅ Welcome newcomers and help them learn
- ✅ Focus on constructive feedback
- ✅ Respect different viewpoints and experiences

### Enforcement
Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to the project maintainers.

---

## 💡 Pro Tips for Contributors

<div align="center">

| 💎 **Best Practices** |
|------------------------|
| 🎯 **Small, focused PRs** are easier to review than massive changes |
| 📝 **Descriptive commit messages** help maintain project history |
| 🧪 **Run tests locally** before submitting changes |
| 💬 **Communicate early** - discuss major changes in issues first |
| 📖 **Read existing code** to understand project patterns |

</div>

### Commit Message Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Examples:**
- `feat(voice): add new media control commands`
- `fix(gui): resolve window sizing issue on macOS`
- `docs(readme): update installation instructions`

---

## 🏆 Recognition

Contributors will be:
- 📝 Listed in our **Contributors** section
- 🎖️ Recognized in release notes
- 💫 Featured in our **Hall of Fame**

---

## 📞 Get Help

Need assistance? Reach out through:

- 💬 **GitHub Discussions** - For general questions
- 🐛 **GitHub Issues** - For bug reports and feature requests  
- 📧 **Email** - For private inquiries

---

<div align="center">

## 🎉 Thank You!

**Every contribution, no matter how small, makes VYOM better for everyone.**

---

> **Made with ❤️ by [Shivam Singh](https://github.com/shivamsingh) and the VYOM Community**

[![GSSoC'25 Project](https://img.shields.io/badge/GSSoC'25-Project-orange?style=for-the-badge)](https://gssoc.girlscript.tech/)

**⭐ Star this repository if you found it helpful!**

</div>
