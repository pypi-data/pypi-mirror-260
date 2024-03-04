__author__ = "PyPSA meets Earth"
__copyright__ = "Copyright 2022, The PyPSA meets Earth Initiative"
__license__ = "MIT"

"""Utilities functions for earth_osm

This module contains utilities functions for handling OSM data.

"""

import ast
import logging
import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString, Point, Polygon

from earth_osm import logger as base_logger

logger = logging.getLogger("eo.utils")
logger.setLevel(logging.INFO)

# Notes: Types
# Three main types returned by extraction: Node, Way, Relation
# Node: Point
# Way: LineString or Polygon
# Relation: MultiLineString or MultiPolygon
# So really it is Node, Way, Area, Relation

# Notes: CRS
# geo_crs: EPSG:4326  # general geographic projection, not used for metric measures. "EPSG:4326" is the standard used by OSM and google maps
# distance_crs: EPSG:3857  # projection for distance measurements only. Possible recommended values are "EPSG:3857" (used by OSM and Google Maps)
# area_crs: ESRI:54009  # projection for area measurements only. Possible recommended values are Global Mollweide "ESRI:54009"

def lonlat_lookup(df_way, primary_data):
    """
    Lookup refs and convert to list of longlats
    """
    if "refs" not in df_way.columns:
        logger.warning("refs column not found")
        return []

    def look(ref):
        lonlat_row = list(map(lambda r: tuple(primary_data["Node"][str(r)]["lonlat"]), ref))
        return lonlat_row

    lonlat_list = df_way["refs"].apply(look)

    return lonlat_list

def way_or_area(df_way):
    if "refs" not in df_way.columns:
        raise KeyError("refs column not found")
    
    def check_closed(refs):
        if (refs[0] == refs[-1]) and (len(refs) >= 4):
            return "area"
        elif len(refs) >= 2:
            return "way"
        else:
            logger.debug(f"Way with less than 2 refs: {refs}")
            return None

    type_list = df_way["refs"].apply(check_closed)

    return type_list



def tags_melt(df_exp, nan_threshold=0.75):
    # Find columns with high percentage of NaN values
    high_nan_cols = df_exp.columns[df_exp.isnull().mean() > nan_threshold]

    logger.debug(f"Melting tags from the following columns: {high_nan_cols}")

    df_high_nan = df_exp[high_nan_cols]

    # assert other_tags column does not already exist, if it does,
    assert 'other_tags' not in df_exp.columns, "other_tags column already exists in dataframe"
    df_exp['other_tags'] = df_high_nan.apply(lambda x: x.dropna().to_dict(), axis=1)

    # drop {} in other tags so that its nan
    df_exp['other_tags'] = df_exp['other_tags'].apply(lambda x: x if x != {} else None)


    df_exp.drop(columns=high_nan_cols, inplace=True)
    return df_exp

def columns_melt(df_exp, columns_to_move):
    def concat_melt(row, col):
        # check if value to melt is NaN
        if str(row[col]) == 'nan':
            return None
        # if other_tags column does not exist, no need to concat
        # or if other tags exist, but is empty/none/nan, still no need to concat
        if (
            'other_tags' not in row.keys() or
            row['other_tags'] == {} or
            row['other_tags'] is None or
            str(row['other_tags']) == 'nan'
        ):
            return {col: row[col]}
        else:
            # before concating, check if the column already exists in other_tags
            if col in row['other_tags']:
                logger.warning(f"'{col}' already exists in 'row'.")
            return {**row['other_tags'], col: row[col]}

    # Move specified columns to other_tags
    for col in columns_to_move:
        if col in df_exp.columns:
            df_exp['other_tags'] = df_exp.apply(lambda x: concat_melt(x, col), axis=1)
            df_exp.drop(columns=col, inplace=True)
        else:
            logger.warning(f"Column '{col}' not found in dataframe.")

    return df_exp

