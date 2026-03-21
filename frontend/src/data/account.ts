import type { Account } from "@/types";

export const mockAccount: Account = {
  id: "usr_001",
  name: "Alex Rivera",
  email: "alex.rivera@email.com",
  accountNumber: "****4821",
  tier: "Premium",
  balance: 12847.32,
  currency: "USD",
  monthlyChange: 3.2,
  joinDate: "2024-03-15",
  cards: [
    { type: "Virtual", last4: "7823", status: "Active" },
    { type: "Physical", last4: "4129", status: "Active" },
  ],
};
