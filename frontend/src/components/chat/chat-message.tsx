import { cn } from "@/lib/utils";
import type { ChatMessage as ChatMessageType } from "@/types";
import { ChatToolStatus } from "./chat-tool-status";
import { MarkdownRenderer } from "./markdown-renderer";

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <div className="flex flex-col animate-in fade-in slide-in-from-bottom-1 duration-200">
      {isUser ? (
        <div className="ml-auto max-w-[80%]">
          <div className="rounded-2xl bg-foreground px-4 py-2.5 text-sm leading-relaxed text-background">
            <p className="whitespace-pre-wrap">{message.content}</p>
          </div>
        </div>
      ) : (
        <div className={cn("max-w-[88%] py-1 text-foreground")}>
          {message.toolUse && <ChatToolStatus toolUse={message.toolUse} />}
          {message.content && <MarkdownRenderer content={message.content} />}
        </div>
      )}
    </div>
  );
}
