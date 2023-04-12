from utils.processor import Processor


def simple_prompt(question, store):
    max_context_length = 500
    print("Searching for context...", question)
    results = store.search(question)
    text = results[0].doc_text
    processor = Processor()
    context = processor.html_to_text(text)
    context = context[:max_context_length]
    prompt = f"""
      You are a customer support representative, using the following context:
      Context: {context}
        
      Answer the question:
      Question: {question}
      
      Only reply with the answer to the question above and if you don't know the answer, reply with "Sorry, I don't know".
    """
    return prompt
