#!/usr/bin/env Rscript
# Example usage of pt-deputados data in R

library(arrow)
library(dplyr)

df <- read_parquet("data/deputies.parquet")

cat(sprintf("Total deputies: %d
", nrow(df)))

# Filter by party
psd <- df %>% filter(party == "PSD")
cat(sprintf("PSD deputies: %d
", nrow(psd)))
