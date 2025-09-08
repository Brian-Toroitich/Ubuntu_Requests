import requests
import os
from urllib.parse import urlparse
import hashlib

def get_filename_from_url(url):
    """Extract filename from URL or generate a default one."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    return filename if filename else "downloaded_image.jpg"

def generate_unique_filename(content, original_filename):
    """Prevent duplicates by appending hash to filename."""
    file_hash = hashlib.md5(content).hexdigest()[:8]
    name, ext = os.path.splitext(original_filename)
    return f"{name}_{file_hash}{ext}"

def fetch_image(url):
    """Download and save an image with safety checks."""
    try:
        os.makedirs("Fetched_Images", exist_ok=True)

        # Request with timeout
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()

        # Precaution: Ensure it's an image
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ Not an image: {url} ({content_type})")
            return

        # Extract and generate filename
        filename = get_filename_from_url(url)
        unique_filename = generate_unique_filename(response.content, filename)
        filepath = os.path.join("Fetched_Images", unique_filename)

        # Prevent duplicate downloads
        if os.path.exists(filepath):
            print(f"⚠ Duplicate detected, skipped: {unique_filename}")
            return

        # Save image
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {unique_filename}")
        print(f"✓ Saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    urls = input("Enter one or more image URLs (separated by spaces): ").split()
    for url in urls:
        fetch_image(url)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
