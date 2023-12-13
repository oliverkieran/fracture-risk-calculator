import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { cn } from "@/lib/utils";

type RiskScoreProps = {
  vertebral: number;
  hip: number;
  any: number;
};

export function RiskScore({
  risks,
  riskHorizon = "2",
}: {
  risks: RiskScoreProps;
  riskHorizon: string;
}) {
  const fx_types: (keyof RiskScoreProps)[] = ["vertebral", "hip", "any"];

  const getColorClass = (risk: number) => {
    if (risk < 3) return "bg-green-400/75";
    if (risk > 10) return "bg-red-400/75";
    return "bg-amber-400/75";
  };

  return (
    <Card className="bg-accent">
      <CardHeader>
        <CardTitle>Risk Score</CardTitle>
        <CardDescription className="text-base">
          {`${riskHorizon}-year fracture risk score at different sites.`}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-3 gap-4">
          {fx_types.map((fx_type) => (
            <div
              key={fx_type}
              className={cn(
                "p-2 bg-green-400/75 rounded-md",
                getColorClass(risks[fx_type])
              )}
            >
              <p className="font-semibold">
                {fx_type.charAt(0).toUpperCase() + fx_type.slice(1)}
              </p>
              <p> {risks[fx_type]}%</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
