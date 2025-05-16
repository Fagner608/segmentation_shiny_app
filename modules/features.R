
#libraryes and environment variables
source("./modules/libraryes.R")

## funções auxiliares
source("./modules/funcoes_auxiliares.R")

## Acesso aos dados
source("./modules/dataWrangling.R")

# testando nova feature
# source("./modules/features.R")

#carregando dados
retorno_get_data <- get_data()

##aqui são os dados mensais
# ribbon_chart <- rfm_score_table_ribon_chart # usado na função viz_ribon
ribbon_chart <- my_rfm_function(retorno_get_data$dados_mensais)

data_chart <- my_rfm_function(retorno_get_data$dados_agrupados)
head(data_chart)
data_map <- data_chart


#segment_scores  <-  c("Champions")
#date_input <- '2025-03-03'
#rfm_score_table_ribon_chart <- ribbon_chart
dados2 <- monitoring_status(ribbon_chart,
                           '2025-03-03',
                           'Need Attention')




data_2 <- dados2$merge_final
data_map_2 <- data_2[, c("status_anterior", "status_atual", "lat", "lon")]


#######################
# viz_map <- function(data_map, label = NULL){
#   
#   if(!is.null(label)){data_map  = data_map %>% filter(status_atual == label)}
#   data_map <- data_map[data_map$lat != 46.3144754 & data_map$lon != 11.04803, ]
#   brasil <- map_data("world", region = "Brazil")
#   
#   segment_names <- c("Champions", "Loyal Customers", "Potential Loyalist",
#                      "New Customers", "Promising", "Need Attention", "About To Sleep",
#                      "At Risk", "Can't Lose Them", "Lost")
#   
#   data_map$status_atual <- factor(data_map$status_atual, levels = segment_names, ordered = TRUE)
#   data_map$status_anterior <- factor(data_map$status_anterior, levels = segment_names, ordered = TRUE)
#   
#   plot_1 <- data_map[data_map$status_atual < data_map$status_anterior ,]
#   print("plot1")
#   print(dim(data_map))
#   
#   
#   plot_2 <- data_map
#   
#   
#   grafico_map <- ggplot() +
#     geom_polygon(data = brasil, aes(x = long, y = lat, group = group), fill = "white", color = "black") +
#     
#     geom_point(data = plot_1, aes(x = lon, y = lat, color = as.factor(status_atual)), size = 3) +
#     
#     
#     geom_point(data = plot_2, aes(x = lon, y = lat, color = as.factor(status_atual)), size = 2) +
#   
#     
#     
#     scale_color_manual(values = segment_color_map) +
#     
#     labs(title = "Distribuição dos parceiros com RFM Score",
#          x = "",
#          y = "",
#          color = "RFM Score") +
#     
#     theme_minimal() +
#     theme(axis.text = element_blank(), axis.ticks = element_blank())
#   
#   
#   ggplotly(grafico_map, tooltip = 'all')
#   
# }
# 

viz_map_teste <- function(data_map, label = NULL){
  
  if(!is.null(label)){data_map  = data_map %>% filter(status_atual == label)}
  data_map <- data_map[data_map$lat != 46.3144754 & data_map$lon != 11.04803, ]
  brasil <- map_data("world", region = "Brazil")
  
  segment_names <- c("Champions", "Loyal Customers", "Potential Loyalist",
                     "New Customers", "Promising", "Need Attention", "About To Sleep",
                     "At Risk", "Can't Lose Them", "Lost")
  
  data_map$status_atual <- factor(data_map$status_atual, levels = segment_names, ordered = TRUE)
  data_map$status_anterior <- factor(data_map$status_anterior, levels = segment_names, ordered = TRUE)
  
  plot_1 <- data_map[data_map$status_atual < data_map$status_anterior ,]
  print("plot1")
  print(dim(data_map))
  
  plot_2 <- data_map
  
  # Paleta de cores em tons de vermelho
  #plot_1_colors <- c("red3", "darkred", "firebrick1", "firebrick4", "salmon")
  
  # Agora, modificando o gráfico com a nova escala de cores
  grafico_map <- ggplot() +
    geom_polygon(data = brasil, aes(x = long, y = lat, group = group), fill = "white", color = "black") +
    
    geom_point(data = plot_1, aes(x = lon, y = lat), color = '#FF9999', size = 5) +
    
    geom_point(data = plot_2, aes(x = lon, y = lat, color = as.factor(status_atual)), size = 2) +
    
    #scale_color_manual(values = plot_1_colors) +  # Aplicando os tons de vermelho
    
    labs(title = "Decaimento do status - painel de sensibilidade",
         x = "",
         y = "",
         color = "RFM Score") +
    
    theme_minimal() +
    theme(axis.text = element_blank(), axis.ticks = element_blank())
  
  ggplotly(grafico_map, tooltip = 'all')
  
}

viz_map(data_map_2, label = 'Need Attention')
 