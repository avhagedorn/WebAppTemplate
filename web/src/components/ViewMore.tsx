import React, { useState } from "react";
import { FaPlus, FaMinus } from "react-icons/fa";

export default function ViewMore({ children }: { children: React.ReactNode }) {
  const [isExpanded, setIsExpanded] = useState(false);

  const handleToggle = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className="w-full">
      <div className="w-full flex flex-row items-center space-x-4 text-gray-400">
        <button className="py-2" onClick={handleToggle}>
          <div className="flex items-center">
            {isExpanded ? (
              <FaMinus className="mr-2" />
            ) : (
              <FaPlus className="mr-2" />
            )}
            <span className="font-medium">
              {isExpanded ? "View Less" : "View More"}
            </span>
          </div>
        </button>
        <hr className="flex-grow border-gray-400" />
      </div>
      {isExpanded && <div>{children}</div>}
    </div>
  );
}
