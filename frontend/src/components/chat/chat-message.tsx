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
    <div className="flex flex-col animate-in fade-in slide-in-from-bottom-2 duration-300">
      {isUser ? (
        <div className="ml-auto max-w-[85%] mt-2">
          <div className="rounded-2xl rounded-tr-sm bg-primary/10 text-foreground px-4 py-2.5 text-sm leading-relaxed shadow-sm">
            <p className="whitespace-pre-wrap font-medium">{message.content}</p>
          </div>
        </div>
      ) : (
        <div className={cn("max-w-[90%] py-2 text-foreground")}>
          {message.toolUse && <ChatToolStatus toolUse={message.toolUse} />}
          {message.content && (
            <div className="text-sm text-foreground/90 leading-relaxed">
              <MarkdownRenderer content={message.content} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
