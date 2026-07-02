export type MessageRole = "user" | "assistant";

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: string;
  sources?: string[];
}

export interface Conversation {
  id: string;
  title: string;
  preview: string;
  updatedAt: string;
  messages: ChatMessage[];
}

export interface Suggestion {
  id: string;
  title: string;
  description: string;
}

export interface UserProfile {
  name: string;
  role: string;
  initials: string;
}
