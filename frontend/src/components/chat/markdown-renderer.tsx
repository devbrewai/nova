import type { CSSProperties, ReactNode } from "react";
import ReactMarkdown, { type Components } from "react-markdown";
import remarkGfm from "remark-gfm";

interface MarkdownRendererProps {
  content: string;
}

const components: Components = {
  p: ({ children }) => <p className="leading-relaxed">{children}</p>,
  strong: ({ children }) => (
    <strong className="font-semibold text-foreground">{children}</strong>
  ),
  em: ({ children }) => <em className="italic">{children}</em>,
  a: ({ children, href }) => (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="text-primary underline underline-offset-2 hover:text-primary/80"
    >
      {children}
    </a>
  ),
  ul: ({ children }) => (
    <ul className="list-disc list-outside space-y-1 pl-5">{children}</ul>
  ),
  ol: ({ children }) => (
    <ol className="list-decimal list-outside space-y-1 pl-5">{children}</ol>
  ),
  li: ({ children }) => <li className="leading-relaxed">{children}</li>,
  h1: ({ children }) => (
    <h1 className="mt-2 text-base font-semibold">{children}</h1>
  ),
  h2: ({ children }) => (
    <h2 className="mt-2 text-sm font-semibold">{children}</h2>
  ),
  h3: ({ children }) => (
    <h3 className="text-sm font-semibold text-muted-foreground">{children}</h3>
  ),
  hr: () => <hr className="my-3 border-border" />,
  blockquote: ({ children }) => (
    <blockquote className="border-l-2 border-border pl-3 italic text-muted-foreground">
      {children}
    </blockquote>
  ),
  pre: ({ children }) => (
    <pre className="my-2 overflow-x-auto rounded-md bg-muted/60 p-3 font-mono text-xs">
      {children}
    </pre>
  ),
  code: ({ className, children }) => {
    // Fenced code blocks get a language-* class from remark; style those via <pre>.
    const isBlock = typeof className === "string" && className.includes("language-");
    if (isBlock) {
      return <code className={className}>{children}</code>;
    }
    return (
      <code className="rounded bg-muted px-1 py-0.5 font-mono text-[0.85em]">
        {children}
      </code>
    );
  },
  table: ({ children }) => (
    <div className="my-2 overflow-x-auto rounded-md border border-border">
      <table className="w-full border-collapse text-xs">{children}</table>
    </div>
  ),
  thead: ({ children }) => <thead className="bg-muted/40">{children}</thead>,
  tr: ({ children }) => (
    <tr className="border-b border-border/60 last:border-0">{children}</tr>
  ),
  th: ({ children, style }) => (
    <th
      style={style as CSSProperties | undefined}
      className="whitespace-nowrap px-2.5 py-1.5 text-left text-[10px] font-medium uppercase tracking-wide text-muted-foreground"
    >
      {children}
    </th>
  ),
  td: ({ children, style }) => (
    <td
      style={style as CSSProperties | undefined}
      className="px-2.5 py-1.5 align-top text-foreground"
    >
      {children}
    </td>
  ),
};

export function MarkdownRenderer({ content }: MarkdownRendererProps): ReactNode {
  return (
    <div className="space-y-2 text-sm leading-relaxed text-foreground/90">
      <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
        {content}
      </ReactMarkdown>
    </div>
  );
}
