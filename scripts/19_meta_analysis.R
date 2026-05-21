# ============================================================
# 19_meta_analysis.R
# Random-effects meta-analysis of FM-vs-Radiomics Delta AUC
# PROSPERO CRD420261393443
# ============================================================
#
# Inputs:  ./12_Final_Included_Corpus.csv
# Outputs: outputs/meta_analysis_results.csv
#          outputs/subgroup_summary.csv
#
# Methodology:
# - Hanley-McNeil SE(AUC) per arm (assumes balanced classes when prevalence NR)
# - Delta AUC variance: SE_FM^2 + SE_Rad^2 (independent-arms assumption -> conservative)
# - Random-effects pooling: DerSimonian-Laird estimator
# - Knapp-Hartung adjustment for small-sample CI
# - Subgroups: FM tier, modality, task type, validation status
# - Sensitivity: low-ROB only, high-RQS only, externally-validated only,
#                exclude weak-Rad-arm (Rad AUC < 0.60), AUC-only
# ============================================================

library(metafor)
library(dplyr)
library(readr)

# ------------------------------------------------------------
# 1. Load corpus
# ------------------------------------------------------------
corpus <- read_csv("./12_Final_Included_Corpus.csv",
                   show_col_types = FALSE,
                   locale = locale(encoding = "UTF-8"))

cat("Loaded", nrow(corpus), "papers\n")
cat("Columns:", paste(colnames(corpus), collapse = ", "), "\n\n")

# ------------------------------------------------------------
# 2. Build analysis dataframe with derived columns
# ------------------------------------------------------------
# Convert cohort sizes to numeric (handle "NR", "—", "~350" patterns)
parse_n <- function(x) {
  x <- gsub("[~—]", "", as.character(x))
  x <- gsub("NR|^$", "0", x)
  suppressWarnings(as.numeric(x))
}

corpus <- corpus %>%
  mutate(
    n_train    = parse_n(Cohort_Train),
    n_int_test = parse_n(Cohort_Internal_Test),
    n_ext_test = parse_n(Cohort_External_Test),
    # Primary test cohort: external if available, else internal
    n_test = ifelse(n_ext_test > 0, n_ext_test, n_int_test),
    fm_auc  = as.numeric(FM_Arm_Value),
    rad_auc = as.numeric(Rad_Arm_Value),
    delta   = as.numeric(Metric_Difference),
    # FM tier from FM_Pretraining
    fm_tier = case_when(
      grepl("BiomedCLIP|CLIP|RadImageNet|MedicalNet|PMC-15M|MedSAM", FM_Pretraining, ignore.case = TRUE) ~ "Domain-pretrained",
      grepl("ImageNet", FM_Pretraining, ignore.case = TRUE) ~ "ImageNet-CNN",
      TRUE ~ "Other/Unclear"
    )
  )

# ------------------------------------------------------------
# 3. Hanley-McNeil SE(AUC) per arm
# ------------------------------------------------------------
# Assumes 50/50 class balance when paper doesn't report prevalence.
# Total test n is used; positives = negatives = n_test/2.
hanley_mcneil_se <- function(auc, n_test, prevalence = 0.5) {
  if (is.na(auc) || is.na(n_test) || n_test < 10) return(NA_real_)
  n_pos <- round(n_test * prevalence)
  n_neg <- n_test - n_pos
  if (n_pos < 2 || n_neg < 2) return(NA_real_)
  q1 <- auc / (2 - auc)
  q2 <- 2 * auc^2 / (1 + auc)
  var_auc <- (auc * (1 - auc) + (n_pos - 1) * (q1 - auc^2) + (n_neg - 1) * (q2 - auc^2)) / (n_pos * n_neg)
  sqrt(var_auc)
}

corpus <- corpus %>%
  rowwise() %>%
  mutate(
    se_fm  = hanley_mcneil_se(fm_auc, n_test),
    se_rad = hanley_mcneil_se(rad_auc, n_test),
    se_delta = sqrt(se_fm^2 + se_rad^2),  # independent-arms assumption
    var_delta = se_delta^2,
    ci_lo = delta - 1.96 * se_delta,
    ci_hi = delta + 1.96 * se_delta
  ) %>%
  ungroup()

# Drop papers without sufficient data for meta-analysis
ma_data <- corpus %>% filter(!is.na(delta), !is.na(se_delta))
cat("Papers eligible for meta-analysis:", nrow(ma_data), "/ 28\n")
cat("Papers excluded (insufficient SE data):\n")
print(corpus %>% filter(is.na(se_delta)) %>% select(Order, PMID, Title, fm_auc, rad_auc, n_test))
cat("\n")

# ------------------------------------------------------------
# 4. Primary random-effects meta-analysis
# ------------------------------------------------------------
cat("\n=== PRIMARY ANALYSIS: All eligible papers (random-effects DL, Knapp-Hartung) ===\n")
primary <- rma(yi = delta, vi = var_delta, data = ma_data,
               method = "DL", test = "knha", slab = paste0("P", Order, " (", PMID, ")"))
print(primary)

