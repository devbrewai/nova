import { Minus, X } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ChatHeaderProps {
  onClose: () => void;
}

export function ChatHeader({ onClose }: ChatHeaderProps) {
  return (
    <div className="flex items-center justify-between border-b border-border bg-card px-4 py-3">
      <h2 className="text-sm font-semibold">Ask Nova</h2>
      <div className="flex items-center gap-1">
        <Button variant="ghost" size="icon" className="size-7">
          <Minus className="size-3.5" />
        </Button>
        <Button variant="ghost" size="icon" className="size-7" onClick={onClose}>
          <X className="size-3.5" />
        </Button>
      </div>
    </div>
  );
}
