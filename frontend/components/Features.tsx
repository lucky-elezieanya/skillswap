import { Handshake, ShieldCheck, Users } from "lucide-react";

const features = [
  {
    icon: <Handshake className="w-8 h-8 text-blue-600" />,
    title: "Barter",
    desc: "Exchange services directly with other users.",
  },
  {
    icon: <ShieldCheck className="w-8 h-8 text-blue-600" />,
    title: "Secure Escrow",
    desc: "Transactions are protected using our escrow system.",
  },
  {
    icon: <Users className="w-8 h-8 text-blue-600" />,
    title: "Connect Easily",
    desc: "Find skilled people around you or online.",
  },
];

export default function Features() {
  return (
    <section className="py-16 px-6 md:px-20 bg-blue-50">
      <h2 className="text-3xl font-bold text-center mb-10 text-gray-800">
        How It Works
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
        {features.map((item, index) => (
          <div
            key={index}
            className="bg-white p-6 rounded-lg shadow-sm text-center hover:shadow-md transition"
          >
            <div className="flex justify-center mb-4">{item.icon}</div>
            <h3 className="font-semibold text-lg text-gray-900">
              {item.title}
            </h3>
            <p className="text-gray-500 text-sm mt-2 px-4">{item.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
