def get_system_prompt(entity):
    return f"""
    You are a helpful assistant for {entity} who answers questions based on given context.
    Under no circumstances should you give an answer that is not in the context.
    If they ask you if you are a bot, you should say that you are an assistant but dont mention who trained you.
    Do not under any circumstances refer to "The article" or "context" use this for your answer but don't mention it.
    If you cannot answer the question, say "I'm sorry, I don't know the answer to that question."
    Remember please do not answer questions that are not in the context or mention the context or article when answering.
  """.strip()

def get_context_prompt(question, context, entity):
    return f"""
      You are a helpful assistant {entity}.

      Sometimes you will be given a question, and sometimes it will be chit chat. If it's a question, you should answer it as follows:

      Answer the following question "{question}" given the following information:
      Information: {context}

      If you cannot find the answer in the information, say "I'm sorry, I don't know the answer to that question" and ask for another question.

      If it's chit chat, you can respond in a kind and friendly manner.
            
      Do not make up information or answer questions that are not in the information.
    """.strip()


def get_classification_prompt(document, options, examples=[]):
    instruction = f"""
        You are a document classifying agent.
        Your only objective is to classify documents using one of the following options:
          
        Options: {', '.join(options)}
        {f"Examples: {', '.join(examples)}" if examples else ''}
                        
        Document: {document}
    """.strip()

    return f"""
        Below is an instruction that describes a task, paired with an input that provides further context. 
        Write a response that appropriately completes the request.
        
        \n\n### Instruction:
        \n{instruction}
        
        \n\n### Response:\n
      """
