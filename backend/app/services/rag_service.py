from openai import OpenAI

from app.config import settings
from app.services.embedding_service import embed_text
from app.services.qdrant_service import search_similar_chunks

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def build_context_from_chunks(chunks: list[dict]) -> str:
    context_parts = []

    for index, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"[Source {index}] "
            f"(Document: {chunk.get('document_name', 'unknown')}, "
            f"Page: {chunk.get('page', 'unknown')}, "
            f"Chunk: {chunk.get('chunk_index', 'unknown')})\n"
            f"{chunk.get('text', '')}"
        )

    return "\n\n".join(context_parts)


def is_comparison_or_list_question(question: str) -> bool:
    question_lower = question.lower()

    keywords = [
        "improvement",
        "improvements",
        "before",
        "after",
        "difference",
        "differences",
        "compare",
        "comparison",
        "list",
        "points",
        "steps",
        "changes",
        "what are the 3",
        "what are the three",
    ]

    return any(keyword in question_lower for keyword in keywords)


def generate_answer(question: str, top_k: int = 5) -> dict:
    query_vector = embed_text(question)
    retrieved_chunks = search_similar_chunks(query_vector, limit=top_k)

    context = build_context_from_chunks(retrieved_chunks)
    comparison_mode = is_comparison_or_list_question(question)

    if comparison_mode:
        formatting_rules = """
Formatting rules (STRICT):
- Always use valid markdown.
- Start with a short 1-line introduction.
- If multiple items are present, ALWAYS use a numbered list.
- For each item, use this exact format:

1. **Title**
   - **Before:**
     - point 1
     - point 2
   - **After:**
     - point 1
     - point 2

- The bullet points under Before and After MUST use real markdown bullets (`- `).
- Leave a blank line between numbered items.
- End with: **Sources:** Source X, Source Y
- Do NOT write everything as one paragraph.
- Do NOT use markdown code fences.
"""
    else:
        formatting_rules = """
Formatting rules:
- Always use valid markdown.
- Start with a short 1-line introduction.
- Then explain the answer clearly in a student-friendly way.
- Use short paragraphs.
- Use bullet points only when they genuinely help readability.
- Do NOT force Before/After structure unless the question explicitly asks for comparison.
- End with: **Sources:** Source X, Source Y
- Do NOT use markdown code fences.
"""

    prompt = f"""
You are a helpful assistant answering questions only from the provided document context.

Rules:
1. Answer ONLY from the context.
2. If the answer is not clearly present in the context, say exactly:
   "I could not find that in the uploaded document."
3. Do NOT make up information.
4. Keep answers clean, compact, and easy to scan.
5. Adapt the structure to the question type.

{formatting_rules}

Document Context:
{context}

Question:
{question}
"""

    if comparison_mode:
        prompt += "\n\nImportant: This question requires a numbered markdown list with Before/After bullet points."
    else:
        prompt += "\n\nImportant: This question requires a natural explanation, not a Before/After comparison."

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You answer questions strictly from provided document context and format output as valid markdown."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    answer = response.choices[0].message.content.strip()

    return {
        "answer": answer,
        "sources": retrieved_chunks
    }