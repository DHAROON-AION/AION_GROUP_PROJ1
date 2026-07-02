import { Mic, Paperclip, Send } from "lucide-react";
import { type ChangeEvent, type KeyboardEvent, useRef } from "react";

import "./ChatInput.css";

interface ChatInputProps {
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  isLoading?: boolean;
  isUploading?: boolean;
  uploadNotice?: string | null;
  onUpload?: (file: File) => void;
}

export function ChatInput({
  value,
  onChange,
  onSend,
  isLoading = false,
  isUploading = false,
  uploadNotice = null,
  onUpload,
}: ChatInputProps) {
  const fileRef = useRef<HTMLInputElement>(null);

  const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      if (value.trim() && !isLoading) onSend();
    }
  };

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && onUpload) onUpload(file);
    event.target.value = "";
  };

  return (
    <footer className="chat-input" aria-label="Message composer">
      <input
        ref={fileRef}
        type="file"
        accept=".md,.txt,text/markdown,text/plain"
        hidden
        onChange={handleFileChange}
      />
      <div className="chat-input__wrapper">
        <button
          type="button"
          className="chat-input__icon-btn"
          aria-label="Attach policy document"
          onClick={() => fileRef.current?.click()}
          disabled={isLoading || isUploading}
        >
          <Paperclip size={18} />
        </button>

        <textarea
          className="chat-input__field"
          placeholder="Ask about accounts, loans, cards, and more..."
          value={value}
          onChange={(event) => onChange(event.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
          disabled={isLoading || isUploading}
          aria-label="Message input"
        />

        <button
          type="button"
          className="chat-input__icon-btn"
          aria-label="Voice input"
          disabled
        >
          <Mic size={18} />
        </button>

        <button
          type="button"
          className="chat-input__send"
          aria-label="Send message"
          onClick={onSend}
          disabled={!value.trim() || isLoading}
        >
          <Send size={18} />
        </button>
      </div>

      {isUploading && (
        <p className="chat-input__status chat-input__status--loading" role="status">
          Adding document to the knowledge base…
        </p>
      )}
      {!isUploading && uploadNotice && (
        <p className="chat-input__status chat-input__status--error" role="alert">
          {uploadNotice}
        </p>
      )}

      <p className="chat-input__disclaimer">
        Attach <strong>.md</strong> or <strong>.txt</strong> policy documents only.
        Images and PDFs are not supported. Uploaded files are indexed for future questions.
      </p>
    </footer>
  );
}
