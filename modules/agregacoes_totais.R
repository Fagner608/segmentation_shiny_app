con <- con_function()


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
      	id_corretor
      
       
      from(
      
      select 
      
      	*,
      	current_date - data_maxima_pagamento as recencia
      
      from(
      select 
      
      	co."nome_corretor",
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
      	data_pagamento_comissao between \'2025-01-01\' and \'2025-03-31\'
      group by 
      	co."id_corretor", 
      	co."nome_corretor"
      
      	))
      order by
      	nome_corretor

'


dados_teste <- dbGetQuery(con, query)

teste <- my_rfm_function(dados_teste)

head(teste)
## pare fazer o resumo, vou precisar do monetary e dos demais campos




