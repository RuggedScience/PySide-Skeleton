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
        
        print("\n[SUCCESS] Git repository initialized for setuptools_scm!")
        
    except FileNotFoundError:
        print("\n[ERROR] Git is not installed or not in the system PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Failed to initialize git repository: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_git_repo()