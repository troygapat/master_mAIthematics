# GitHub Setup Instructions

Your code is now saved in a local Git repository! Follow these steps to push it to GitHub.

## Step 1: Create a New GitHub Repository

1. **Go to GitHub**
   - Visit https://github.com
   - Log in to your account

2. **Create New Repository**
   - Click the "+" icon in the top right
   - Select "New repository"

3. **Repository Settings**
   - **Name**: `master-maithematics` (or any name you prefer)
   - **Description**: `Interactive AI Math Tutor with Claude Sonnet 4.5`
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)

4. **Click "Create repository"**

## Step 2: Connect Your Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
cd "C:\Users\LSBru\Python\Bactest w Claude\math_tutor"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

**Replace** `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual values!

### Example:
If your username is "TroyBrumfield" and repo name is "master-maithematics":
```bash
git remote add origin https://github.com/TroyBrumfield/master-maithematics.git
git branch -M main
git push -u origin main
```

## Step 3: Authenticate

When you push for the first time, you'll need to authenticate:

### Option A: Personal Access Token (Recommended)
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` permissions
3. Copy the token
4. When git asks for password, paste the token

### Option B: GitHub Desktop
1. Download GitHub Desktop from https://desktop.github.com
2. Sign in with your GitHub account
3. Add your local repository
4. Push to GitHub through the GUI

## Step 4: Verify

Visit your repository URL:
```
https://github.com/YOUR_USERNAME/YOUR_REPO_NAME
```

You should see all your files!

## Future Updates

After making changes to your code:

```bash
cd "C:\Users\LSBru\Python\Bactest w Claude\math_tutor"
git add .
git commit -m "Description of your changes"
git push
```

## Current Status

✅ Local Git repository initialized
✅ All files committed (39 files, 7,811 lines)
✅ .gitignore configured
✅ Ready to push to GitHub!

## What's Protected

The `.gitignore` file ensures these sensitive items are NOT pushed to GitHub:
- `.env` file (contains your API key)
- Database files (`tutoring.db`)
- `__pycache__` folders
- Virtual environment files

## Repository Contents

Your repository includes:
- ✅ Full source code
- ✅ README with installation instructions
- ✅ All documentation
- ✅ Requirements file
- ✅ Setup scripts
- ✅ Launcher files

---

**Questions?** Open an issue on GitHub after pushing your repository!

