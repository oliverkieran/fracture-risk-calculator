import * as z from "zod";

export type Feature = {
  id: number;
  name: string;
  description: string;
  category: "anamnesis" | "BMD" | "treatment";
  key: string;
  type: "boolean" | "number" | "array";
};

export const features: Feature[] = [
  {
    id: 1,
    name: "Hip Fracture Parents",
    description: "",
    category: "anamnesis",
    key: "hip_fracture_parents",
    type: "boolean",
  },
  {
    id: 2,
    name: "Osteoporotic Fracture Parents",
    description: "",
    category: "anamnesis",
    key: "osteoporotic_fracture_parents",
    type: "boolean",
  },
  {
    id: 3,
    name: "Corticosteroids",
    description: "≥5 mg/day for ≥3 months",
    category: "anamnesis",
    key: "corticosteroids",
    type: "boolean",
  },
  {
    id: 4,
    name: "Steroid Daily Dosage",
    description: "mg/day",
    category: "anamnesis",
    key: "steroid_daily_dosage",
    type: "number",
  },
  {
    id: 5,
    name: "Aromatase Inhibitors",
    description: "",
    category: "anamnesis",
    key: "aromatase_inhibitors",
    type: "boolean",
  },
  {
    id: 6,
    name: "Antiepileptics",
    description: "",
    category: "anamnesis",
    key: "antiepileptics",
    type: "boolean",
  },
  {
    id: 7,
    name: "Rheumatoid Arthritis",
    description: "",
    category: "anamnesis",
    key: "rheumatoid_arthritis",
    type: "boolean",
  },
  {
    id: 8,
    name: "Ankylosing Spondylitis",
    description: "",
    category: "anamnesis",
    key: "ankylosing_spondylitis",
    type: "boolean",
  },
  {
    id: 9,
    name: "Number of Falls",
    description: "Number of falls in the last 12 months.",
    category: "anamnesis",
    key: "number_of_falls",
    type: "number",
  },
  {
    id: 10,
    name: "Immobility",
    description: "Need for walking aid",
    category: "anamnesis",
    key: "immobility",
    type: "boolean",
  },
  {
    id: 11,
    name: "Type 1 Diabetes",
    description: "",
    category: "anamnesis",
    key: "type_1_diabetes",
    type: "boolean",
  },
  {
    id: 12,
    name: "COPD",
    description: "Chronic obstructive pulmonary disease",
    category: "anamnesis",
    key: "copd",
    type: "boolean",
  },
  {
    id: 13,
    name: "Gastrointestinal Disease",
    description: "",
    category: "anamnesis",
    key: "gastrointestinal_disease",
    type: "boolean",
  },
  {
    id: 14,
    name: "Early Menopause",
    description: "Menopause before 45 years old",
    category: "anamnesis",
    key: "early_menopause",
    type: "boolean",
  },
  {
    id: 15,
    name: "Hyperpara",
    description: "Primary hyperparathyroidism",
    category: "anamnesis",
    key: "hyperpara",
    type: "boolean",
  },
  {
    id: 16,
    name: "Falling Test: abnormal",
    description: "",
    category: "anamnesis",
    key: "falling_test_abnormal",
    type: "boolean",
  },
  {
    id: 17,
    name: "Alcohol",
    description: ">30g/day",
    category: "anamnesis",
    key: "alcohol",
    type: "boolean",
  },
  {
    id: 18,
    name: "Nicotin",
    description: "",
    category: "anamnesis",
    key: "nicotin",
    type: "boolean",
  },
  {
    id: 19,
    name: "Decrease in Height",
    description: "",
    category: "anamnesis",
    key: "decrease_in_height",
    type: "boolean",
  },
  {
    id: 20,
    name: "Low Back Pain",
    description: "",
    category: "anamnesis",
    key: "low_back_pain",
    type: "boolean",
  },
  {
    id: 21,
    name: "Hyperkyphosis",
    description: "",
    category: "anamnesis",
    key: "hyperkyphosis",
    type: "boolean",
  },
  {
    id: 22,
    name: "Previous Fractures",
    description: "",
    category: "anamnesis",
    key: "previous_fracture",
    type: "number",
  },
  {
    id: 23,
    name: "Recent Fractures",
    description: "Number of fractures in the last 2 years.",
    category: "anamnesis",
    key: "recent_fracture",
    type: "number",
  },
  {
    id: 24,
    name: "Femoral Neck BMD",
    description: "",
    category: "BMD",
    key: "tscore_neck",
    type: "number",
  },
  {
    id: 25,
    name: "Total Hip BMD",
    description: "",
    category: "BMD",
    key: "tscore_total_hip",
    type: "number",
  },
  {
    id: 26,
    name: "Lumbar Spine BMD",
    description: "",
    category: "BMD",
    key: "tscore_ls",
    type: "number",
  },
  {
    id: 27,
    name: "TBS",
    description: "Trabecular Bone Score",
    category: "BMD",
    key: "tbs",
    type: "number",
  },
  {
    id: 28,
    name: "Bisphosphonate",
    description: "",
    category: "treatment",
    key: "bisphosphonate",
    type: "array",
  },
  {
    id: 29,
    name: "Denosumab",
    description: "",
    category: "treatment",
    key: "denosumab",
    type: "array",
  },
  {
    id: 30,
    name: "SERM",
    description: "Selective Estrogen Receptor Modulator",
    category: "treatment",
    key: "serm",
    type: "array",
  },
  {
    id: 31,
    name: "Teriparatide",
    description: "",
    category: "treatment",
    key: "teriparatide",
    type: "array",
  },
  {
    id: 32,
    name: "HRT",
    description: "Hormone Replacement Therapy",
    category: "treatment",
    key: "hrt",
    type: "array",
  },
];

