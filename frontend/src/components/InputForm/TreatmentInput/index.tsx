import * as React from "react";
import * as CheckboxPrimitive from "@radix-ui/react-checkbox";
import {
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form";
import { Feature } from "@/components/InputForm/schema.ts";

import { cn } from "@/lib/utils";

const TreatmentCheckbox = React.forwardRef<
  React.ElementRef<typeof CheckboxPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof CheckboxPrimitive.Root>
>(({ className, ...props }, ref) => {
  return (
    <CheckboxPrimitive.Root
      ref={ref}
      className={cn(
        "peer h-10 w-32 shrink-0 border border-slate-200 ring-offset-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-950 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary/90 data-[state=checked]:text-slate-50 dark:border-slate-800 dark:ring-offset-slate-950 dark:focus-visible:ring-slate-300 dark:data-[state=checked]:bg-slate-50 dark:data-[state=checked]:text-slate-900",
        className
      )}
      {...props}
    >
      {props.name}
    </CheckboxPrimitive.Root>
  );
});

export function TreatmentInput({
  form,
  feature,
  treatment,
}: {
  form: any;
  feature: Feature;
  treatment: "Prior" | "Current" | "New";
}) {
  const featureKey = `${feature.key}_${treatment.toLowerCase()}`;
  let buttonStyle = "";
  switch (treatment) {
    case "Prior":
      buttonStyle = "rounded-l-xl";
      break;
    case "New":
      buttonStyle = "rounded-r-xl";
      break;
  }
  return (
    <FormField
      control={form.control}
      name={featureKey}
      render={({ field }) => (
        <FormItem className="w-32">
          <FormControl>
            <div className="flex items-center space-x-2 py-1">
              <TreatmentCheckbox
                className={`${buttonStyle}`}
                name={treatment}
                checked={field.value as boolean}
                onCheckedChange={field.onChange}
              />
            </div>
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
  );
}
