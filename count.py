import re
import html
import chardet
from bs4 import BeautifulSoup


def detect_encoding(fdf_path):
    """Detects the encoding of the FDF file automatically."""
    with open(fdf_path, "rb") as file:  # Read as binary
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result["encoding"]


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

    # Decode the file properly as UTF-16 (or fallback)
    try:
        content = raw_data.decode(encoding)
    except UnicodeDecodeError:
        print(f"⚠️ UnicodeDecodeError with {encoding}, trying ISO-8859-2")
        content = raw_data.decode("iso-8859-2", errors="replace")

    # Strip UTF-16 BOM if present
    #content = content.lstrip("\ufeff")

    # Normalize line endings and remove unnecessary characters
    #content = content.replace("\r\n", "\n").replace("\r", "")
    #content = content.replace("\r\n", "\n")

    comments = []

    # Extract plain text comments from /Contents(...)
    matches_contents = re.findall(r"/Contents\((.*?)\)", content, re.DOTALL)
    for match in matches_contents:
        #cleaned_text = match.replace(r"\(", "(").replace(r"\)", ")").strip()
        #comments.append(cleaned_text)
        comments.append(match)

    comments_dict = {}

    # Extract HTML/XML-encoded comments from /RC(...)
    matches_rc = re.findall(r"/RC\((.*?)\)", content, re.DOTALL)
    for idx, match in enumerate(matches_rc):
        # Convert HTML entities (&#250; → ú, etc.)
        decoded_text = html.unescape(match)

        # Extract plain text from XML
        #cleaned_text = extract_text_from_xml(decoded_text)
        #cleaned_text.replace("\r", "")  # Extra safeguard to remove \r

        # Append cleaned comment
        #comments_dict[idx] = cleaned_text
        comments_dict[idx] = decoded_text

    return comments_dict


def save_comments_to_file(comments: dict[int, str], output_path):
    """Saves extracted comments to a text file in UTF-8 without corruption."""
    total_chars = sum(len(comment) for idx, comment in comments.items())
    total_words = sum(len(comment.split()) for idx, comment in comments.items())

    with open(output_path, "w", encoding="utf-8", newline="\n") as file:
        for idx, comment in comments.items():
            cleaned_comment = comment.replace("\r", "")  # Extra safeguard to remove \r
            file.write(f"{idx}. {cleaned_comment}\n\n")
        file.write(f"Total words: {total_words}\n")
        file.write(f"Total letters (including spaces): {total_chars}\n")

    print(f"✅ Total words: {total_words}")
    print(f"✅ Total letters (including spaces): {total_chars}")


# Path to your FDF file
fdf_file_path = "output.fdf"
output_text_file = "comments.txt"

# Extract comments
comments = extract_comments_from_fdf(fdf_file_path)
# Save to text file
save_comments_to_file(comments, output_text_file)

print(f"\n📂 Comments successfully saved to {output_text_file} with correct encoding and clean text!")
