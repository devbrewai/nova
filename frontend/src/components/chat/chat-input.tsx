import { useState, type FormEvent, type KeyboardEvent } from "react";
import type { ChatStatus } from "@/types";

interface ChatInputProps {
  onSend: (message: string) => void;
  status: ChatStatus;
}

export function ChatInput({ onSend, status }: ChatInputProps) {
  const [value, setValue] = useState("");
  const disabled = status === "streaming" || status === "tool_calling";

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="border-t border-border bg-card px-4 py-3"
    >
      <textarea
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask Nova anything..."
        disabled={disabled}
        rows={1}
        className="w-full resize-none bg-transparent text-sm placeholder:text-muted-foreground focus:outline-none disabled:opacity-50"
      />
    </form>
  );
}
