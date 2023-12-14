import { Button } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Info } from "lucide-react";
import { cn } from "@/lib/utils";

export function InfoTooltip({
  content = "Information",
  className = "",
}: {
  content: string;
  className?: string;
}) {
  return (
    <TooltipProvider delayDuration={0}>
      <Tooltip>
        <TooltipTrigger asChild>
          <div className={cn("h-auto w-fit", className)}>
            <Info size={18} className="text-primary/80" />
          </div>
        </TooltipTrigger>
        <TooltipContent>
          <p>{content}</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
