import sys, re, trafilatura, requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import os
from mistralai import Mistral
from decouple import config


lang = "Russian"
chunk_size = int(config('SCRAPECHUNKSIZE'))


def split_user_input(text):
    # Split the input text into paragraphs
    paragraphs = text.split('\n')
    # Remove empty paragraphs and trim whitespace
    paragraphs = [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]
    return paragraphs

def scrape_text_from_url(url):
    """
    Scrape the content from the URL
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        text = trafilatura.extract(downloaded, include_formatting=True)
        if text is None:
            return []
        text_chunks = text.split("\n")
        article_content = [text for text in text_chunks if text]
        return article_content
    except Exception as e:
        print(f"Error: {e}")

def summarize(text_array):
    """
    Summarize the text using GPT API
    """
    def create_chunks(paragraphs):
        chunks = []
        chunk = ''
        for paragraph in paragraphs:
            if len(chunk) + len(paragraph) < chunk_size:
                chunk += paragraph + ' '
            else:
                chunks.append(chunk.strip())
                chunk = paragraph + ' '
        if chunk:
            chunks.append(chunk.strip())
        return chunks

    try:
        text_chunks = create_chunks(text_array)
        text_chunks = [chunk for chunk in text_chunks if chunk] # Remove empty chunks

        # Call the GPT API in parallel to summarize the text chunks
        summaries = []
        system_messages = [
            {"role": "system", "content": "You are an expert in creating summaries that capture the main points and key details."},
            {"role": "system", "content": f"You will show the bulleted list content without translate any technical terms."},
            {"role": "system", "content": f"You will print all the content in {lang}."},
        ]
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(call_gpt_api, f"Summary keypoints for the following text:\n{chunk}", system_messages) for chunk in text_chunks]
            for future in tqdm(futures, total=len(text_chunks), desc="Summarizing"):
                summaries.append(future.result())

        if len(summaries) <= 5:
            summary = ' '.join(summaries)
            with tqdm(total=1, desc="Final summarization") as progress_bar:
                final_summary = call_gpt_api(f"Create a bulleted list using {lang} to show the key points of the following text:\n{summary}", system_messages)
                progress_bar.update(1)
            return final_summary
        else:
            return summarize(summaries)
    except Exception as e:
        print(f"Error: {e}")
        return "Unknown error! Please contact the developer."

def call_gpt_api(prompt, additional_messages=[]):
    """
    Call GPT API
    """
    messages = additional_messages+[{"role": "user", "content": prompt}]
    client = Mistral(api_key=config('MISTRALTOK'))

    chat_response = client.chat.complete(
        model= 'mistral-large-latest',
        messages=messages
    )
    return chat_response.choices[0].message.content if chat_response is not None else None
    

def process_user_input(user_input):
    url_patterns = re.compile(r"https?://")
    url_pattern = re.compile(r"http?://")

    if url_patterns.match(user_input) or url_pattern.match(user_input):
        text_array = scrape_text_from_url(user_input)
    else:
        text_array = split_user_input(user_input)

    return text_array

def main():
    args = sys.argv
    if args[1]:
        text_array = process_user_input(args[1])
        print(summarize(text_array))

if __name__ == '__main__':
    main()