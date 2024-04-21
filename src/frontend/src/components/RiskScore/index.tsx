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
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useState } from "react";

export function SHAPDialog({
  shapURLs,
}: {
  shapURLs: {
    vertebral: string;
    hip: string;
    any: string;
  };
}) {
  const [location, setLocation] = useState("any");
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button
          type="button"
          variant="outline"
          size="icon"
          className="bg-inherit border-stone-900"
        >
          <Lightbulb size={18} className="text-foreground" />
        </Button>
      </DialogTrigger>
      <DialogContent className="w-3/4 max-w-[425px] md:max-w-[1028px] bg-white dark:bg-white">
        <DialogHeader>
          <DialogTitle className="text-black md:text-2xl">
            SHAP Waterfall Plot for{" "}
            {location.charAt(0).toUpperCase() + location.slice(1)} Fracture
          </DialogTitle>
          <DialogDescription className="text-lg flex justify-between">
            <p>
              This plot shows the contribution of each feature to the final risk
              score.
            </p>
            <div>
              <Select value={location} onValueChange={setLocation}>
                <SelectTrigger className="w-[180px] bg-white dark:bg-white text-black dark:text-black">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-white dark:bg-white text-black dark:text-black">
                  <SelectGroup>
                    <SelectLabel>Location</SelectLabel>
                    <SelectItem value="vertebral">Vertebral</SelectItem>
                    <SelectItem value="hip">Hip</SelectItem>
                    <SelectItem value="any">Any</SelectItem>
                  </SelectGroup>
                </SelectContent>
              </Select>
            </div>
          </DialogDescription>
        </DialogHeader>

        <div className="py-4">
          <img
            src={shapURLs[location as keyof typeof shapURLs]}
            alt="SHAP Waterfall Plot"
            className="w-full"
          ></img>
          {/* <img
            src={`https://stbonoai.blob.core.windows.net/shap/2024-04-21/16-09-32/${location}-shap-71926.png`}
            alt={shapURL}
            className="w-full"
          ></img> */}
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

type RiskProps = {
  risks: RiskScoreProps;
  riskHorizon: string;
  shapURLs: {
    vertebral: string;
    hip: string;
    any: string;
  };
};

export function RiskScore({ risks, riskHorizon = "2", shapURLs }: RiskProps) {
  const fx_types: (keyof RiskScoreProps)[] = ["vertebral", "hip", "any"];

  const getColorClass = (
    risk: number,
    fx_type: "vertebral" | "hip" | "any"
  ) => {
    const thresholds = {
      vertebral: {
        low: 4,
        high: 10,
      },
      hip: {
        low: 2,
        high: 8,
      },
      any: {
        low: 8,
        high: 15,
      },
    };
    if (risk < thresholds[fx_type]["low"]) return "bg-green-400/75";
    if (risk > thresholds[fx_type]["high"]) return "bg-red-400/75";
    return "bg-amber-400/75";
  };

  return (
    <Card className="bg-accent">
      <CardHeader>
        <CardTitle className="flex items-center gap-4 justify-between">
          Risk Score
          <SHAPDialog shapURLs={shapURLs} />
        </CardTitle>
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
                  getColorClass(risks[fx_type], fx_type)
                )}
              >
                <p className="font-semibold">
                  {fx_type.charAt(0).toUpperCase() + fx_type.slice(1)}
                </p>
                <p> {risks[fx_type]}%</p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
