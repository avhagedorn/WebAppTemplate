"use client";

import { useRouter } from "next/navigation";
import { useQuery } from "react-query";
import { fetchSS } from "@/lib/fetch";
import ContentWrapper from "@/components/ContentWrapper";

export default function Home() {
  const router = useRouter();
  const { data, isFetching } = useQuery("user", () => fetchSS("/user/me"));

  if (isFetching) {
    return null;
  } else if (data) {
    router.push("/home");
  } else {
    return (
      <ContentWrapper className="bg-gradient-to-r from-white to-emerald-50">
        <h1 className="text-4xl font-bold text-center">Welcome to project_name!</h1>
      </ContentWrapper>
    );
  }
}
