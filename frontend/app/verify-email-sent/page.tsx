"use client";

import { useSearchParams } from "next/navigation";
import Link from "next/link";

export default function VerifyEmailSent() {
  const searchParams = useSearchParams();
  const email = searchParams.get("email");

  return (
    <div className="max-w-md mx-auto mt-10 p-6 border rounded-lg shadow bg-white text-center">
      <h1 className="text-2xl font-semibold mb-4 text-sky-700">
        Verify Your Email
      </h1>
      <p className="text-gray-700 mb-2">
        We’ve sent a verification email to{" "}
        <span className="font-medium text-gray-900">{email}</span>.
      </p>
      <p className="text-gray-600 mb-6">
        Please click the link in that email to activate your SkillSwap account.
        Check your spam folder if you don't see it.
      </p>
      <Link href="/login" className="text-sky-600 hover:underline font-medium">
        Go to Login
      </Link>
    </div>
  );
}
