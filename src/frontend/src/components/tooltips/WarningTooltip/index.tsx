import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { TriangleAlert } from "lucide-react";
import { cn } from "@/lib/utils";

export function WarningTooltip({
  title,
  content = "Warning",
  className = "",
  size = 18,
}: {
  title?: string;
  content: string;
  className?: string;
  size?: number;
}) {
  return (
    <TooltipProvider delayDuration={0}>
      <Tooltip>
        <TooltipTrigger asChild>
          <div className={cn("h-auto w-fit hidden md:block", className)}>
            <TriangleAlert size={size} className="text-amber-500" />
          </div>
        </TooltipTrigger>
        <TooltipContent className="max-w-lg md:text-base px-4 pt-2 pb-4 bg-amber-50 dark:bg-amber-50 dark:text-background">
          {title && <p className="font-semibold">{title}</p>}
          <p className="font-normal leading-snug">{content}</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