export const FormSchema = z
  .object({
    sex: z.string().startsWith("female", {
      message: "Bono is currently only available for female patients.",
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
    hip_fracture_parents: z.boolean().default(false).optional(),
    osteoporotic_fracture_parents: z.boolean().default(false).optional(),
    corticosteroids: z.boolean().default(false).optional(),
    steroid_daily_dosage: z.coerce
      .number()
      .min(0, {
        message: "Steroid daily dosage must be greater or equal to 0.",
      })
      .max(100, { message: "Steroid daily dosage must be less than 100." })
      .default(0)
      .optional(),
    aromatase_inhibitors: z.boolean().default(false).optional(),
    antiepileptics: z.boolean().default(false).optional(),
    rheumatoid_arthritis: z.boolean().default(false).optional(),
    ankylosing_spondylitis: z.boolean().default(false).optional(),
    number_of_falls: z.coerce.number().min(0).max(100).default(0).optional(),
    immobility: z.boolean().default(false).optional(),
    type_1_diabetes: z.boolean().default(false).optional(),
    copd: z.boolean().default(false).optional(),
    gastrointestinal_disease: z.boolean().default(false).optional(),
    early_menopause: z.boolean().default(false).optional(),
    hyperpara: z.boolean().default(false).optional(),
    falling_test_abnormal: z.boolean().default(false).optional(),
    alcohol: z.boolean().default(false).optional(),
    nicotin: z.boolean().default(false).optional(),
    decrease_in_height: z.boolean().default(false).optional(),
    low_back_pain: z.boolean().default(false).optional(),
    hyperkyphosis: z.boolean().default(false).optional(),
    previous_fracture: z.coerce.number().min(0).max(20).default(0),
    recent_fracture: z.coerce.number().min(0).max(10).default(0),
    tscore_neck: z.coerce
      .number({ invalid_type_error: "Enter a T-score." })
      .min(-10)
      .max(10),
    tscore_total_hip: z.coerce
      .number({ invalid_type_error: "Enter a T-score." })
      .min(-10)
      .max(10),
    tscore_ls: z.coerce
      .number({ invalid_type_error: "Enter a T-score." })
      .min(-10)
      .max(10),
    tbs: z.coerce.number({ invalid_type_error: "Enter a TBS." }).min(0).max(2),
    bisphosphonate_prior: z.boolean().default(false).optional(),
    bisphosphonate_current: z.boolean().default(false).optional(),
    bisphosphonate_new: z.boolean().default(false).optional(),
    denosumab_prior: z.boolean().default(false).optional(),
    denosumab_current: z.boolean().default(false).optional(),
    denosumab_new: z.boolean().default(false).optional(),
    serm_prior: z.boolean().default(false).optional(),
    serm_current: z.boolean().default(false).optional(),
    serm_new: z.boolean().default(false).optional(),
    teriparatide_prior: z.boolean().default(false).optional(),
    teriparatide_current: z.boolean().default(false).optional(),
    teriparatide_new: z.boolean().default(false).optional(),
    hrt_prior: z.boolean().default(false).optional(),
    hrt_current: z.boolean().default(false).optional(),
    hrt_new: z.boolean().default(false).optional(),
  })
  .refine((data) => data.previous_fracture >= data.recent_fracture, {
    message: "Previous fractures must be greater than recent fractures.",
  });

export const formDefaultValues = {
  sex: "female",
  age: 65,
  height: 160,
  weight: 60,
  hip_fracture_parents: false,
  osteoporotic_fracture_parents: false,
  corticosteroids: false,
  steroid_daily_dosage: 0,
  aromatase_inhibitors: false,
  antiepileptics: false,
  rheumatoid_arthritis: false,
  ankylosing_spondylitis: false,
  number_of_falls: 0,
  immobility: false,
  type_1_diabetes: false,
  copd: false,
  gastrointestinal_disease: false,
  early_menopause: false,
  hyperpara: false,
  falling_test_abnormal: false,
  alcohol: false,
  nicotin: false,
  decrease_in_height: false,
  low_back_pain: false,
  hyperkyphosis: false,
  previous_fracture: 0,
  recent_fracture: 0,
  tscore_neck: -2,
  tscore_total_hip: -2,
  tscore_ls: -2,
  tbs: 1.3,
  bisphosphonate_prior: false,
  bisphosphonate_current: false,
  bisphosphonate_new: false,
  denosumab_prior: false,
  denosumab_current: false,
  denosumab_new: false,
  serm_prior: false,
  serm_current: false,
  serm_new: false,
  teriparatide_prior: false,
  teriparatide_current: false,
  teriparatide_new: false,
  hrt_prior: false,
  hrt_current: false,
  hrt_new: false,
};
