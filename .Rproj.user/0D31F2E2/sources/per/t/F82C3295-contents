
con_function <- function(){
  
    con  = DBI::dbConnect(
    RPostgres::Postgres(),
    host = Sys.getenv("DB_HOST"),
    dbname = Sys.getenv("DB_NAME"),
    user = Sys.getenv("DB_USER"),
    password = Sys.getenv("DB_PASSWORD"),
    port = 5432,
    sslmode = "require" 
    )

  return(con)
}

# Definir um vetor de cores fixas mapeado para os segmentos
segment_labels <- c(
  "Loyal Customers", 
  "At Risk", 
  "About To Sleep", 
  "Need Attention", 
  "Lost", 
  "Potential Loyalist", 
  "Champions", 
  "Others", 
  NA
)


fixed_colors <- c(
  "#66c2a5",  # Loyal Customers
  "#fc8d62",  # At Risk
  "#cccccc",  # About To Sleep
  "#8da0cb",  # Need Attention
  "#FF7F7F",  # Lost
  "#a6d854",  # Potential Loyalist
  "#E6A8D7",  # Champions
  "#e5c494",  # Others
  "#b3b3b3"   # NA (sem segmento)
)

segment_color_map <- setNames(fixed_colors, segment_labels)

viz_map <- function(data_map, label = NULL){
  
  if(!is.null(label)){data_map  = data_map %>% filter(segment == label)}
  
  data_map <- data_map[data_map$lat != 46.3144754 & data_map$lon != 11.04803, ]
  
  brasil <- map_data("world", region = "Brazil")
  
  grafico_map <- ggplot() +
    geom_polygon(data = brasil, aes(x = long, y = lat, group = group), fill = "white", color = "black") +
    
    geom_point(data = data_map, aes(x = lon, y = lat, color = as.factor(segment)), size = 2) + 
    
    scale_color_manual(values = segment_color_map) +
    
    labs(title = "Distribuição dos parceiros com RFM Score",
         x = "",
         y = "",
         color = "RFM Score") +
    
    theme_minimal() +
    theme(axis.text = element_blank(), axis.ticks = element_blank())
  
  
  ggplotly(grafico_map, tooltip = 'all')
  
}


plot_partiner <- function(parceiro_dados, partiner){
  
  #partiner <- 'Julice Evelyn Paulo'
  parceiro <- partiner
  #parceiro_dados <- ribbon_chart
  data_wide <- parceiro_dados[grepl(parceiro, parceiro_dados$customer_id, ignore.case = T) | 
                              grepl(parceiro, parceiro_dados$id_storm, ignore.case = T), c("customer_id", "date", "recencia", "segment")]
  
  data_wide <- data_wide %>% 
    pivot_wider(
      id_cols = customer_id,
      names_from = date,
      values_from = segment
    )
  
  
  
  
  data_wide_log <- data_wide %>%
    make_long(colnames(data_wide)[colnames(data_wide) != 'customer_id'])
  
  head(data_wide)
  
  
  viz <- ggplot(data_wide_log, aes(x = x, 
                                   next_x = next_x, 
                                   node = node, 
                                   next_node = next_node,
                                   fill = node)) +
    geom_sankey() +
    theme_sankey(base_size = 12) +  # Apenas um base_size
    scale_fill_manual(values = segment_color_map) +
    scale_x_discrete(labels = function(x) gsub('segment', "", x)) +
    labs(fill = "Segmentos", title = "Trajetória do parceiro", x = "Mês") +
    #labs(fill = "Segmentos") +
    theme(
      plot.title = element_text(size = 14),
      axis.text = element_text(size = 10),
      axis.title = element_text(size = 12),
      legend.title = element_text(size = 10),
      legend.text = element_text(size = 8),
      plot.margin = margin(50, 50 ,50 ,50)
    )
  
  ggplotly(viz, tooltip = c("text", "size"))
  
  
}


