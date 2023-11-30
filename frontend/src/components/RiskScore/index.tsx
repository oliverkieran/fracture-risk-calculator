import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";

export function RiskScore({ risk = -1 }: { risk: number }) {
  const fx_types = ["vertebral", "hip", "any"];
  return (
    <Card className="bg-accent">
      <CardHeader>
        <CardTitle>Risk Score</CardTitle>
        <CardDescription className="text-base">
          2-year fracture risk score at different sites.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-3 gap-4">
          {fx_types.map((fx_type) => (
            <div key={fx_type} className="p-2 bg-green-400/75 rounded-md">
              <p className="font-semibold">
                {fx_type.charAt(0).toUpperCase() + fx_type.slice(1)}
              </p>
              <p> {risk}</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
