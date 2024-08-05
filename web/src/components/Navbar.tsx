import React from "react";
import "@/style/loading.css";
import StockSearch from "./StockSearch";

interface NavbarProps {
  hideFooter: boolean;
}

export default function Navbar({ hideFooter }: NavbarProps) {
  if (!hideFooter) {
    return (
      <div className="px-8 top-0 w-full">
        <div className="flex justify-between items-center space-x-4 font-bold">
          <div className="py-4 flex-none">
            <a href="/" className="mr-4">
              [⍺T]
            </a>
          </div>
          <div className="py-4 flex-none">
            <a href="/auth/login" className="mr-4">
              Login
            </a>
          </div>
        </div>
      </div>
    );
  } else {
    return (
      <div className="px-8 top-0 w-full">
        <div className="relative flex items-center justify-between font-bold">
          <div className="py-4">
            <a href="/home" className="mr-4">
              [⍺T]
            </a>
          </div>
          <div className="absolute w-1/5 left-1/2 transform -translate-x-1/2 font-normal">
            <StockSearch />
          </div>
          <div className="py-4">
            <a href="/compare" className="mr-4">
              Compare
            </a>
            <a href="/strategies" className="mr-4">
              Strategies
            </a>
            <a href="/account" className="mr-4">
              Account
            </a>
            <a href="/api/auth/logout">Logout</a>
          </div>
        </div>
      </div>
    );
  }
}
