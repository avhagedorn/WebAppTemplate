import React, { useState, useCallback, useRef, useEffect } from "react";
import debounce from "lodash/debounce";
import { fetchServer } from "@/lib/fetch";
import { toast } from "react-toastify";
import { highlightText } from "@/lib/displayUtils";

interface SearchResult {
  id: number;
  name: string;
}

interface SearchProps {
  onSelect: (result: SearchResult) => void;
  fetchResults: (term: string) => Promise<SearchResult[]>;
  focusInput?: boolean;
  placeholder?: string;
  className?: string;
  inline?: boolean;
}

export default function GeneralSearch({
  onSelect,
  fetchResults,
  placeholder,
  className,
  focusInput = false,
  inline = false,
}: SearchProps) {
  const [searchTerm, setSearchTerm] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [focusedIndex, setFocusedIndex] = useState(-1);
  const debouncedSearch = useRef<any>(null);
  const componentRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (focusInput) {
      componentRef.current?.focus();
    }
  }, [focusInput]);

  const handleSearch = useCallback(async (term: string) => {
    if (term.length === 0 || term.startsWith(" ")) {
      setResults([]);
      return;
    }
    try {
      const searchResults = await fetchResults(term);
      setResults(searchResults);
    } catch (error: any) {
      toast.error("Failed to search: " + String(error));
    }
  }, [fetchResults]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (results.length === 0) return;

    if (e.key === "ArrowUp") {
      e.preventDefault();
      setFocusedIndex((prevIndex) => (prevIndex <= 0 ? results.length - 1 : prevIndex - 1));
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      setFocusedIndex((prevIndex) => (prevIndex === results.length - 1 ? 0 : prevIndex + 1));
    } else if (e.key === "Enter" && focusedIndex !== -1) {
      handleSelect(results[focusedIndex]);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const term = e.target.value;
    setSearchTerm(term);
    if (debouncedSearch.current) {
      debouncedSearch.current.cancel();
    }
    debouncedSearch.current = debounce(() => handleSearch(term), 200);
    debouncedSearch.current();
  };

  const handleSelect = (selectedResult: SearchResult) => {
    onSelect(selectedResult);
    setSearchTerm("");
    setResults([]);
  };

  return (
    <div className={inline ? "relative inline-block" : undefined}>
      <input
        type="text"
        className={className}
        placeholder={placeholder}
        value={searchTerm}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
        autoFocus={focusInput}
        ref={componentRef}
      />
      {results.length > 0 && (
        <div className="absolute w-full text-center z-10 mt-1 bg-white border border-gray-300 rounded-md shadow-lg">
          {results.map((result, index) => (
            <button
              key={index}
              onClick={() => handleSelect(result)}
              className={`w-full rounded-md px-4 py-2 hover:bg-gray-100 cursor-pointer ${index === focusedIndex ? "bg-gray-200" : ""}`}
            >
              {highlightText(searchTerm, result.name)}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
