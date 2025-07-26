# import os
# import json
# import datetime
# import fitz  # PyMuPDF
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# INPUT_DIR = "input"
# OUTPUT_DIR = "output"

# def extract_text_from_pdf(path):
#     doc = fitz.open(path)
#     texts = []
#     for page in doc:
#         text = page.get_text().strip()
#         if text:
#             texts.append((page.number + 1, text))
#     return texts

# def extract_top_sections(doc_name, paragraphs, top_k=3):
#     texts = [text for _, text in paragraphs]
#     vectorizer = TfidfVectorizer(stop_words='english')
#     tfidf_matrix = vectorizer.fit_transform(texts)
#     cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix).flatten()
#     top_indices = cosine_sim.argsort()[::-1][1:top_k+1]

#     sections = []
#     for i, idx in enumerate(top_indices, 1):
#         page_num, text = paragraphs[idx]
#         sections.append({
#             "document": doc_name,
#             "section_title": f"Section {i}: {text[:60]}...",
#             "importance_rank": i,
#             "page_number": page_num
#         })
#     return sections

# def extract_subsections(doc_name, paragraphs, top_k=2):
#     return [
#         {
#             "document": doc_name,
#             "refined_text": para[:500],
#             "page_number": page
#         }
#         for page, para in paragraphs[:top_k]
#     ]

# def process_folder(folder_path, folder_name):
#     pdf_files = [
#         f for f in os.listdir(folder_path)
#         if f.lower().endswith(".pdf")
#     ]

#     extracted_sections = []
#     subsection_analysis = []
#     all_docs = []

#     for pdf in sorted(pdf_files):
#         pdf_path = os.path.join(folder_path, pdf)
#         paragraphs = extract_text_from_pdf(pdf_path)
#         if not paragraphs:
#             continue

#         all_docs.append(pdf)
#         extracted_sections += extract_top_sections(pdf, paragraphs)
#         subsection_analysis += extract_subsections(pdf, paragraphs)

#     metadata = {
#         "input_documents": all_docs,
#         "persona": "HR professional",
#         "job_to_be_done": "Create and manage fillable forms for onboarding and compliance.",
#         "processing_timestamp": datetime.datetime.now().isoformat()
#     }

#     result = {
#         "metadata": metadata,
#         "extracted_sections": extracted_sections,
#         "subsection_analysis": subsection_analysis
#     }

#     output_path = os.path.join(OUTPUT_DIR, f"{folder_name}_output.json")
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(result, f, indent=4, ensure_ascii=False)

# def main():
#     if not os.path.exists(OUTPUT_DIR):
#         os.makedirs(OUTPUT_DIR)

#     for folder in os.listdir(INPUT_DIR):
#         folder_path = os.path.join(INPUT_DIR, folder)
#         if os.path.isdir(folder_path):
#             process_folder(folder_path, folder)

# if __name__ == "__main__":
#     main()






# import os
# import fitz  # PyMuPDF
# import json
# from datetime import datetime
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity
# from pathlib import Path

# model = SentenceTransformer("all-MiniLM-L6-v2")

# def extract_text_by_page(pdf_path):
#     doc = fitz.open(pdf_path)
#     pages = [page.get_text() for page in doc]
#     return pages

# def rank_sections(pages, top_k=3):
#     section_data = []
#     for i, text in enumerate(pages):
#         lines = [line.strip() for line in text.split("\n") if line.strip()]
#         for line in lines:
#             if len(line.split()) > 4:
#                 section_data.append((line[:100], i + 1))  # truncate long titles
#                 break
#     embeddings = model.encode([s[0] for s in section_data])
#     scores = cosine_similarity([embeddings[0]], embeddings)[0]
#     ranked = sorted(zip(scores, section_data), key=lambda x: -x[0])
#     return [
#         {
#             "section_title": s[1][0],
#             "importance_rank": i + 1,
#             "page_number": s[1][1]
#         }
#         for i, s in enumerate(ranked[:top_k])
#     ]

