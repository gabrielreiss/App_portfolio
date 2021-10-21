DROP TABLE IF EXISTS '{doc}_PL_{dfs}';

create table '{doc}_PL_{dfs}' as 

select t1.CNPJ_CIA,
        T1.DT_FIM_EXERC,
        t1.VERSAO,
        t1.VL_CONTA as 'Patrimônio Líquido Consolidado',
        t2.VL_CONTA as 'Participação dos Acionistas Não Controladores',
        t1.VL_CONTA - t2.VL_CONTA as VL_CONTA
from (
    select 
        CNPJ_CIA,
        DT_FIM_EXERC,
        VERSAO,
        case
            when escala_moeda = 'MIL' then vl_conta * 1000
            when escala_moeda = 'MILHAR' then vl_conta * 1000
            when escala_moeda = 'UNIDADE' then vl_conta
            else 0
        end as VL_CONTA
    FROM '{doc}_BPP_{dfs}'
    where (ds_conta = 'Patrimônio Líquido Consolidado')
    /* and DT_FIM_EXERC = "2020-03-31" */
) as T1

left join (
    select 
        CNPJ_CIA,
        DT_FIM_EXERC,
        VERSAO,
        case
            when escala_moeda = 'MIL' then vl_conta * 1000
            when escala_moeda = 'MILHAR' then vl_conta * 1000
            when escala_moeda = 'UNIDADE' then vl_conta
            else 0
        end as VL_CONTA
    FROM '{doc}_BPP_{dfs}'
    where (ds_CONTA = 'Participação dos Acionistas Não Controladores')
    /* and DT_FIM_EXERC = "2020-03-31" */
) as T2
on (T1.CNPJ_CIA = T2.CNPJ_CIA
and T1.DT_FIM_EXERC = T2.DT_FIM_EXERC
and t1.VERSAO = t2.VERSAO)

GROUP by  
    T1.CNPJ_CIA,
    T1.DT_FIM_EXERC,
    t1.VERSAO

order by 
    t1.CNPJ_CIA, 
    t1.DT_FIM_EXERC, 
    t1.VERSAO
;

DROP TABLE IF EXISTS '{doc}_PL_cod_{dfs}';

create table '{doc}_PL_cod_{dfs}' as
select 
    T2.CNPJ_CIA,
    T1.Código_x,
    T1.`Nome de Pregão`,
    T1.`Razão Social`,
    T2.DT_FIM_EXERC,
    T2.VERSAO,
    T2.VL_CONTA

from cad_cod as T1

left JOIN '{doc}_PL_{dfs}' as T2
on T1.CNPJ = T2.CNPJ_CIA

;