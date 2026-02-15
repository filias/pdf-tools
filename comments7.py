import fitz  # PyMuPDF

def extract_annotations(pdf_path):
    """Extracts annotations (comments) from a PDF and properly formats newlines."""
    try:
        doc = fitz.open(pdf_path)
        annotations = []

        for page in doc:
            for annot in page.annots():
                if "content" in annot.info:
                    comment = annot.info["content"]

                    # Fix misrepresented newlines (if any)
                    comment = comment.replace("\r", "\n").strip()

                    annotations.append(comment)

        if annotations:
            with open("comments.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(annotations))  # Separate comments with blank lines
            print(f"✅ Extracted {len(annotations)} comments to comments.txt")
        else:
            print("❌ No annotations found.")

        total_chars = sum(len(comment) for comment in annotations)
        total_words = sum(len(comment.split()) for comment in annotations)

        print(f"✅ Total words: {total_words}")
        print(f"✅ Total letters (including spaces): {total_chars}")

    except Exception as e:
        print(f"❌ Error reading PDF: {e}")

# Run the extraction
extract_annotations("books03/_LZ5_B3_CompleteSpreads_7.5-HU.pdf")
