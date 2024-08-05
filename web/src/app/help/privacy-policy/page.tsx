"use client";

import ContentWrapper from "@/components/ContentWrapper";
import React from "react";

export default function PrivacyPolicy() {
  return (
    <ContentWrapper>
      <div className="w-1/3 mx-auto">
        <h1 className="text-4xl font-bold mb-2">Privacy Policy</h1>
        <p className="mb-4">Last Updated: 5/22/2024</p>
        <p>
          AlphaTracker is committed to protecting the privacy and security of
          your personal information. This privacy policy explains how we
          collect, use, and safeguard your data when you use our application. By
          using our application, you consent to the practices described in this
          policy.
        </p>
        <h2 className="text-xl font-bold mt-4">Information We Collect</h2>
        <p>
          We collect the following personal information when you use our
          application:
        </p>
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
        <h2 className="text-xl font-bold mt-4">How We Use Your Information</h2>
        <p>We use the collected information to:</p>
        <ul className="list-disc list-inside ml-2">
          <li>Provide and maintain our application&apos;s functionality</li>
          <li>Personalize your user experience</li>
          <li>Communicate with you about your account and our services</li>
          <li>Improve our application and develop new features</li>
          <li>
            Detect, prevent, and address technical issues and security threats
          </li>
        </ul>
        <h2 className="text-xl font-bold mt-4">Data Storage and Security</h2>
        <p>
          Your data is stored in a secure database and is not shared with any
          third parties. We employ industry-standard security measures to
          protect your information from unauthorized access, alteration,
          disclosure, or destruction. However, no method of transmission over
          the internet or electronic storage is 100% secure, and we cannot
          guarantee absolute security.
        </p>
        <h2 className="text-xl font-bold mt-4">Cookies</h2>
        <p>
          Our application uses cookies to store your session data. By using our
          application, you agree to the use of cookies. Cookies are not shared
          with any third parties and are solely used to maintain your session
          information.
        </p>
        <h2 className="text-xl font-bold mt-4">Data Retention and Deletion</h2>
        <p>
          We retain your personal information for as long as necessary to
          fulfill the purposes outlined in this privacy policy, unless a longer
          retention period is required or permitted by law. If you delete your
          account, all your data will be permanently removed from our servers.
        </p>
        <h2 className="text-xl font-bold mt-4">Your Rights</h2>
        <p>You have the right to:</p>
        <ul className="list-disc list-inside ml-2">
          <li>
            Request a copy of your personal data stored by our application
          </li>
          <li>Correct any inaccuracies in your personal information</li>
          <li>Delete your account and associated data</li>
          <li>Object to the processing of your personal data</li>
          <li>Restrict the processing of your personal data</li>
        </ul>
        <p>
          To exercise any of these rights, please submit a request through the{" "}
          <a href="/account" className="text-blue-500">
            Account
          </a>{" "}
          page in our application or contact us at{" "}
          <a href="mailto:me@avhagedorn.dev" className="text-blue-500">
            me@avhagedorn.dev
          </a>
          .
        </p>
        <h2 className="text-xl font-bold mt-4">Third-Party Services</h2>
        <p>
          Our application may use third-party services that have access to some
          of your personal data. These services are subject to their own privacy
          policies, which we encourage you to review.
        </p>
        <h2 className="text-xl font-bold mt-4">
          Changes to This Privacy Policy
        </h2>
        <p>
          We may update this privacy policy from time to time. We will notify
          you of any changes by posting the new privacy policy on this page and
          updating the &quot;Last Updated&quot; date at the top of the policy.
        </p>
        <h2 className="text-xl font-bold mt-4">Contact Us</h2>
        <p>
          If you have any questions, concerns, or requests regarding this
          privacy policy or our data practices, please contact us at:{" "}
          <a href="mailto:me@avhagedorn.dev" className="text-blue-500">
            me@avhagedorn.dev
          </a>
          .
        </p>
      </div>
    </ContentWrapper>
  );
}
