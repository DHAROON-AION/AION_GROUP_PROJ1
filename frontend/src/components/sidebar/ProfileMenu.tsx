import { LogOut, Settings } from "lucide-react";

import { USER_PROFILE } from "@/data/mockData";

import { Avatar } from "@/components/common/Avatar";

import "./ProfileMenu.css";

export function ProfileMenu() {
  return (
    <div className="profile-menu">
      <div className="profile-menu__user">
        <Avatar initials={USER_PROFILE.initials} variant="user" size="md" />
        <div className="profile-menu__details">
          <span className="profile-menu__name">{USER_PROFILE.name}</span>
          <span className="profile-menu__role">{USER_PROFILE.role}</span>
        </div>
      </div>
      <div className="profile-menu__actions">
        <button type="button" className="profile-menu__action" aria-label="Settings" disabled>
          <Settings size={18} />
        </button>
        <button type="button" className="profile-menu__action" aria-label="Sign out" disabled>
          <LogOut size={18} />
        </button>
      </div>
    </div>
  );
}
