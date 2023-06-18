
import os
import threading
import glob
import pandas as pd

def main():
    threads = []
    for file in os.listdir():
        if file.endswith(".py") and file != "main.py":
            t = threading.Thread(target=os.system, args=(f"python {file}",))
            t.start()
            threads.append(t)
            
    for thread in threads:
        thread.join()
    path = 'data/*.csv'
    file_list = glob.glob(path)
    dataframes = []

    for file in file_list:
        df = pd.read_csv(file, encoding='latin-1')
        dataframes.append(df)
        

    combined_df = pd.concat(dataframes, axis=0)
    combined_df = combined_df.reset_index(drop=True)
    combined_df.to_csv('data/products.csv', index=False)

if __name__ == "__main__":
    main()