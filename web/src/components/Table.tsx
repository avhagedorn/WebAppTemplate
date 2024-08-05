import React, { useEffect, useState } from "react";
import { FiChevronDown, FiChevronUp } from "react-icons/fi";

interface TableProps<T> {
  headers: {
    name: string;
    sort?: (a: any, b: any) => number;
  }[];
  data?: T[];
  itemToRow: (item: T) => JSX.Element;
  className?: string;
  loading?: boolean;
}

interface SortState {
  key: string;
  ascending: boolean;
}

const Table = <T,>({
  headers,
  data = [],
  itemToRow,
  className,
  loading = false,
}: TableProps<T>) => {
  const [orderedData, setOrderedData] = useState<T[]>([]);
  const [sort, setSort] = useState<SortState>({
    key: "",
    ascending: true,
  });

  useEffect(() => {
    setOrderedData(data);
  }, [setOrderedData, data]);

  return (
    <table className={`table-auto border-collapse w-full ${className}`}>
      <thead>
        <tr>
          {headers.map((header, index) => (
            <th key={index} className="px-4 py-2 text-left text-l">
              {!header.sort && <p className="text-gray-500">{header.name}</p>}
              {header.sort && (
                <button
                  className={`flex items-center hover:text-black ${header.name === sort.key ? "text-black" : "text-gray-500"}`}
                  onClick={() => {
                    const isAscending =
                      sort.key === header.name && sort.ascending;
                    const sortFn = isAscending
                      ? header.sort
                      : (a: any, b: any) => -header.sort!!(a, b);
                    setOrderedData([...data.sort(sortFn)]);
                    setSort({
                      key: header.name,
                      ascending: !isAscending,
                    });
                  }}
                  disabled={loading}
                >
                  <span className="mr-2">{header.name}</span>
                  {header.name === sort.key ? (
                    <span className="inline-flex items-center justify-center w-4 h-4">
                      {sort.ascending ? (
                        <FiChevronUp size={16} />
                      ) : (
                        <FiChevronDown size={16} />
                      )}
                    </span>
                  ) : (
                    <span className="w-4" />
                  )}
                </button>
              )}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {orderedData.map((item, index) => (
          <tr key={index} className="border-t border-gray-200">
            {itemToRow(item)}
          </tr>
        ))}
        {!orderedData.length &&
          loading &&
          [...Array(5)].map((_, i) => (
            <tr key={i} className="border-t border-gray-200">
              {headers.map((_, index) => (
                <td key={index} className="px-4 py-2">
                  <div className="h-4 bg-gray-200 animate-pulse" />
                </td>
              ))}
            </tr>
          ))}
      </tbody>
    </table>
  );
};

export default Table;
