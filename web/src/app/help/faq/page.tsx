"use client";

import ContentWrapper from "@/components/ContentWrapper";
import React from "react";

export default function FAQ() {
  return (
    <ContentWrapper>
      <div className="w-1/3 mx-auto">
        <h1 className="text-4xl font-bold mb-4">Frequently Asked Questions</h1>
        <h2 className="text-xl font-bold mt-4">What is project_title?</h2>
        <p>
          project_title is a web application.
        </p>
        <h2 className="text-xl font-bold mt-4">
          What can I do on project_title?
        </h2>
      </div>
    </ContentWrapper>
  );
}
