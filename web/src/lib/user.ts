import { useQuery } from "react-query";
import { fetchSS } from "./fetch";
import { UserResponse } from "@/types";

export default function useGetUser() {
  const { data, isFetching } = useQuery("user", () => fetchSS("/user/me"));
  const user = <UserResponse | undefined>data;
  return { user, isFetching };
}
