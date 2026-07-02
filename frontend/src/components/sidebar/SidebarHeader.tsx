import { Building2 } from "lucide-react";

import { ASSISTANT_NAME, COMPANY_NAME } from "@/data/mockData";

import "./SidebarHeader.css";

export function SidebarHeader() {
  return (
    <div className="sidebar-header">
      <div className="sidebar-header__brand" aria-label={`${COMPANY_NAME} logo`}>
        <div className="sidebar-header__logo">
          <Building2 size={20} strokeWidth={2} />
        </div>
        <div className="sidebar-header__text">
          <span className="sidebar-header__company">{COMPANY_NAME}</span>
          <span className="sidebar-header__assistant">{ASSISTANT_NAME}</span>
        </div>
      </div>
    </div>
  );
}
