#!/usr/bin/env python

"""
Agregates several data tables of deepimpact WP1 and creates askomics inputs
"""

import sys
import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_folder", help="root folder of deepimpact-wp1-like data")
parser.add_argument("-o", "--output_folder", help="output folder for WP1 askofiles")
args = parser.parse_args()

# input_folder = '/home/vmataign/Documents/genecodata/usecase/deepimpact/data/raw_data
# output_folder = '/home/vmataign/Documents/genecodata/usecase/deepimpact/data/concatenated_input_data'

def concat_yearly_data(content):
    bn_y1 = os.path.join(os.path.join(args.input_folder, f'brassica_napus/sampling_campaign_y1/bn_{content}_y1.xlsx'))
    bn_y2 = os.path.join(os.path.join(args.input_folder, f'brassica_napus/sampling_campaign_y2/bn_{content}_y2.xlsx'))
    ta_y1 = os.path.join(os.path.join(args.input_folder, f'triticum_aestivum/sampling_campaign_y1/ta_{content}_y1.xlsx'))
    ta_y2 = os.path.join(os.path.join(args.input_folder, f'triticum_aestivum/sampling_campaign_y2/ta_{content}_y2.xlsx'))

    df_list = [pd.read_excel(bn_y1, sheet_name=1, index_col=0, header=0),
               pd.read_excel(bn_y2, sheet_name=1, index_col=0, header=0),
               pd.read_excel(ta_y1, sheet_name=1, index_col=0, header=0),
               pd.read_excel(ta_y2, sheet_name=1, index_col=0, header=0)]

    df = pd.concat(df_list, axis=0)

    if 'DATE' in df.columns:
        df['DATE'] = df['DATE'].astype(str)

    df.to_csv(os.path.join(args.output_folder, f'{content}.tsv'), sep="\t")

def concat_seasonal_data(content):
    bn_y1_s1 = os.path.join(os.path.join(args.input_folder, f'brassica_napus/sampling_campaign_y1/sampling_season_s1/bn_{content}_y1_s1.xlsx'))
    bn_y1_s2 = os.path.join(os.path.join(args.input_folder, f'brassica_napus/sampling_campaign_y1/sampling_season_s2/bn_{content}_y1_s2.xlsx'))
    bn_y2_s1 = os.path.join(os.path.join(args.input_folder, f'brassica_napus/sampling_campaign_y2/sampling_season_s1/bn_{content}_y2_s1.xlsx'))
    bn_y2_s2 = os.path.join(os.path.join(args.input_folder, f'brassica_napus/sampling_campaign_y2/sampling_season_s2/bn_{content}_y2_s2.xlsx'))
    ta_y1_s1 = os.path.join(os.path.join(args.input_folder, f'triticum_aestivum/sampling_campaign_y1/sampling_season_s1/ta_{content}_y1_s1.xlsx'))
    ta_y1_s2 = os.path.join(os.path.join(args.input_folder, f'triticum_aestivum/sampling_campaign_y1/sampling_season_s2/ta_{content}_y1_s2.xlsx'))
    ta_y2_s1 = os.path.join(os.path.join(args.input_folder, f'triticum_aestivum/sampling_campaign_y2/sampling_season_s1/ta_{content}_y2_s1.xlsx'))
    ta_y2_s2 = os.path.join(os.path.join(args.input_folder, f'triticum_aestivum/sampling_campaign_y2/sampling_season_s2/ta_{content}_y2_s2.xlsx'))

    df_list = [pd.read_excel(bn_y1_s1, sheet_name=1, index_col=0, header=0),
               pd.read_excel(bn_y1_s2, sheet_name=1, index_col=0, header=0),
               pd.read_excel(bn_y2_s1, sheet_name=1, index_col=0, header=0),
               pd.read_excel(bn_y2_s2, sheet_name=1, index_col=0, header=0),
               pd.read_excel(ta_y1_s1, sheet_name=1, index_col=0, header=0),
               pd.read_excel(ta_y1_s2, sheet_name=1, index_col=0, header=0),
               pd.read_excel(ta_y2_s1, sheet_name=1, index_col=0, header=0),
               pd.read_excel(ta_y2_s2, sheet_name=1, index_col=0, header=0)]

    df = pd.concat(df_list, axis=0)
    # df.rename(columns={'FIELD_ID': 'season_of@FIELD_ID'}, inplace=True)

    # if "DATE" in df.columns:        
    #     # df['DATE']=df['DATE'].dt.strftime('%m/%d/%Y')
    #     df['DATE'] = pd.to_datetime(df['DATE'], dayfirst=True)
    #     df['DATE'] = df['DATE'].dt.strftime('%d/%m/%y')

    if "PLANT" in df.columns:
        df["PLOT_ID_SEASONAL"] = df.index
        cols = ["PLOT_ID_SEASONAL", "PLANT"]
        df["SAMPLED_PLANT"] = df[cols].apply(lambda row: '-'.join(row.values.astype(str)), axis=1)
        df.set_index("SAMPLED_PLANT", inplace=True)
        df.drop(cols, axis=1, inplace=True)

    df.to_csv(os.path.join(args.output_folder, f'{content}.tsv'), sep="\t")

# concat_yearly_data('location')
# concat_yearly_data('biomass')
# concat_yearly_data('nirs')
# concat_yearly_data('yields')
# concat_yearly_data('agriculture')
# concat_seasonal_data('soils')
# concat_seasonal_data('weeds')
# concat_seasonal_data('bioagressors_field_general')
# concat_seasonal_data('bioagressors_field_details')
concat_seasonal_data('bioagressors_lab')

# ------------
# Weather data
# ------------

# df = pd.read_csv(os.path.join(args.input_folder, 'weather_data', 'siclima_extraction_quotidien_1898_20240422.csv'), header=0, index_col=0, sep=";")
# df.index.rename('SAFRAN', inplace=True)
# df.to_csv(os.path.join(args.output_folder, 'climatic.tsv'), sep="\t")
