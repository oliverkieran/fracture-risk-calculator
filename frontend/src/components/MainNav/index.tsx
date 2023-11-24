import { cn } from "@/lib/utils";

export default function MainNav({
  className,
  ...props
}: React.HTMLAttributes<HTMLElement>) {
  return (
    <nav
      className={cn("flex items-center space-x-4 lg:space-x-8", className)}
      {...props}
    >
      <a
        href="#"
        className="text-sm font-medium transition-colors hover:text-primary"
      >
        Overview
      </a>
      <a
        href="#"
        className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary"
      >
        How does it work?
      </a>
      <a
        href="#"
        className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary"
      >
        Settings
      </a>
    </nav>
  );
}
