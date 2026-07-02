import type { Conversation, Suggestion, UserProfile } from "@/types/chat";

export const ASSISTANT_NAME = "AION Assistant";
export const COMPANY_NAME = "AION Bank";

export const USER_PROFILE: UserProfile = {
  name: "User ABC",
  role: "xyz",
  initials: "SA",
};

export const SUGGESTIONS: Suggestion[] = [
  {
    id: "account",
    title: "Check account information",
    description: "View balances, recent activity, and account details",
  },
  {
    id: "loan",
    title: "Loan eligibility",
    description: "Explore personal and business lending options",
  },
  {
    id: "card",
    title: "Credit card information",
    description: "Compare cards, limits, and benefits",
  },
  {
    id: "open-account",
    title: "Open a new account",
    description: "Start an application for savings or current accounts",
  },
  {
    id: "investment",
    title: "Investment guidance",
    description: "Learn about wealth management and portfolio services",
  },
  {
    id: "issue",
    title: "Report an issue",
    description: "Get help with transactions, cards, or online banking",
  },
];

export const PLACEHOLDER_CONVERSATIONS: Conversation[] = [
  {
    id: "conv-1",
    title: "Customer Support",
    preview: "Thank you for contacting AION Bank support.",
    updatedAt: "Today, 9:14 AM",
    messages: [
      {
        id: "m1",
        role: "user",
        content: "I need help resetting my online banking password.",
        timestamp: "9:12 AM",
      },
      {
        id: "m2",
        role: "assistant",
        content:
          "I can guide you through a secure password reset. For your protection, I will verify your identity before any changes are made. Would you like to proceed with the reset process?",
        timestamp: "9:14 AM",
      },
    ],
  },
  {
    id: "conv-2",
    title: "Loan Inquiry",
    preview: "Based on your profile, you may qualify for competitive rates.",
    updatedAt: "Yesterday",
    messages: [
      {
        id: "m3",
        role: "user",
        content: "What are the current personal loan rates for salaried customers?",
        timestamp: "4:20 PM",
      },
      {
        id: "m4",
        role: "assistant",
        content:
          "Personal loan rates vary based on tenure, income, and credit profile. I can outline indicative rates and the documents required for a formal assessment.",
        timestamp: "4:22 PM",
      },
    ],
  },
  {
    id: "conv-3",
    title: "Credit Card Questions",
    preview: "Our premium card includes travel insurance and lounge access.",
    updatedAt: "Mon",
    messages: [
      {
        id: "m5",
        role: "user",
        content: "Which credit card is best for frequent international travel?",
        timestamp: "11:05 AM",
      },
      {
        id: "m6",
        role: "assistant",
        content:
          "For international travel, our premium card offers competitive foreign exchange rates, travel insurance, and airport lounge benefits. I can compare this with our other card options.",
        timestamp: "11:07 AM",
      },
    ],
  },
  {
    id: "conv-4",
    title: "Account Opening",
    preview: "Opening a current account typically takes 2–3 business days.",
    updatedAt: "Sun",
    messages: [
      {
        id: "m7",
        role: "user",
        content: "What documents do I need to open a business current account?",
        timestamp: "2:45 PM",
      },
      {
        id: "m8",
        role: "assistant",
        content:
          "For a business current account, you will typically need trade license, memorandum of association, authorized signatory IDs, and proof of business address. I can provide a complete checklist.",
        timestamp: "2:47 PM",
      },
    ],
  },
  {
    id: "conv-5",
    title: "Transaction Help",
    preview: "I can help you review recent transactions and dispute status.",
    updatedAt: "Sat",
    messages: [
      {
        id: "m9",
        role: "user",
        content: "I see a pending transaction I do not recognize on my statement.",
        timestamp: "8:30 AM",
      },
      {
        id: "m10",
        role: "assistant",
        content:
          "I understand your concern. I can help you review the transaction details and explain the steps to raise a dispute if needed. Your account security is our priority.",
        timestamp: "8:32 AM",
      },
    ],
  },
];
