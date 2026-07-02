import { X } from "lucide-react";

import type { Conversation } from "@/types/chat";

import { ConversationList } from "./ConversationList";
import { NewChatButton } from "./NewChatButton";
import { ProfileMenu } from "./ProfileMenu";
import { SidebarHeader } from "./SidebarHeader";

import "./Sidebar.css";

interface SidebarProps {
  conversations: Conversation[];
  activeConversationId: string | null;
  isOpen: boolean;
  onNewChat: () => void;
  onSelectConversation: (id: string) => void;
  onClose: () => void;
}

export function Sidebar({
  conversations,
  activeConversationId,
  isOpen,
  onNewChat,
  onSelectConversation,
  onClose,
}: SidebarProps) {
  return (
    <aside className={`sidebar${isOpen ? " sidebar--open" : ""}`} aria-label="Main navigation">
      <div className="sidebar__top">
        <SidebarHeader />
        <button
          type="button"
          className="icon-button mobile-only sidebar__close"
          aria-label="Close navigation"
          onClick={onClose}
        >
          <X size={20} />
        </button>
        <NewChatButton onClick={onNewChat} />
        <ConversationList
          conversations={conversations}
          activeConversationId={activeConversationId}
          onSelect={onSelectConversation}
        />
      </div>
      <ProfileMenu />
    </aside>
  );
}
