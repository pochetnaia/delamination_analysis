import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import napari
from matplotlib.lines import Line2D

def get_absolute_timing(df_temp, event_reference, events, timing_reference, dt=5):
    
    """
    This function retuns absolute timing of the event from the dataframe
    """
    
    row = event_reference[0]
    division_number = event_reference[1]
    
    df_filtered = df_temp[ (df_temp.loc[:, 'row'] == row) & (df_temp.loc[:, 'division_number'] == division_number)]
    
    frames_reference = df_filtered.loc[:,['frame']].values
    frame_reference = np.mean(frames_reference)
    
    

    
    frames_final = []
    timings = []
    
    # Gather the absolute timings for all new events
    for event in events: 
        

        #Gather the mean frame
        frames = df_temp[(df_temp["row"] == event[0]) & (df_temp['division_number'] == event[1])].loc[:,['frame']].values
        # contains the mean frame
        frame = np.mean(frames)
        
        
        delta_frames  = frame - frame_reference
        delta_timing = delta_frames * dt
        
        #Estimate its timing (you will use dt)
        timing = timing_reference + delta_timing
        
    
        frames_final.append(frame)
        timings.append(timing)
    
    
    return frames_final, timings

def get_mean(animal_names, frame_number, absolute_timimg, timings_paths, division_number, row):
    
    """
    Returns the mean value of absolute timing per event
    """
    
    # Convert the paths to names
    names = [j.split("/")[-1][:-4] for j in  timings_paths]
    
    list_means = []
    
    # For each animal that ze want to study (in animal_names)
    for i in range(len(animal_names)):
        
        # Fetch the position of thqt animal in the list
        idx = names.index(animal_names[i])
        
        # read the csv associated to it
        df_temp = pd.read_csv(timings_paths[idx])

        # get the mean value for a divisionnumber and row specified
        df_filtered = df_temp[ (df_temp['row'] == row) & (df_temp['division_number'] == division_number)]
        
        #display(df_filtered)
        frames = df_filtered["frame"]
        frames  = absolute_timimg - 5 * (frame_number[i] - frames)
        
        #print(frames)
        mean = frames.mean()
        #print(mean)

        
        list_means.append(mean)
    list_means = np.array(list_means)
        

    return list_means.mean()

#Rescaling the plot for delamination
#Finding mean of medians per each event
#Declaring function for this purpose. It's like get_mean, but for median
def get_median(animal_names, frame_number, absolute_timimg, timings_paths, division_number, row):
    
    """
    Returns the median value of absolute timing per event
    """
    
    # Convert the paths to names
    names = [j.split("/")[-1][:-4] for j in  timings_paths]
    list_medians = []
    
    # For each animal that ze want to study (in animal_names)
    for i in range(len(animal_names)):
        
        # Fetch the position of thqt animal in the list
        idx = names.index(animal_names[i])
        
        # read the csv associated to it
        df_temp = pd.read_csv(timings_paths[idx])

        # get the mean value for a divisionnumber and row specified
        df_filtered = df_temp[ (df_temp['row'] == row) & (df_temp['division_number'] == division_number)]
        frames = df_filtered["frame"]
        frames  = absolute_timimg - 5 * (frame_number[i] - frames)
        median = frames.median()

        list_medians.append(median)
    list_medians = np.array(list_medians)

    return list_medians.mean()

def get_frame_using_etalon(df_temp, event_reference, timing_reference, timing_desired, dt=5):
    
    
    row = event_reference[0]
    division_number = event_reference[1]
    
    df_filtered = df_temp[ (df_temp.loc[:, 'row'] == row) & (df_temp.loc[:, 'division_number'] == division_number)]
    
    frames_reference = df_filtered.loc[:,['frame']].values
    frame_reference = np.mean(frames_reference)
    
    frame_difference = (timing_desired - timing_reference) / dt
    
    
    
    return frame_reference + frame_difference
    