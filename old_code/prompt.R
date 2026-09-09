
suppressPackageStartupMessages({
    library(tidyverse)
    library(igraph)
    library(networkD3)
    library(htmlwidgets)
})

get_input <- function(prompt_text) {
  cat(prompt_text)
  line <- readLines(file("stdin"), n = 1)
  return(line)
}

data <- suppressMessages(read_csv("data.csv"))

title <- get_input("Enter book title: ")
author_yr <- get_input("Enter author (year): ")


add_ref <- TRUE

while (add_ref) {
    ref_title <- get_input("Enter reference title: ")
    ref_author_yr <- get_input("Enter reference author (year): ")
    row <- data.frame(
        source_title = title,
        source_author_yr = author_yr,
        ref_title = ref_title,
        ref_author_yr = ref_author_yr
    )

    new_data <- rbind(data, row)

    more_ans <- get_input(paste0("Enter another reference mentioned in ", title, "? (y/n)"))

    if (more_ans != "y") {
        add_ref = FALSE
    }
}

# generate visual
p <- simpleNetwork(new_data, height="100px", width="100px",        
        Source = "source_title",                 # column number of source
        Target = "ref_title",                 # column number of target
        linkDistance = 10,          # distance between node. Increase this value to have more space between nodes
        charge = -900,                # numeric value indicating either the strength of the node repulsion (negative value) or attraction (positive value)
        fontSize = 14,               # size of the node names
        fontFamily = "serif",       # font og node names
        linkColour = "#666",        # colour of edges, MUST be a common colour for the whole graph
        nodeColour = "#69b3a2",     # colour of nodes, MUST be a common colour for the whole graph
        opacity = 0.9,              # opacity of nodes. 0=transparent. 1=no transparency
        zoom = T                    # Can you zoom on the figure?
        )

# view visual?
view_ans <- get_input("View visual? (y/n)")

if (view_ans == "y") {
    saveWidget(p, file = "temp.html")
    system("open temp.html")
    readLines(file("stdin"), n = 1)
}

if (file.exists("temp.html")) {
    unlink("temp.html")
}
save_ans <- get_input("Save updated visual and dataset? (y/n)")

if (save_ans == "y") {
    write_csv(new_data, "data.csv")
    saveWidget(p, file= "viz.html")
}
