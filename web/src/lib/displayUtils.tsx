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
