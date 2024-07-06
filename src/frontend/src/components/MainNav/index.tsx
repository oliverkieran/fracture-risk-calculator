import { cn } from "@/lib/utils";
import { useState } from "react";
import { Menu } from "lucide-react";
import { ModeToggle } from "@/components/Theme/mode-toggle";

export default function MainNav({
  className,
  ...props
}: React.HTMLAttributes<HTMLElement>) {
  const [state, setState] = useState(false);

  const menus = [
    { title: "Home", path: "/" },
    // { title: "How does it work?", path: "/" },
    { title: "Contact", path: "/contact" },
  ];
  return (
    <nav
      className={cn(
        `bg-white dark:bg-background w-full ${
          state
            ? "bg-primary/20 rounded-b-3xl border-b-indigo-200 pb-4"
            : "bg-white"
        }`,
        className
      )}
      {...props}
    >
      <div className="items-center px-4 max-w-screen-xl mx-auto md:flex md:px-8">
        <div className="flex items-center justify-between py-3 md:py-5 md:block">
          <a href="/">
            <h1 className="text-2xl font-bold mr-auto text-foreground">
              Bono AI
            </h1>
          </a>
          <div className="md:hidden">
            <button
              className="text-gray-700 outline-none p-2 rounded-md focus:border-gray-400 focus:border"
              onClick={() => setState(!state)}
            >
              <Menu />
            </button>
          </div>
        </div>
        <div
          className={`flex-1 justify-self-center pb-3 mt-4 md:block md:pb-0 md:mt-0 ${
            state ? "block" : "hidden"
          }`}
        >
          <ul className="justify-center items-center space-y-8 md:flex md:space-x-6 md:space-y-0">
            {menus.map((item, idx) => (
              <li
                key={idx}
                className="text-gray-600 font-medium transition-colors hover:text-primary"
              >
                <a href={item.path}>{item.title}</a>
              </li>
            ))}
          </ul>
        </div>
        <ModeToggle />
      </div>
    </nav>
  );
}