# ------------------------------------------------------------
# 5. Subgroup analyses
# ------------------------------------------------------------
run_subgroup <- function(data, var, label) {
  cat("\n=== SUBGROUP:", label, "===\n")
  groups <- split(data, data[[var]])
  results <- lapply(names(groups), function(g) {
    d <- groups[[g]]
    if (nrow(d) < 2) {
      cat(" ", g, ": n =", nrow(d), "(too few for pooling)\n")
      return(NULL)
    }
    fit <- rma(yi = delta, vi = var_delta, data = d, method = "DL", test = "knha")
    cat(sprintf("  %-25s n=%2d   Delta=%+.4f [%+.4f, %+.4f]   I2=%.1f%%   p=%.4f\n",
                g, nrow(d), fit$b, fit$ci.lb, fit$ci.ub, fit$I2, fit$pval))
    data.frame(subgroup_var = var, group = g, n = nrow(d),
               pooled_delta = as.numeric(fit$b), ci_lo = fit$ci.lb, ci_hi = fit$ci.ub,
               I2 = fit$I2, tau2 = fit$tau2, p_value = fit$pval)
  })
  do.call(rbind, results)
}

sg_tier <- run_subgroup(ma_data, "fm_tier", "FM tier (Domain-pretrained vs ImageNet-CNN)")
sg_mod  <- run_subgroup(ma_data, "Modality", "Modality")
sg_task <- run_subgroup(ma_data, "Clinical_Task", "Clinical task (full string — narrative)")
sg_val  <- run_subgroup(ma_data, "External_Validation", "External validation (YES/NO)")
sg_rob  <- run_subgroup(ma_data, "PROBAST_Rating", "PROBAST Overall ROB")

# ------------------------------------------------------------
# 6. Sensitivity analyses
# ------------------------------------------------------------
cat("\n=== SENSITIVITY ANALYSES ===\n")

run_sensitivity <- function(data, condition, label) {
  d <- data[condition, ]
  if (nrow(d) < 3) {
    cat(sprintf("  %-40s n=%2d (underpowered — narrative)\n", label, nrow(d)))
    return(NULL)
  }
  fit <- rma(yi = delta, vi = var_delta, data = d, method = "DL", test = "knha")
  cat(sprintf("  %-40s n=%2d   Delta=%+.4f [%+.4f, %+.4f]   I2=%.1f%%\n",
              label, nrow(d), fit$b, fit$ci.lb, fit$ci.ub, fit$I2))
  data.frame(analysis = label, n = nrow(d),
             pooled_delta = as.numeric(fit$b), ci_lo = fit$ci.lb, ci_hi = fit$ci.ub,
             I2 = fit$I2, tau2 = fit$tau2, p_value = fit$pval)
}

sens1 <- run_sensitivity(ma_data, ma_data$External_Validation == "YES", "Externally-validated only")
sens2 <- run_sensitivity(ma_data, as.numeric(ma_data$RQS_Score) >= 12, "High-RQS only (>=12)")
sens3 <- run_sensitivity(ma_data, ma_data$PROBAST_Rating != "High", "Low/Unclear PROBAST only")
sens4 <- run_sensitivity(ma_data, ma_data$rad_auc >= 0.60, "Exclude weak-Rad-arm (Rad AUC >=0.60)")
sens5 <- run_sensitivity(ma_data, ma_data$FM_Arm_Metric == "AUC", "AUC-only (exclude C-index)")
sens6 <- run_sensitivity(ma_data, ma_data$fm_tier == "Domain-pretrained", "Domain-pretrained FM only")
sens7 <- run_sensitivity(ma_data, ma_data$fm_tier == "ImageNet-CNN", "ImageNet-CNN only")

# ------------------------------------------------------------
# 7. Save per-paper results + summary tables
# ------------------------------------------------------------
dir.create("outputs", showWarnings = FALSE)

per_paper <- ma_data %>%
  select(Order, PMID, Title, Modality, fm_tier, fm_auc, rad_auc, delta,
         se_fm, se_rad, se_delta, ci_lo, ci_hi, n_test, External_Validation,
         RQS_Score, CLAIM_Score, PROBAST_Rating)
write_csv(per_paper, "outputs/meta_analysis_results.csv")

subgroup_all <- bind_rows(sg_tier, sg_mod, sg_val, sg_rob,
                          sens1, sens2, sens3, sens4, sens5, sens6, sens7)
write_csv(subgroup_all, "outputs/subgroup_summary.csv")

# Save primary fit object for reuse by forest plot script
saveRDS(primary, "outputs/primary_fit.rds")
saveRDS(ma_data, "outputs/ma_data.rds")

cat("\n=== Outputs written ===\n")
cat("  outputs/meta_analysis_results.csv  (per-paper SE/CI)\n")
cat("  outputs/subgroup_summary.csv       (subgroup + sensitivity)\n")
cat("  outputs/primary_fit.rds            (for forest plot script)\n")
cat("  outputs/ma_data.rds                (for forest plot script)\n")
cat("\nDone. Run 20_forest_plot.R next.\n")
