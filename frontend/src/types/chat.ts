export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: number;
  toolUse?: ToolUseEvent;
}

export type ChatStatus = "idle" | "streaming" | "tool_calling" | "error";

export interface ToolUseEvent {
  name: string;
  status: "running" | "complete";
  result?: string;
}

export interface SSEEvent {
  type:
    | "conversation_id"
    | "text_delta"
    | "tool_use"
    | "tool_result"
    | "done"
    | "error";
  id?: string;
  content?: string;
  name?: string;
  status?: string;
  result?: string;
  message?: string;
}
