import re
import chardet


def detect_encoding(fdf_path):
    """Detects the encoding of the FDF file automatically and verifies it."""
    with open(fdf_path, "rb") as file:
        raw_data = file.read()

    detected = chardet.detect(raw_data)
    encoding = detected["encoding"]

    print(f"🔍 Detected Encoding: {encoding}")

    # If detection is unreliable, manually set it to a more common encoding for Hungarian FDFs
    if encoding is None or encoding.lower() in ["ascii", "utf-8", "utf-8-sig", "latin-1"]:
        encoding = "iso-8859-2"  # Default to Hungarian-friendly encoding

    return encoding


def extract_comments_from_fdf(fdf_path):
    """Extracts text annotations (comments) from an FDF file, ensuring correct encoding."""
    encoding = detect_encoding(fdf_path)

    comments = []

    with open(fdf_path, "r", encoding=encoding, errors="replace") as file:
        content = file.read()

    # Normalize line endings and remove unnecessary characters
    content = content.replace("\r\n", "\n").replace("\r", "")

    # Extract annotation text (stored in /Contents(...) in FDF)
    matches = re.findall(r"/Contents\((.*?)\)", content, re.DOTALL)

    # Cleaning up escaped characters like \( and \), ensuring text is properly readable
    for match in matches:
        cleaned_text = match.encode(encoding, "ignore").decode("utf-8", "ignore")  # Fix encoding issues
        cleaned_text = cleaned_text.replace(r"\(", "(").replace(r"\)", ")").strip()
        comments.append(cleaned_text)

    return comments


def save_comments_to_file(comments, output_path):
    """Saves extracted comments to a text file in UTF-8 without any encoding corruption."""
    total_chars = sum(len(comment) for comment in comments)
    total_words = sum(len(comment.split()) for comment in comments)

    with open(output_path, "w", encoding="utf-8", newline="\n") as file:
        for idx, comment in enumerate(comments, 1):
            file.write(f"{idx}. {comment}\n\n")  # Properly formatted comments
        file.write(f"Total words: {total_words}\n")
        file.write(f"Total letters (including spaces): {total_chars}\n")

    # Print extracted comments for verification
    print("\n📜 Extracted Comments:\n" + "-" * 30)
    for idx, comment in enumerate(comments, 1):
        print(f"{idx}. {comment}\n")

    print(f"✅ Total words: {total_words}")
    print(f"✅ Total letters (including spaces): {total_chars}")


# Path to your FDF file
fdf_file_path = "example.fdf"  # Change this to your actual file
output_text_file = "comments.txt"

# Extract comments
comments = extract_comments_from_fdf(fdf_file_path)

# Save to text file
save_comments_to_file(comments, output_text_file)

print(f"\n📂 Comments successfully saved to {output_text_file} with proper encoding!")
