"use client";

import ContentWrapper from "@/components/ContentWrapper";
import React from "react";

export default function DataUsage() {
  return (
    <ContentWrapper>
      <div className="w-1/3 mx-auto">
        <h1 className="text-4xl font-bold">Data Usage</h1>
        <h2 className="text-xl font-bold mt-4">Cookies</h2>
        <p>
          This application uses cookies to store your session data. By using
          this application, you agree to the use of cookies. Cookies are used to
          store your session data and are not shared with any third parties.
        </p>
        <h2 className="text-xl font-bold mt-4">Data Storage</h2>
        <p>
          This application stores your data in a secure database. We do not
          share your data with any third parties. If you have any questions or
          concerns, please email{" "}
          <a href="mailto:me@avhagedorn.dev" className="text-blue-500">
            me@avhagedorn.dev
          </a>
          .
        </p>
        <h2 className="text-xl font-bold mt-4">Type of Data Stored</h2>
        <ul className="list-disc list-inside ml-2">
          <li>Username</li>
          <li>Email Address</li>
          <li>Password (hashed)</li>
          <li>Session Data</li>
          <li>Portfolios (Strategies) Created</li>
          <li>
            Positions in Portfolios
            <ul className="list-disc list-inside ml-6">
              <li>Symbol</li>
              <li>Quantity</li>
              <li>Price</li>
              <li>Timestamp</li>
            </ul>
          </li>
          <li>Transactions in Portfolios</li>
        </ul>
        <h2 className="text-xl font-bold mt-4">Data Deletion</h2>
        <p>
          If you delete your account, all of your data will be permanently
          deleted from our servers.
        </p>
        <h2 className="text-xl font-bold mt-4">Request a Copy of Your Data</h2>
        <p>
          If you have an account and would like to request a copy of your data,
          please submit a data copy request in the{" "}
          <a href="/account" className="text-blue-500">
            Account
          </a>{" "}
          page. We will send you a copy of your data within 30 days.
        </p>
        <h2 className="text-xl font-bold mt-4">Third Party Services</h2>
        <p>
          We use third party services to provide additional functionality to
          this application. These services may have their own privacy policies
          and terms of service. We are not responsible for the privacy practices
          of these services.
        </p>
      </div>
    </ContentWrapper>
  );
}
