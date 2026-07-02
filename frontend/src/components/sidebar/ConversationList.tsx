import type { Conversation } from "@/types/chat";

import { ConversationItem } from "./ConversationItem";

import "./ConversationList.css";

interface ConversationListProps {
  conversations: Conversation[];
  activeConversationId: string | null;
  onSelect: (id: string) => void;
}

export function ConversationList({
  conversations,
  activeConversationId,
  onSelect,
}: ConversationListProps) {
  return (
    <nav className="conversation-list" aria-label="Conversation history">
      <p className="conversation-list__label">Recent conversations</p>
      <ul className="conversation-list__items">
        {conversations.map((conversation) => (
          <ConversationItem
            key={conversation.id}
            conversation={conversation}
            isActive={conversation.id === activeConversationId}
            onSelect={onSelect}
          />
        ))}
      </ul>
    </nav>
  );
}