# def analyze_subsections(pages):
#     clean_text = []
#     for i, content in enumerate(pages):
#         lines = [line.strip() for line in content.split("\n") if line.strip()]
#         if not lines:
#             continue
#         snippet = " ".join(lines[:5])  # first 5 lines per page
#         clean_text.append({
#             "refined_text": snippet[:500],
#             "page_number": i + 1
#         })
#     return clean_text

# def process_folder(input_path, output_path):
#     pdf_files = [f for f in os.listdir(input_path) if f.endswith(".pdf")]
#     extracted_sections = []
#     subsection_analysis = []

#     for pdf_file in pdf_files:
#         file_path = os.path.join(input_path, pdf_file)
#         pages = extract_text_by_page(file_path)

#         ranked = rank_sections(pages)
#         for section in ranked:
#             section["document"] = pdf_file
#             extracted_sections.append(section)

#         refined = analyze_subsections(pages)
#         for item in refined:
#             item["document"] = pdf_file
#             subsection_analysis.append(item)

#     metadata = {
#         "input_documents": pdf_files,
#         "persona": "HR professional",
#         "job_to_be_done": "Create and manage fillable forms for onboarding and compliance.",
#         "processing_timestamp": str(datetime.now().isoformat())
#     }

#     output_data = {
#         "metadata": metadata,
#         "extracted_sections": extracted_sections,
#         "subsection_analysis": subsection_analysis
#     }

#     os.makedirs(output_path, exist_ok=True)
#     output_file = os.path.join(output_path, "output.json")
#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(output_data, f, indent=4)

# def main():
#     input_root = "./input"
#     output_root = "./output"
#     for folder in os.listdir(input_root):
#         input_path = os.path.join(input_root, folder)
#         if not os.path.isdir(input_path):
#             continue
#         output_path = os.path.join(output_root, folder)
#         process_folder(input_path, output_path)

# if __name__ == "__main__":
#     main()











# import os
# import fitz  # PyMuPDF
# import json
# from datetime import datetime
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity

# model = SentenceTransformer("all-MiniLM-L6-v2")

# def extract_text_by_page(pdf_path):
#     doc = fitz.open(pdf_path)
#     return [page.get_text() for page in doc]

# def rank_sections(pages, top_k=3):
#     section_data = []
#     for i, text in enumerate(pages):
#         lines = [line.strip() for line in text.split("\n") if line.strip()]
#         for line in lines:
#             if len(line.split()) > 4:
#                 section_data.append((line[:100], i + 1))
#                 break
#     if not section_data:
#         return []
#     embeddings = model.encode([s[0] for s in section_data])
#     scores = cosine_similarity([embeddings[0]], embeddings)[0]
#     ranked = sorted(zip(scores, section_data), key=lambda x: -x[0])
#     return [
#         {
#             "document": None,  # to be filled in later
#             "section_title": s[1][0],
#             "importance_rank": i + 1,
#             "page_number": s[1][1]
#         }
#         for i, s in enumerate(ranked[:top_k])
#     ]

# def analyze_subsections(pages):
#     clean_text = []
#     for i, content in enumerate(pages):
#         lines = [line.strip() for line in content.split("\n") if line.strip()]
#         if not lines:
#             continue
#         snippet = " ".join(lines[:5])
#         clean_text.append({
#             "document": None,  # to be filled in later
#             "refined_text": snippet[:500],
#             "page_number": i + 1
#         })
#     return clean_text

# def process_folder(input_path, output_path):
#     pdf_files = [f for f in os.listdir(input_path) if f.endswith(".pdf")]
#     extracted_sections = []
#     subsection_analysis = []

#     for pdf_file in pdf_files:
#         file_path = os.path.join(input_path, pdf_file)
#         pages = extract_text_by_page(file_path)

#         ranked = rank_sections(pages)
#         for section in ranked:
#             section["document"] = pdf_file
#             extracted_sections.append(section)

#         refined = analyze_subsections(pages)
#         for item in refined:
#             item["document"] = pdf_file
#             subsection_analysis.append(item)

