DROP TABLE IF EXISTS '{doc}_margem_bruta_{dfs}';

create table '{doc}_margem_bruta_{dfs}' as 

select 
    t1.CNPJ_CIA,
    t1.CD_CVM,
    t1.DT_FIM_EXERC,
    t1.VERSAO,
    t1.VL_CONTA / t2.VL_CONTA as VL_CONTA

from (
    select *,
        case
            when escala_moeda = 'MIL' then vl_conta * 1000
            when escala_moeda = 'MILHAR' then vl_conta * 1000
            when escala_moeda = 'UNIDADE' then vl_conta
            else 0
        end as vl_conta
    from '{doc}_DRE_{dfs}'
    where cd_conta = '3.03'
    and ORDEM_EXERC = 'ÚLTIMO'
) as t1

left join (
    SELECT *,
        case
            when escala_moeda = 'MIL' then vl_conta * 1000
            when escala_moeda = 'MILHAR' then vl_conta * 1000
            when escala_moeda = 'UNIDADE' then vl_conta
            else 0
        end as vl_conta
    from '{doc}_DRE_{dfs}'
    where cd_conta = '3.01'
    and ORDEM_EXERC = 'ÚLTIMO'
) as t2
on t1.CNPJ_CIA = t2.CNPJ_CIA
and t1.DT_FIM_EXERC = t2.DT_FIM_EXERC
and t1.VERSAO = t2.VERSAO

order by 
    t1.CNPJ_CIA, 
    t1.DT_FIM_EXERC, 
    t1.VERSAO
;

DROP TABLE IF EXISTS '{doc}_margem_bruta_{dfs}_cod';

create table '{doc}_margem_bruta_{dfs}_cod' as 

select 
    t3.CNPJ_CIA,
    T1.Código_x,
    T1.`Nome de Pregão`,
    T1.`Razão Social`,
    t3.CD_CVM,
    t3.DT_FIM_EXERC,
    t3.VERSAO,
    t3.VL_CONTA

from cad_cod as T1

left JOIN '{doc}_margem_bruta_{dfs}' as t3
on T1.CNPJ = t3.CNPJ_CIA
;