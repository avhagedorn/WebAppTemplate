import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";

const protectedRoutes = [
  "/home",
];

export default function middleware(req: NextRequest) {
  const path = req.nextUrl.pathname;
  const isProtectedRoute = protectedRoutes.includes(path);
  const token = cookies().get("access_token")?.value;

  // Redirect to login if user is not logged in and tries to access protected routes
  if (isProtectedRoute && !token) {
    return NextResponse.redirect(new URL("/auth/login", req.nextUrl));
  }

  // Redirect to home if user is logged in and tries to access login or register page
  else if (("/auth/login" === path || "/auth/register" === path) && token) {
    return NextResponse.redirect(new URL("/home", req.nextUrl));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|.*\\.png$).*)"],
};
