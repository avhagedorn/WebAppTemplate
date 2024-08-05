import React from "react";
import Navbar from "./Navbar";
import Link from "next/link";
import { Bounce, ToastContainer } from "react-toastify";

interface ContentWrapperProps {
  children: React.ReactNode;
  hideFooter?: boolean;
  className?: string;
  hideNavbar?: boolean;
}

export default function ContentWrapper({
  children,
  hideFooter = false,
  className = "bg-white",
  hideNavbar = false,
}: ContentWrapperProps) {
  return (
    <main className={className}>
      <div className="min-h-screen pb-10">
        {!hideNavbar && <Navbar hideFooter={hideFooter} />}
        <div className={hideNavbar ? "" : "pt-8"}>{children}</div>
        <ToastContainer
          position="bottom-left"
          autoClose={2000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable={false}
          pauseOnHover
          theme="colored"
          transition={Bounce}
        />
      </div>
      {!hideFooter && (
        <footer className="bg-gray-100 py-8">
          <div className="container mx-auto px-4">
            <div className="flex flex-wrap justify-between">
              <div className="w-full md:w-1/3 mb-4 md:mb-0">
                <h3 className="text-lg font-semibold mb-2">AlphaTracker</h3>
                <p className="text-gray-600">
                  &copy; {new Date().getFullYear()} AlphaTracker
                </p>
              </div>
              <div className="w-full md:w-1/3 mb-4 md:mb-0">
                <h3 className="text-lg font-semibold mb-2">Legal</h3>
                <ul className="text-gray-600">
                  <li className="mb-1">
                    <Link
                      href="/help/privacy-policy"
                      className="hover:text-gray-800"
                    >
                      Privacy Policy
                    </Link>
                  </li>
                  <li>
                    <Link
                      href="/help/data-usage"
                      className="hover:text-gray-800"
                    >
                      Data Usage
                    </Link>
                  </li>
                </ul>
              </div>
              <div className="w-full md:w-1/3">
                <h3 className="text-lg font-semibold mb-2">Contact Us</h3>
                <ul className="text-gray-600">
                  <li className="mb-1">
                    <Link href="/help/support" className="hover:text-gray-800">
                      Support
                    </Link>
                  </li>
                  <li>
                    <Link href="/help/faq" className="hover:text-gray-800">
                      FAQ
                    </Link>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </footer>
      )}
    </main>
  );
}
