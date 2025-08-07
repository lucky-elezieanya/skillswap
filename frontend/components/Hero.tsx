// components/Hero.tsx
"use client";
import Image from "next/image";
import Link from "next/link";
import { Button } from "@/components/ui/button"; // Using ShadCN or Tailwind-based button

export default function Hero() {
  return (
    <section className="relative h-screen w-full overflow-hidden">
      {/* Background Image */}
      <div className="absolute inset-0 z-0">
        <Image
          src="/images/hero.webp" // Ensure this is in your /public/images folder
          alt="Hero background"
          fill
          className="object-cover"
          priority
        />
        {/* Optional dark overlay */}
        <div className="absolute inset-0 bg-blue-950 bg-opacity-60" />
      </div>
      {/* Top Navigation */}
      <div className="absolute top-0 left-0 w-full z-20 flex items-center justify-between px-6 py-5">
        {/* Logo */}
        <div className="flex items-center gap-2">
          {/* <Image src="/logo.png" alt="SkillSwap Logo" width={40} height={40} /> */}
          <h1 className="text-white text-2xl font-bold tracking-wide">
            SkillSwap
          </h1>
        </div>

        {/* Buttons */}
        <div className="flex items-center gap-4">
          <Link href="/login" className="">
            <Button
              variant="ghost"
              className="w-full text-white hover:bg-white hover:text-blue-600 transition-colors"
            >
              Log In
            </Button>
          </Link>
          <Link href="/signup" className="">
            <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white transition-colors">
              Sign Up
            </Button>
          </Link>
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
