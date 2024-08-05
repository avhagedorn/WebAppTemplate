"use client";

import Button from "@/components/Button";
import ContentWrapper from "@/components/ContentWrapper";
import { fetchServer } from "@/lib/fetch";
import { useState } from "react";
import { toast } from "react-toastify";

export default function ResetPassword({
  params,
}: {
  params: {
    uuid: string;
  };
}) {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    setIsSubmitting(true);
    event.preventDefault();
    const form = event.currentTarget;
    const result = await fetchServer("/auth/reset-password", {
      method: "POST",
      body: JSON.stringify({
        password: form.password.value,
        confirm_password: form.confirm_password.value,
        reset_password_request_id: params.uuid,
      }),
    });

    setIsSubmitting(false);
    if (result.data) {
      toast.success("Password reset successful");
      window.location.href = "/auth/login";
    } else {
      toast.error("Failed to reset password. " + result.error);
    }
  };

  return (
    <ContentWrapper hideNavbar hideFooter className="p-0">
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="bg-white p-8 rounded shadow-md w-full max-w-md">
          <h2 className="text-2xl font-bold mb-6">Set New Password</h2>
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label
                htmlFor="password"
                className="block text-gray-700 font-bold mb-2"
              >
                New Password
              </label>
              <input
                type="password"
                id="password"
                name="password"
                className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-emerald-500"
                placeholder="Enter your password"
                minLength={8}
                required
              />
            </div>
            <div className="mb-6">
              <label
                htmlFor="confirmPassword"
                className="block text-gray-700 font-bold mb-2"
              >
                Confirm Password
              </label>
              <input
                type="password"
                id="confirmPassword"
                name="confirm_password"
                className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-emerald-500"
                placeholder="Confirm your password"
                minLength={8}
                required
              />
            </div>
            <Button type="submit" isLoading={isSubmitting}>
              Save
            </Button>
          </form>
        </div>
      </div>
    </ContentWrapper>
  );
}
