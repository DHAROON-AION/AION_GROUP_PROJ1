import { Plus } from "lucide-react";

import "./NewChatButton.css";

interface NewChatButtonProps {
  onClick: () => void;
}

export function NewChatButton({ onClick }: NewChatButtonProps) {
  return (
    <button type="button" className="new-chat-button" onClick={onClick}>
      <Plus size={18} />
      <span>New chat</span>
    </button>
  );
}
