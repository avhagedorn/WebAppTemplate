"use client";

import Button from "@/components/Button";
import register from "./lib";
import { useState } from "react";
import { toast } from "react-toastify";
import ContentWrapper from "@/components/ContentWrapper";
import { fetchServer } from "@/lib/fetch";

export default function RegisterPage() {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    setIsSubmitting(true);
    event.preventDefault();
    const form = event.currentTarget;
    const data = new FormData(form);
    const result = await fetchServer("/auth/register", {
      method: "POST",
      body: JSON.stringify({
        username: data.get("username"),
        email: data.get("email"),
        password: data.get("password"),
        confirm_password: data.get("confirm_password"),
      }),
    });

    if (result.data) {
      window.location.href = "/home";
    } else {
      setIsSubmitting(false);
      toast.error("Failed to register. " + result.error);
    }
  };

  return (
    <ContentWrapper hideNavbar hideFooter className="p-0">
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="bg-white p-8 rounded shadow-md w-full max-w-md">
          <h2 className="text-2xl font-bold mb-6">Register</h2>
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
            <div className="mb-4">
              <label
                htmlFor="email"
                className="block text-gray-700 font-bold mb-2"
              >
                Email
              </label>
              <input
                type="email"
                id="email"
                name="email"
                className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-emerald-500"
                placeholder="Enter your email"
                required
              />
            </div>
            <div className="mb-4">
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
            <div className="flex items-center justify-between">
              <Button type="submit" isLoading={isSubmitting}>
                Register
              </Button>
              <p>
                Have an account?{" "}
                <a
                  href="/auth/login"
                  className="text-emerald-500 hover:text-emerald-600"
                >
                  Login
                </a>
              </p>
            </div>
          </form>
        </div>
      </div>
    </ContentWrapper>
  );
}
