import numpy as np
import re
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer


def scaling(dataframe):
    """
    Perform data scaling using StandardScaler.

    Arguments:
    dataframe: Pandas DataFrame containing the data to be scaled.

    Return:
    prep_data: Scaled data.
    scaler: StandardScaler object used for scaling.
    """
    scaler=StandardScaler()
    prep_data=scaler.fit_transform(dataframe.iloc[:,6:15].to_numpy())
    return prep_data,scaler

def nn_predictor(prep_data):
    """
    Build and train a nearest neighbors model.

    Arguments:
    prep_data: Scaled data used to train the model.

    Returns:
    neigh: Trained NearestNeighbors model.
    """
    neigh = NearestNeighbors(metric='cosine',algorithm='brute')
    neigh.fit(prep_data)
    return neigh

def build_pipeline(neigh,scaler,params):
    """
    Build a pipeline for preprocessing and prediction.

    Arguments:
    neigh: Trained NearestNeighbors model.
    scaler: StandardScaler object used for scaling.
    params: Parameters for NearestNeighbors.

    Returns:
    pipeline: Pipeline object for preprocessing and prediction.
    """
    transformer = FunctionTransformer(neigh.kneighbors,kw_args=params)
    pipeline=Pipeline([('std_scaler',scaler),('NN',transformer)])
    return pipeline

def extract_data(dataframe,ingredients):
    """
    Extract relevant data based on ingredients.

    Arguments:
    dataframe: Original DataFrame containing recipe data.
    ingredients: List of ingredients to filter data.

    Returns:
    extracted_data: Extracted DataFrame based on ingredients.
    """
    extracted_data=dataframe.copy()
    extracted_data=extract_ingredient_filtered_data(extracted_data,ingredients)
    return extracted_data
    
def extract_ingredient_filtered_data(dataframe,ingredients):
    """
    Filter DataFrame based on ingredients.

    Arguments:
    dataframe: Original DataFrame containing recipe data.
    ingredients: List of ingredients to filter data.

    Returns:
    extracted_data: Filtered DataFrame based on ingredients.
    """
    extracted_data=dataframe.copy()
    regex_string=''.join(map(lambda x:f'(?=.*{x})',ingredients))
    extracted_data=extracted_data[extracted_data['RecipeIngredientParts'].str.contains(regex_string,regex=True,flags=re.IGNORECASE)]
    return extracted_data

def apply_pipeline(pipeline,_input,extracted_data):
    """
    Apply the pipeline for preprocessing and prediction.

    Args:
    pipeline: Pipeline object for preprocessing and prediction.
    _input: Input data for prediction.
    extracted_data: DataFrame containing extracted data.

    Returns:
    Extracted recipe based on the input.
    """
    _input=np.array(_input).reshape(1,-1)
    return extracted_data.iloc[pipeline.transform(_input)[0]]

def recommend(dataframe,_input,ingredients=[],params={'n_neighbors':5,'return_distance':False}):
    """
    Generate recipe recommendations based on input data.

    Arguments:
    dataframe: Original DataFrame containing recipe data.
    _input: Input data for recommendation.
    ingredients: List of ingredients to consider.
    params: Parameters for recommendation.

    Returns:
    Recommended recipes based on input data.
    """
        extracted_data=extract_data(dataframe,ingredients)
        if extracted_data.shape[0]>=params['n_neighbors']:
            prep_data,scaler=scaling(extracted_data)
            neigh=nn_predictor(prep_data)
            pipeline=build_pipeline(neigh,scaler,params)
            return apply_pipeline(pipeline,_input,extracted_data)
        else:
            return None

def extract_quoted_strings(s):
    """
    Extract strings enclosed in double quotes from a given string.

    Arguments:
    s: Input string containing quoted strings.

    Returns:
    List of strings enclosed in double quotes.
    """
    # Find all of the strings inside double quotes
    strings = re.findall(r'"([^"]*)"', s)
    # Join the recommended strings with 'and'
    return strings

def output_recommended_recipes(dataframe):
    if dataframe is not None:
        output=dataframe.copy()
        output=output.to_dict("records")
        for recipe in output:
            recipe['RecipeIngredientParts']=extract_quoted_strings(recipe['RecipeIngredientParts'])
            recipe['RecipeInstructions']=extract_quoted_strings(recipe['RecipeInstructions'])
    else:
        output=None
    return output

