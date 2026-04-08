import { Plus, X } from "react-feather";
import { Button } from "@/components/ui/button";

interface ChatHeaderProps {
  title: string;
  onClose: () => void;
  onNewConversation?: () => void;
}

export function ChatHeader({ title, onClose, onNewConversation }: ChatHeaderProps) {
  return (
    <div className="flex items-center justify-between border-b border-border/40 bg-card/80 backdrop-blur-md px-6 py-4">
      <h2 className="text-sm font-semibold text-foreground">{title}</h2>
      <div className="flex items-center gap-1">
        {onNewConversation && (
          <Button
            variant="ghost"
            size="icon"
            className="size-8 cursor-pointer rounded-full text-muted-foreground hover:text-foreground hover:bg-muted"
            onClick={onNewConversation}
            aria-label="New conversation"
          >
            <Plus size={16} />
          </Button>
        )}
        <Button
          variant="ghost"
          size="icon"
          className="size-8 cursor-pointer rounded-full text-muted-foreground hover:text-foreground hover:bg-muted"
          onClick={onClose}
          aria-label="Close chat"
        >
          <X size={16} />
        </Button>
      </div>
    </div>
  );
}
