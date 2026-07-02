import "./TypingIndicator.css";

export function TypingIndicator() {
  return (
    <div className="typing-indicator" role="status" aria-label="Assistant is typing">
      <span className="typing-indicator__dot" />
      <span className="typing-indicator__dot" />
      <span className="typing-indicator__dot" />
    </div>
  );
}
