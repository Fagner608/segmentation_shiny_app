# #libraryes and environment variables
# source("./modules/libraryes.R")
# 
# ## funções auxiliares
# source("./modules/funcoes_auxiliares.R")
# 
# ## Acesso aos dados
# source("./modules/dataWrangling.R")
# 
# #carregando dados
# retorno_get_data <- get_data()
# 
# ##aqui são os dados mensais
# # ribbon_chart <- rfm_score_table_ribon_chart # usado na função viz_ribon
# ribbon_chart <- my_rfm_function(retorno_get_data$dados_mensais)
# 
# 
# ## aqui são os dados agrupados - inserir lat, lon
# # data_chart <- segment_data_analitcs
# 
# data_chart <- my_rfm_function(retorno_get_data$dados_agrupados)
# 
# data_map <- data_chart
# 
# ## resumo do analitcs
# segment_chart <- summary_rfm_table(data_chart)
# 



monitoring_status <- function(rfm_score_table_ribon_chart, date_input, segment_scores){
  #segment_scores  <-  c("Champions")
  #date_input <- '2025-03-03'
  #rfm_score_table_ribon_chart <- ribbon_chart
  
  
  date_search <- format(as.Date(date_input, format = '%Y-%m-%d'), '%Y-%m')
  #month_search <- month(as.Date(date_input, format = '%Y-%m-%d'))
  
  early_month <- format(ym(date_search) %m-% months(1), "%Y-%m")
  
  segment_names <- c("Champions", "Loyal Customers", "Potential Loyalist",
                     "New Customers", "Promising", "Need Attention", "About To Sleep",
                     "At Risk", "Can't Lose Them", "Lost", 'No Segment')
  
  
  
  early_segment <- rfm_score_table_ribon_chart %>%
    filter(date == early_month) %>%
    select(id_corretor, early_month = segment)
  
  
  ids_segment <- rfm_score_table_ribon_chart %>%
    filter(date == date_search,
           segment %in% segment_scores) %>%
    distinct(id_corretor, date, segment) %>%
    left_join(early_segment, by = 'id_corretor')
  
  ids_segment[is.na(ids_segment$early_month), "early_month"] = 'No Segment'
  ids_segment[is.na(ids_segment$segment), "segment"] = 'No Segment'
  
  
  ids_segment$early_month <- factor(ids_segment$early_month, levels = segment_names, ordered = TRUE)
  ids_segment$segment <- factor(ids_segment$segment, levels = segment_names, ordered = TRUE)
  
  ids_segment$status <- ifelse(ids_segment$segment < ids_segment$early_month, 'Segmento promovido', 
                               ifelse(ids_segment$segment == ids_segment$early_month, 'Acompanhar', 'Atuar'))
  

  vector_ids <- paste(na.omit(ids_segment$id_corretor), collapse = ',')
  
  
  query <- glue("
        select cor.*
        
        from public.corretor cor
        where cor.\"id_corretor\" IN ({vector_ids})
    
    ")
  
  
  # executando query
  con = con_function()
  retorno_query <- dbGetQuery(con, query)
  # desconectando com DB
  dbDisconnect(con)
  
  merge_final <- merge(retorno_query, ids_segment, by = 'id_corretor')
  
  head(merge_final)
  
  dados_mapa <- merge_final
  
  data_filtred <- merge_final[, c('nome_corretor', 'numero_corretor', 'early_month', 'segment', 'status')]
  
  
  
  
  
  colnames(data_filtred) <- c("Parceiro", 'Código storm', "Status anterior", "Status Atual", "Recomendação")
  merge_final <- merge_final %>% rename(
    parceiro = nome_corretor,
    status_anterior = early_month,
    status_atual = segment,
    recomendacao = status
  )

  
  dados_mapa <- dados_mapa[dados_mapa$lat != 46.3144754 & dados_mapa$lon != 11.04803, ]
  
  
  
  brasil <- map_data("world", region = "Brazil")
  
  
  grafico_map <- ggplot() +
    geom_polygon(data = brasil, aes(x = long, y = lat, group = group), fill = "white", color = "black") +
    
    #geom_point(data = dados_mapa[dados_mapa$status == "Acompanhar", ], aes(x = lon, y = lat, color = as.factor(segment)), size = 3) +
    #geom_point(data = dados_mapa[dados_mapa$status != "Acompanhar", ], aes(x = lon, y = lat), color = '#FF9999', size = 2) +
    geom_point(data = dados_mapa[dados_mapa$status == "Acompanhar", ], aes(x = lon, y = lat), color = 'red', size = 3, alpha= .25) +
    geom_point(data = dados_mapa[dados_mapa$status == "Atuar", ], aes(x = lon, y = lat), color = 'red', size = 3, alpha= .75) +
    
    geom_point(data = dados_mapa[dados_mapa$status == "Segmento promovido", ], aes(x = lon, y = lat, color = as.factor(segment)), size = 2) +
    
    scale_color_manual(values = segment_color_map) + 
    
    
        labs(title = "Decaimento do status - painel de sensibilidade",
         x = "",
         y = "",
         color = "RFM Score") +
    
    theme_minimal() +
    
    guides(fill = FALSE) + 
  
    theme(axis.text = element_blank(), axis.ticks = element_blank())
  
    ggplotly(grafico_map, tooltip = 'all')
  
  return(list(data_filtred = data_filtred, 
              merge_final = merge_final,
              mapa = grafico_map))

  }