def tags_explode(df_melt):
    # check if df_melt has column 'other_tags'
    if not 'other_tags' in df_melt.columns:
        logger.warning("df is not melted, but tags_explode was called")
        return df_melt

    # check if other_tags is empty
    if df_melt['other_tags'].isnull().all():
        logger.debug("nothing to explode, other_tags is empty, returning df with dropped other_tags column")
        # drop other_tags column
        df_melt.drop(columns=['other_tags'], inplace=True)
        return df_melt
    # convert stringified dicts to dict
    df_melt['other_tags'] = df_melt['other_tags'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    # explode other_tags column into multiple columns
    df_exploded = df_melt.join(pd.json_normalize(df_melt['other_tags']))

    # drop the original other_tags column
    df_exploded.drop(columns=['other_tags'], inplace=True)

    return df_exploded


def convert_pd_to_gdf(pd_df):
    # check if pd_df has a lonlat column
    if not 'lonlat' in pd_df.columns:
        raise KeyError("pandas dataframe does not have a lonlat column")
    if not 'Type' in pd_df.columns:
        raise KeyError("pandas dataframe does not have a Type ('node', 'way' or 'area') column")
    # unstringify lonlat column if necessary
    pd_df['lonlat'] = pd_df['lonlat'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    def create_geometry(lonlat_list, geom_type):
        if geom_type == 'node':
            return Point(lonlat_list[0])
        elif geom_type == 'way':
            return LineString(lonlat_list)
        elif geom_type == 'area':
            return Polygon(lonlat_list)
    
    geometry_col = pd_df.apply(lambda row: create_geometry(row['lonlat'], row['Type']), axis=1)
    lonlat_index = pd_df.columns.get_loc('lonlat')
    pd_df.insert(lonlat_index, "geometry", geometry_col)
    gdf = gpd.GeoDataFrame(pd_df, geometry='geometry')
    gdf.drop(columns=['lonlat'], inplace=True)
    pd_df.drop(columns=['geometry'], inplace=True)

    return gdf


def get_list_slug(str_list):
    import hashlib
    str_list.sort()
    if len(str_list) == 1:
        return str_list[0]
    else:
        file_slug = "_".join(str_list)
        if len(file_slug)>15:
            name_string = file_slug[:15] # TODO: could be partial string
            name_code = hashlib.md5(file_slug[15:].encode()).hexdigest()[:8]
            file_slug = name_string + '_' + name_code
        return file_slug

class OutFileWriter:

    def __init__(self, region_list, primary_name, feature_list, data_dir, out_format):
        self.region_list = region_list
        self.primary_name = primary_name
        self.feature_list = feature_list
        self.data_dir = data_dir
        self.out_format = out_format
        logger.info(f'File writer initialized with region_list: {region_list}, primary_name: {primary_name}, feature_list: {feature_list}')

    def __enter__(self):
        # setup file name etc.
        region_slug = get_list_slug(self.region_list) # country code e.g. BJ
        feature_slug = get_list_slug(self.feature_list)
    
        out_dir = os.path.join(self.data_dir, "out")  # Output file directory
        out_slug = os.path.join(out_dir, f"{region_slug}_{feature_slug}")

        self.out_slug = out_slug

        if not os.path.exists(out_dir):
            os.makedirs(
                out_dir, exist_ok=True
            )

        # delete file if it already exists
        if isinstance(self.out_format, str):
            self.out_format = [self.out_format]
        for ext in self.out_format:
            out_path = out_slug + '.' + ext
            if os.path.exists(out_path):
                logger.debug(f"Deleting existing file: {out_path}")
                os.remove(out_path)

        return self
    

    def __call__(self, df_feature):
        if df_feature.empty:
            # exit function
            return

        df_feature.reset_index(drop=True, inplace=True) # avoids weird index

        # Append by concating
        if os.path.exists(self.out_slug + '.csv'):
            # read the existing csv
            df_existing = pd.read_csv(self.out_slug + '.csv')

            # explode other_tags to get back original columns
            df_existing = tags_explode(df_existing)

            # concat the existing df with the new df
            df_feature = pd.concat([df_existing, df_feature], ignore_index=True)

        # melt 95% nan tags (TODO: remove hardcode)
        df_feature = tags_melt(df_feature, 0.95)
        # move refs column to other_tags
        df_feature = columns_melt(df_feature,   ['refs'])

        df_feature.to_csv(self.out_slug + '.csv', index=False)


        # Apend by writing to csv (more efficient, but problem with dynamically changing columns)
        # if os.path.exists(self.out_slug + '.csv'):
        #     # read the existing columns
        #     col_existing = pd.read_csv(self.out_slug + '.csv', nrows=1).columns.to_list()
        #     # check if the columns are the same
        #     col_incoming = df_feature.columns.to_list()
        #     if col_existing != col_incoming:
        #         # add missing columns to the end
        #         missing_cols_in_incoming = [col for col in col_existing if col not in col_incoming]
        #         new_cols_in_incoming = [col for col in col_incoming if col not in col_existing]
        #     TODO: incomplete, should melt new_cols_in_incoming, and add missing cols

        # write the new df to csv
        # df_feature.to_csv(self.out_slug + '.csv', index=False, header= not os.path.exists(self.out_slug + '.csv'), mode="a")


    def __exit__(self, exc_type, exc_value, traceback):
        if os.path.exists(self.out_slug + '.csv'):
            logger.info(f"Output file written to: {self.out_slug}.csv")
            
            if 'geojson' in self.out_format:
                # read the csv file
                df_feature = pd.read_csv(self.out_slug + '.csv')
                # convert to geodataframe
                gdf_feature = convert_pd_to_gdf(df_feature)

                gdf_feature.to_file(
                    self.out_slug + '.geojson', driver="GeoJSON", index=False, mode="w"
                )
                logger.info(f"Output file written to: {self.out_slug}.geojson")


# TODO: deprecate/remove (moved into contextmanager)
def output_creation(df_feature, primary_name, feature_list, region_list, data_dir, out_format):
    """
    Save Dataframe to disk
    Currently supports 
        CSV: Comma Separated Values
        GeoJSON: GeoJSON format (including geometry)

    Args:
        df_feature
    """

    region_slug = get_list_slug(region_list) # country code e.g. BJ
    feature_slug = get_list_slug(feature_list)
    
    out_dir = os.path.join(data_dir, "out")  # Output file directory
    out_slug = os.path.join(out_dir, f"{region_slug}_{feature_slug}")
    

    if not os.path.exists(out_dir):
        os.makedirs(
            out_dir, exist_ok=True
        )  # create raw directory

    df_feature.reset_index(drop=True, inplace=True)

    # Generate Files
    if df_feature.empty:
        logger.warning(f"feature data frame empty for {feature_name}")
        return None

    if "csv" in out_format:
        logger.debug("Writing CSV file")
        df_feature.to_csv(out_slug + '.csv')

    if "geojson" in out_format:
        logger.debug("Writing GeoJSON file")
        gdf_feature = convert_pd_to_gdf(df_feature)
        gdf_feature.to_file(out_slug + '.geojson', driver="GeoJSON")

if __name__ == "__main__":

    from earth_osm.filter import get_filtered_data
    from earth_osm.gfk_data import get_region_tuple
    region = "DE"
    primary_name = "power"
    feature_name = "line"
    mp = True
    update = False
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "earth_data")

    primary_dict, feature_dict = get_filtered_data(get_region_tuple(region), primary_name, feature_name, mp, update, data_dir)

    primary_data = primary_dict['Data']
    feature_data = feature_dict['Data']

    df_node = pd.json_normalize(feature_data["Node"].values())
    df_way = pd.json_normalize(feature_data["Way"].values())

#%%
# sort columns by percentage of nan missing values
# df_feature.isna().mean().sort_values(ascending=True)
# move geometry column to second place
# cols = df_feature.columns.tolist()
# cols.insert(1, cols.pop(cols.index('geometry')))
# df_feature = df_feature.reindex(columns= cols)


#%%
# df_feature.isna().mean()*100
# df_feature.info(memory_usage='deep')
# df_feature['Type'].value_counts(dropna=False)

# drop columns thar are all nan, count them before dropping
# logger.debug(f"Dropping {df_way.isna().all().sum()} columns with all NaN (percentage of columns: {df_way.isna().all().sum()/len(df_way.columns):.2%})")
# df_way.dropna(axis=1, how="all", inplace=True)

# drop columns that have 99% nan values
# logger.debug(f"Dropping {df_way.isna().sum().gt(len(df_way)*0.99).sum()} columns out of {len(df_way.columns)} with more than 99% NaN (percentage of columns: {df_way.isna().sum().gt(len(df_way)*0.99).sum()/len(df_way.columns):.2%})")
# df_way.dropna(axis=1, thresh=len(df_way)*0.01, inplace=True)

# element_set = set(primary_feature_element[primary_name][feature_name])
# print(element_set)
# assert element_set <= set(['node', 'way', 'area']), f"Currenly only supports node, way and area. Got {element_set}"
# if set(['way', 'area']) <= element_set: