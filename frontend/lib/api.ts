const BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

export async function uploadPdfs(files: File[]) {
  const formData = new FormData();

  files.forEach((file) => {
    formData.append("files", file);
  });

  const response = await fetch(`${BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to upload PDFs");
  }

  return response.json();
}

export async function askQuestion(question: string) {
  const response = await fetch(`${BASE_URL}/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch answer");
  }

  return response.json();
}

export async function getKnowledgeBaseStatus() {
  const response = await fetch(`${BASE_URL}/kb-status`);

  if (!response.ok) {
    throw new Error("Failed to fetch knowledge base status");
  }

  return response.json();
}