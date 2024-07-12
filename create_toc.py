import fitz  # PyMuPDF
import re
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
import time

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = {}
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text[page_num + 1] = page.get_text("text")
    return text

def identify_headers(text):
    headers = {}
    header_pattern = re.compile(r"^(I{1,3}|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII|XIV|XV|XVI|XVII|XVIII|XIX|XX)\.\s+.*|^[A-Z]\.\s+.*|^[1-9]+\.\s+.*|^[a-z]\.\s+.*", re.MULTILINE)
    for page, content in text.items():
        matches = header_pattern.findall(content)
        if matches:
            headers[page] = [line.strip() for line in content.split('\n') if header_pattern.match(line)]
    return headers

def create_toc(headers):
    toc = []
    for page, titles in headers.items():
        for title in titles:
            toc.append(f"{title} (p {page})")
    return toc

def refine_toc_with_gpt2(toc):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    # Split the input into manageable chunks
    max_length = 1024
    chunk_size = max_length - 50  # Leave some space for the prompt and formatting
    toc_text = "\n".join(toc)
    chunks = [toc_text[i:i + chunk_size] for i in range(0, len(toc_text), chunk_size)]

    refined_toc = ""
    total_chunks = len(chunks)
    start_time = time.time()

    for i, chunk in enumerate(chunks):
        prompt = "Refine the following table of contents:\n\n" + chunk
        inputs = tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=max_length)
        attention_mask = torch.ones(inputs.shape, dtype=torch.long)

        outputs = model.generate(inputs, max_new_tokens=200, num_return_sequences=1, no_repeat_ngram_size=2, attention_mask=attention_mask, pad_token_id=tokenizer.eos_token_id)
        refined_chunk = tokenizer.decode(outputs[0], skip_special_tokens=True)
        refined_toc += refined_chunk.split("Refine the following table of contents:")[1].strip() + "\n"

        # Progress tracking
        elapsed_time = time.time() - start_time
        avg_time_per_chunk = elapsed_time / (i + 1)
        remaining_chunks = total_chunks - (i + 1)
        estimated_time_remaining = avg_time_per_chunk * remaining_chunks

        print(f"Processed chunk {i + 1}/{total_chunks} - "
              f"Elapsed time: {elapsed_time:.2f}s, "
              f"Estimated time remaining: {estimated_time_remaining:.2f}s")

    return refined_toc.strip()

def main():
    pdf_path = "2025 PFS QPP NPRM -14828.pdf"
    pdf_text = extract_text_from_pdf(pdf_path)
    headers = identify_headers(pdf_text)
    toc = create_toc(headers)
    refined_toc = refine_toc_with_gpt2(toc)
    
    # Save the refined TOC to a file with UTF-8 encoding
    with open("refined_table_of_contents.txt", "w", encoding="utf-8") as file:
        file.write(refined_toc)
    
    print("Table of contents created and saved to 'refined_table_of_contents.txt'.")

if __name__ == "__main__":
    main()
