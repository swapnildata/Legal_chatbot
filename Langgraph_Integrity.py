from langgraph.graph import StateGraph, END
from typing import List, TypedDict
from langchain_core.messages import BaseMessage
from datetime import datetime

class LegalBotState(TypedDict):
    messages: List[BaseMessage]
    timestamp: str
    category: str
    response: str

class LegalChatbot:
    def __init__(self, llm, legal_categories: List[str]):
        self.llm = llm
        self.legal_categories = legal_categories
        self.graph = self.buildGraph()

    def classifyIssue(self):
        def inner(state):
            # Join all messages content in state to provide full context
            full_convo = "\n".join(msg.content for msg in state["messages"])
            prompt = (
                "You are a legal expert. Classify the user's issue into one of the following categories. "
                "Just give one word of classification. No explanation required: "
                f"{', '.join(self.legal_categories)}.\n\nConversation:\n{full_convo}"
                )
            response = self.llm.invoke(prompt)
            state["category"] = response.content.strip()
            return state
        return inner

    def provideGuidance(self, state):
        full_convo = "\n".join(msg.content for msg in state["messages"])
        category = state["category"]
        prompt = (
            f"Category: {category}\n\n"
            f"Conversation:\n{full_convo}\n\n"
            "As you are legal advisor, provide me legal advice, suggested steps, actions, and links if applicable. In response no need of mention your responsibility."
            "Response must be coherent and should be approx 5 lines."
            )
        response = self.llm.invoke(prompt)
        state["response"] = response.content.strip()
        return state


    def buildGraph(self):
        graph = StateGraph(LegalBotState)
        graph.add_node("classify", self.classifyIssue())
        graph.add_node("guide", self.provideGuidance)
        graph.set_entry_point("classify")
        graph.add_edge("classify", "guide")
        graph.add_edge("guide", END)
        return graph.compile()

    def run(self, messages: List[BaseMessage]) -> dict:
        state = {
            "messages": messages,
            "timestamp": str(datetime.now())
        }
        result = self.graph.invoke(state)
        return {
            "category": result["category"],
            "guidance": result["response"],
            "timestamp": result["timestamp"]
        }
