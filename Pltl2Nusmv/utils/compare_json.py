import json
import argparse
import pandas as pd
import os


def main(settings):
    file1 = settings['file1']
    file2 = settings['file2']
    dataset = settings['dataset']
    
    name = os.path.basename(dataset)
    
    file1 = pd.read_csv(file1, sep=',')
    file2 = pd.read_csv(file2, sep=',')
    
    
    # print(file1.head())
    # print(file2.head())
    
    file1.sort_values(by=['formula'], inplace=True)
    file2.sort_values(by=['formula'], inplace=True)
    
    # print(file1.head())
    # print(file2.head())
    
    # print(file1.columns)
    # print(file2.columns)
    
    # file1.rename(columns={'result': 'result_nusmv'}, inplace=True)
    
    file_compare = pd.merge(file1, file2, how='left', on='formula')
    
    file_compare['comparison'] = file_compare['result_x'] == file_compare['result_y']
    
    
    with open(dataset, "r") as ifile:
        dataset =  json.load(ifile)
    
    data = {}
    
    
    inconsistensies = list(file_compare['formula'][file_compare['comparison']==False])
    
    print(inconsistensies)
    
    for i in inconsistensies:
        data[i] = [dataset[i]["formula_past"], dataset[i]["controllable"]]
    
    with open(f"inconsistentencies_in_{name}", "w") as ofile:
        json.dump(data, ofile)
        
    
    
    
    
    
    

if __name__ == "__main__": 
    argsparser = argparse.ArgumentParser()
    argsparser.add_argument(
        "-f1",
        "--file1",
        default=None,
        required=True,
        type=str,
        help="The first csv file",
    )
    
    argsparser.add_argument(
        "-f2",
        "--file2",
        default=None,
        required=True,
        type=str,
        help="The second csv file",
    )
    
    argsparser.add_argument(
        "-j",
        "--dataset",
        default=None,
        required=True,
        type=str,
        help="The json file containing the formulas",
    )
    
    settings = vars(argsparser.parse_args())
    
    main(settings)