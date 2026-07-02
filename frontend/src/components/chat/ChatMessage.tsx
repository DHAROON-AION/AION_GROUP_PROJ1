import type { ChatMessage as ChatMessageType } from "@/types/chat";

import { Avatar } from "@/components/common/Avatar";
import { USER_PROFILE } from "@/data/mockData";

import "./ChatMessage.css";

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <article
      className={`chat-message chat-message--${message.role}`}
      aria-label={isUser ? "Your message" : "Assistant message"}
    >
      <Avatar
        variant={isUser ? "user" : "assistant"}
        initials={USER_PROFILE.initials}
      />
      <div className="chat-message__body">
        <div className="chat-message__bubble">
          <p>{message.content}</p>
        </div>
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="chat-message__sources">
            {message.sources.map((source) => (
              <span key={source} className="chat-message__source">
                {source}
              </span>
            ))}
          </div>
        )}
        <time className="chat-message__timestamp">{message.timestamp}</time>
      </div>
    </article>
  );
}
