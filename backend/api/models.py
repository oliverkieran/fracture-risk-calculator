from django.db import models


class Patient(models.Model):
    sex = models.CharField(
        choices=[("female", "female"), ("male", "male")], max_length=10
    )
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    bmi = models.FloatField(blank=True, null=True)
    hip_fracture_parents = models.BooleanField()
    osteoporotic_fracture_parents = models.BooleanField()
    corticosteroids = models.BooleanField()
    steroid_daily_dosage = models.IntegerField()
    aromatase_inhibitors = models.BooleanField()
    antiepileptics = models.BooleanField()
    rheumatoid_arthritis = models.BooleanField()
    ankylosing_spondylitis = models.BooleanField()
    number_of_falls = models.IntegerField()
    immobility = models.BooleanField()
    type_1_diabetes = models.BooleanField()
    copd = models.BooleanField()
    gastrointestinal_disease = models.BooleanField()
    early_menopause = models.BooleanField()
    hyperpara = models.BooleanField()
    malfunction_of_kidney = models.BooleanField()
    alcohol = models.BooleanField()
    nicotin = models.BooleanField()
    decrease_in_height = models.BooleanField()
    low_back_pain = models.BooleanField()
    hyperkyphosis = models.BooleanField()
    previous_fracture = models.IntegerField()
    recent_fracture = models.IntegerField()
    tscore_neck = models.FloatField()
    tscore_total_hip = models.FloatField()
    tscore_ls = models.FloatField()
    tbs = models.FloatField()
    bisphosphonate_prior = models.BooleanField()
    bisphosphonate_current = models.BooleanField()
    bisphosphonate_new = models.BooleanField()
    denosumab_prior = models.BooleanField()
    denosumab_current = models.BooleanField()
    denosumab_new = models.BooleanField()
    serm_prior = models.BooleanField()
    serm_current = models.BooleanField()
    serm_new = models.BooleanField()
    teriparatide_prior = models.BooleanField()
    teriparatide_current = models.BooleanField()
    teriparatide_new = models.BooleanField()
    hrt_prior = models.BooleanField()
    hrt_current = models.BooleanField()
    hrt_new = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
