import { fetchServer } from "@/lib/fetch";

export default async function register({
  username,
  email,
  password,
  confirm_password,
}: {
  username: string;
  email: string;
  password: string;
  confirm_password: string;
}) {
  const params = new URLSearchParams({
    username,
    email,
    password,
    confirm_password,
  }).toString();

  return fetchServer(`/auth/register?${params}`, {
    method: "POST",
  });
}
