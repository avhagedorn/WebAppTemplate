import React, { useState } from "react";
import { FiHelpCircle } from "react-icons/fi";

interface TooltipProps {
  text: string;
}

export default function Tooltip({ text }: TooltipProps) {
  const [isHovered, setIsHovered] = useState(false);

  const handleMouseEnter = () => {
    setIsHovered(true);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
  };

  const getTooltipWidthClass = (text: string) => {
    const length = text.length;
    if (length <= 20) {
      return "w-48";
    } else if (length <= 40) {
      return "w-64";
    } else {
      return "w-80";
    }
  };

  return (
    <div
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      className="relative inline-block"
    >
      <FiHelpCircle />
      {isHovered && (
        <div
          className={`absolute left-1/2 transform -translate-x-1/2 mt-2 bg-black text-white px-2 py-1 rounded z-10 ${getTooltipWidthClass(text)} tooltip`}
        >
          <div
            style={{
              position: "absolute",
              top: "-4px",
              left: "50%",
              transform: "translateX(-50%)",
              borderLeft: "8px solid transparent",
              borderRight: "8px solid transparent",
              borderBottom: "6px solid black",
            }}
          ></div>
          {text}
        </div>
      )}
    </div>
  );
}
