import { Code, Palette, Megaphone, PenLine } from "lucide-react";

const categories = [
  { name: "Programming", icon: <Code className="w-15 h-15 text-white" /> },
  { name: "Design", icon: <Palette className="w-15 h-15 text-white" /> },
  { name: "Marketing", icon: <Megaphone className="w-15 h-15 text-white" /> },
  { name: "Writing", icon: <PenLine className="w-15 h-15 text-white" /> },
];

export default function Categories() {
  return (
    <section className="py-16 px-6 md:px-20">
      <h2 className="text-3xl font-bold text-center mb-10 text-gray-800">
        Popular Categories
      </h2>
      <div className="flex flex-wrap justify-center gap-4">
        {categories.map((cat, idx) => {
          return (
            <div
              key={idx}
              className="bg-blue-800 md:w-[20%] md:h-40 text-white px-6 py-4 rounded-lg flex flex-col items-center gap-2 shadow-sm"
            >
              <span>{cat.icon}</span>
              <span className="text-md font-medium">{cat.name}</span>
            </div>
          );
        })}
      </div>
    </section>
  );
}
