// frontend/app/login/page.tsx
import Login from "./LoginForm";
import React from "react";

export const metadata = {
  title: "Login - SkillSwap",
  description: "Log in to your SkillSwap account",
};

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-blue-100 px-4">
      <Login />
    </div>
  );
}
