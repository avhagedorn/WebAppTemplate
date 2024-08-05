"use client";

import ContentWrapper from "@/components/ContentWrapper";
import React from "react";

export default function Support() {
  return (
    <ContentWrapper>
      <div className="w-1/3 mx-auto">
        <h1 className="text-4xl font-bold mb-4">Support</h1>
        <p>
          If you have any questions or concerns, please contact us at{" "}
          <a href={`mailto:me@avhagedorn.dev`} className="text-blue-500">
            me@avhagedorn.dev
          </a>
          .
        </p>
      </div>
    </ContentWrapper>
  );
}
