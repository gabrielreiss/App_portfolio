DROP TABLE IF EXISTS '{doc}_indicadores_{dfs}';

create table '{doc}_indicadores_{dfs}' as

select t1.*,
    t2.VL_CONTA as PL,
    t3.VL_CONTA as Liquidez_Corrente,
    t4.VL_CONTA as margem_bruta,
    t5.VL_CONTA as roe

from (
    select DISTINCT
        CNPJ_CIA,
        DT_FIM_EXERC,
        VERSAO,
        DENOM_CIA,
        CD_CVM
    from '{doc}_bpa_{dfs}'
) as t1

left join
    '{doc}_PL_{dfs}' as t2
on t1.CNPJ_CIA=t2.CNPJ_CIA
and t1.DT_FIM_EXERC=t2.DT_FIM_EXERC
and t1.VERSAO=t2.VERSAO

left join
    '{doc}_liq_corrente_{dfs}' as t3
on t1.CNPJ_CIA=t3.CNPJ_CIA
and t1.DT_FIM_EXERC=t3.DT_FIM_EXERC
and t1.VERSAO=t3.VERSAO

left join
    '{doc}_margem_bruta_{dfs}' as t4
on t1.CNPJ_CIA=t4.CNPJ_CIA
and t1.DT_FIM_EXERC=t4.DT_FIM_EXERC
and t1.VERSAO=t4.VERSAO

left join
    '{doc}_roe_{dfs}' as t5
on t1.CNPJ_CIA=t5.CNPJ_CIA
and t1.DT_FIM_EXERC=t5.DT_FIM_EXERC
and t1.VERSAO=t5.VERSAO

ORDER BY 
    t1.CNPJ_CIA,
    t1.DT_FIM_EXERC desc,
    t1.VERSAO
;

