import re
import html
import chardet
from bs4 import BeautifulSoup


def detect_encoding(fdf_path):
    """Detects the encoding of the FDF file, considering UTF-16 cases."""
    with open(fdf_path, "rb") as file:
        raw_data = file.read()

    # If the file starts with UTF-16 BOM, force UTF-16 decoding
    if raw_data.startswith(b'\xff\xfe'):
        print("⚠️ Detected UTF-16 LE BOM, forcing UTF-16 LE decoding")
        return "utf-16-le"
    elif raw_data.startswith(b'\xfe\xff'):
        print("⚠️ Detected UTF-16 BE BOM, forcing UTF-16 BE decoding")
        return "utf-16-be"

    detected = chardet.detect(raw_data)
    encoding = detected["encoding"]
    print(f"🔍 Detected Encoding: {encoding}")

    # If chardet detection is uncertain, default to UTF-16
    if encoding is None or encoding.lower() in ["ascii", "utf-8", "utf-8-sig", "latin-1"]:
        encoding = "utf-16"

    return encoding


def extract_text_from_xml(xml_string):
    """Extracts readable text from an XML string using BeautifulSoup."""
    soup = BeautifulSoup(xml_string, "lxml")
    return soup.get_text(separator=" ").strip()


def extract_comments_from_fdf(fdf_path):
    """Extracts and cleans comments from an FDF file, handling encoding properly."""
    encoding = detect_encoding(fdf_path)

    # Read FDF as binary and manually decode
    with open(fdf_path, "rb") as file:
        raw_data = file.read()

    # Decode with detected encoding
    content = raw_data.decode(encoding, errors="replace")

    # Remove UTF-16 BOM (þÿ)
    content = content.lstrip("\ufeff")

    # Normalize line endings and remove unnecessary characters
    content = content.replace("\r\n", "\n").replace("\r", "")

    comments = []

    # Extract plain text comments from /Contents(...)
    matches_contents = re.findall(r"/Contents\((.*?)\)", content, re.DOTALL)
    for match in matches_contents:
        cleaned_text = match.replace(r"\(", "(").replace(r"\)", ")").strip()
        comments.append(cleaned_text)

    # Extract HTML/XML-encoded comments from /RC(...)
    matches_rc = re.findall(r"/RC\((.*?)\)", content, re.DOTALL)
    for match in matches_rc:
        # Convert HTML entities (&#250; → ú, etc.)
        decoded_text = html.unescape(match)

        # Extract plain text from XML
        cleaned_text = extract_text_from_xml(decoded_text)

        # Append cleaned comment
        comments.append(cleaned_text)

    return comments


def save_comments_to_file(comments, output_path):
    """Saves extracted comments to a text file in UTF-8 without corruption."""
    total_chars = sum(len(comment) for comment in comments)
    total_words = sum(len(comment.split()) for comment in comments)

    with open(output_path, "w", encoding="utf-8", newline="\n") as file:
        for idx, comment in enumerate(comments, 1):
            cleaned_comment = comment.replace("\r", "")  # Extra safeguard to remove \r
            file.write(f"{idx}. {cleaned_comment}\n\n")
        file.write(f"Total words: {total_words}\n")
        file.write(f"Total letters (including spaces): {total_chars}\n")

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

print(f"\n📂 Comments successfully saved to {output_text_file} with correct encoding and clean text!")
