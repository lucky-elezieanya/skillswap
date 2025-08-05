// export default function Footer() {
//   return (
//     <footer className="bg-blue-900 text-white py-10 px-6 md:px-20">
//       <div className="flex flex-col md:flex-row justify-between items-center gap-4">
//         <p>© 2025 SkillSwap. All rights reserved.</p>
//         <div className="flex gap-4 text-sm">
//           <a href="#" className="hover:underline">
//             About
//           </a>
//           <a href="#" className="hover:underline">
//             Contact
//           </a>
//           <a href="#" className="hover:underline">
//             Privacy
//           </a>
//         </div>
//       </div>
//     </footer>
//   );
// }
// components/Footer.tsx
import Link from "next/link";
import Image from "next/image";
import {
  FaFacebookF,
  FaTwitter,
  FaLinkedinIn,
  FaInstagram,
} from "react-icons/fa";

export default function Footer() {
  return (
    <footer className="bg-blue-900 text-white pt-16 pb-10 px-6 md:px-20">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-10">
        {/* Brand and Description */}
        <div>
          <div className="flex items-center gap-3 mb-4">
            <Image
              src="/logo.png"
              alt="SkillSwap Logo"
              width={40}
              height={40}
            />
            <h2 className="text-2xl font-bold">SkillSwap</h2>
          </div>
          <p className="text-blue-100 text-sm leading-relaxed">
            SkillSwap connects people around the world to exchange services
            through a secure barter or escrow-based system. Learn, grow, and
            earn with your skills.
          </p>
        </div>

        {/* Navigation Links */}
        <div>
          <h3 className="text-white font-semibold mb-4">Product</h3>
          <ul className="space-y-2 text-blue-100 text-sm">
            <li>
              <Link href="/explore">Explore Skills</Link>
            </li>
            <li>
              <Link href="/how-it-works">How It Works</Link>
            </li>
            <li>
              <Link href="/pricing">Pricing</Link>
            </li>
            <li>
              <Link href="/faq">FAQs</Link>
            </li>
          </ul>
        </div>

        <div>
          <h3 className="text-white font-semibold mb-4">Company</h3>
          <ul className="space-y-2 text-blue-100 text-sm">
            <li>
              <Link href="/about">About Us</Link>
            </li>
            <li>
              <Link href="/careers">Careers</Link>
            </li>
            <li>
              <Link href="/blog">Blog</Link>
            </li>
            <li>
              <Link href="/contact">Contact</Link>
            </li>
          </ul>
        </div>

        <div>
          <h3 className="text-white font-semibold mb-4">Resources</h3>
          <ul className="space-y-2 text-blue-100 text-sm">
            <li>
              <Link href="/terms">Terms of Service</Link>
            </li>
            <li>
              <Link href="/privacy">Privacy Policy</Link>
            </li>
            <li>
              <Link href="/support">Help & Support</Link>
            </li>
          </ul>
        </div>
      </div>

      {/* Socials and Copyright */}
      <div className="border-t border-blue-700 mt-10 pt-8 flex flex-col md:flex-row justify-between items-center text-sm text-blue-300 gap-4">
        <p>© {new Date().getFullYear()} SkillSwap. All rights reserved.</p>
        <div className="flex space-x-4 text-white">
          <a href="#" className="hover:text-blue-300">
            <FaFacebookF />
          </a>
          <a href="#" className="hover:text-blue-300">
            <FaTwitter />
          </a>
          <a href="#" className="hover:text-blue-300">
            <FaLinkedinIn />
          </a>
          <a href="#" className="hover:text-blue-300">
            <FaInstagram />
          </a>
        </div>
      </div>
    </footer>
  );
}
