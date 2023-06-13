#!/usr/bin/env python
# coding: utf-8
# Created by AMIN TORABI
# 06/13/2023



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


def main():
    input_location = 'P:/2022\Albany/21250022_070_Embankment Breach Modeling and Risk Assessment (Att. B)/03-SEProducts/02-Calcs/06- Systematic breach code/Input'
    output_location = 'P:/2022/Albany/21250022_070_Embankment Breach Modeling and Risk Assessment (Att. B)/03-SEProducts/02-Calcs/06- Systematic breach code/output'
    list_csv = input_df(input_location)
    results_summary = pd.DataFrame(columns=['ID', 'Less than 1 ft', 'greater than 1 ft', 'Judgment'])

    for i, item in enumerate(list_csv):
        # Read CSV
        df = pd.read_csv(item)
        
        # Calculate ACER values for CSV
        df = calculate_ACER(df)

        # Assign colors based on ACER values
        df['ACER_Colors'] = np.where(df['ACER'] == 'Low Danger, Less than 1 ft', 'green',
                                     np.where(df['ACER'] == 'Low Danger, greater than 1 ft', 'yellow', 'red'))

        # Plot data
        plot_data(df, output_location,i)

        # Count the occurrences of each unique value in 'ACER' column
        value_counts = df['ACER'].value_counts()
        
        # Create a row with the counts for each unique value
        row = [i, value_counts.get(2, 0), value_counts.get(1, 0), value_counts.get(0, 0)]
    
        # Append the row to the results_summary DataFrame
        results_summary.loc[len(results_summary)] = row

    # Reset the index of the DataFrame
    results_summary.reset_index(drop=True, inplace=True)
    results_summary = results_summary.iloc[:, 1:]
    save_csv(results_summary, output_location)


def input_df(location):
    list_csv = []
    for filename in os.listdir(location):
        if filename.endswith('.csv'):
            # Read the CSV
            df_file = os.path.join(location, filename)
            list_csv.append(df_file)
    return list_csv



def categorize_ACER(velocity, depth):
    judgea = 0.0004
    judgeb = -0.0118
    judgec = -0.0841
    judged = 3.1364
    higha = 0.0008
    highb = -0.0284
    highc = 0.0223
    highd = 6.0179
    
    
    if ((depth < judgea * velocity ** 3 + judgeb * velocity ** 2 + judgec * velocity + judged) and (depth <= 1)):
        ACER = "Low Danger, Less than 1 ft"
    elif ((depth < judgea * velocity ** 3 + judgeb * velocity ** 2 + judgec * velocity + judged) and (depth > 1)):
        ACER = "Low Danger, greater than 1 ft"    
    # elif (depth < higha * velocity ** 3 + highb * velocity ** 2 + highc * velocity + highd):
    #     ACER = "Judgment"
    else:
        ACER = "Judgment"

    return ACER



def calculate_ACER(df):
    df['ACER'] = df.apply(lambda row: categorize_ACER(row['Water_Velocity_ft_s'], row['Water_Depth_ft']), axis=1)
    return df



def plot_data(df, output_location,i):
    judgea = 0.0004
    judgeb = -0.0118
    judgec = -0.0841
    judged = 3.1364
    higha = 0.0008
    highb = -0.0284
    highc = 0.0223
    highd = 6.0179
    velocity = np.linspace(0, 25, 500)
    depth1 = judgea * velocity ** 3 + judgeb * velocity ** 2 + judgec * velocity + judged
    depth2 = higha * velocity ** 3 + highb * velocity ** 2 + highc * velocity + highd

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(velocity, depth1, label='Low Danger')
    ax.plot(velocity, depth2, label='Judgment')
    ax.scatter(df['Water_Velocity_ft_s'], df['Water_Depth_ft'], c=df['ACER_Colors'])

    ax.legend()
    ax.grid(True, linestyle=':')
    ax.set_xlim([0, 25])
    ax.set_ylim([0, 10])
    ax.text(3, 1, 'Low Danger Zone', fontsize=12)
    ax.text(6, 3.4, 'Judgment Zone', fontsize=12)
    ax.text(10, 7, 'High Danger Zone', fontsize=12)
    ax.set_xlabel('Velocity')
    ax.set_ylabel('Depth')

    plt.savefig(os.path.join(output_location, f'plot_{i}.png'))
    plt.close()



def save_csv(df, location):
    print(df)
    Summary_Data_File_Path = os.path.join(location, "Summary_Results.csv")
    df.to_csv(Summary_Data_File_Path)


if __name__ == '__main__':
    main()

