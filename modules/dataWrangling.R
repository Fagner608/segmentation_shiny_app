# omitindo warnings
options(warn = -1)


get_data <- function(date = Sys.Date(), range_date = 12){
  
  date_from <- date
  date_to <- date_from %m-% months(range_date)

  query_mensal <- '
        select
          
          	nome_corretor as customer_id,
          	numero_corretor as id_storm,
          	recencia,
          	frequencia,
          	monetary_log,
          	TO_CHAR(TO_DATE(ano || \'-\' || mes, \'YYYY-MM\'), \'YYYY-MM\') AS date,
              ntile(5) OVER (ORDER BY - recencia) AS recency_score,
              ntile(5) OVER (ORDER BY frequencia) AS frequency_score,
              ntile(5) OVER (ORDER BY monetary_log) AS monetary_score,
           	id_corretor
          
           
          from(
          
          select 
          
          	*,
          	ultimo_dia_mes - data_maxima_pagamento as recencia
          
          from(
          select 
          
          	co."nome_corretor",
          	extract (year from ct."data_pagamento_comissao") as ano,
          	extract (month from ct."data_pagamento_comissao") as mes,
          	(DATE_TRUNC(\'MONTH\', ct."data_pagamento_comissao") + INTERVAL \'1 MONTH\' - INTERVAL \'1 day\')::DATE AS ultimo_dia_mes,
          	sum(LOG(abs(ct."valor_base"))) as monetary_log,
          	max(ct."data_pagamento_comissao") as data_maxima_pagamento,
          	co."id_corretor" ,
          	co."numero_corretor",
          	count(*) as frequencia
          
          from 
          	public.contrato ct
          left join 
          	cliente_multiloja climul on climul."id_cliente_multiloja" = ct."id_cliente_multiloja"
          left join 
          	cliente_corretor clicor on clicor."id_cliente_corretor" = climul."id_cliente_corretor"
          left join 
          	corretor co on co."id_corretor" = clicor."id_corretor"
          left join 
          	public.banco_orgao banorg on banorg."id_banco_orgao" = ct."id_banco_orgao"
          left join 
          	public.tabela_banco tabban on tabban."id_tabela_banco" = banorg."id_tabela_banco"
          where 
          	tabban."id_banco" = 3
          and 
          	data_pagamento_comissao between \'2024-01-01\' and \'2025-03-31\'
          and
            ct."valor_base" is not null and ct."valor_base" > 0
          group by 
          	ano,
          	mes,
          	ultimo_dia_mes,
          	co."id_corretor", 
          	co."nome_corretor"
          	        	))
          order by
          	nome_corretor, ano, mes
  
        '
  
  query <- '
  
  
          select
        
        	nome_corretor as customer_id,
          recencia,
          frequencia,
          monetary_log,
        	ntile(5) OVER (ORDER BY - recencia) AS recency_score,
          ntile(5) OVER (ORDER BY frequencia) AS frequency_score,
          ntile(5) OVER (ORDER BY monetary_log) AS monetary_score,
          concat(ntile(5) OVER (ORDER BY - recencia), 
              	 ntile(5) OVER (ORDER BY frequencia), 
              	 ntile(5) OVER (ORDER BY monetary_log)) as rfm,
        	id_corretor,
        	lat,
        	lon
        
         
        from(
        
        select 
        
        	*,
        	current_date - data_maxima_pagamento as recencia
        
        from(
        select 
        
        	co."nome_corretor",
        	co."lat",
        	co."lon",
        	sum(LOG(abs(ct."valor_base"))) as monetary_log,
        	max(ct."data_pagamento_comissao") as data_maxima_pagamento,
        	co."id_corretor" ,
        	count(*) as frequencia
        
        from 
        	public.contrato ct
        left join 
        	cliente_multiloja climul on climul."id_cliente_multiloja" = ct."id_cliente_multiloja"
        left join 
        	cliente_corretor clicor on clicor."id_cliente_corretor" = climul."id_cliente_corretor"
        left join 
        	corretor co on co."id_corretor" = clicor."id_corretor"
        left join 
        	public.banco_orgao banorg on banorg."id_banco_orgao" = ct."id_banco_orgao"
        left join 
        	public.tabela_banco tabban on tabban."id_tabela_banco" = banorg."id_tabela_banco"
        where 
        	tabban."id_banco" = 3
        and 
        	data_pagamento_comissao between \'2024-01-01\' and \'2025-03-31\'
        and
            ct."valor_base" is not null and ct."valor_base" > 0
        group by 
        	co."id_corretor", 
        	co."nome_corretor"
        
        	))
        order by
        	nome_corretor
  
  '
  
  
  # executando query
  con <- con_function()
  dados_mensais <- dbGetQuery(con, query_mensal)
  dados_agrupados <- dbGetQuery(con, query)
  
  # desconectando com DB
  dbDisconnect(con)
  
  dados_mensais$customer_id <- sub("\\d+ - ", "", dados_mensais$customer_id)
  dados_agrupados$customer_id <- sub("\\d+ - ", "", dados_agrupados$customer_id)
  
  
  return(list(dados_mensais = dados_mensais,
              dados_agrupados = dados_agrupados))
  
   
}

