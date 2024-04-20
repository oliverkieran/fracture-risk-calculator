"use client";

import { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import axios from "axios";

import { Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardHeader,
  CardDescription,
  CardTitle,
  CardContent,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { Switch } from "@/components/ui/switch";
import { cn } from "@/lib/utils";
import toast from "react-hot-toast";

import { FormSchema, formDefaultValues, features } from "./schema";
import { RiskScore } from "@/components/RiskScore";
import { TreatmentInput } from "@/components/InputForm/TreatmentInput";
import { InfoTooltip } from "@/components/InfoTooltip";

export function InputForm() {
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: formDefaultValues,
  });

  const anamnesisBooleanFeatures = features.filter(
    (feature) => feature.category === "anamnesis" && feature.type === "boolean"
  );
  const anamnesisNumberFeatures = features.filter(
    (feature) => feature.category === "anamnesis" && feature.type === "number"
  );
  const tscoreFeatures = features.filter(
    (feature) => feature.category === "BMD"
  );
  const treatmentFeatures = features.filter(
    (feature) => feature.category === "treatment"
  );

  const [height, weight] = form.watch(["height", "weight"]);
  const bmi = (weight / (height / 100) ** 2).toFixed(2);

  const [riskHorizion, setRiskHorizon] = useState("2");

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [risks, setRisks] = useState({ vertebral: -1, hip: -1, any: -1 });
  function onSubmit(data: z.infer<typeof FormSchema>) {
    console.log("Sending data to backend:", data);
    setIsSubmitting(true);

    const requestData = {
      riskHorizon: riskHorizion,
      patientData: data,
    };

    // send data to api
    axios({
      method: "post",
      url: "/api/getRisk",
      data: requestData,
    }).then((response) => {
      console.log("Received response from backend:", response.data);
      const computedRisks = response.data.risks;
      setRisks(computedRisks);
      setIsSubmitting(false);
    });
  }

  function onSubmitErrors(errors: object) {
    console.error(errors);
    toast.error("Recent fractures cannot be greater than previous fractures.");
  }

  return (
    <div className="border border-border rounded-xl w-full max-w-5xl p-4">
      <h1 className="text-3xl font-bold text-foreground py-4 lg:px-2">
        Fracture Risk Calculator
      </h1>
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit, onSubmitErrors)}
          className="w-full space-y-6"
        >
          <div className="space-y-4 md:flex md:gap-4 md:space-y-0 p-2 bg-card -text--card-foreground">
            <FormField
              control={form.control}
              name="sex"
              render={({ field }) => (
                <FormItem className="w-56">
                  <FormLabel>Sex</FormLabel>
                  <Select
                    onValueChange={field.onChange}
                    defaultValue={field.value}
                  >
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="female" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      <SelectItem value="female">female</SelectItem>
                      <SelectItem value="male">male</SelectItem>
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />
            <div className="flex md:flex-none gap-4">
              <FormField
                control={form.control}
                name="age"
                render={({ field }) => (
                  <FormItem className="w-20">
                    <FormLabel>Age</FormLabel>
                    <FormControl>
                      <Input type="number" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="height"
                render={({ field }) => (
                  <FormItem className="w-20">
                    <FormLabel>Height</FormLabel>
                    <FormControl>
                      <Input type="number" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="weight"
                render={({ field }) => (
                  <FormItem className="w-20">
                    <FormLabel>Weight</FormLabel>
                    <FormControl>
                      <Input type="number" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            <div className="flex items-center space-x-2 rounded-md bg-primary/20 dark:bg-primary/80 px-3 border border-border h-14 w-32 md:h-auto ">
              <Label>BMI:</Label>
              <p className="text-sm">{bmi}</p>
            </div>
          </div>
          <Separator className="my-4" />
          <div className="md:flex space-x-2 lg:space-x-4 space-y-4 md:space-y-0">
            <Card className="md:w-1/2">
              <CardHeader>
                <CardTitle>Anamnesis</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="grid grid-cols-2">
                    {anamnesisNumberFeatures.map((feature) => (
                      <FormField
                        control={form.control}
                        key={feature.id}
                        name={
                          feature.key as
                            | "steroid_daily_dosage"
                            | "number_of_falls"
                            | "previous_fracture"
                            | "recent_fracture"
                        }
                        render={({ field }) => (
                          <FormItem className="mb-2">
                            <div className="flex items-center">
                              <FormLabel className="mr-2">
                                {feature.name}
                              </FormLabel>
                              {feature.description !== "" && (
                                <InfoTooltip content={feature.description} />
                              )}
                            </div>
                            <FormControl>
                              <Input
                                type="number"
                                className="w-20"
                                {...field}
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    ))}
                  </div>
                  {anamnesisBooleanFeatures.map((feature) => (
                    <FormField
                      control={form.control}
                      key={feature.id}
                      name={
                        feature.key as
                          | "hip_fracture_parents"
                          | "osteoporotic_fracture_parents"
                          | "corticosteroids"
                          | "aromatase_inhibitors"
                          | "antiepileptics"
                          | "rheumatoid_arthritis"
                          | "ankylosing_spondylitis"
                          | "immobility"
                          | "type_1_diabetes"
                          | "copd"
                          | "gastrointestinal_disease"
                          | "early_menopause"
                          | "hyperpara"
                          | "falling_test_abnormal"
                          | "alcohol"
                          | "nicotin"
                          | "decrease_in_height"
                          | "low_back_pain"
                          | "hyperkyphosis"
                      }
                      render={({ field }) => (
                        <FormItem className="w-32">
                          <FormControl>
                            <div className="flex items-center space-x-2 py-1">
                              <Switch
                                checked={field.value as boolean}
                                onCheckedChange={field.onChange}
                              />
                              <Label className="text-base whitespace-nowrap">
                                {feature.name}
                              </Label>
                              {feature.description !== "" && (
                                <InfoTooltip content={feature.description} />
                              )}
                            </div>
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  ))}
                </div>
              </CardContent>
            </Card>
            <div className="md:w-1/2 space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Bone Density Measurements</CardTitle>
                  <CardDescription className="text-base">
                    All values should be entered as T-scores.
                  </CardDescription>
                </CardHeader>
                <CardContent className="grid grid-cols-2">
                  {tscoreFeatures.map((feature) => (
                    <FormField
                      control={form.control}
                      key={feature.id}
                      name={
                        feature.key as
                          | "tscore_neck"
                          | "tscore_total_hip"
                          | "tscore_ls"
                          | "tbs"
                      }
                      render={({ field }) => (
                        <FormItem className="w-32 mb-2">
                          <FormLabel>{feature.name}</FormLabel>
                          <FormControl>
                            <Input type="number" step="0.1" {...field} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  ))}
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Treatment History</CardTitle>
                </CardHeader>
                <CardContent>
                  {treatmentFeatures.map((feature) => (
                    <div key={feature.id} className="mb-2">
                      <h2 className="text-base font-medium mb-0.5">
                        {feature.name}
                      </h2>
                      <div className="flex">
                        <TreatmentInput
                          form={form}
                          feature={feature}
                          treatment="Prior"
                        />
                        <TreatmentInput
                          form={form}
                          feature={feature}
                          treatment="Current"
                        />
                        <TreatmentInput
                          form={form}
                          feature={feature}
                          treatment="New"
                        />
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
              {risks.any >= 0 && (
                <RiskScore
                  risks={risks}
                  riskHorizon={riskHorizion}
                  shapPath="/path/to/s3-bucket"
                />
              )}
            </div>
          </div>

          <Separator className="my-4" />
          <div className="flex items-end justify-between px-2 pb-4 bg-card -text--card-foreground">
            <div className="space-y-2">
              <Label>Time horizon</Label>
              <Select onValueChange={setRiskHorizon}>
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Select a time horizon" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1">1 year</SelectItem>
                  <SelectItem value="2">2 years</SelectItem>
                  <SelectItem value="3">3 years</SelectItem>
                  <SelectItem value="4">4 years</SelectItem>
                  <SelectItem value="5">5 years</SelectItem>
                  <SelectItem value="6">6 years</SelectItem>
                  <SelectItem value="7">7 years</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button
              type="submit"
              className="bg-primary hover:bg-blue-700"
              disabled={isSubmitting}
            >
              <Loader2
                className={cn(
                  "mr-2 h-4 w-4 animate-spin",
                  isSubmitting ? "block" : "hidden"
                )}
              />
              Compute Risk
            </Button>
          </div>
        </form>
      </Form>
    </div>
  );
}