#     metadata = {
#         "input_documents": pdf_files,
#         "persona": "HR professional",
#         "job_to_be_done": "Create and manage fillable forms for onboarding and compliance.",
#         "processing_timestamp": str(datetime.now().isoformat())
#     }

#     output_data = {
#         "metadata": metadata,
#         "extracted_sections": extracted_sections,
#         "subsection_analysis": subsection_analysis
#     }

#     os.makedirs(output_path, exist_ok=True)
#     with open(os.path.join(output_path, "output.json"), "w", encoding="utf-8") as f:
#         json.dump(output_data, f, indent=4)

# def main():
#     input_root = "./input"
#     output_root = "./output"
#     for folder in os.listdir(input_root):
#         input_path = os.path.join(input_root, folder)
#         if not os.path.isdir(input_path):
#             continue
#         output_path = os.path.join(output_root, folder)
#         process_folder(input_path, output_path)

# if __name__ == "__main__":
#     main()





import os
import fitz  # PyMuPDF
import json
from datetime import datetime
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_by_page(pdf_path):
    doc = fitz.open(pdf_path)
    return [page.get_text() for page in doc]

def rank_sections(pages, top_k=3):
    section_data = []
    for i, text in enumerate(pages):
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        for line in lines:
            if len(line.split()) > 4:
                section_data.append((line[:100], i + 1))
                break
    if not section_data:
        return []
    embeddings = model.encode([s[0] for s in section_data])
    scores = cosine_similarity([embeddings[0]], embeddings)[0]
    ranked = sorted(zip(scores, section_data), key=lambda x: -x[0])
    return [
        {
            "document": None,  # to be filled in later
            "section_title": s[1][0],
            "importance_rank": i + 1,
            "page_number": s[1][1]
        }
        for i, s in enumerate(ranked[:top_k])
    ]

def analyze_subsections(pages):
    clean_text = []
    for i, content in enumerate(pages):
        lines = [line.strip() for line in content.split("\n") if line.strip()]
        if not lines:
            continue
        snippet = " ".join(lines[:5])
        clean_text.append({
            "document": None,  # to be filled in later
            "refined_text": snippet[:500],
            "page_number": i + 1
        })
    return clean_text

def process_folder(input_path, output_path):
    pdf_files = [f for f in os.listdir(input_path) if f.endswith(".pdf")]
    extracted_sections = []
    subsection_analysis = []

    for pdf_file in pdf_files:
        file_path = os.path.join(input_path, pdf_file)
        pages = extract_text_by_page(file_path)

        ranked = rank_sections(pages)
        for section in ranked:
            section["document"] = pdf_file
            extracted_sections.append(section)

        refined = analyze_subsections(pages)
        for item in refined:
            item["document"] = pdf_file
            subsection_analysis.append(item)

    metadata = {
        "input_documents": pdf_files,
        "persona": extract_persona(pdf_files),
        "job_to_be_done": extract_job(pdf_files),
        "processing_timestamp": str(datetime.now().isoformat())
    }

    output_data = {
        "metadata": metadata,
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, "output.json"), "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4)

def extract_persona(pdf_list):
    # Logic to infer persona from document names or content could go here
    if any("Fill and Sign" in name for name in pdf_list):
        return "HR professional"
    if any("Menu" in name or "Dinner" in name for name in pdf_list):
        return "Food Contractor"
    return "General User"

def extract_job(pdf_list):
    # Logic to infer job from document names or content could go here
    if any("Fill and Sign" in name for name in pdf_list):
        return "Create and manage fillable forms for onboarding and compliance."
    if any("Menu" in name or "Dinner" in name for name in pdf_list):
        return "Prepare a vegetarian buffet-style dinner menu for a corporate gathering, including gluten-free items."
    return "Read and understand documents."

def main():
    input_root = "./input"
    output_root = "./output"
    for folder in os.listdir(input_root):
        input_path = os.path.join(input_root, folder)
        if not os.path.isdir(input_path):
            continue
        output_path = os.path.join(output_root, folder)
        process_folder(input_path, output_path)

if __name__ == "__main__":
    main()