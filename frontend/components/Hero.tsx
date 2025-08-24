// components/Hero.tsx
"use client";
import Image from "next/image";
import Link from "next/link";
import { Button } from "@/components/ui/button"; // Using ShadCN or Tailwind-based butt// import { isLoggedIn, logout } from "../utils/auth";
import { useAuth } from "../context/AuthContext";

export default function Hero() {
  // const loggedIn = isLoggedIn()
  const { authenticated, username, logout } = useAuth();

  return (
    <section className="relative h-screen w-full overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 z-0 pointer-events-none">
        <div className="absolute inset-0 bg-blue-950 bg-opacity-60 pointer-events-none" />
      </div>

      {/* Navigation */}
      <div className="relative top-0 left-0 w-full z-20 flex items-center justify-between px-6 py-5">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <Image
            src="/images/logo.jpeg"
            alt="SkillSwap Logo"
            width={30}
            height={30}
          />
          <h1 className="text-white text-2xl font-bold tracking-wide">
            SkillSwap
          </h1>
        </div>

        {/* Conditional buttons */}
        <div className="relative flex items-center gap-4 z-20">
          {!authenticated ? (
            <>
              <Button
                asChild
                variant="ghost"
                className="text-white hover:bg-white hover:text-blue-600"
              >
                <Link href="/login">Log In</Link>
              </Button>
              <Button
                asChild
                className="bg-blue-600 hover:bg-blue-700 text-white"
              >
                <Link href="/signup">Sign Up</Link>
              </Button>
            </>
          ) : (
            <>
              <span className="text-white">Hi, {username}</span>
              <Button
                asChild
                variant="ghost"
                className="text-white hover:bg-white hover:text-blue-600"
              >
                <Link href="/dashboard">Dashboard</Link>
              </Button>
              <Button
                onClick={logout}
                className="bg-red-600 hover:bg-red-700 text-white"
              >
                Logout
              </Button>
            </>
          )}
        </div>
      </div>

      {/* Hero Content */}
      <div className="relative z-20 flex flex-col items-center justify-center text-center h-full px-4">
        <h1 className="text-white text-4xl md:text-6xl font-extrabold max-w-4xl leading-tight">
          Trade Skills. Build Connections.
        </h1>
        <p className="text-blue-100 mt-6 text-lg md:text-xl max-w-2xl">
          Connect with talented people in your community or around the world.
          Swap skills, save money, and grow together.
        </p>
        <div className="mt-8 flex flex-wrap gap-4">
          <Link href="/explore">
            <Button className="bg-white font-bold text-blue-600 hover:bg-blue-100 transition-colors">
              Explore Skills
            </Button>
          </Link>
          <Link href="/how-it-works">
            <Button
              variant="outline"
              className="text-blue-600 font-bold border-white hover:bg-white hover:text-blue-600"
            >
              How It Works
            </Button>
          </Link>
        </div>
      </div>
    </section>
  );
}
