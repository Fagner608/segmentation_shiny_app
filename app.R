options(warn = -1)

#libraryes and environment variables
source("./modules/libraryes.R")

## funções auxiliares
source("./modules/funcoes_auxiliares.R")

## Acesso aos dados
source("./modules/dataWrangling.R")

#carregando dados
retorno_get_data <- get_data()

##aqui são os dados mensais
# ribbon_chart <- rfm_score_table_ribon_chart # usado na função viz_ribon
ribbon_chart <- my_rfm_function(retorno_get_data$dados_mensais)


## aqui são os dados agrupados - inserir lat, lon
# data_chart <- segment_data_analitcs

data_chart <- my_rfm_function(retorno_get_data$dados_agrupados)

data_map <- data_chart

## resumo do analitcs
segment_chart <- summary_rfm_table(data_chart)



ui <- fluidPage(
  # Application title
  titlePanel("Acompanhamento de segmentação"),
  
  sidebarLayout(
    sidebarPanel(
      width = 2,  
      selectInput("segmento",
                  "Escolha o segmento que deseja filtrar:",
                  choices = c(
                    "About To Sleep", 
                    "Need Attention", 
                    "At Risk",
                    "Lost", 
                    "Potential Loyalist", 
                    "Others", 
                    "Loyal Customers", 
                    "Champions"
                  ),
                  selected = 'Champions'
      ),
      textInput("date_input", 
                "Insira a data para fazer a pesquisa no seguinte formato: YYYY-MM-DD", 
                value = '2025-03-01'),
    ),
    
    mainPanel(
      tabsetPanel(
        tabPanel("Visão Geral",
                 fluidRow(
                   column(6, plotlyOutput("treemap_plot")), 
                   column(6, plotlyOutput("viz_map")) 
                 ),
                 fluidRow(
                   column(12, plotlyOutput("viz_ribbon")) 
                 ),
                 fluidRow(
                   column(12, textOutput('definicao_text', container = pre)), 
                   column(12, textOutput("recomendacao_text", container = pre))  
                   
                 )
        ),
        
        tabPanel("Tabela de acompanhamento",
                 fluidRow(
                   column(7, DTOutput("monitoramento")),
                   column(5,
                           fluidRow(
                                   column(12, textOutput("proporcao")),
                                   column(12, plotlyOutput('viz_map_2')),
                                   )
                          ),
                   column(12, downloadButton('downloadData', label = "Download", class = NULL, icon = shiny::icon("download"))),
                   column(12, plotlyOutput('fluxo_segmento'))
                 )
          
          
        ),
      )
      
      
    )
    
    
  )
)

server <- function(input, output) {
  label_choice <- reactive({input$segmento})
  
  partiner_choice <- reactive({ input$partiner })
  
  date_input_choice <- reactive({input$date_input})
  
  
  
  monitoramento_result <- reactive({
    req(label_choice())
    req(date_input_choice())
    segment_scores = label_choice()
    date_input = date_input_choice()
    data <- ribbon_chart
    req(data)
    monitoring_status(data,
                      date_input,
                      segment_scores)
    
  })  
  
  
  output$treemap_plot <- renderPlotly({
    plot_ly(
      type = "treemap",
      labels = segment_chart$segment,
      parents = rep("", nrow(segment_chart)),
      values = segment_chart$customer_id,
      #text = segment_chart$recomendacao,  # Adiciona a recomendação como texto
      hoverinfo = "label+percent entry",  # Exibe o label e a porcentagem no hover
      marker = list(
        colors = segment_color_map[segment_chart$segment]
      )
    ) %>% layout(title = list(text = "Distribuição dos perceiros por segmento"))
  })
  
  
  
  output$viz_map <- renderPlotly(({
    
    viz_map(data_map = data_map, label = label_choice())
    
  }))
  
  
  output$viz_map_2 <- renderPlotly(({
    
    
    monitoramento_result()$mapa

  }))
  
  
  output$recomendacao_text <- renderText({
    label = label_choice()
    definicao <- segment_chart[segment_chart$segment == label, 'recomendacao']
    texto <- paste(paste("Recomenação: ", label), definicao, sep = "\n")
    return(texto)
    
  })
  
  
  output$definicao_text <- renderText({
    
    label = label_choice()
    definicao <- segment_chart[segment_chart$segment == label, 'definicao']
    texto <- paste(paste("Definicao: ", label), definicao, sep = "\n")
    return(texto)
    
    
    
  })
  #   
  
  output$fluxo_segmento <- renderPlotly({
    
    search <- trimws(toupper(input$monitoramento_search))
    req(search != "")
    
    plot_partiner(parceiro_dados = ribbon_chart,
                  partiner = search)
    
    
  })
  
  # output$fluxo_segmento <- renderPlotly({
  #   
  #   req(partiner_choice())
  #   
  #   plot_partiner(parceiro_dados = ribbon_chart,
  #                 partiner = partiner_choice())
  #   
  #   
  # })
  # 
  
  
  output$parceiros <- renderTable({
    
    req(partiner_choice())
    data <- ribbon_chart
    unique(data.frame(Nomes = data[grepl(partiner_choice(), data$customer_id, ignore.case = T), 'customer_id']))
    
    
  })
  
  
  output$proporcao <- renderText({
    
    req(label_choice())
    dat <- monitoramento_result()$data_filtred
    result <- round(prop.table(table(dat$Recomendação)) * 100, 2)
    paste("Acompanhar: ", result[1], "%  -  ", "\tAtuar: ", result[3], "% - ", "\tSegmento promovido: ", result[2], "%")
    
  })
  
  output$data <- renderTable({
    
    req(partiner_choice())
    resume <- data_map[grepl(partiner_choice(), data_map$customer_id, ignore.case = T), ]
    resume %>% 
      select(recency_days) %>%
      rename(
        dias_sem_produzir = recency_days
      )
    
    
  })
  
  
  output$monitoramento <- renderDT({
    
    
    
    dat <- monitoramento_result()$data_filtred
    
    
    
    
    
    datatable(dat,
              options = list(pageLength = 10, scrolly = "400px")) %>%
                formatStyle(
                  'Recomendação',
                  target = 'cell',
                  backgroundColor = styleEqual(
                    c('Segmento promovido', 'Acompanhar', "Atuar"),
                    c('#d4edda', 'white', '#f8d7da')
                  ),
                  color = styleEqual(
                    c('Segmento promovido', 'Acompanhar', "Atuar"),
                    c('green', 'red', 'red')

                  ),
                  fontWeight = 'bold'
                )
    


  })
  
  
  # output$monitoramento <- renderDT({
  #   
  #   monitoramento_result()$data_filtred
  #   
  # }, options = list(pageLength = 10, scrolly = "400px"))
  # 
  # 
  
  
  
  output$viz_ribbon <- renderPlotly({
    
    viz_ribbon(data = ribbon_chart, 
               label = label_choice(), 
               segment = TRUE)
  })
  


    output$downloadData <- downloadHandler(
      
      
      filename = function() {
        paste(paste(label_choice(), sep = "_"), Sys.Date(), "_", '.csv', sep='')
      },
      content = function(con) {
        #write.csv(monitoramento_result()$merge_final, con, row.names = F, sep = ';')
        write.xlsx(monitoramento_result()$merge_final, con, row.names = F)
      }
    )
    

  
  
  
}

# Run the application 
shinyApp(ui = ui, server = server)

