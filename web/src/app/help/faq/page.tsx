"use client";

import ContentWrapper from "@/components/ContentWrapper";
import React from "react";

export default function FAQ() {
  return (
    <ContentWrapper>
      <div className="w-1/3 mx-auto">
        <h1 className="text-4xl font-bold mb-4">Frequently Asked Questions</h1>
        <h2 className="text-xl font-bold mt-4">What is AlphaTracker?</h2>
        <p>
          AlphaTracker is a web application that allows users to track their
          investments and portfolios. Users can create portfolios, add
          positions, and compare their performance against various benchmarks.
        </p>
        <h2 className="text-xl font-bold mt-4">
          What kinds of assets can I track?
        </h2>
        <p>
          AlphaTracker only supports tracking equities (stocks) at this time. We
          plan to add support for other asset classes in the future.
        </p>
        <h2 className="text-xl font-bold mt-4">Do you allow trading?</h2>
        <p>
          No, AlphaTracker is a portfolio tracking application only. We do not
          support trading or brokerage services.
        </p>
        <h2 className="text-xl font-bold mt-4">Is AlphaTracker free?</h2>
        <p>
          Yes, AlphaTracker is free to use. You can create an account and start
          tracking your investments at no cost.
        </p>
      </div>
    </ContentWrapper>
  );
}
