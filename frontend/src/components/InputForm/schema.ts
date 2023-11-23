import * as z from "zod";

const features = [
  {
    id: 0,
    name: "HRT",
    description: "Hormone replacement therapy",
    category: "anamnesis",
    key: "hrt",
  },
  {
    id: 1,
    name: "Hip Fracture Parents",
    description: "Hip fracture in parents",
    category: "anamnesis",
    key: "hip_fracture_parents",
  },
  {
    id: 2,
    name: "Osteoporotic Fracture Parents",
    description: "Osteoporotic fracture in parents",
    category: "anamnesis",
    key: "osteoporotic_fracture_parents",
  },
  {
    id: 3,
    name: "Corticosteroids",
    description: "",
    category: "anamnesis",
    key: "corticosteroids",
  },
  {
    id: 4,
    name: "Steroid Daily Dosage",
    description: "",
    category: "anamnesis",
    key: "steroid_daily_dosage",
  },
  {
    id: 5,
    name: "Aromatase Inhibitors",
    description: "",
    category: "anamnesis",
    key: "aromatase_inhibitors",
  },
  {
    id: 6,
    name: "Antiepileptics",
    description: "",
    category: "anamnesis",
    key: "antiepileptics",
  },
  {
    id: 7,
    name: "Rheumatoid Arthritis",
    description: "",
    category: "anamnesis",
    key: "rheumatoid_arthritis",
  },
  {
    id: 8,
    name: "Ankylosing Spondylitis",
    description: "",
    category: "anamnesis",
    key: "ankylosing_spondylitis",
  },
  {
    id: 9,
    name: "Number of Falls",
    description: "",
    category: "anamnesis",
    key: "number_of_falls",
  },
  {
    id: 10,
    name: "Immobility",
    description: "",
    category: "anamnesis",
    key: "immobility",
  },
  {
    id: 11,
    name: "Type 1 Diabetes",
    description: "",
    category: "anamnesis",
    key: "type_1_diabetes",
  },
  {
    id: 12,
    name: "COPD",
    description: "",
    category: "anamnesis",
    key: "copd",
  },
  {
    id: 13,
    name: "Gastrointestinal Disease",
    description: "",
    category: "anamnesis",
    key: "gastrointestinal_disease",
  },
  {
    id: 14,
    name: "Early Menopause",
    description: "",
    category: "anamnesis",
    key: "early_menopause",
  },
  {
    id: 15,
    name: "Hyperpara",
    description: "",
    category: "anamnesis",
    key: "hyperpara",
  },
  {
    id: 16,
    name: "Malfunction of Kidney",
    description: "",
    category: "anamnesis",
    key: "malfunction_of_kidney",
  },
  {
    id: 17,
    name: "Alcohol",
    description: "",
    category: "anamnesis",
    key: "alcohol",
  },
  {
    id: 18,
    name: "Nicotin",
    description: "",
    category: "anamnesis",
    key: "nicotin",
  },
  {
    id: 19,
    name: "Decrease in Height",
    description: "",
    category: "anamnesis",
    key: "decrease_in_height",
  },
  {
    id: 20,
    name: "Low Back Pain",
    description: "",
    category: "anamnesis",
    key: "low_back_pain",
  },
  {
    id: 21,
    name: "Hyperkyphosis",
    description: "",
    category: "anamnesis",
    key: "hyperkyphosis",
  },
  {
    id: 22,
    name: "Previous Fracture",
    description: "",
    category: "anamnesis",
    key: "previous_fracture",
  },
  {
    id: 23,
    name: "Recent Fracture",
    description: "A fracture in the last 2 years.",
    category: "anamnesis",
    key: "recent_fracture",
  },
  {
    id: 24,
    name: "Femoral Neck BMD",
    description: "",
    category: "BMD",
    key: "tscore_neck",
  },
  {
    id: 25,
    name: "Total Hip BMD",
    description: "",
    category: "BMD",
    key: "tscore_total_hip",
  },
  {
    id: 26,
    name: "Lumbar Spine BMD",
    description: "",
    category: "BMD",
    key: "tscore_ls",
  },
  {
    id: 27,
    name: "TBS",
    description: "Trabecular Bone Score",
    category: "BMD",
    key: "tbs",
  },
  {
    id: 28,
    name: "Bisphosphonates",
    description: "",
    category: "treatment",
    key: "bisphosphonates",
  },
  {
    id: 29,
    name: "Denosumab",
    description: "",
    category: "treatment",
    key: "denosumab",
  },
  {
    id: 30,
    name: "SERM",
    description: "Selective Estrogen Receptor Modulator",
    category: "treatment",
    key: "serm",
  },
  {
    id: 31,
    name: "Teriparatide",
    description: "",
    category: "treatment",
    key: "teriparatide",
  },
  {
    id: 32,
    name: "HRT",
    description: "Hormone Replacement Therapy",
    category: "treatment",
    key: "hrt",
  },
];

const FormSchema = z.object({
  sex: z.string().startsWith("female", {
    message: "Amelia is currently only available for female patients.",
  }),
  age: z.coerce
    .number()
    .min(0, { message: "Patient must be older than 40 years old." })
    .max(120, { message: "Patient must be younger than 120 years old." }),
  height: z.coerce
    .number()
    .min(50, { message: "Height must be greater than 50." })
    .max(225, { message: "Height must be less than 225." }),
  weight: z.coerce
    .number()
    .min(20, { message: "Height must be greater than 20." })
    .max(400, { message: "Height must be less than 400." }),
  hrt: z.boolean().default(false).optional(),
  tscore_neck: z.coerce
    .number({ invalid_type_error: "Please enter a T-score." })
    .min(-10)
    .max(10),
  tscore_total_hip: z.coerce
    .number({ invalid_type_error: "Please enter a T-score." })
    .min(-10)
    .max(10),
  tscore_ls: z.coerce
    .number({ invalid_type_error: "Please enter a T-score." })
    .min(-10)
    .max(10),
  tbs: z.coerce
    .number({ invalid_type_error: "Please enter a TBS." })
    .min(0)
    .max(2),
});

const formDefaultValues = {
  sex: "female",
  age: 65,
  height: 160,
  weight: 60,
};

export { FormSchema, formDefaultValues, features };
