"use client";

import ContentWrapper from "@/components/ContentWrapper";
import useGetUser from "@/lib/user";

export default function Home() {
  const { user, isFetching } = useGetUser();

  if (isFetching) {
    return null;
  } else {
    return (
      <ContentWrapper className="bg-gradient-to-r from-white to-emerald-50">
        <h1 className="text-4xl font-bold text-center">
          Welcome to project_title!
        </h1>
        <p className="text-center">{user?.username}</p>
      </ContentWrapper>
    );
  }
}
