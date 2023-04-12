from utils.processor import Processor


def simple_prompt(question, store):
    max_prompt_length = 1024
    results = store.search(question)
    text = results[0].doc_text
    url = results[0].doc_url
    processor = Processor()
    context = processor.html_to_text(text)
    context = context[:max_prompt_length]
    prompt = f"""
      Url: {url}
      Context: {context}
      Question: {question}
    """
    return prompt
