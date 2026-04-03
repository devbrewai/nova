import { X, Zap } from "react-feather";
import { Button } from "@/components/ui/button";

interface ChatHeaderProps {
  onClose: () => void;
}

export function ChatHeader({ onClose }: ChatHeaderProps) {
  return (
    <div className="flex items-center justify-between border-b border-border/40 bg-card/80 backdrop-blur-md px-6 py-4">
      <div className="flex items-center gap-2">
        <div className="flex size-6 items-center justify-center rounded-full bg-primary/10 text-primary">
          <Zap size={12} className="fill-primary" />
        </div>
        <h2 className="text-sm font-bold text-foreground">Nova Assistant</h2>
      </div>
      <div className="flex items-center gap-1">
        <Button variant="ghost" size="icon" className="size-8 rounded-full text-muted-foreground hover:text-foreground hover:bg-muted" onClick={onClose}>
          <X size={16} />
        </Button>
      </div>
    </div>
  );
}
