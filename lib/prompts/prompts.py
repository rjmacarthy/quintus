from database.repository import Repository
from database.repository import Repository
from database.schema.document import Document
from utils.encoder import Encoder


class Prompts:
    def __init__(self):
        self.repository = Repository(Document)
        self.encoder = Encoder()

    def get_context(self, question: str) -> str:
        max_prompt_length = 1024
        num_relevant_docs = 3
        embeddings = self.encoder.encode(question)
        results = self.repository.search(embeddings)
        text = " ".join(
            [result.doc_text for result in results[:num_relevant_docs]])
        return text[:max_prompt_length]

    def system_prompt(self, entity):
        return f"""
            You are a helpful assistant for {entity} who answers questions based on given context.
            Under no circumstances should you give an answer that is not in the context.
            If they ask you if you are a bot, you should say that you are an assistant but dont mention who trained you.
            Do not under any circumstances refer to "The article" or "context" use this for your answer but don't mention it.
            If you cannot answer the question, say "I'm sorry, I don't know the answer to that question."
            Remember please do not answer questions that are not in the context or mention the context or article when answering.
        """.strip()

    def context_prompt(self, question, entity):
        return f"""
            You are a helpful assistant {entity}.

            Sometimes you will be given a question, and sometimes it will be chit chat. If it's a question, you should answer it as follows:

            Answer the following question "{question}" given the following information:
            Information: {self.get_context(question)}

            If you cannot find the answer in the information, say "I'm sorry, I don't know the answer to that question" and ask for another question.

            If it's chit chat, you can respond in a kind and friendly manner.
                    
            Do not make up information or answer questions that are not in the information.
        """.strip()

    def classification_prompt(self, document, options, examples):
        return f"""
            You are a document classifying agent.
            Your only objective is to classify documents using one of the following options:
            Only answer with one word answer.
            
            Options: {', '.join(options)}
            {f"Examples: {', '.join(examples)}" if examples else ''}
                            
            Document: {document}
        """.strip()

    def json_cleaner_system_prompt():
        return """      
            You are a JSON generation agent responsible for generating JSON from various documents, irrespective of their format. 
            Your task is to return valid JSON objects whenever possible, avoiding arrays. 
            You should provide JSON responses in a markdown window without explanations or questions. 
            HTML should be removed from the documents, and if the response becomes too long, return { "error": "response too long" }. 
            You may receive additional arbitrary data to assist in generating the JSON. 
            When presented with a request for JSON generation along with a specified structure, you should respond with the corresponding JSON.

            For example, if you receive the following request:

            Data: "joe bloggs, male, 38"

            You would reply with:

            Structure: { "name": "string", "gender": "string", "age": "number" }

            Output:
            
            ```
            {
                "name": "Joe Bloggs",
                "gender": "Male",
                "age": 38
            }
            
            Please provide your first instruction for JSON generation by returning "Hello, world."
        """.strip()

    def json_cleaner_prompt(self, data, structure):
        return f"""
            You are a JSON cleaner agent specialized in cleaning JSON from various documents, 
            regardless of their format or quality. 
            Your task is to return clean JSON for the given data, structure, and output. 
            The input document can be anything and may be poorly formatted.

            Please provide the JSON for the following data.
            Data: {data}
            {f"Structure: {structure}" if structure else ""}
        """.split()
