from scipy.ndimage import gaussian_filter
from PIL import Image
import plotly.graph_objects as go
import numpy as np
import math
import pandas as pd
import plotly.express as px
import plotly.offline as py
from coverage_figure import CoverageFigure

def normalize(min, max, x):
    a = 26
    b = 255
    return (b-a) * (x - min)/(max - min) + a

def resize(size, img,visulization):
    img = img.resize(size)
    img.save(visulization+".png")
    return img


def create_scatter(scatter_df,group,visulization):
    avg_workload = scatter_df['Dilation'].mean()
    print(avg_workload)
    for index,row in scatter_df.iterrows():
        if(row['Dilation'] >=avg_workload):
            scatter_df.loc[index,"Flag"]=1
        else:
            scatter_df.loc[index,"Flag"]=0
    

    
    fig = go.Figure(data=go.Scatter(
            x=scatter_df["X"],
            y=scatter_df["Y"],
            mode='markers',
            marker=dict(
            size=scatter_df["Dilation"]*2,
            color=scatter_df["Flag"], #set color equal to a variable
            colorscale='Viridis', # one of plotly colorscales
            showscale=False
    )
    ))
    print("Generating scatter plot")
    fig.update_layout(title="Cognitive workload for Group - "+group)
    py.plot(fig,filename="AOI_Scatter_plot_Output/Output/"+group+"_"+visulization+".png")
    
"""
Create heatmap trace
"""
def create_heatmap(fxd_data, group,visulization):
    print("Creating Total Fixation Trace+NOW")
    #print(fxd_data.head)
    indexNames = fxd_data[(fxd_data['ScreenX'] >1064 ) &(fxd_data['ScreenY'] >768)].index
    fxd_data.drop(indexNames,inplace=True)
    #print(fxd_data.shape)
    img = Image.open(visulization+".png")
    img = resize((1600, 1200), img,visulization)
    img = img.convert('RGBA')
    pixels = np.array(img)

    zList = [[0 for x in range(2000)] for y in range(2000)]
    fxd_data= fxd_data[fxd_data['ScreenX'] <1600]
    fxd_data= fxd_data[fxd_data['ScreenY'] <1600]
    print(fxd_data.shape)
    for index, row in fxd_data.iterrows():
        
        cx = row['ScreenX']
        cy = row['ScreenY']
        z = row['Duration']
        r = 25
       # print(cx)
        for x in range(cx - r-1, cx + r-1):
            for y in range(cy - r-1, cy + r-1):
                d = math.sqrt((cx - x) ** 2 + (cy - y) ** 2)
                
                if d <= r and zList[y][x] < 1200:
                    zList[y][x] = zList[y][x] + float(z)

    blurred = gaussian_filter(zList, sigma = 25)
    

    min = 0
    max = np.amax(blurred)
    for i in range(len(pixels)):
        for j in range(len(pixels[0])):
                pixels[i][j][3] = normalize(min, max, blurred[i][j])

    img = Image.fromarray(pixels)
    
    print("Saving Image")
    img.save("AOI_Scatter_plot_Output/AOI_"+group+"_"+visulization+".png")

"""
Main function to create figures and its components
"""
if __name__ == '__main__':
    TIMESTEP = 10000

    WIDTH = 1600
    HEIGHT = 1200
    fList = [   ["O1V1","fixation_o1v1.csv","csvfilesforpupildilation/groupO1V1.csv","Tree"],
                ["O1V2","fixation_o1v2.csv","csvfilesforpupildilation/groupO1V2.csv","Graph"],
                ["O2V1","fixation_o1v2.csv","csvfilesforpupildilation/groupO2V1.csv","Tree"],
                ["O2V2","fixation_o2v2.csv","csvfilesforpupildilation/groupO2V2.csv","Graph"]]
    
    fileList=pd.DataFrame(fList, columns = ['Group','fixationPath',"CognitionPath","Visulization"])
    fixColNames = ["number", "time", "duration", "x", "y"]
    
    for index, row in fileList.iterrows():
        fixationFile = row['fixationPath']
        fixColNames = ["number", "time", "duration", "x", "y"]
        df = pd.read_csv(fixationFile)
        indexNames = df[(df['ScreenX'] >1600 ) &(df['ScreenY'] >1200)].index
        df.drop(indexNames,inplace=True)  
        print("Creating heatmap for"+row['Group'])
        trace = []
        #create_heatmap(df,row['Group'],row["Visulization"])
        print("Creating scatter"+row['Group'])
        scatterPath=row["CognitionPath"]
        scatter_df=pd.read_csv(scatterPath,names=["X","Y","Dilation"],header=None)
        create_scatter(scatter_df,row['Group'],row["Visulization"])
        print("Scatter finished")
        
print("Finished finally")
    
    