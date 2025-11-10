#!/usr/bin/env Rscript

# Set working directory
setwd("C:/Users/benke/devEnv/llmproc/coding_batches/batch7/batch6_vs_batch7")

# Load required libraries
library(coin)  # For permutation tests

# Open output file for writing results
output_file <- "batch_comparison_results.txt"
sink(output_file)

cat("IMPORTANT NOTE!!!\nThis analysis compares batch 6 (pre-study-period) with batch 7 (study period) which is not the same as comparing pre-study-period with study period, because (1) batch 7 was balanced to quotas and batch 6 was not; (2) implementation of owe-specific shifted a bit between the two (this latter factor probably not very important). We get some indication of changes from this analysus but it isn't watertight.\n\n")

# 1. Read in the files
cat("Reading files...\n")

human_coding <- read.delim(
  "Article Characteristics Coding v4c (Responses) - Short column names.tsv",
  sep = "\t",
  header = TRUE,
  stringsAsFactors = FALSE
)

batch6 <- read.delim(
  "batch6_llm_screening.tsv",
  sep = "\t",
  header = TRUE,
  stringsAsFactors = FALSE
)

batch7 <- read.delim(
  "../batch7_quota_screening.tsv",
  sep = "\t",
  header = TRUE,
  stringsAsFactors = FALSE
)

cat("Files read successfully.\n\n")

# 2. Process article IDs
# Strip "_original.html" suffix from human coding IDs
human_coding$id_cleaned <- sub("_original\\.html$", "", human_coding$id)

# Get the included batch 6 articles (those in human coding file)
included_batch6_ids <- human_coding$id_cleaned

# Verify all human coding IDs are present in batch 6
missing_ids <- setdiff(included_batch6_ids, batch6$ID)
if (length(missing_ids) > 0) {
  stop("ERROR: The following article IDs from human coding are not present in batch 6 file:\n",
       paste(missing_ids, collapse = "\n"))
}

cat("All human coding article IDs found in batch 6 file.\n\n")

# Filter batch 6 to included articles
batch6_included <- batch6[batch6$ID %in% included_batch6_ids, ]

cat("Batch 6 included articles:", nrow(batch6_included), "\n")

# 3. Filter batch 7 to included articles (PASSES_SCREENING_SPECIFIC == "Yes")
batch7_included <- batch7[batch7$PASSES_SCREENING_SPECIFIC == "Yes", ]

cat("Batch 7 included articles:", nrow(batch7_included), "\n")

# Get word counts for original versions only
# Note: R converts "Word count" to "Word.count" when reading the file
batch6_wordcounts <- batch6_included$Word.count[batch6_included$Version == "original"]
batch7_wordcounts <- batch7_included$Word.count[batch7_included$Version == "original"]

cat("Number of included articles:\n")
cat("  Batch 6:", length(batch6_wordcounts), "\n")
cat("  Batch 7:", length(batch7_wordcounts), "\n\n")

# 4. Summary statistics
cat(paste(rep("=", 70), collapse=""), "\n")
cat("SUMMARY STATISTICS - ORIGINAL VERSION WORD COUNTS\n")
cat(paste(rep("=", 70), collapse=""), "\n\n")

print_summary <- function(data, label) {
  cat(label, "\n")
  cat("  Mean:   ", mean(data, na.rm = TRUE), "\n")
  cat("  Median: ", median(data, na.rm = TRUE), "\n")
  cat("  SD:     ", sd(data, na.rm = TRUE), "\n")
  cat("  Min:    ", min(data, na.rm = TRUE), "\n")
  cat("  Max:    ", max(data, na.rm = TRUE), "\n")
  cat("  Q1:     ", quantile(data, 0.25, na.rm = TRUE), "\n")
  cat("  Q3:     ", quantile(data, 0.75, na.rm = TRUE), "\n")
  cat("  N:      ", sum(!is.na(data)), "\n")
  cat("  NA:     ", sum(is.na(data)), "\n\n")
}

print_summary(batch6_wordcounts, "Batch 6 (Included Articles)")
print_summary(batch7_wordcounts, "Batch 7 (PASSES_SCREENING_SPECIFIC == Yes)")

# 5. Permutation test
cat(paste(rep("=", 70), collapse=""), "\n")
cat("PERMUTATION TEST (Two-Sample)\n")
cat(paste(rep("=", 70), collapse=""), "\n\n")

# Prepare data for permutation test
combined_data <- data.frame(
  word_count = c(batch6_wordcounts, batch7_wordcounts),
  batch = factor(c(rep("Batch 6", length(batch6_wordcounts)),
                   rep("Batch 7", length(batch7_wordcounts))))
)

# Perform permutation test using coin package (Wilcoxon-Mann-Whitney test)
perm_test <- wilcox_test(word_count ~ batch, data = combined_data,
                         distribution = "approximate")

cat("Wilcoxon-Mann-Whitney Permutation Test\n")
cat("Null hypothesis: No difference in word count distributions\n\n")
print(perm_test)

cat("\n")
cat("Test statistic (Z):", statistic(perm_test), "\n")
cat("P-value:           ", pvalue(perm_test), "\n")

# Additional effect size measure
mean_diff <- mean(batch6_wordcounts, na.rm = TRUE) - mean(batch7_wordcounts, na.rm = TRUE)
cat("\nMean difference (Batch 6 - Batch 7):", mean_diff, "\n")

cat("\n")
cat(paste(rep("=", 70), collapse=""), "\n")
cat("Analysis complete.\n")
cat("Results saved to:", output_file, "\n")

# Close the output file
sink()

# Also print to console that analysis is complete
cat("\nAnalysis complete. Results saved to:", output_file, "\n")