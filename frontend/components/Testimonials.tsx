// components/Testimonials.tsx
import { Quote } from "lucide-react";

export default function Testimonials() {
  return (
    <section className="py-20 bg-white text-center">
      <div className="max-w-4xl mx-auto px-4">
        <h2 className="text-3xl md:text-4xl font-bold mb-12 text-gray-800">
          What Our Users Say
        </h2>

        <div className="grid gap-10 md:grid-cols-2 lg:grid-cols-3">
          {[
            {
              quote:
                "SkillSwap helped me trade my photography skills for web design. It's an amazing platform for creatives!",
              name: "Ada N.",
              role: "Photographer",
            },
            {
              quote:
                "I was able to get expert legal advice in exchange for my content writing service. Love this concept!",
              name: "Tunde A.",
              role: "Freelance Writer",
            },
            {
              quote:
                "Such a helpful tool. I’ve learned so much by bartering services with others. Highly recommend SkillSwap!",
              name: "Chinwe K.",
              role: "UI Designer",
            },
          ].map((testimonial, index) => (
            <div
              key={index}
              className="relative bg-gray-50 rounded-2xl p-6 shadow-md text-left flex flex-col justify-between h-full"
            >
              <Quote className="text-blue-800 w-8 h-8 mb-4" />
              <p className="text-gray-700 text-lg italic">
                “{testimonial.quote}”
              </p>

              <div className="mt-6">
                <p className="font-semibold text-gray-900">
                  {testimonial.name}
                </p>
                <p className="text-sm text-gray-600">{testimonial.role}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
