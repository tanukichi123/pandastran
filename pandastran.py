# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) Mineo Sudo
#
###############################################################################
import pandas as pd

class pandastran(object):
    '''
    pandas + nastran
    optistruct
    '''
    def __init__(self):
        self.out_file_path = "out_file.dat"
        self.df_in=pd.DataFrame()

    def read_file(self,in_file_path):
        """read input file(for all format)
        
        Arguments:
            in_file_path {path} -- read file path
        """

        with open(in_file_path, 'r', encoding="utf-8") as bdf_file:
            lines = bdf_file.readlines()
        self.df_in["text"]=lines
        self.df_in = self.df_in.replace("\n","",regex=True)

    def write_file(self,df_out):
        """write out_put file 
        
        Arguments:
            df_out {pandas dataframe} -- must colum "text" -< output text
        """

        df_out=df_out+"\n"
        with open(self.out_file_path, 'w', encoding='utf8') as bdf_file:
            bdf_file.writelines(df_out["text"].tolist())
        print("out file " + self.out_file_path )

    def _make_df_card(self,card_name):
        """make card dataframe
        
        Arguments:
            card_name {str} -- card name ex)GRID
        
        Returns:
            pandas dataframe -- only card dataframe
        """
        df=self.df_in.copy()
        df=df[df["text"].str.contains(card_name)]
        start_num = df.index[0]
        count_row = df.index[1]-df.index[0]
        end_num = df.tail(1).index[0]+count_row
        df_card=self.df_in.copy()
        df_card=df_card[start_num:end_num]
        return df_card

    def _separate_8moji(self,df):
        """hyper mesh output dat or fem separete colunm
        
        Arguments:
            df {pandas dataframe} -- one colum dataframe ex)"text"colum only
        
        Returns:
            pandas dataframe -- 8string separate dataframe
        """

        moji = lambda x: x[8:]
        for i in range(0,11,1):
            df[str(i)]=df["text"].str.extract('(........)')
            df["text"]= df["text"].map(moji)

        df = df.drop('text', axis=1)
        df = df.dropna(axis=1)
        return df

    def _separate_open_vsp(self,df):
        """openvsp output dat separate colum
        
        Arguments:
            df {pandas dataframe} -- one colum dataframe ex)"text"colum only
        
        Returns:
            pandas dataframe -- ","separate dataframe
        """

        df = df["text"].str.split(',', expand=True)
        return df

    def _eight_moji(self,df):
        """formatting eight string for make output file
        
        Arguments:
            df {pandas dataframe} -- any dataframe OK
        
        Returns:
            df -- string dataframe 8string
        """

        moji = lambda x: x + " "* (8-len(x))
        df= df.applymap(moji)
        return df

    def _create_output_row(self,df):
        """crate output dataframe
        
        Arguments:
            df {pandas dataframe} -- any dataframe OK
        
        Returns:
            pandas dataframe -- for out put
        """

        df=df.assign(
            text=lambda df: df.apply(lambda row: "".join(row), axis=1) # A-Eの和
        )
        return df[["text"]]