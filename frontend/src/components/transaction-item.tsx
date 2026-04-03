import type { ComponentType } from "react";
import {
  Coffee,
  Navigation,
  ShoppingBag,
  Film,
  FileText,
  TrendingUp,
  Shuffle,
  Heart,
  Map,
  Tv,
} from "react-feather";
import { Badge } from "@/components/ui/badge";
import type { Transaction, TransactionCategory } from "@/types";

type FeatherIcon = ComponentType<{ size?: number; className?: string }>;

const categoryConfig: Record<
  TransactionCategory,
  { icon: FeatherIcon; color: string }
> = {
  food:          { icon: Coffee,      color: "bg-primary/10 text-primary" },
  transport:     { icon: Navigation,  color: "bg-primary/10 text-primary" },
  shopping:      { icon: ShoppingBag, color: "bg-primary/10 text-primary" },
  entertainment: { icon: Film,        color: "bg-primary/10 text-primary" },
  bills:         { icon: FileText,    color: "bg-muted text-muted-foreground" },
  income:        { icon: TrendingUp,  color: "bg-primary/10 text-primary" },
  transfer:      { icon: Shuffle,     color: "bg-muted text-muted-foreground" },
  health:        { icon: Heart,       color: "bg-primary/10 text-primary" },
  travel:        { icon: Map,         color: "bg-primary/10 text-primary" },
  subscriptions: { icon: Tv,          color: "bg-muted text-muted-foreground" },
};

function formatDate(dateStr: string): string {
  const date = new Date(dateStr + "T00:00:00");
  return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

function formatAmount(amount: number): string {
  const formatted = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
  }).format(Math.abs(amount));
  return amount >= 0 ? `+${formatted}` : `-${formatted}`;
}

interface TransactionItemProps {
  transaction: Transaction;
}

export function TransactionItem({ transaction }: TransactionItemProps) {
  const config = categoryConfig[transaction.category];
  const Icon = config.icon;
  const isIncome = transaction.amount >= 0;

  return (
    <div className="flex items-center gap-3 py-3">
      <div className={`flex size-9 shrink-0 items-center justify-center rounded-md ${config.color}`}>
        <Icon size={16} />
      </div>

      <div className="flex-1 min-w-0">
        <p className="truncate text-sm font-medium">{transaction.merchant}</p>
        <p className="text-xs text-muted-foreground">
          {formatDate(transaction.date)}
          {transaction.description ? ` · ${transaction.description}` : ""}
        </p>
      </div>

      <div className="flex items-center gap-2">
        {transaction.status !== "completed" && (
          <Badge
            variant={transaction.status === "pending" ? "secondary" : "destructive"}
            className="text-[10px] px-1.5 py-0"
          >
            {transaction.status}
          </Badge>
        )}
        <span
          className={`text-sm font-medium tabular-nums ${
            isIncome ? "text-primary" : "text-foreground"
          }`}
        >
          {formatAmount(transaction.amount)}
        </span>
      </div>
    </div>
  );
}
