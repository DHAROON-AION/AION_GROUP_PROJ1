import { Menu } from "lucide-react";

import { ChatContainer } from "@/components/chat/ChatContainer";
import { ChatInput } from "@/components/chat/ChatInput";
import { Sidebar } from "@/components/sidebar/Sidebar";
import { useChatState } from "@/hooks/useChatState";

import "./App.css";

export default function App() {
  const {
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
  } = useChatState();

  return (
    <div className="app-shell">
      <Sidebar
        conversations={conversations}
        activeConversationId={activeConversationId}
        isOpen={sidebarOpen}
        onNewChat={startNewChat}
        onSelectConversation={selectConversation}
        onClose={closeSidebar}
      />

      {sidebarOpen && (
        <button
          type="button"
          className="sidebar-overlay"
          aria-label="Close navigation"
          onClick={closeSidebar}
        />
      )}

      <main className="main-panel">
        <header className="main-header">
          <button
            type="button"
            className="icon-button mobile-only"
            aria-label="Open navigation"
            onClick={toggleSidebar}
          >
            <Menu size={20} />
          </button>
          <div className="main-header__title">
            <h1>AION Banking Assistant</h1>
            <p>Secure support for your banking needs</p>
          </div>
        </header>

        <ChatContainer
          conversation={activeConversation}
          greeting={greeting}
          isLoading={isLoading}
          onSuggestionSelect={updateDraft}
        />

        <ChatInput
          value={draftMessage}
          onChange={updateDraft}
          onSend={sendDraft}
          isLoading={isLoading}
          isUploading={isUploading}
          uploadNotice={uploadNotice}
          onUpload={uploadFile}
        />
      </main>
    </div>
  );
}
