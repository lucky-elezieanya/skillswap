import SignupForm from "./SignupForm";

export const metadata = {
  title: "Sign Up - SkillSwap",
  description: "Log in to your SkillSwap account",
};

export default function SignupPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-sky-50">
      <SignupForm />
    </div>
  );
}
