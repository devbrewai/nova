import type { ReactNode } from "react";

interface MarkdownRendererProps {
  content: string;
}

type Block =
  | { type: "bullet"; lines: string[] }
  | { type: "text"; lines: string[] };

function parseBoldInline(text: string): ReactNode[] {
  const parts = text.split(/\*\*(.+?)\*\*/g);
  return parts.map((part, i) =>
    i % 2 === 1 ? <strong key={i}>{part}</strong> : part,
  );
}

function parseBlocks(content: string): Block[] {
  const lines = content.split("\n");
  const blocks: Block[] = [];
  let current: Block | null = null;

  for (const line of lines) {
    const isBullet = /^[-•]\s/.test(line);

    if (isBullet) {
      const text = line.replace(/^[-•]\s/, "");
      if (current?.type === "bullet") {
        current.lines.push(text);
      } else {
        current = { type: "bullet", lines: [text] };
        blocks.push(current);
      }
    } else {
      if (current?.type === "text") {
        current.lines.push(line);
      } else {
        current = { type: "text", lines: [line] };
        blocks.push(current);
      }
    }
  }

  return blocks;
}

export function MarkdownRenderer({ content }: MarkdownRendererProps) {
  const blocks = parseBlocks(content);

  const nodes: ReactNode[] = [];

  for (let i = 0; i < blocks.length; i++) {
    const block = blocks[i];

    if (block.type === "bullet") {
      nodes.push(
        <ul key={i} className="space-y-1 pl-4">
          {block.lines.map((line, j) => (
            <li key={j} className="list-disc list-outside">
              {parseBoldInline(line)}
            </li>
          ))}
        </ul>,
      );
    } else {
      // text block: render each non-empty line as a <p>
      block.lines
        .filter((line) => line.trim() !== "")
        .forEach((line, j) => {
          nodes.push(<p key={`${i}-${j}`}>{parseBoldInline(line)}</p>);
        });
    }
  }

  return <div className="space-y-2 text-sm leading-relaxed">{nodes}</div>;
}
