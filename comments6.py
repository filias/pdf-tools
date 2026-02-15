import re

def extract_only_comments(input_file, output_file="result.txt"):
    try:
        comments = []

        with open(input_file, "r", encoding="utf-8") as file:

            content = file.read()
            # Regular expression to match text between Page #1: and Page #2:
            pattern = rf"Page #1:(.*?)Page #2:"
            match = re.search(pattern, content, re.DOTALL)  # DOTALL makes it multi-line

            if match:
                extracted_text = match.group(1).strip()  # Remove extra spaces/newlines
                comments.append(extracted_text)

        breakpoint()
        # Save to file
        with open(output_file, "w", encoding="utf-8") as f:
            for comment in comments:
                f.write(comment + "\n")

        print(f"✅ Extracted {len(comments)} comments to {output_file}")

    except Exception as e:
        print(f"❌ Error extracting comments: {e}")

# Run extraction
extract_only_comments("comments.txt")
