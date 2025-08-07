"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import Link from "next/link";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

const loginSchema = z.object({
  identifier: z.string().min(1, "Email or username is required"),
  password: z.string().min(1, "Password is required"),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export default function LoginForm() {
  const router = useRouter();

  const form = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      identifier: "",
      password: "",
    },
  });

  const onSubmit = async (data: LoginFormValues) => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/login/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            identifier: data.identifier,
            password: data.password,
          }),
          credentials: "include", // to include cookies if you're using session-based auth
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Login failed");
      }

      toast.success("Login successful");
      router.replace("/"); // ✅ redirect to homepage without keeping login in browser history
    } catch (error: unknown) {
      const errorMessage =
        error instanceof Error ? error.message : "Something went wrong";
      toast.error(errorMessage);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto mt-12 p-8 border rounded-md shadow-md bg-white">
      <h1 className="text-3xl font-bold text-blue-600 mb-6 text-center">
        Welcome Back
      </h1>

      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <FormField
            control={form.control}
            name="identifier"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email or Username</FormLabel>
                <FormControl>
                  <Input
                    placeholder="Enter your email or username"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="password"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Password</FormLabel>
                <FormControl>
                  <Input
                    type="password"
                    placeholder="Enter your password"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <div className="flex justify-between items-center text-sm text-gray-600">
            <Link
              href="/forgot-password"
              className="text-blue-600 hover:underline"
            >
              Forgot Password?
            </Link>
          </div>

          <Button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold"
          >
            Login
          </Button>
        </form>
      </Form>

      <div className="mt-6 text-center text-sm text-gray-600">
        Don&apos;t have an account?{" "}
        <Link href="/signup" className="text-blue-600 hover:underline">
          Sign up
        </Link>
      </div>

      {/* Future: Social login buttons */}
      {/*
      <div className="mt-6">
        <div className="flex items-center space-x-4">
          <button className="w-full border px-4 py-2 rounded flex items-center justify-center space-x-2 hover:bg-gray-100">
            <FcGoogle className="text-xl" />
            <span>Continue with Google</span>
          </button>
          <button className="w-full border px-4 py-2 rounded flex items-center justify-center space-x-2 hover:bg-gray-100">
            <AppleIcon className="text-xl" />
            <span>Continue with Apple</span>
          </button>
        </div>
      </div>
      */}
    </div>
  );
}
