import React from "react";
import "@/style/loading.css";

interface ButtonProps {
  children: React.ReactNode;
  onClick?: (() => void) | undefined;
  isLoading?: boolean;
  disabled?: boolean;
  type?: "button" | "submit";
  color?: "emerald" | "red" | "blue" | "gray" | "transparent";
  className?: string;
}

export default function Button({
  children,
  onClick = undefined,
  isLoading = false,
  disabled = false,
  type = "button",
  color = "emerald",
  className = "",
}: ButtonProps) {
  const getColors = () => {
    if (disabled) {
      return "bg-gray-300 cursor-not-allowed";
    } else if (isLoading) {
      return `bg-${color}-700 cursor-wait`;
    } else {
      return `bg-${color}-500 hover:bg-${color}-700`;
    }
  };

  return (
    <button
      className={`${className} text-white font-bold py-2 px-4 rounded ${getColors()}`}
      onClick={onClick}
      disabled={disabled || isLoading}
      type={type}
    >
      {children} {isLoading && <span className="inline-loading" />}
    </button>
  );
}
