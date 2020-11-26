import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.metrics as Metrics
import pandas as pd
import matplotlib.pyplot as plt
import unidecode

import streamlit as st

# Override tweepy.StreamListener to add logic to on_status
class DF_prep:

    #===================================#
    #     Initialization                #
    #===================================#
    def __init__(self):
        self.__relational_data()
        self.cat_dict = {}
        self.df_long = pd.DataFrame()
        self.df_td = pd.DataFrame()
        self.df_concat = pd.DataFrame()

    #===================================#
    #     Load CSV file                 #
    #===================================#
    def load_file(self, path):
        self.df_long = pd.DataFrame()
        #self.raw_df = pd.read_csv(path, sep=';', encoding='iso-8859-1')
        
        self.raw_df = pd.read_excel(path)
        self.__process_df()

    #===================================#
    #     Load DataFrame                #
    #===================================#
    def load_df(self, df):
        self.df_long = pd.DataFrame()
        self.raw_df = df.copy()
        self.__process_df()

    #===================================#
    #     Load Terridata XLS file       #
    #===================================#
    def load_file_td(self, path, filename):
        print("{}/{}".format(path, filename))
        self.df_td = pd.DataFrame()
        self.raw_df_td = pd.read_excel("{}/{}".format(path, filename))
        self.__process_df_td()

    #===================================#
    #     Load Terridata DataFrame      #
    #===================================#
    def load_df_td(self, df):
        self.df_td = pd.DataFrame()
        self.raw_df_td = df.copy()
        self.__process_df_td()

    #===================================#
    #     Returns the concat DF         #
    #===================================#
    def get_concat_df(self):
        return self.df_concat.copy()

    #===================================#
    #     Processing function (core)    #
    #===================================#
    def __process_df(self):
        df = self.__clear_df(self.raw_df.copy())
        df = self.__check_and_transform(df)
        df = self.__filter(df)
        self.df_long = self.__post_filter(df)
        self.df_concat = pd.concat([self.df_concat, self.df_long])
        self.df_concat = self.df_concat.reset_index(drop=True)

    #===================================#
    #     Processing Terridata          #
    #===================================#
    def __process_df_td(self):
        df = self.__clear_df(self.raw_df_td.copy())
        df = self.__filter_td(df)
        self.df_td = self.__post_filter_td(df)
        self.df_concat = pd.concat([self.df_concat, self.df_td])
        self.df_concat = self.df_concat.reset_index(drop=True)

    #===================================#
    #     Relationships                 #
    #===================================#
    def __relational_data(self):
        self.replacement_cols = {
            'cod_mpio'              :   ['codmpio', 'codigodane', 'codigodane'],
            'cod_producto'          :   ['codigoproducto', 'codigometa', 'idvariable'],
            'producto'              :   ['producto', 'descripcionmeta', 'descripcion'],
            'producto_ind'          :   ['indicadorproducto', 'indicador', 'indicador'],
            'orientacion'           :   ['orientacion', 'tipometa', 'tipometa_a'],
            'producto_lb'           :   ['lbproducto', 'lineabase', 'lineabase'],
            'producto_meta'         :   ['metaproducto', 'metacuatrienio', 'metacuatrenio'],
            'valor_esperado'        :   ['valoresperado', 'valoresperado', 'valoresperado'],
            'valor_ejecutado'       :   ['valorejecutado', 'valorlogrado', 'valorlogradometaproducto'],
            'sector'                :   ['codigosector', 'codfut', 'codfut'],
            'ejec_rec_propios'      :   ['ejecrecursospropios', 'recursospropios', 'recursospropios'],
            'ejec_credito'          :   ['ejeccredito', 'credito', 'credito'],
            'ejec_otros'            :   ['ejecotros', 'otros', 'otros'],
            'ejec_funcionamiento'   :   ['ejecfuncionamiento', 'recursosfuncionamiento', 'recursosfuncionamiento'],
            'ejec_gestionados'      :   ['ejecgestionados', 'recursosgestionados', 'recursosgestionados'],
            'year'                  :   ['year', 'ano'],
            'avance'                :   ['%avance', 'eficacia', 'eficacia2013'],
            'rango_calificacion'    :   ['rangocalificacion', 'nivelcumplimiento', 'nivel2013'],
            'ejec_total'            :   ['ejectotal'],
            'ejec_total_cuatrienio' :   ['ejectotalcuatrienio']
        }
        self.resource_sum = ['recursospropios', 'sgp', 'conacion', 'codepartamento', 'sgr', 'credito', 'otros', 'recursosfuncionamiento', \
                        'recursosgestionados']
        self.sectors = [1, 2, 10, 18]

        self.replacement_cols_td = {
            'sector'                :   ['dimension'],
            'year'                  :   ['ano'],
            'cod_mpio'              :   ['codigoentidad'],
            'td_indicador'          :   ['indicador'],
            'td_ind_value'          :   ['datonumerico'],
            'td_ind_unit'           :   ['unidaddemedida'],
            'td_ind_value_norm'     :   ['datonumericonorm'],
        }
        self.td_sectors = {
            'educacion'             :   1,
            'salud'                 :   2,
            'conflicto armado y seguridad ciudadana'  : 18,
            'ambiente'              :   10
        }

    #===================================#
    #     Main cleaner                  #
    #===================================#
    def __clear_df(self, df):
        new_columns = {}
        for c in list(df.columns):
            new_columns[c] = unidecode.unidecode(c.strip().replace(' ', '').lower())
            if str(df[c].dtype) == 'object':
                df[c] = df[c].str.strip().str.lower()
                df[c] = df[c].str.normalize('NFD')
                df[c] = df[c].str.replace(r'([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+', r'\1')
                df[c] = df[c].str.normalize('NFC')
                df[c] = df[c].str.replace('\n', '')
                df[c] = df[c].str.replace('\r', '')
                df[c] = df[c].str.replace('\r', '')
                df[c] = df[c].apply(self.__comma_check)

        df.rename(columns=new_columns, inplace = True)

        df.replace('', np.nan, inplace=True)
        df.replace('-', np.nan, inplace=True)
        df.replace('np', np.nan, inplace=True)   # NP = No programada
        df.replace('ne', np.nan, inplace=True)   # NE = No esperada
        df.replace('sc', np.nan, inplace=True)
        df.replace('n/a', np.nan, inplace=True)

        return df

    #===================================#
    #     Numeric type cleaner          #
    #===================================#
    def __comma_check(self, s):
        new_value = s
        if isinstance(s, str):
            comma_index = s.rfind(',')
            if comma_index != -1 and comma_index != 0 and comma_index != (len(s) - 1) and len(s) < 28:
                if s[comma_index - 1].isnumeric() and s[comma_index + 1].isnumeric():
                    s = s[:comma_index].replace('.', '').replace(',', '') + '.' + s[comma_index + 1:]
        try:
            new_value = int(s)
        except:
            try:
                new_value = float(s)
            except:
                new_value = s

        return new_value

    #=======================================#
    #     Column filtering & arrangement    #
    #=======================================#
    def __filter(self, df):
        df_result = pd.DataFrame()

        #### Create a new dataframe, only with the filtered columns
        for c in list(df.columns):
            for c_new in self.replacement_cols:
                if c in self.replacement_cols[c_new]:
                    df_result[c_new] = df[c]

        #### Create "ejec total" columns for historic dataframes
        for c_new in self.replacement_cols:
            if c_new not in list(df_result.columns):
                if c_new == 'ejec_total':
                    df_result['ejec_total'] = df[self.resource_sum].agg('sum', axis=1)
                if c_new == 'ejec_total_cuatrienio':
                    df_result['ejec_total_cuatrienio'] = np.nan

        #### Create additional NaN columns (Terridata compatibility)
        for c_new in self.replacement_cols_td:
            if c_new not in list(self.replacement_cols):
                df_result[c_new] = np.nan

        return df_result

    #=======================================#
    #     Terridata filtering & arrangement #
    #=======================================#
    def __filter_td(self, df):
        df_result = pd.DataFrame()

        #### Create a new dataframe, only with the filtered columns
        for c in list(df.columns):
            for c_new in self.replacement_cols_td:
                if c in self.replacement_cols_td[c_new]:
                    df_result[c_new] = df[c]

        #### Create additional NaN columns (SIEE compatibility)
        for c_new in self.replacement_cols:
            if c_new not in list(self.replacement_cols_td):
                df_result[c_new] = np.nan

        return df_result

    #=====================================#
    #     Transformation (if applicable)  #
    #=====================================#
    def __check_and_transform(self, df):
        column_list = list(df.columns)
        if ('year' not in column_list) and ('ano' not in column_list):
            year_list = []
            for c in column_list:
                if 'valoresperado' in c:
                    year_list.append(c[-4:])
            dynamic_cols = []
            for y in year_list:
                dynamic_cols += [x for x in column_list if y in x]
            static_cols = list(set(column_list).difference(dynamic_cols))
            df_result = pd.DataFrame()
            for y in year_list:
                name_dict = {}
                year_cols = [x for x in column_list if y in x]
                for name in year_cols:
                    name_dict[name] = name[:-4].strip()
                new_df = df[static_cols + year_cols]
                new_df.rename(columns=name_dict, inplace=True)
                new_df['year'] = int(y)
                df_result = pd.concat([df_result, new_df])

            df_result.reset_index(drop=True)
            return df_result
        else:
            return df

    #===================================#
    #     Post-processing               #
    #===================================#
    def __post_filter(self, df):
        df['sector'] = df['sector'].str.replace('a.', '')
        df['sector'] = pd.to_numeric(df['sector'], errors='ignore')
        df = df[df['sector'].isin(self.sectors)]
        return df

    #===================================#
    #     Terridata Post-processing     #
    #===================================#
    def __post_filter_td(self, df):
        df = df[df['sector'].isin(list(self.td_sectors))]
        df['sector'] = df['sector'].apply(lambda x: self.td_sectors[x])
        df['sector'] = pd.to_numeric(df['sector'], errors='ignore')
        df.dropna(subset=['td_ind_value', 'year'], inplace=True)
        df = df[df['year'] > 2012]
        ind_max = df.groupby('td_indicador')['td_ind_value'].max()
        new_df = pd.DataFrame()
        for g in df.groupby('td_indicador'):
            temp_df = g[1]
            temp_df['td_ind_value_norm'] = temp_df['td_ind_value'] / ind_max[g[0]]
            new_df = pd.concat([new_df, temp_df])
        new_df = new_df.reset_index(drop=True)
        return new_df
