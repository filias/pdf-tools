import re
import chardet

def detect_encoding(fdf_path):
    """Detects the encoding of the FDF file automatically."""
    with open(fdf_path, "rb") as file:  # Read as binary
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result["encoding"]

def extract_comments_from_fdf(fdf_path):
    """Extracts text annotations (comments) from an FDF file and removes all '\r' characters."""
    # Detect correct encoding
    encoding = detect_encoding(fdf_path)
    print(f"Detected Encoding: {encoding}")

    comments = []
    
    with open(fdf_path, "r", encoding=encoding, errors="replace") as file:
        #content = file.read()

        # Read each line in the file
        for line in file:
            # Print each line
            print(line.strip())

            # Ensure all line endings are Unix-style (\n only)
            breakpoint()
            content = line.replace("\r\n", "\n").replace("\r", "")

            # Extract annotation text (stored in /Contents(...) in FDF)
            matches = re.findall(r"/Contents\((.*?)\)", content, re.DOTALL)

            # Cleaning up escaped characters like \( and \), ensuring no \r remains
            for match in matches:
                cleaned_text = match.replace(r"\(", "(").replace(r"\)", ")").replace("\r", "").strip()
                comments.append(cleaned_text)

    return comments

def save_comments_to_file(comments, output_path):
    """Saves extracted comments to a text file in UTF-8 without \r characters."""
    total_chars = sum(len(comment) for comment in comments)  # Count letters including spaces
    total_words = sum(len(comment.split()) for comment in comments)  # Count words

    with open(output_path, "w", encoding="utf-8", newline="\n") as file:
        for idx, comment in enumerate(comments, 1):
            file.write(f"{idx}. {comment}\n\n")  # Adds numbering and spacing
        file.write(f"Total words: {total_words}\n")
        file.write(f"Total letters (including spaces): {total_chars}\n")

    # Print the same stats to console
    print("\nExtracted Comments:\n" + "-" * 30)
    for idx, comment in enumerate(comments, 1):
        print(f"{idx}. {comment}\n")
    
    print(f"Total words in comments: {total_words}")
    print(f"Total letters (including spaces): {total_chars}")

# Path to your FDF file
fdf_file_path = "example.fdf"  # Change this to your actual file
output_text_file = "comments.txt"

# Extract comments
comments = extract_comments_from_fdf(fdf_file_path)

# Save to text file and print stats
save_comments_to_file(comments, output_text_file)

print(f"\nComments successfully saved to {output_text_file} with proper encoding and no \\r characters!")
