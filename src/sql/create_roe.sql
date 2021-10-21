DROP TABLE IF EXISTS '{doc}_roe_{dfs}';

create table '{doc}_roe_{dfs}' as 

select 
    t1.CNPJ_CIA,
    t1.CD_CVM,
    t1.DT_FIM_EXERC,
    t1.VERSAO,
    t1.VL_CONTA as LL,
    t2.VL_CONTA as PL,
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
    where cd_conta = '3.11'
    and ORDEM_EXERC = 'ÚLTIMO'
) as t1

left join (
    SELECT *,
        VL_CONTA as vl_conta
    from '{doc}_PL_{dfs}'
) as t2
on t1.CNPJ_CIA = t2.CNPJ_CIA
and t1.DT_FIM_EXERC = t2.DT_FIM_EXERC
and t1.VERSAO = t2.VERSAO

order by 
    t1.CNPJ_CIA, 
    t1.DT_FIM_EXERC, 
    t1.VERSAO
;

DROP TABLE IF EXISTS '{doc}_roe_{dfs}_cod';

create table '{doc}_roe_{dfs}_cod' as 

select 
    t3.CNPJ_CIA,
    t1.Código_x,
    t1.`Nome de Pregão`,
    t1.`Razão Social`,
    t3.CD_CVM,
    t3.DT_FIM_EXERC,
    t3.VERSAO,
    t3.LL,
    t3.pl,
    t3.VL_CONTA

from cad_cod as t1

left JOIN '{doc}_roe_{dfs}' as t3
on t1.CNPJ = t3.CNPJ_CIA
;