import { useCallback, useEffect, useMemo, useState } from "react";

import { PLACEHOLDER_CONVERSATIONS } from "@/data/mockData";
import {
  fetchConversations,
  fetchMessages,
  sendMessage,
  uploadDocument,
} from "@/services/chatService";
import type { ChatMessage, Conversation } from "@/types/chat";

function getGreeting(): string {
  const hour = new Date().getHours();
  if (hour < 12) return "Good morning";
  if (hour < 17) return "Good afternoon";
  return "Good evening";
}

function mapApiToConversation(
  id: string,
  title: string,
  preview: string,
  messages: ChatMessage[] = [],
): Conversation {
  return {
    id,
    title,
    preview: preview || "No messages yet",
    updatedAt: "Recently",
    messages,
  };
}

export function useChatState() {
  const [conversations, setConversations] = useState<Conversation[]>(
    PLACEHOLDER_CONVERSATIONS,
  );
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const [draftMessage, setDraftMessage] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadNotice, setUploadNotice] = useState<string | null>(null);

  const activeConversation = useMemo(
    () => conversations.find((c) => c.id === activeConversationId) ?? null,
    [activeConversationId, conversations],
  );

  const greeting = useMemo(() => getGreeting(), []);

  useEffect(() => {
    fetchConversations()
      .then((apiConvs) => {
        if (apiConvs.length > 0) {
          setConversations(
            apiConvs.map((c) =>
              mapApiToConversation(c.id, c.title, c.preview),
            ),
          );
        }
      })
      .catch(() => undefined);
  }, []);

  const startNewChat = useCallback(() => {
    setActiveConversationId(null);
    setDraftMessage("");
    setSidebarOpen(false);
  }, []);

  const selectConversation = useCallback(async (id: string) => {
    setActiveConversationId(id);
    setDraftMessage("");
    setSidebarOpen(false);

    try {
      const messages = await fetchMessages(id);
      if (messages.length > 0) {
        setConversations((prev) =>
          prev.map((c) =>
            c.id === id
              ? {
                  ...c,
                  messages: messages.map((m) => ({
                    id: m.id,
                    role: m.role,
                    content: m.content,
                    timestamp: m.timestamp,
                    sources: m.sources,
                  })),
                }
              : c,
          ),
        );
      }
    } catch {
      // Keep existing local messages
    }
  }, []);

  const updateDraft = useCallback((value: string) => {
    setDraftMessage(value);
  }, []);

  const sendDraft = useCallback(async () => {
    const text = draftMessage.trim();
    if (!text || isLoading) return;

    setIsLoading(true);
    setDraftMessage("");

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      content: text,
      timestamp: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };

    const localId = activeConversationId ?? `local-${Date.now()}`;

    if (!activeConversationId) {
      setConversations((prev) => [
        mapApiToConversation(localId, text.slice(0, 40), text, [userMessage]),
        ...prev,
      ]);
      setActiveConversationId(localId);
    } else {
      setConversations((prev) =>
        prev.map((c) =>
          c.id === localId
            ? { ...c, messages: [...c.messages, userMessage] }
            : c,
        ),
      );
    }

    try {
      const sessionForApi = activeConversationId?.startsWith("local-")
        ? null
        : activeConversationId;

      const res = await sendMessage(sessionForApi, text);

      const assistantMessage: ChatMessage = {
        id: `assistant-${Date.now()}`,
        role: "assistant",
        content: res.reply,
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
        sources: res.sources,
      };

      setActiveConversationId(res.session_id);
      setConversations((prev) =>
        prev.map((c) =>
          c.id === localId || c.id === res.session_id
            ? {
                ...c,
                id: res.session_id,
                title: c.title === text.slice(0, 40) ? c.title : c.title,
                messages: [
                  ...c.messages.filter((m) => m.id !== assistantMessage.id),
                  assistantMessage,
                ],
                preview: res.reply.slice(0, 80),
              }
            : c,
        ),
      );
    } catch {
      const errorMessage: ChatMessage = {
        id: `err-${Date.now()}`,
        role: "assistant",
        content:
          "I'm temporarily unable to respond. Please try again in a moment or contact your relationship manager.",
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };
      setConversations((prev) =>
        prev.map((c) =>
          c.id === localId
            ? { ...c, messages: [...c.messages, errorMessage] }
            : c,
        ),
      );
    } finally {
      setIsLoading(false);
    }
  }, [activeConversationId, draftMessage, isLoading]);

  const appendChatMessages = useCallback(
    (localId: string, messages: ChatMessage[]) => {
      setConversations((prev) =>
        prev.map((c) =>
          c.id === localId ? { ...c, messages: [...c.messages, ...messages] } : c,
        ),
      );
    },
    [],
  );

  const uploadFile = useCallback(
    async (file: File) => {
      if (isUploading || isLoading) return;

      setIsUploading(true);
      setUploadNotice(null);

      const timestamp = new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });

      const localId = activeConversationId ?? `local-${Date.now()}`;
      const userNotice: ChatMessage = {
        id: `upload-user-${Date.now()}`,
        role: "user",
        content: `Uploaded document: ${file.name}`,
        timestamp,
      };

      if (!activeConversationId) {
        setConversations((prev) => [
          mapApiToConversation(localId, `Upload: ${file.name}`, file.name, [userNotice]),
          ...prev,
        ]);
        setActiveConversationId(localId);
      } else {
        appendChatMessages(localId, [userNotice]);
      }

      try {
        const result = await uploadDocument(file);
        const assistantNotice: ChatMessage = {
          id: `upload-assistant-${Date.now()}`,
          role: "assistant",
          content: result.message,
          timestamp: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
          sources: [result.filename],
        };
        appendChatMessages(localId, [assistantNotice]);
        setUploadNotice(null);
      } catch (error) {
        const message =
          error instanceof Error
            ? error.message
            : "This file could not be added to the knowledge base.";
        const assistantError: ChatMessage = {
          id: `upload-error-${Date.now()}`,
          role: "assistant",
          content: message,
          timestamp: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        };
        appendChatMessages(localId, [assistantError]);
        setUploadNotice(message);
      } finally {
        setIsUploading(false);
      }
    },
    [
      activeConversationId,
      appendChatMessages,
      isLoading,
      isUploading,
    ],
  );

  const toggleSidebar = useCallback(() => {
    setSidebarOpen((open) => !open);
  }, []);

  const closeSidebar = useCallback(() => {
    setSidebarOpen(false);
  }, []);

  return {
    conversations,
    activeConversation,
    activeConversationId,
    draftMessage,
    greeting,
    sidebarOpen,
    isLoading,
    isUploading,
    uploadNotice,
    startNewChat,
    selectConversation,
    updateDraft,
    sendDraft,
    uploadFile,
    toggleSidebar,
    closeSidebar,
  };
}
