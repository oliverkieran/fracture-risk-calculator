export type FormSchemaType = {
  sex: string;
  age: number;
  height: number;
  weight: number;
  hip_fracture_parents?: boolean;
  osteoporotic_fracture_parents?: boolean;
  corticosteroids?: boolean;
  steroid_daily_dosage?: number;
  aromatase_inhibitors?: boolean;
  antiepileptics?: boolean;
  rheumatoid_arthritis?: boolean;
  ankylosing_spondylitis?: boolean;
  number_of_falls?: number;
  immobility?: boolean;
  type_1_diabetes?: boolean;
  copd?: boolean;
  gastrointestinal_disease?: boolean;
  early_menopause?: boolean;
  hyperpara?: boolean;
  falling_test_abnormal?: boolean;
  alcohol?: boolean;
  nicotin?: boolean;
  decrease_in_height?: boolean;
  low_back_pain?: boolean;
  hyperkyphosis?: boolean;
  previous_fracture: number;
  recent_fracture: number;
  tscore_neck: number;
  tscore_total_hip: number;
  tscore_ls: number;
  tbs: number;
  bisphosphonate_prior?: boolean;
  bisphosphonate_current?: boolean;
  bisphosphonate_new?: boolean;
  denosumab_prior?: boolean;
  denosumab_current?: boolean;
  denosumab_new?: boolean;
  serm_prior?: boolean;
  serm_current?: boolean;
  serm_new?: boolean;
  teriparatide_prior?: boolean;
  teriparatide_current?: boolean;
  teriparatide_new?: boolean;
  hrt_prior?: boolean;
  hrt_current?: boolean;
  hrt_new?: boolean;
};