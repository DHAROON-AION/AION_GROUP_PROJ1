/**
 * API integration layer for the banking assistant.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

export interface ChatApiResponse {
  reply: string;
  session_id: string;
  agent_framework: string;
  sources: string[];
  metadata: Record<string, unknown>;
}

export interface ConversationSummary {
  id: string;
  title: string;
  preview: string;
  updated_at: string;
}

export interface ApiMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: string[];
  timestamp: string;
}

export async function sendMessage(
  sessionId: string | null,
  message: string,
): Promise<ChatApiResponse> {
  const response = await fetch(`${API_BASE_URL}/api/chat/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      session_id: sessionId,
      agent_framework: "langgraph",
    }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(
      (error as { detail?: string }).detail ?? "Unable to send message",
    );
  }

  return response.json();
}

export async function fetchConversations(): Promise<ConversationSummary[]> {
  const response = await fetch(`${API_BASE_URL}/api/chat/conversations`);
  if (!response.ok) return [];
  const data = await response.json();
  return data.conversations ?? [];
}

export async function fetchMessages(
  conversationId: string,
): Promise<ApiMessage[]> {
  const response = await fetch(
    `${API_BASE_URL}/api/chat/conversations/${conversationId}/messages`,
  );
  if (!response.ok) return [];
  const data = await response.json();
  return data.messages ?? [];
}

export async function streamResponse(
  sessionId: string | null,
  message: string,
  onChunk: (chunk: string) => void,
  onDone: (sessionId: string) => void,
  onError: (error: string) => void,
): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      session_id: sessionId,
      agent_framework: "langgraph",
    }),
  });

  if (!response.ok || !response.body) {
    onError("Streaming unavailable");
    return;
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";

    for (const line of lines) {
      if (!line.startsWith("data: ")) continue;
      try {
        const event = JSON.parse(line.slice(6));
        if (event.type === "token") onChunk(event.content);
        if (event.type === "done") onDone(event.session_id);
        if (event.type === "error") onError(event.message);
      } catch {
        // skip malformed events
      }
    }
  }
}

export interface UploadDocumentResult {
  filename: string;
  chunks_ingested: number;
  status: string;
  message: string;
}

export async function uploadDocument(file: File): Promise<UploadDocumentResult> {
  const formData = new FormData();
  formData.append("file", file);
  const response = await fetch(`${API_BASE_URL}/api/documents/upload`, {
    method: "POST",
    body: formData,
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    const detail = (error as { detail?: string | { msg?: string }[] }).detail;
    const message =
      typeof detail === "string"
        ? detail
        : Array.isArray(detail)
          ? detail.map((d) => d.msg).join(", ")
          : "Unable to upload this document.";
    throw new Error(message);
  }
  return response.json();
}
