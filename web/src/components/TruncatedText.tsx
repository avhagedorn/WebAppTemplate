import React, { useEffect, useRef, useState } from "react";

interface TruncatedTextProps {
  text: string;
}

export default function TruncatedText({ text }: TruncatedTextProps) {
  const [isTruncated, setIsTruncated] = useState(true);
  const hasOverflow = useRef(true);
  const textRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const checkTextHeight = () => {
      if (!textRef.current) return;

      const clampHeight =
        parseInt(getComputedStyle(textRef.current).lineHeight) * 3;
      const textHeight = textRef.current.scrollHeight;

      hasOverflow.current = textHeight > clampHeight;
      setIsTruncated(textHeight > clampHeight);
    };

    checkTextHeight();
    window.addEventListener("resize", checkTextHeight);

    return () => {
      window.removeEventListener("resize", checkTextHeight);
    };
  }, [textRef]);

  const toggleTruncate = () => {
    setIsTruncated(!isTruncated);
  };

  return (
    <div className="relative">
      <div ref={textRef} className={`${isTruncated ? "line-clamp-3" : ""}`}>
        {text}
      </div>
      <div className="flex justify-end">
        {hasOverflow.current &&
          (isTruncated ? (
            <button
              onClick={toggleTruncate}
              className="mt-2 text-emerald-500 hover:text-emerald-700 focus:outline-none text-sm"
            >
              Read More
            </button>
          ) : (
            <button
              onClick={toggleTruncate}
              className="mt-2 text-emerald-500 hover:text-emerald-700 focus:outline-none text-sm"
            >
              Read Less
            </button>
          ))}
      </div>
    </div>
  );
}