viz_ribbon <- function(data, label = NULL, segment = NULL){
  
  
  data_wide <- data[, c("customer_id","date", "recencia", "segment")]
  data_wide <- data_wide %>% 
    pivot_wider(
      id_cols = customer_id,
      names_from = date,
      values_from = segment
    )
  
  if (!is.null(segment) && !is.null(label)) {
    
    data_wide <- data_wide[data_wide[[colnames(data_wide)[2]]] %in% label, ]
    
    
  } else if (!is.null(segment) && is.null(label)) {
    stop("Informe o label do segmento")
  } else if (is.null(segment) && !is.null(label)) {
    stop("Para segmentar, deve informar True no argumento segment")
  }
  
  
  data_wide_log <- data_wide %>%
    make_long(colnames(data_wide)[colnames(data_wide) != 'customer_id'])
  
  segment_order <- c(
    "Champions", 
    "Loyal Customers", 
    "Potential Loyalist",
    "New Customers", 
    "Promising", 
    "Need Attention", 
    "About To Sleep",
    "At Risk", 
    "Can't Lose Them", 
    "Lost", 
    "Others",
    "No Segment",
    NA
  )
  
  

  data_wide_log <- data_wide_log %>%
    mutate(node = factor(node, levels = segment_order, exclude = NULL) %>% 
             fct_explicit_na(na_level = "No Segment"),
           next_node = factor(next_node, levels = segment_order, exclude = NULL) %>%
             fct_explicit_na(na_level = "No Segment"))
  
  viz <- ggplot(data_wide_log, aes(x = x, 
                                   next_x = next_x, 
                                   node = node, 
                                   next_node = next_node,
                                   fill = node)) +
    geom_sankey() +
    theme_sankey(base_size = 12) +  # Apenas um base_size
    scale_fill_manual(values = segment_color_map) +
    scale_x_discrete(labels = function(x) gsub('segment', "", x)) +
    labs(fill = "Segmentos", title = paste("Fluxo dos clientes que iniciaram com status: ", label), x = "Mês") + 
    theme(
      plot.title = element_text(size = 14),
      axis.text = element_text(size = 10),
      axis.title = element_text(size = 12),
      legend.title = element_text(size = 10),
      legend.text = element_text(size = 8)
    )
  
  ggplotly(viz, tooltip = c("text", "size"))
  
}



####
my_rfm_function <- function(rfm_score_table_ribon_chart){
  
  # Classificando segmentos
  segment_names <- c("Champions", "Loyal Customers", "Potential Loyalist",
                     "New Customers", "Promising", "Need Attention", "About To Sleep",
                     "At Risk", "Can't Lose Them", "Lost")
  
  recency_lower   <- c(4, 2, 3, 4, 3, 2, 2, 1, 1, 1)
  recency_upper   <- c(5, 5, 5, 5, 4, 3, 3, 2, 1, 2)
  frequency_lower <- c(4, 3, 1, 1, 1, 2, 1, 2, 4, 1)
  frequency_upper <- c(5, 5, 3, 1, 1, 3, 2, 5, 5, 2)
  monetary_lower  <- c(4, 3, 1, 1, 1, 2, 1, 2, 4, 1)
  monetary_upper  <- c(5, 5, 3, 1, 1, 3, 2, 5, 5, 2)
  
  
  n_segments <- length(segment_names)
  
  rfm_score_table_ribon_chart$segment <- NA
  
  for (i in seq_len(n_segments)) {
    
    rfm_score_table_ribon_chart$segment[((rfm_score_table_ribon_chart$recency_score %>% 
                                            
                                            between(recency_lower[i], recency_upper[i])) & (rfm_score_table_ribon_chart$frequency_score %>% 
                                                                                              
                                                                                              between(frequency_lower[i], frequency_upper[i])) & 
                                           
                                           (rfm_score_table_ribon_chart$monetary_score %>% between(monetary_lower[i],
                                                                                                   
                                                                                                   monetary_upper[i])) & !rfm_score_table_ribon_chart$segment %in% 
                                           
                                           segment_names)] <- segment_names[i]
    
  }
  
  rfm_score_table_ribon_chart$segment[is.na(rfm_score_table_ribon_chart$segment)] <- "Others"
  
  rfm_score_table_ribon_chart$segment[rfm_score_table_ribon_chart$segment == 1] <- "Others"
  
  return(rfm_score_table_ribon_chart)
  
}

