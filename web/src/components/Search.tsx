import React, { useState, useCallback, useRef, useEffect } from "react";
import debounce from "lodash/debounce";
import { fetchServer } from "@/lib/fetch";
import { toast } from "react-toastify";
import { highlightText } from "@/lib/displayUtils";
import { SearchableSymbol } from "@/types";

interface PortfolioResult {
  id: number;
  name: string;
}

interface StockResult {
  ticker: string;
  name: string;
}

interface SearchProps {
  onSelect: (symbol: SearchableSymbol) => void;
  focusInput?: boolean;
  placeholder?: string;
  className?: string;
  inline?: boolean;
}

export default function Search({
  onSelect,
  placeholder,
  className,
  focusInput = false,
  inline = false,
}: SearchProps) {
  const [searchTerm, setSearchTerm] = useState("");
  const [stockResults, setStockResults] = useState<StockResult[]>([]);
  const [portfolioResults, setPortfolioResults] = useState<PortfolioResult[]>(
    [],
  );
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
      setStockResults([]);
      setPortfolioResults([]);
      return;
    }
    const response = await fetchServer(`/search/stock?q=${term}`);
    if (response.data) {
      setStockResults(response.data.ticker_results || []);
      setPortfolioResults(response.data.portfolio_results || []);
    } else {
      toast.error("Failed to search: " + response.error);
    }
  }, []);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    const totalResults = stockResults.length + portfolioResults.length;
    if (totalResults === 0) return;

    if (e.key === "ArrowUp") {
      e.preventDefault();
      setFocusedIndex((prevIndex) =>
        prevIndex <= 0 ? totalResults - 1 : prevIndex - 1,
      );
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      setFocusedIndex((prevIndex) =>
        prevIndex === totalResults - 1 ? 0 : prevIndex + 1,
      );
    } else if (e.key === "Enter" && focusedIndex !== -1) {
      const selectionIsStock = focusedIndex < stockResults.length;

      if (selectionIsStock) {
        const stock = stockResults[focusedIndex];
        handleSelect({
          ticker: stock.ticker,
          name: stock.name,
          type: "STOCK",
        });
      } else {
        const portfolio = portfolioResults[focusedIndex - stockResults.length];
        handleSelect({
          id: portfolio.id,
          name: portfolio.name,
          type: "PORTFOLIO",
        });
      }
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

  const handleSelect = (selectedSymbol: SearchableSymbol) => {
    onSelect(selectedSymbol);
    setSearchTerm("");
    setStockResults([]);
    setPortfolioResults([]);
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
      {(stockResults.length > 0 || portfolioResults.length > 0) && (
        <div className="absolute w-full text-center z-10 mt-1 bg-white border border-gray-300 rounded-md shadow-lg">
          {stockResults.length > 0 && (
            <>
              <div className="text-left text-sm text-gray-600 px-4 py-2 border-b border-gray-300">
                Stocks
              </div>
              {stockResults.map((result, index) => (
                <button
                  key={index}
                  onClick={() =>
                    handleSelect({
                      ticker: result.ticker,
                      name: result.ticker,
                      type: "STOCK",
                    })
                  }
                  className={`w-full rounded-md px-4 py-2 hover:bg-gray-100 cursor-pointer ${index === focusedIndex ? "bg-gray-200" : ""}`}
                >
                  {highlightText(
                    searchTerm,
                    `${result.ticker} - ${result.name}`,
                  )}
                </button>
              ))}
            </>
          )}
          {portfolioResults.length > 0 && (
            <>
              <div className="text-left text-sm text-gray-600 px-4 py-2 border-b border-gray-300 my-2">
                Portfolios
              </div>
              {portfolioResults.map((result, index) => (
                <button
                  key={index + stockResults.length}
                  onClick={() =>
                    handleSelect({
                      id: result.id,
                      name: result.name,
                      type: "PORTFOLIO",
                    })
                  }
                  className={`w-full rounded-md px-4 py-2 hover:bg-gray-100 cursor-pointer ${index + stockResults.length === focusedIndex ? "bg-gray-200" : ""}`}
                >
                  {highlightText(searchTerm, result.name)}
                </button>
              ))}
            </>
          )}
        </div>
      )}
    </div>
  );
}
