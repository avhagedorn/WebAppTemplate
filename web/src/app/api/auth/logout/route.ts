import { NextResponse, NextRequest } from "next/server";

export async function GET(request: NextRequest) {
  const response = NextResponse.redirect(new URL("/", request.url));

  response.headers.set(
    "Set-Cookie",
    "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;",
  );

  return response;
}
