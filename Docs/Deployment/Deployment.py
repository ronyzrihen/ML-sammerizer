import subprocess
import sys
import shutil


def check_docker_installed():
    """Check if Docker CLI is installed and accessible."""
    docker_path = shutil.which("docker")
    if docker_path is None:
        print("❌ Docker is not installed or not in PATH.")
        print("➡️  Please install Docker Desktop or Docker Engine and try again.")
        sys.exit(1)
    print(f"✅ Docker found at: {docker_path}")


def check_docker_running():
    """Check if the Docker daemon is running."""
    try:
        subprocess.run(["docker", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print("✅ Docker daemon is running.")
    except subprocess.CalledProcessError:
        print("❌ Docker daemon is not running.")
        print("➡️  Please start Docker before running this script.")
        sys.exit(1)


def run_docker_compose():
    """Run docker compose up -d to deploy services."""
    try:
        print("🚀 Starting deployment using Docker Compose...")
        subprocess.run(["docker", "compose", "up", "-d"], check=True)
        print("✅ Deployment successful! Containers are running in detached mode.")
        print("➡️  Run 'docker logs -it ml-summarizer-app' to view application logs")
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("🔍 Checking environment...")
    check_docker_installed()
    check_docker_running()
    run_docker_compose()
