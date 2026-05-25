suppressPackageStartupMessages({
  library(networkD3)
  library(tidyverse)
  library(htmlwidgets)
  library(webshot2)
})

df <- suppressMessages(read_csv("temp.csv"))

# put every unique book into a dataframe
nodes <- bind_rows(
  df %>% dplyr::select(title = source_title, author = source_author, year = source_year, notes = notes),
  df %>% dplyr::select(title = ref_title, author = ref_author, year = ref_year)
) %>%
  dplyr::distinct(title, .keep_all = TRUE) %>% # make sure there are no duplicates
  dplyr::mutate(
    name = title, # this is for JavaScript clickAction to recognize as the node ID
    author_year = paste0(author, " (", year, ")"), # format to author (year)
    linkNote = ifelse(is.na(notes) | notes == "", "No notes available.", as.character(notes)),
    group = ifelse(name %in% df$source_title, "Source", "Reference")  # if a title has ever been a source, group it as a source
  )

# source row number to target row number
links <- df %>%
  mutate(
    source = match(source_title, nodes$name) - 1,
    target = match(ref_title, nodes$name) - 1,
    linkNote = ifelse(is.na(notes) | notes == "", "No notes available.", as.character(notes))
  )

network <- forceNetwork(
  Links = links, Nodes = nodes,
  Source = "source", Target = "target",
  NodeID = "name", # title of book will be displayed next to its node
  Group = "group",
  linkWidth = JS("function(d) { return 2; }"),
  charge = -200,
  linkDistance = 100,
  bounded = FALSE,
  colourScale = JS('d3.scaleOrdinal().domain(["Source", "Reference"]).range(["#C22148", "#21C29A"]);'),
  fontSize = 14,
  zoom = TRUE,
  opacityNoHover = 0.9
)

# feed in the hover and popup data into the wisget
network$x$nodes$popupNote <- nodes$author_year
network$x$links$linkNote <- links$linkNote

# onRender applies JavaScript intructions after the network diagram is created
# el is the html element

network_final <- onRender(network, "
  function(el, x) {
    var tooltip = d3.select('body').append('div')
      .attr('class', 'network-tooltip')
      .style('position', 'absolute')
      .style('visibility', 'hidden')
      .style('background', 'rgba(255, 255, 255, 0.95)')
      .style('color', '#333')
      .style('border', '1px solid #e0e0e0')
      .style('padding', '12px 16px')
      .style('border-radius', '12px')
      .style('font-family', 'sans-serif')
      .style('font-size', '13px')
      .style('line-height', '1.5')
      .style('box-shadow', '0 10px 25px rgba(0,0,0,0.1)')
      .style('pointer-events', 'none')
      .style('z-index', '1000');

    var isLocked = false;

    function hideTooltip() {
      isLocked = false;
      tooltip.style('visibility', 'hidden');
      d3.selectAll('.link').style('stroke-opacity', '0.6')
    }

    d3.select(el).on('click', function() {
      hideTooltip();
    });

    d3.selectAll('.node')
      .style('cursor', 'pointer')
      .on('mouseover', function(d) {
        tooltip.style('visibility', 'visible')
          .html('<em>' + d.popupNote + '</em>');
      })
      .on('mousemove', function() {
        tooltip.style('top', (d3.event.pageY + 10) + 'px')
               .style('left', (d3.event.pageX + 10) + 'px');
      })
      .on('mouseout', function() {
        if (!isLocked) hideTooltip();
      })
      .on('click', function(d) {
        d3.event.stopPropagation();
        isLocked = true;
        tooltip.style('visibility', 'visible')
          .html('<em>' + d.popupNote + '</em>');
      });

    d3.selectAll('.link')
      .style('cursor', 'pointer')
      .on('mouseover', function(d) {
        if(!isLocked) {
          d3.select(this).style('stroke-opacity', '1');
          var source_title = d.source.name;
          var target_title = d.target.name;
          tooltip.style('visibility', 'visible')
                 .html('<strong>' + source_title + ' ➜ ' + target_title + '</strong><br>' + d.linkNote);
        }
     
      })
      .on('mousemove', function(){
        if (!isLocked) {
        tooltip.style('top', (d3.event.pageY + 10) + 'px')
               .style('left', (d3.event.pageX + 10) + 'px');
        }
      })
      .on('mouseout', function(){
        if (!isLocked) {
          d3.select(this).style('stroke-opacity', '0.6');
          hideTooltip();
        }
      })
      .on('click', function(d) {
        d3.event.stopPropagation();
        isLocked = true;
        var source_title = d.source.name;
        var target_title = d.target.name;

        d3.selectAll('.link').style('stroke-opacity', '0.2');
        d3.select(this).style('stroke-opacity', '1');
        tooltip.style('visibility', 'visible')
               .html('<strong>' + source_title + ' ➜ ' + target_title + '</strong><br>' + d.linkNote);
      });
  }
")


saveWidget(network_final, file= "temp.html")

webshot("temp.html", file = "temp_sc.png", delay = 5)
