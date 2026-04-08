import { useEffect, useState } from "react";
import type { ChatStatus } from "@/types";

const STREAMING_WORDS = ["Thinking", "Reasoning", "Composing", "Shaping"];
const TOOL_WORDS = ["Searching", "Looking up", "Checking"];
const ROTATE_INTERVAL_MS = 1500;

interface TypingIndicatorProps {
  phase: ChatStatus;
}

export function TypingIndicator({ phase }: TypingIndicatorProps) {
  const words = phase === "tool_calling" ? TOOL_WORDS : STREAMING_WORDS;
  const [index, setIndex] = useState(0);

  useEffect(() => {
    setIndex(0);
    const id = window.setInterval(() => {
      setIndex((prev) => (prev + 1) % words.length);
    }, ROTATE_INTERVAL_MS);
    return () => window.clearInterval(id);
  }, [words]);

  return (
    <span className="px-4 py-2 text-sm font-medium text-muted-foreground animate-pulse">
      {words[index]}…
    </span>
  );
}
