// "use client";

// import Image from "next/image";

// export default function Hero() {
//   return (
//     <section className="bg-blue-900 text-white py-16 px-6 md:px-20">
//       <div className="grid grid-cols-1 md:grid-cols-2 gap-10 items-center">
//         <div className="z-100">
//           <h1 className="text-4xl md:text-5xl font-bold mb-4">
//             Swap Skills, Not Bills
//           </h1>
//           <p className="mb-6 max-w-md text-lg">
//             Barter or offer services securely with professionals in your area or
//             globally.
//           </p>
//           <button className="bg-white text-blue-600 font-semibold px-6 py-3 rounded-md hover:bg-blue-100">
//             Get Started
//           </button>
//         </div>
//         <div>
//           <Image
//             src="/images/hero-1.webp"
//             alt="Freelancer woman"
//             width={500}
//             height={500}
//             className="rounded-lg shadow-lg object- w-full h-full"
//           />
//         </div>
//       </div>
//     </section>
//   );
// }

// components/HeroSection.tsx
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
          <Link href="/login">
            <Button
              variant="ghost"
              className="text-white hover:bg-white hover:text-blue-600 transition-colors"
            >
              Log In
            </Button>
          </Link>
          <Link href="/signup">
            <Button className="bg-blue-600 hover:bg-blue-700 text-white transition-colors">
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
