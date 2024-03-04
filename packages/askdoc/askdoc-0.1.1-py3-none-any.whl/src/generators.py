from .engines import LLM, LVM

localhost = 'http://127.0.0.1:8002/v1/'

sys_prompt = [
    "You are an assistant to a general physician. You ALWAYS answer in just one word, YES OR NO.",
    "On receiving a query from me, consider the complete conversation and answer in one word if",
    "the latest user query is a medical query or not that a general physician can answer."
]

verify = LLM(
    model_id='biomistral',
    uri=localhost,
    messages=[{'role': 'system', 'content': ' '.join(sys_prompt)}]
)

sys_prompt = [
    "Presume the role of a general physician.",
    "You should ALWAYS ask me questions to help with the diagnosis of my medical condition.",
    "You should respond with a diagnosis only when you have sufficient knowledge.",
    "Otherwise always ask me more questions to collect more data about my condition.",
    "Do not ask too many questions in one go otherwise I will get overwhelmed.",
    "Ask me 1-2 questions when required in each turn.",
    "You should take more turns asking me questions to arrive at a diagnostic.",
    "Be very empathetic to me while asking or suggesting things.",
    "I might provide some context from my medical reports. You can choose to use that context to reply.",
    "NEVER GIVE ME ANY ADVICE ON MEDICINE OR ANY PRESCRIPTION."
]

medical = LVM(model_id='gpt-4-vision-preview')
medical._add_assistant_msg(msg=' '.join(sys_prompt), role='system')

sys_prompt = [
    "Following is a conversation between a general physician doctor and a patient.",
    "Your task is to summarize the conversation."
    "The summary should include all the important details like what issues was the patient facing.",
    "And what solution or dicussions did the doctor provide."
    "Start with, ",
    "Summary of the past conversation: <actual summary>"
]
summarizer = LLM(
    model_id='biomistral',
    uri=localhost,
    messages=[{'role': 'system', 'content': ' '.join(sys_prompt)}]
)
