import { Button } from "../ui/button";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Lightbulb } from "lucide-react";
import { cn } from "@/lib/utils";

export function SHAPDialog({ fxType = "any" }: { fxType?: string }) {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button type="button" variant="outline" size="icon">
          <Lightbulb size={18} className="text-foreground" />
        </Button>
      </DialogTrigger>
      <DialogContent className="w-3/4 max-w-[425px] md:max-w-[1028px] bg-white dark:bg-white">
        <DialogHeader>
          <DialogTitle className="text-black md:text-2xl">
            SHAP Waterfall Plot for{" "}
            {fxType.charAt(0).toUpperCase() + fxType.slice(1)} Fracture
          </DialogTitle>
          <DialogDescription className="text-lg">
            This plot shows the contribution of each feature to the final risk
            score.
          </DialogDescription>
        </DialogHeader>
        <div className="py-4">
          <img
            src="https://fracture-risk.s3.eu-central-1.amazonaws.com/shap-plots/2024/01/03/shapPlot.png"
            alt="SHAP Waterfall Plot"
            className="w-full"
          ></img>
        </div>
      </DialogContent>
    </Dialog>
  );
}

type RiskScoreProps = {
  vertebral: number;
  hip: number;
  any: number;
};

export function RiskScore({
  risks,
  riskHorizon = "2",
  shapPath,
}: {
  risks: RiskScoreProps;
  riskHorizon: string;
  shapPath: string;
}) {
  const fx_types: (keyof RiskScoreProps)[] = ["vertebral", "hip", "any"];

  const getColorClass = (risk: number) => {
    if (risk < 3) return "bg-green-400/75";
    if (risk > 10) return "bg-red-400/75";
    return "bg-amber-400/75";
  };

  console.log(shapPath);

  return (
    <Card className="bg-accent">
      <CardHeader>
        <CardTitle>Risk Score</CardTitle>
        <CardDescription className="text-base">
          {`${riskHorizon}-year fracture risk score at different sites.`}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-3 gap-4">
          {fx_types.map((fx_type) => (
            <div key={fx_type} className="space-y-3">
              <div
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
              <SHAPDialog fxType={fx_type} />
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
