"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Form,
  FormControl,
  FormDescription,
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
import { toast } from "@/components/ui/use-toast";
import { FormSchema, formDefaultValues, features } from "./schema";

export function InputForm() {
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: formDefaultValues,
  });

  const anamnesisFeatures = features.filter(
    (feature) => feature.category === "anamnesis"
  );
  const tscoreFeatures = features.filter(
    (feature) => feature.category === "BMD"
  );
  const treatmentList = features
    .filter((feature) => feature.category === "treatment")
    .map((feature) => <li key={feature.id}>{feature.name}</li>);

  const [height, weight] = form.watch(["height", "weight"]);
  const bmi = (weight / (height / 100) ** 2).toFixed(2);

  function onSubmit(data: z.infer<typeof FormSchema>) {
    console.log("data", data);
    toast({
      title: "You submitted the following values:",
      description: (
        <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
          <code className="text-white">{JSON.stringify(data, null, 2)}</code>
        </pre>
      ),
    });
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="w-full space-y-6">
        <div className="flex gap-4 p-2">
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
          <div className="flex items-center space-x-2 rounded-md w-32 bg-primary/20 px-3 border border-slate-200">
            <Label>BMI:</Label>
            <p className="text-sm">{bmi}</p>
          </div>
        </div>
        <Separator className="my-4" />
        <div className="flex space-x-2 lg:space-x-4">
          <div className="w-1/2 border rounded-xl p-2 lg:px-4">
            <h1 className="text-2xl font-bold mb-2">Anamnesis</h1>
            <div className="space-y-2">
              {anamnesisFeatures.map((feature) => (
                <FormField
                  control={form.control}
                  key={feature.id}
                  name="hrt"
                  render={({ field }) => (
                    <FormItem className="w-32">
                      <FormControl>
                        <div className="flex items-center space-x-2 py-1">
                          <Switch
                            checked={field.value}
                            onCheckedChange={field.onChange}
                          />
                          <Label className="text-base whitespace-nowrap">
                            {feature.name}
                          </Label>
                        </div>
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              ))}
            </div>
          </div>
          <div className="w-1/2 space-y-4">
            <div className="h-fit border rounded-xl px-2 pt-2 pb-4 lg:px-4">
              <h1 className="text-2xl font-bold mb-2">
                Bone Density Measurements
              </h1>
              <div>
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
                      <FormItem className="w-32">
                        <FormLabel>{feature.name}</FormLabel>
                        <FormControl>
                          <Input type="number" step="0.1" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                ))}
              </div>
            </div>
            <div className="h-fit border rounded-xl px-2 pt-2 pb-4 lg:px-4">
              <h1 className="text-2xl font-bold">Treatment History</h1>
              <ul>{treatmentList}</ul>
            </div>
          </div>
        </div>

        <Separator className="my-4" />
        <Button type="submit" className="bg-primary hover:bg-blue-700">
          Compute Risk
        </Button>
      </form>
    </Form>
  );
}
