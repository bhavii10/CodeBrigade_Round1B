**🧠 Adobe India Hackathon 2025 — Round 1B: Summarize & Structure Multiple PDFs**
This solution recursively processes all PDFs in subfolders under /app/input, extracts structured content, and generates output.json per subfolder following a specified schema.

**🚀 Problem Statement**
Build a PDF intelligence engine that:

✅ Accepts multiple folders of PDFs

✅ Extracts clean, structured content

✅ Outputs one JSON per folder

✅ Works fully offline, without persona.json or hardcoded rules

**✅ Features**
**📁 Recursive Input Support**
Scans /app/input and its subfolders for PDFs.

**📄 Per-folder Output**
Generates /app/output/{Folder}/output.json for each input collection.

**📦 Structured Output Schema**
Includes:

metadata: Input filenames, persona (auto-detected or passed), job, and processing timestamp

extracted_sections: Top 3 important headings per document with page numbers and ranking

subsection_analysis: Refined, deduplicated content snippets with corresponding page numbers

🧠 Intelligent Parsing
Ignores irrelevant content (e.g., images, bullet noise, footers/watermarks)

Uses heading detection + sentence transformers for semantic similarity

Extracts sections without relying on hardcoded rules

🔒 Fully Offline & Stateless
No external API calls or cloud dependencies

Consistent behavior across runs and environments

🐳 Docker-Ready
Works in any Docker-supported environment.

Build

docker build --platform linux/amd64 -t round1b_solution:pdf-summarizer .

docker run --rm -v ${PWD}/input:/app/input -v ${PWD}/output:/app/output --network none round1b_solution:pdf-summarizer

Ensure input PDFs are placed under input/{collection_name}/ folders.
Output JSON will be generated under output/{collection_name}/output.json.

**🧰 Tech Stack**
Python 3.10+

PyMuPDF (fitz) — Fast and accurate PDF parsing

SentenceTransformers — For semantic ranking

JSON — For structured output

Docker — Containerized execution
******
