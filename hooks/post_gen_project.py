import subprocess
import sys


def init_git_repo():
    """Initializes a git repository and makes the first commit."""
    try:
        # Initialize the repository
        subprocess.check_call(["git", "init"])
        
        # Add all generated files
        subprocess.check_call(["git", "add", "."])
        
        # Make the initial commit
        subprocess.check_call([
            "git", "commit", "-m", "Initial commit: Scaffolding from template"
        ])

        name = '{{ cookiecutter.author_name }}'
        email = '{{ cookiecutter.author_email }}'
        remote = '{{ cookiecutter.git_url }}'
        if name:
            try:
                subprocess.check_call(["git", "config", "--global", "user.name", f'"{name}"'])
            except subprocess.CalledProcessError:
                print("\n[WARN] Failed to set git user name.")

        if email:
            try:
                subprocess.check_call(["git", "config", "--global", "user.email", f'"{email}"'])
            except subprocess.CalledProcessError:
                print("\n[WARN] Failed to set git user email.")

        if remote:
            try:
                subprocess.check_call(["git", "remote", "add", "origin", remote])
            except subprocess.CalledProcessError:
                print("\n[WARN] Failed to set remote URL.")
        
        print("\n[SUCCESS] Git repository initialized for setuptools_scm!")
        
    except FileNotFoundError:
        print("\n[ERROR] Git is not installed or not in the system PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Failed to initialize git repository: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_git_repo()