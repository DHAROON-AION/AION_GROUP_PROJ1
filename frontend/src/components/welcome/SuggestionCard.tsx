import type { Suggestion } from "@/types/chat";

import "./SuggestionCard.css";

interface SuggestionCardProps {
  suggestion: Suggestion;
  onSelect?: () => void;
}

export function SuggestionCard({ suggestion, onSelect }: SuggestionCardProps) {
  return (
    <button type="button" className="suggestion-card" tabIndex={0} onClick={onSelect}>
      <span className="suggestion-card__title">{suggestion.title}</span>
      <span className="suggestion-card__description">{suggestion.description}</span>
    </button>
  );
}
