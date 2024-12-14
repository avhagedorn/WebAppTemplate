import { ReactQueryClientProvider } from "@/components/ReactQueryClientProvider";
import "./globals.css";
import type { Metadata } from "next";
import { Manrope } from "next/font/google";

export const metadata: Metadata = {
  title: "project_title",
  description: "Track your portfolio against the market",
};

const manrope = Manrope({
  style: "normal",
  weight: "variable",
  subsets: ["latin", "latin-ext"],
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <ReactQueryClientProvider>
        <body className={manrope.className}>{children}</body>
      </ReactQueryClientProvider>
    </html>
  );
}
