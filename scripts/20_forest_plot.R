# ============================================================
# 20_forest_plot.R
# Forest plot of FM-vs-Radiomics Delta AUC with FM-tier subgroup
# annotation. Run AFTER 19_meta_analysis.R.
# ============================================================

library(metafor)
library(dplyr)

# Load saved objects from 19_meta_analysis.R
primary <- readRDS("outputs/primary_fit.rds")
ma_data <- readRDS("outputs/ma_data.rds")

# Order papers by FM tier then Delta (DPM at top, descending Delta)
ma_data <- ma_data %>%
  arrange(desc(fm_tier == "Domain-pretrained"), desc(delta))

# Rebuild model with new order
fit <- rma(yi = delta, vi = var_delta, data = ma_data,
           method = "DL", test = "knha",
           slab = paste0("P", Order, " ", substr(Title, 1, 40)))

# Subgroup-stratified pooled estimates
dpm_data    <- ma_data %>% filter(fm_tier == "Domain-pretrained")
inet_data   <- ma_data %>% filter(fm_tier == "ImageNet-CNN")
fit_dpm     <- rma(yi = delta, vi = var_delta, data = dpm_data,  method = "DL", test = "knha")
fit_inet    <- rma(yi = delta, vi = var_delta, data = inet_data, method = "DL", test = "knha")

# ------------------------------------------------------------
# PNG output (high-res)
# ------------------------------------------------------------
png("outputs/forest_plot.png",
    width = 10, height = 13, units = "in", res = 300)

forest(fit,
       xlim = c(-0.7, 0.7),
       alim = c(-0.3, 0.3),
       at = c(-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3),
       header = c("Study (PMID + short title)", "Delta AUC [95% CI]"),
       xlab = "Delta AUC (FM - Radiomics)   |   Favours Radiomics <--> Favours FM",
       refline = 0,
       cex = 0.7,
       mlab = sprintf("Pooled (random-effects DL, KHa): Delta = %.3f [%.3f, %.3f], I2 = %.0f%%, tau2 = %.4f",
                      fit$b, fit$ci.lb, fit$ci.ub, fit$I2, fit$tau2),
       ilab = cbind(sprintf("%.3f", ma_data$fm_auc),
                    sprintf("%.3f", ma_data$rad_auc),
                    ma_data$fm_tier),
       ilab.xpos = c(-0.55, -0.45, -0.30),
       ilab.lab  = c("FM AUC", "Rad AUC", "FM Tier"))

# Add subgroup pooled estimates
addpoly(fit_dpm, row = -2, mlab = sprintf("Domain-pretrained FM (n=%d): Delta = %.3f [%.3f, %.3f]",
                                          nrow(dpm_data), fit_dpm$b, fit_dpm$ci.lb, fit_dpm$ci.ub))
addpoly(fit_inet, row = -3.5, mlab = sprintf("ImageNet-CNN (n=%d): Delta = %.3f [%.3f, %.3f]",
                                              nrow(inet_data), fit_inet$b, fit_inet$ci.lb, fit_inet$ci.ub))

dev.off()

# ------------------------------------------------------------
# PDF output (vector for publication)
# ------------------------------------------------------------
pdf("outputs/forest_plot.pdf",
    width = 10, height = 13)
forest(fit, xlim = c(-0.7, 0.7), alim = c(-0.3, 0.3),
       at = c(-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3),
       header = c("Study", "Delta AUC [95% CI]"),
       xlab = "Delta AUC (FM - Radiomics)",
       refline = 0, cex = 0.7,
       mlab = sprintf("Pooled: Delta = %.3f [%.3f, %.3f], I2 = %.0f%%",
                      fit$b, fit$ci.lb, fit$ci.ub, fit$I2))
addpoly(fit_dpm,  row = -2,   mlab = sprintf("Domain-pretrained FM (n=%d)", nrow(dpm_data)))
addpoly(fit_inet, row = -3.5, mlab = sprintf("ImageNet-CNN (n=%d)", nrow(inet_data)))
dev.off()

cat("Forest plot saved:\n")
cat("  outputs/forest_plot.png\n")
cat("  outputs/forest_plot.pdf\n")
