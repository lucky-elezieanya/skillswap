import { NextRequest, NextResponse } from "next/server";

// Define public routes that don't require authentication
const publicRoutes = ["/", "/login", "/signup", "/api/auth/login"];

export function middleware(request: NextRequest) {
  const token = request.cookies.get("token")?.value;
  const { pathname } = request.nextUrl;

  // Allow public routes through
  if (publicRoutes.includes(pathname)) {
    return NextResponse.next();
  }

  // Redirect unauthenticated users to login
  if (!token) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("redirect", pathname); // optionally pass redirect path
    return NextResponse.redirect(loginUrl);
  }

  // User is authenticated
  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/profile/:path*", "/services/:path*"], // secured routes
};
