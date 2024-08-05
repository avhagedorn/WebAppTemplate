import { GraphData } from "@/types";

export function highlightText(highlight: string, text: string) {
  const regex = new RegExp(`(${highlight})`, "i");
  const match = text.match(regex);

  if (match && match.index !== undefined) {
    const startIndex = match.index;
    const endIndex = startIndex + match[0].length;
    const beforeMatch = text.slice(0, startIndex);
    const afterMatch = text.slice(endIndex);

    return (
      <span>
        {beforeMatch}
        <span className="font-bold">{match[0]}</span>
        {afterMatch}
      </span>
    );
  }

  return text;
}

export function getLineColor(data: GraphData[]) {
  if (data.length === 0) return "#10b981"; // emerald-500

  const firstPrice = data[0].left;
  const lastPrice = data[data.length - 1].left;
  return firstPrice < lastPrice ? "#10b981" : "#ef4444"; // emerald-500 : red-500
}
