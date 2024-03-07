
import pandas as pd
import re


profission_regexs = [
    r"(APOSENTAD)|(PENCION)|(PENSION)",
    r"(ESTAGIAR)|(BOLSIST)|(APRENDIZ)", r"(SERVIC)|(GERAIS)",
    r"(AUXILIAR)|(ASSISTENTE)|(AJUDANT)|(SERVENT)", r"(^TECNIC)|(.TECNIC)",
    r"(SECRETAR)|(RECEPC)", r"(^OPERAD)|(PRODUC)|(LINHA)", r"(^ANALIST)",
          
    r"(AUTONOM)|(FREE LANCE)|(AMBULANT)|(FEIRANT)", r"(VENDEDOR)|(VENDA)", r"(GEREN)|(ENCAR)|(LIDER)|(^CHEF)",
    r"(EMPRESAR)|(SOCIO)", r"(PROPRIETAR)|(PROPIETAR)|(FAZEND)", r"(COMERCIA)|(DISTRIBUID)", 
    r"(CABELE)|(BARBEIR)|(MANICUR)|(MAQUIAD)", r"(COSTUR)|(ALFAIATE)|(TECEL)", 
    r"(AGROP)|(RURAL)|(PECUAR)|(HORTI)|(AGRIC)|(AGRON.)", r"(PESCADOR)", 
    r"(COORDENAD)|(CORDENAD)|(^SUPERVISOR)|(INSPETOR)", r"(GESTOR)", r"(COMISS)", 
    r"(ACESSOR)|(ASSESSOR)|(ASSESOR)", r"(CORRET)|(CONSULTOR)|(CONSELHEIR)",
          
    r"(PUBLIC)|(FEDERAL)|(ESTADUA)|(EXECUT)", r"(JUIZ)|(PROCURAD)|(JUST)|(PERIT)",
    r"(ADVOGAD)", r"(AGENTE)|(OFICIAL)", r"(AUDITOR)", r"(FISCAL)", r"(ECONOM)", r"(CONTADOR)|(CONTABIL)", 
    r"(MILITAR)|(SOLDADO)|(TENENT.)|(BOMBEIR.)|(SARGENT.)|(POLICIA)|(ESCRIV)|(EXERC)|(MARINH)",
    r"(PROFESS)|(PEDAGOG)|(ORIENTAD)|(PESQUIS)|(CIENTIST)", r"(INSTRUTOR)|(MONITOR)|(PERSON)", 
    r"(CRECHE)|(INFANTIL)|(EDUCAD)|(CUIDAD)",
          
    r"(MINA)|(MAQUIN)", r"(PEDREIR)|(ENCANAD)", r"(DO LAR)|(DOMESTIC)|(DIARIST)|(BABA)", 
    r"(ZELADOR)|(LIMPEZ)|(LIMPAD)|(FAXINEIR)|(JARDIN)", 
    r"(GARCO.)|(BARMA.)|(SUSHI.)|(LANCH)", r"(METALURGIC)|(FERREIR)",
    r"(^GARI)|(LIXEIR)|(VARRED)", r"(LAVADOR)|(MONTADOR)", r"(SOLDA)|(SOLDADOR)",
    r"(CARPINTEIR)|(SERRALHEIR)|(TORNEIR)|(MARCENEIR)|(SERRAD)|(CORTAD)|(CHAPEAD)", 
    r"(BALCONIST)|(CAIXA)|(ATENDENT)|(COBRAD)", r"(ACOGUEIR)|(ACOUGUEIR)",
    r"(COZINH)|(GASTRON)|(PIZZA)|(CHURRAS)", r"(PADEIRO)|(PADAR)|(CONFEIT)", 
    r"(COPEIR)|(COPER)|(MERENDEIR)|(DOCEIR)|(SALGADEIR)|(CHAPEIR)",
    r"(CAMAREIR)", r"(ABASTECED)|(FRENTIST)", r"(EMPACOTAD)|(EMBALAD)|(PACOTEIR)",
    r"(PORTEIR)|(PORTAR)", r"(^MECANICO)|(ALINHAD)|(VEICUL)", r"(ARRUMAD)|(ALMOXAR)|(ESTOQ)",

    r"(MOTORISTA)|(TAX)|(CONDUTOR)|(CAMINHON)|(FERROV)",
    r"(BOY)|(MOTOCICLIST)|(MOTOQUEIR)|(^ENTREGAD)",
    r"(SEGURANC)|(VIGIA)|(VIGILANT)|(GUARD)", 
          
    r"(ENGENHEIR)|(ARQUITET)|(USINAGEM)", r"(ELETRIC)|(ELETREC)", r"(BIOLOG)|(QUIMIC)|(ZOOTEC)|(ASTROL)",
    r"(MEDIC)|(CIRURGIAO)|(FONOAUD)|(VETERINAR)|(NUTRICIO)", r"(ODONTO)|(DENTISTA)", 
    r"((FISIOT)|(PSICOL)|(TERAP))", r"(ENFERM)|(FARMACEUTIC)", 
          
    r"(PROGRAMAD)|(SISTEMA)", r"(DESIGN)|(DESENHIST)", 
        
    r"(DIRET)|(PRESIDENTE)|(SUPERINT)", r"(BANCO)|(BANCAR)",
    r"(JORNAL)|(REPORT)|(TV)|(RADIO)|(CINEGRAF)|(LOCUTOR)|(RADIALIST)", r"(ROTERISTA)|(CINEMA)",
          
    r"(ATLETA)|(JOGADOR)", r"(ARTES)|(CANTOR)|(ATOR)|(MUSIC)", r"(PINTOR)|(PINTURA)",
    r"(CERIMO)|(EVENT)|(FOTOGRAF)|(PROMOTER)", r"(PAISAG)|(DECORAD)",
    r"(EDITOR)|(DIGITAD)|(DATILOG)|(REVIS)|(ESCRIT)",
    r"(TURISM)|(VIAGEM)", r"(MARKET)|(TELEMARKT)|(PUBLICIT)",

    r"(PASTOR)|(RELIG)|(PADRE)|(MISSIONAR)|(CELULA)|(TEOLOG)",
          
    r"(ESTUDANT)", r"(PROMOT)", r"(ADMINISTR)", r"(VISTORIAD)|(DESPACHANT)", r"(CONSTRUT)",
    r"(MANUTENC)|(MONTA)|(FERRAM)|(INSTALAD)|(MOVEIS)", r"(CONFERENT)", 
]


