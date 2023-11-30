import { cn } from "@/lib/utils";

export function RiskScore({ risk = -1 }: { risk: number }) {
  const display = risk === -1 ? "hidden" : "block";
  return (
    <div
      className={cn(
        "h-64 border rounded-xl px-2 pt-2 pb-4 lg:px-4 bg-secondary -text--secondary-foreground hidden",
        display
      )}
    >
      <h1 className="text-2xl font-bold">2-year Fracture Risk:</h1>
      <p>Vertebral Risk: {risk}</p>
      <p>Hip Risk: {risk}</p>
      <p>Any Risk: {risk}</p>
    </div>
  );
}
