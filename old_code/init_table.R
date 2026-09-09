# make an empty dataframe
data <- data.frame(
    source_title = character(),
    source_author_yr = character(),
    ref_title = character(),
    ref_author_yr = character()
    )

write_csv(data, "data.csv")
