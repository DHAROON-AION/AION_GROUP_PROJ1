import { SUGGESTIONS } from "@/data/mockData";

import { SuggestionCard } from "./SuggestionCard";

import "./WelcomeScreen.css";

interface WelcomeScreenProps {
  greeting: string;
  onSuggestionSelect?: (text: string) => void;
}

export function WelcomeScreen({ greeting, onSuggestionSelect }: WelcomeScreenProps) {
  return (
    <section className="welcome-screen" aria-label="Welcome">
      <div className="welcome-screen__hero">
        <div className="welcome-screen__logo" aria-hidden="true">
          <span>A</span>
        </div>
        <h2 className="welcome-screen__greeting">{greeting}</h2>
        <p className="welcome-screen__subtitle">How can I help you today?</p>
      </div>

      <div className="welcome-screen__suggestions">
        {SUGGESTIONS.map((suggestion) => (
          <SuggestionCard
            key={suggestion.id}
            suggestion={suggestion}
            onSelect={() => onSuggestionSelect?.(suggestion.title)}
          />
        ))}
      </div>
    </section>
  );
}
