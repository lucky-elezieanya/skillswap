"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";

export default function SignupForm() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    email: "",
    username: "",
    password: "",
    phone: "",
    location: "",
    is_provider: false,
  });

  const [agreeToTerms, setAgreeToTerms] = useState(false);
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const target = e.target as HTMLInputElement | HTMLSelectElement;
    const { name, value, type } = target;

    if (name === "agree") {
      setAgreeToTerms((target as HTMLInputElement).checked);
    } else {
      setFormData((prev) => ({
        ...prev,
        [name]:
          type === "checkbox" ? (target as HTMLInputElement).checked : value,
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!agreeToTerms) {
      toast.error("You must agree to the terms and conditions.");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/signup/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await res.json();

      if (!res.ok) {
        toast.error(data.detail || "Signup failed");
        return;
      }

      router.push(
        "/verify-email-sent?email=" + encodeURIComponent(formData.email)
      );
    } catch {
      toast.error("An error occurred during signup");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto mt-8 p-6 bg-white border border-gray-200 rounded-md shadow-md">
      <h2 className="text-xl font-semibold text-center mb-6 text-gray-800">
        Create Your SkillSwap Account
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <Label htmlFor="email">Email</Label>
          <Input
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            required
            placeholder="you@example.com"
          />
        </div>
        <div>
          <Label htmlFor="username">Username</Label>
          <Input
            name="username"
            type="text"
            value={formData.username}
            onChange={handleChange}
            required
            placeholder="e.g. skillking"
          />
        </div>
        <div>
          <Label htmlFor="password">Password</Label>
          <Input
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            required
            placeholder="Your password"
          />
        </div>
        <div>
          <Label htmlFor="phone">Phone</Label>
          <Input
            name="phone"
            type="tel"
            value={formData.phone}
            onChange={handleChange}
            required
            placeholder="+234..."
          />
        </div>
        <div>
          <Label htmlFor="location">Location</Label>
          <Input
            name="location"
            type="text"
            value={formData.location}
            onChange={handleChange}
            required
            placeholder="Your location"
          />
        </div>
        <div className="flex items-center space-x-2">
          <input
            type="checkbox"
            id="is_provider"
            name="is_provider"
            checked={formData.is_provider}
            onChange={handleChange}
            className="accent-sky-600"
            title="Are you a provider?"
          />
          <Label htmlFor="is_provider">Are you a provider?</Label>
        </div>
        <div className="flex items-center space-x-2">
          <input
            type="checkbox"
            id="agree"
            name="agree"
            checked={agreeToTerms}
            onChange={handleChange}
            className="accent-sky-600"
          />
          <Label htmlFor="agree" className="text-sm">
            I agree to the{" "}
            <a
              href="/terms"
              target="_blank"
              className="text-sky-600 hover:underline"
            >
              Terms and Privacy Policy
            </a>
          </Label>
        </div>
        <Button
          type="submit"
          disabled={loading || !agreeToTerms}
          className="w-full bg-sky-600 hover:bg-sky-700"
        >
          {loading ? "Signing up..." : "Sign Up"}
        </Button>
      </form>

      <p className="text-sm text-center mt-4 text-gray-600">
        Already have an account?{" "}
        <Link href="/login" className="text-sky-600 hover:underline">
          Login
        </Link>
      </p>
    </div>
  );
}