## resumo da rfm_table
summary_rfm_table <- function(rfm_table){
  
  rfm_table <- rfm_table %>% group_by(segment) %>% summarise(customer_id = n(), 
                                                orders = sum(frequencia), revenue = sum(monetary_log)) %>% 
    mutate(aov = round((revenue/orders), 2))
  
  
  
  rfm_table <- rfm_table %>%
    mutate(
      definicao = 
        case_when(
          segment == "About To Sleep" ~ 'Parceiros que estão prestes a se tornar inativos. Eles podem ter digitado recentemente, mas a frequência de sua digitação está diminuindo, e se não forem incentivados, poderão deixar de digitar novamente.',
          segment == "Need Attention" ~ 'parceiros que são regulares, mas apresentam sinais de desinteresse. Eles podem ter diminuído a frequência de digitação, mas ainda são valiosos',
          segment == "At Risk" ~ 'Parceiros que costumavam digitar regularmente, mas sua recência diminuiu significativamente. Esses parceiros não digitam há um tempo, mas ainda têm um histórico de digitação significativo.',
          segment == "Lost" ~ 'Parceiros que têm um histórico de digitação passado, mas que não digitaram há muito tempo. Eles são parceiros que desapareceram e não interagem mais com a empresa.',
          segment == "Potential Loyalist" ~ 'Parceiros que têm potencial para se tornar leais, mas ainda não atingiram a frequência ou valor monetário dos “Loyal Customers”. Eles digitam com certa regularidade, mas têm potencial para se tornar mais valiosos.',
          segment == "Others" ~ 'Este é um segmento genérico que abrange parceiros que não se encaixam bem em nenhum dos outros grupos. Pode incluir parceiros que não se encaixam em termos de recência, frequência ou valor monetário de forma consistente.',
          segment == "Loyal Customers" ~ 'Parceiros que digitam frequentemente, mas não geram tanto quanto os “Champions”. Eles são fiéis à empresa, mas não estão no topo em termos de volume de receita.',
          segment == "Champions" ~ 'São os melhores parceiros. Eles digitam com frequência, geram muito dinheiro e têm um bom histórico de digitação recentes. Esses parceiros são altamente leais.'
        )
      
    )
  
  
  rfm_table <- rfm_table %>%
    mutate(
      recomendacao = 
        case_when(
          segment == "About To Sleep" ~ 'Ação de reengajamento urgente, como promoções especiais ou lembretes para manter o parceiro engajado.',
          segment == "Need Attention" ~ 'Interações personalizadas, como e-mails ou ofertas, para lembrar os parceiros do valor da empresa e incentivá-los a continuar comprando.',
          segment == "At Risk" ~ 'Oferecer promoções personalizadas ou descontos para tentar trazê-los de volta antes que se tornem inativos completamente.',
          segment == "Lost" ~ 'Estratégias de reconquista, como campanhas de reengajamento ou ofertas direcionadas.',
          segment == "Potential Loyalist" ~ 'Estímulos para incentivá-los a digitar mais frequentemente, como recompensas de fidelidade ou incentivos adicionais.',
          segment == "Others" ~ 'Análise mais aprofundada para tentar identificar o comportamento desses parceiros e encontrar maneiras de engajá-los.',
          segment == "Loyal Customers" ~ 'Propor ações de fidelização, como comissões especiais para grandes lotes de digitação ou incentivos para aumentar o valor das propostas.',
          segment == "Champions" ~ 'Focar em programas de fidelidade e recompensas para manter esse grupo de parceiros feliz e incentivá-los a continuar comprando.'
        )
      
    )
  
  
  return(rfm_table)
  
  
}

# 
# monitoring_status <- function(rfm_score_table_ribon_chart, date_input, segment_scores){
#   #segment_scores  <-  c("Champions")
#   #date_input <- '2025-03-03'
#   #rfm_score_table_ribon_chart <- ribbon_chart
#   
#   
#   date_search <- format(as.Date(date_input, format = '%Y-%m-%d'), '%Y-%m')
#   #month_search <- month(as.Date(date_input, format = '%Y-%m-%d'))
#   
#   early_month <- format(ym(date_search) %m-% months(1), "%Y-%m")
#   
#   segment_names <- c("Champions", "Loyal Customers", "Potential Loyalist",
#                      "New Customers", "Promising", "Need Attention", "About To Sleep",
#                      "At Risk", "Can't Lose Them", "Lost", 'No Segment')
#   
#   
#   
#   early_segment <- rfm_score_table_ribon_chart %>%
#     filter(date == early_month) %>%
#     select(id_corretor, early_month = segment)
#   
#   
#   ids_segment <- rfm_score_table_ribon_chart %>%
#     filter(date == date_search,
#            segment %in% segment_scores) %>%
#     distinct(id_corretor, date, segment) %>%
#     left_join(early_segment, by = 'id_corretor')
#   
#   ids_segment[is.na(ids_segment$early_month), "early_month"] = 'No Segment'
#   ids_segment[is.na(ids_segment$segment), "segment"] = 'No Segment'
#   
#   
#   ids_segment$early_month <- factor(ids_segment$early_month, levels = segment_names, ordered = TRUE)
#   ids_segment$segment <- factor(ids_segment$segment, levels = segment_names, ordered = TRUE)
#   
#   ids_segment$status <- ifelse(ids_segment$segment < ids_segment$early_month, 'Segmento promovido', 'Acompanhar')
#   
#   is.na(ids_segment$id_corretor)
#   
#   vector_ids <- paste(na.omit(ids_segment$id_corretor), collapse = ',')
#   
#   
#   query <- glue("
#         select cor.*
#         
#         from public.corretor cor
#         where cor.\"id_corretor\" IN ({vector_ids})
#     
#     ")
#   
#   
#   # executando query
#   con = con_function()
#   retorno_query <- dbGetQuery(con, query)
#   # desconectando com DB
#   dbDisconnect(con)
#   
#   merge_final <- merge(retorno_query, ids_segment, by = 'id_corretor')
#   
#   
#   
#   data_filtred <- merge_final[, c('nome_corretor', 'numero_corretor', 'early_month', 'segment', 'status')]
#   
#   
#   
#   
#   
#   colnames(data_filtred) <- c("Parceiro", 'Código storm', "Status anterior", "Status Atual", "Recomendação")
#   merge_final <- merge_final %>% rename(
#     parceiro = nome_corretor,
#     status_anterior = early_month,
#     status_atual = segment,
#     recomendacao = status
#   )
#   
#   
#   
#   
#   
#   
#   return(list(data_filtred = data_filtred, merge_final = merge_final))
# }





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


