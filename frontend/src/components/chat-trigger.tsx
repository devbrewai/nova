import { MessageCircle } from "react-feather";

interface ChatTriggerProps {
  onOpen: () => void;
}

export function ChatTrigger({ onOpen }: ChatTriggerProps) {
  return (
    <button
      onClick={onOpen}
      className="group fixed bottom-6 right-6 z-50 flex cursor-pointer items-center gap-2.5 rounded-full bg-primary px-5 py-3.5 text-primary-foreground shadow-[0_8px_30px_rgb(0,0,0,0.12)] transition-all hover:shadow-[0_8px_30px_rgb(5,79,49,0.25)] hover:-translate-y-0.5 active:scale-95 border border-primary/20"
    >
      <MessageCircle size={18} className="fill-primary-foreground/20" />
      <span className="text-sm font-bold tracking-wide">Ask Nova</span>
    </button>
  );
}
