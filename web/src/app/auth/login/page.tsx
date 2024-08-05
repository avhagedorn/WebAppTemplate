"use client";

import React, { useState } from "react";
import Button from "@/components/Button";
import { toast } from "react-toastify";
import ContentWrapper from "@/components/ContentWrapper";
import Modal from "@/components/Modal";
import { fetchServer } from "@/lib/fetch";

const ForgotPasswordModal = ({
  showForgotPasswordModal,
  setShowForgotPasswordModal,
}: {
  showForgotPasswordModal: boolean;
  setShowForgotPasswordModal: (show: boolean) => void;
}) => {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    setIsSubmitting(true);
    event.preventDefault();
    const form = event.currentTarget;
    const data = new FormData(form);

    const result = await fetchServer("/auth/forgot-password", {
      method: "POST",
      body: JSON.stringify({
        email_or_username: data.get("email_or_username"),
      }),
    });

    setIsSubmitting(false);
    if (result.data) {
      toast.success("Password reset link sent successfully");
      setShowForgotPasswordModal(false);
    } else {
      toast.error("Request failed. " + result.error);
    }
  };

  return (
    <Modal
      isOpen={showForgotPasswordModal}
      onClose={() => setShowForgotPasswordModal(false)}
      title={"Forgot Password"}
      size="small"
    >
      <p className="text-gray-700 mb-4">
        Enter the email address or username associated with your account and we
        will send you a link to reset your password.
      </p>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <input
            type="text"
            id="email_or_username"
            name="email_or_username"
            className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-emerald-500"
            placeholder="Enter your email or username"
            minLength={4}
            required
          />
        </div>
        <div className="flex items-center justify-between">
          <Button type="submit" isLoading={isSubmitting}>
            Send Reset Link
          </Button>
        </div>
      </form>
    </Modal>
  );
};

export default function LoginPage() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showForgotPassword, setShowForgotPassword] = useState(false);
  const [showForgotPasswordModal, setShowForgotPasswordModal] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    setIsSubmitting(true);
    event.preventDefault();
    const form = event.currentTarget;
    const data = new FormData(form);
    const response = await fetchServer("/auth/token", {
      method: "POST",
      body: JSON.stringify({
        username: data.get("username"),
        password: data.get("password"),
      }),
    });
    if (response.data) {
      window.location.href = "/home";
    } else {
      setShowForgotPassword(true);
      setIsSubmitting(false);
      toast.error("Invalid username or password");
    }
  };

  return (
    <ContentWrapper hideNavbar hideFooter className="p-0">
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="bg-white p-8 rounded shadow-md w-full max-w-md">
          <h2 className="text-2xl font-bold mb-6">Login</h2>
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label
                htmlFor="username"
                className="block text-gray-700 font-bold mb-2"
              >
                Username
              </label>
              <input
                type="text"
                id="username"
                name="username"
                className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-emerald-500"
                placeholder="Enter your username"
                minLength={4}
                required
              />
            </div>
            <div className="mb-6">
              <label
                htmlFor="password"
                className="block text-gray-700 font-bold mb-2"
              >
                Password
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
              {showForgotPassword && (
                <p className="text-sm mt-1">
                  <button
                    type="button"
                    onClick={() => setShowForgotPasswordModal(true)}
                    className="text-emerald-500 hover:text-emerald-600"
                  >
                    Forgot password?
                  </button>
                </p>
              )}
            </div>
            <div className="flex items-center justify-between mb-4">
              <Button type="submit" isLoading={isSubmitting}>
                Login
              </Button>
              <p>
                No account?{" "}
                <a
                  href="/auth/register"
                  className="text-emerald-500 hover:text-emerald-600"
                >
                  Register
                </a>
              </p>
            </div>
          </form>
        </div>
      </div>
      <ForgotPasswordModal
        showForgotPasswordModal={showForgotPasswordModal}
        setShowForgotPasswordModal={setShowForgotPasswordModal}
      />
    </ContentWrapper>
  );
}
