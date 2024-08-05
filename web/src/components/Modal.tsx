"use client";

import React from "react";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  size?: "small" | "medium" | "large";
}

const Modal = ({
  isOpen,
  onClose,
  title,
  children,
  size = "medium",
}: ModalProps) => {
  if (!isOpen) return null;

  const handleOverlayClick = (event: React.MouseEvent<HTMLDivElement>) => {
    if (event.target === event.currentTarget) {
      onClose();
    }
  };

  const modalSize = {
    small: "w-1/4 min-w-96",
    medium: "w-1/3 min-w-96",
    large: "w-1/2 min-w-96",
  }[size];

  return (
    <>
      <div
        className="fixed inset-0 z-40 bg-black opacity-50"
        onClick={handleOverlayClick}
      ></div>
      <div
        className={`z-50 flex items-center justify-center ${modalSize} fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2`}
      >
        <div className="mx-auto my-6 w-full">
          <div className="flex flex-col bg-white rounded-lg">
            <div className="flex items-start justify-between p-5 border-b border-slate-200">
              <h3 className="text-3xl font-semibold">{title}</h3>
              <button onClick={onClose} className="mt-auto mb-auto ml-4">
                <svg
                  className="w-6 h-6 text-slate-600"
                  fill="none"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
            <div className="p-6">{children}</div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Modal;
