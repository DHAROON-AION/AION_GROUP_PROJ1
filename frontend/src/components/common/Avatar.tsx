import { Building2 } from "lucide-react";

import "./Avatar.css";

interface AvatarProps {
  initials?: string;
  variant?: "user" | "assistant";
  size?: "sm" | "md";
}

export function Avatar({
  initials,
  variant = "assistant",
  size = "sm",
}: AvatarProps) {
  return (
    <div
      className={`avatar avatar--${variant} avatar--${size}`}
      aria-hidden="true"
    >
      {variant === "assistant" ? (
        <Building2 size={size === "sm" ? 16 : 18} />
      ) : (
        <span>{initials}</span>
      )}
    </div>
  );
}
