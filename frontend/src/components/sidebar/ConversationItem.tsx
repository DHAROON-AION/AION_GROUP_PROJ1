import { MessageSquare } from "lucide-react";

import type { Conversation } from "@/types/chat";

import "./ConversationItem.css";

interface ConversationItemProps {
  conversation: Conversation;
  isActive: boolean;
  onSelect: (id: string) => void;
}

export function ConversationItem({
  conversation,
  isActive,
  onSelect,
}: ConversationItemProps) {
  return (
    <li>
      <button
        type="button"
        className={`conversation-item${isActive ? " conversation-item--active" : ""}`}
        onClick={() => onSelect(conversation.id)}
        aria-current={isActive ? "page" : undefined}
      >
        <MessageSquare size={16} className="conversation-item__icon" />
        <span className="conversation-item__content">
          <span className="conversation-item__title">{conversation.title}</span>
          <span className="conversation-item__preview">{conversation.preview}</span>
        </span>
      </button>
    </li>
  );
}