def generate_occupation_group(professions, column_name):
    """Group professions based on regex

    Parameters
    ----------
    professions : pd.Series
        Dataframe profession column.
    column_name : str
        Profession column name.

    Returns
    -------
    pd.DataFrame
        Dataframe with the new group profession column.
    """
    occupation_map = {column_name:[], column_name+"_group":[]}
    
    for profession in professions:
        if str(profession) != "nan":
            for regex in profission_regexs:
                x = re.search(regex, profession)
                if x is not None:
                    occupation_map[column_name].append(profession)
                    occupation_map[column_name+"_group"].append(regex)
                    break
                    
    return pd.DataFrame.from_dict(occupation_map)


def encode_zip_code(df):
    """Transform zipcode column.
    
    OBS: the dataframe must be only with zipcode column

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with zipcode column

    Returns
    -------
    pd.DataFrame
        Dataframe with the new transformed zipcodes columns.
    """
    def slice_zip(cep, pos0, pos1):
        try:
            return int(cep[pos0:pos1])
        except:
            return 0
    
    for column in df.columns:
        df[column] = df[column].apply(lambda x: str(x).zfill(8))
        df[column+"_regiao"] = df[column].apply(lambda v: slice_zip(v, 0, 2))
        df[column+"_setor"] = df[column].apply(lambda v: slice_zip(v, 2, 5))
        df[column+"_distribuicao"] = df[column].apply(lambda v: slice_zip(v, 5, 8))
        del df[column]
    
    return df
