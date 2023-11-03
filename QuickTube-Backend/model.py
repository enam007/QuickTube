import g4f
import concurrent.futures
import asyncio

print(g4f.Provider.Ails.params)


def get_summary(text):
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        provider=g4f.Provider.DeepAi,
        messages=[{"role": "user", "content": "Summarize it in bullets and give short title(mandatory)" + text}],
        stream=True,
    )
    result_string = " "
    for message in response:
        result_string += message
    return result_string

def process_row(text):
    #print(row)
    #asyncio.set_event_loop(asyncio.new_event_loop())
    summary = get_summary(text)  # Access the 'text' column
    return summary

def createSummary(text):
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        summaries = list(executor.map(process_row, text))
    
    return summaries


# Add the summaries to your DataFrame


