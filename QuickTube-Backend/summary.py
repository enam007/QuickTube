import utils
import model
import asyncio
import g4f
import concurrent.futures
print(g4f.Provider.Ails.params)
import pandas as pd




def get_Summary(url):
    video_type = utils.identify_video_service(url)
    video_id = utils.extract_video_id(url,video_type)
    df,start = utils.get_video_caption(video_id,video_type)
    print("columns",df.columns)
    ### first Iteration
    data_summary = utils.sample_data(df,10,"text")
    #start = df.loc[0, 'start_time']
    print("sttttttttttttttttttttttttttttttttttttttttttttttttt",start)
    if start.time().minute>0:
        data_summary.at[0, 'start'] = start
    text_data = data_summary['text'].tolist()
    summary = model.createSummary(text_data)
    data_summary['summary'] = summary
    print("Columnssssssss",data_summary.columns)

   
    ## 2nd Iteration
    data_summary_copy = data_summary.copy()
    data_summary.set_index("start", inplace=True)
    print("Columnssssssssafterindex",data_summary_copy.columns)
    print("Columnssssssssafterindex",data_summary.columns)
    data_overview = utils.sample_data(data_summary,60,"summary")
    summary_data = data_overview['summary'].tolist()
    # print("===================================",data.itertuples())
    overview = model.createSummary(summary_data)
    data_overview['overview'] = overview
    print("Columnsssssssso",data_overview.columns)
    merged_df = utils.mergeDf(data_summary_copy,data_overview)
    data = utils.makeJson(merged_df) 
    return data













