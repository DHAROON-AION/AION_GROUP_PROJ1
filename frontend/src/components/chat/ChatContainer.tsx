import type { Conversation } from "@/types/chat";

import { WelcomeScreen } from "@/components/welcome/WelcomeScreen";

import { ChatMessage } from "./ChatMessage";
import { TypingIndicator } from "./TypingIndicator";

import "./ChatContainer.css";

interface ChatContainerProps {
  conversation: Conversation | null;
  greeting: string;
  isLoading?: boolean;
  onSuggestionSelect?: (text: string) => void;
}

export function ChatContainer({
  conversation,
  greeting,
  isLoading = false,
  onSuggestionSelect,
}: ChatContainerProps) {
  const hasMessages = conversation && conversation.messages.length > 0;

  return (
    <section className="chat-container" aria-label="Conversation">
      <div className="chat-container__scroll">
        {!hasMessages ? (
          <WelcomeScreen greeting={greeting} onSuggestionSelect={onSuggestionSelect} />
        ) : (
          <div className="chat-container__messages">
            {conversation.messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            {isLoading && (
              <div className="chat-container__typing">
                <TypingIndicator />
              </div>
            )}
          </div>
        )}
      </div>
    </section>
  );
}
