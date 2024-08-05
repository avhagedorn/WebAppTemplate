import { fetchSS } from "./fetch";

export default function useGetUser() {
  return fetchSS("/user/me");
}
