"""
RAG Pipeline for QC Expert Agent
Uses LangChain with the unified QCDB API for retrieval.
"""

import os
from pathlib import Path
from typing import List, Dict, Optional
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import Chroma
from langchain.llms.base import LLM
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema import Document
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent / "api"))
from unified_qc_api import UnifiedQCAPI


class QCDBEmbeddings(Embeddings):
    """Wrapper for QCDB embedding manager to work with LangChain."""
    
    def __init__(self, qcbd_root: str = None):
        from qcdb_embeddings import EmbeddingManager
        self.embedding_mgr = EmbeddingManager(qcbd_root=qcbd_root)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        return [self.embedding_mgr.embed(text) for text in texts]
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query."""
        return self.embedding_mgr.embed(text)


class QCExpertRAG:
    """Retrieval-Augmented Generation pipeline for QC expert agent."""
    
    def __init__(
        self,
        qcbd_root: str = None,
        llm: LLM = None,
        top_k: int = 5
    ):
        """Initialize RAG pipeline.
        
        Args:
            qcbd_root: Path to QCDB root directory
            llm: LangChain LLM instance (defaults to OpenAI)
            top_k: Number of documents to retrieve
        """
        self.qcbd_root = Path(qcbd_root or os.environ.get('QCBD_ROOT',
                                                          r'G:\My Drive\Databases\QCBD'))
        self.top_k = top_k
        
        # Initialize API
        self.api = UnifiedQCAPI(qcbd_root=str(self.qcbd_root))
        
        # Initialize LLM
        if llm is None:
            from langchain.chat_models import ChatOpenAI
            self.llm = ChatOpenAI(
                model="gpt-4",
                temperature=0.1,  # Low temperature for factual responses
                openai_api_key=os.environ.get('OPENAI_API_KEY')
            )
        else:
            self.llm = llm
        
        # Load system prompt
        prompt_path = self.qcbd_root / "qc_expert_agent_prompt.txt"
        with open(prompt_path, 'r', encoding='utf-8') as f:
            self.system_prompt = f.read()
        
        # Initialize conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
    
    def _format_kb_context(self, retrieved_docs: List[Dict]) -> str:
        """Format retrieved knowledge base entries for prompt."""
        context_parts = []
        
        for i, doc in enumerate(retrieved_docs, 1):
            entity_type = doc['metadata'].get('entity_type', 'Unknown')
            entity_id = doc['id']
            
            context_parts.append(f"[QC-KB CONTEXT {i}]")
            context_parts.append(f"Entity Type: {entity_type}")
            context_parts.append(f"Entity ID: {entity_id}")
            context_parts.append(f"Similarity: {doc.get('similarity', 0):.3f}")
            context_parts.append("")
            context_parts.append(doc['text'])
            context_parts.append("")
            context_parts.append("[QC-KB CONTEXT END]")
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def _retrieve_context(self, query: str, entity_types: List[str] = None) -> List[Dict]:
        """Retrieve relevant context for a query."""
        # Semantic search
        results = self.api.semantic_search(
            query=query,
            entity_types=entity_types,
            top_k=self.top_k
        )
        
        # Enhance with related entities from Neo4j
        enhanced_results = []
        for result in results:
            enhanced_results.append(result)
            
            # If it's a method, add benchmark performance
            if result['metadata'].get('entity_type') == 'Method':
                method_id = result['id']
                details = self.api.get_method_details(method_id)
                if details and 'validated_on' in details:
                    for benchmark in details['validated_on'][:2]:  # Top 2 benchmarks
                        benchmark_perf = self.api.get_benchmark_performance(
                            benchmark['id']
                        )
                        if 'error' not in benchmark_perf:
                            enhanced_results.append({
                                'id': f"benchmark_{benchmark['id']}",
                                'text': f"Benchmark: {benchmark['name']}\n{benchmark_perf}",
                                'metadata': {'entity_type': 'Benchmark'},
                                'similarity': result['similarity'] * 0.8  # Slightly lower relevance
                            })
        
        return enhanced_results[:self.top_k]  # Limit to top_k total
    
    def query(
        self,
        question: str,
        entity_types: List[str] = None,
        include_citations: bool = True
    ) -> Dict[str, str]:
        """Answer a question using RAG.
        
        Args:
            question: User's question
            entity_types: Optional filter for entity types
            include_citations: Whether to include KB citations
        
        Returns:
            Dictionary with 'answer' and optionally 'citations'
        """
        # Retrieve context
        retrieved_docs = self._retrieve_context(question, entity_types)
        
        if not retrieved_docs:
            return {
                'answer': "I couldn't find relevant information in the knowledge base for your question. Could you rephrase or provide more context?",
                'citations': []
            }
        
        # Format context
        kb_context = self._format_kb_context(retrieved_docs)
        
        # Build prompt
        prompt_template = f"""
{self.system_prompt}

---

**Retrieved Knowledge Base Context:**

{kb_context}

---

**User Question:** {question}

**Instructions:**
- Ground your answer in the retrieved KB context above
- Cite specific entity IDs when making claims
- If the context doesn't fully answer the question, say so
- Provide actionable guidance
- Use appropriate technical level for the question

**Your Answer:**
"""
        
        # Generate response
        response = self.llm.predict(prompt_template)
        
        # Extract citations
        citations = []
        if include_citations:
            for doc in retrieved_docs:
                citations.append({
                    'entity_id': doc['id'],
                    'entity_type': doc['metadata'].get('entity_type'),
                    'similarity': doc.get('similarity', 0),
                    'text_preview': doc['text'][:200] + "..."
                })
        
        return {
            'answer': response,
            'citations': citations,
            'num_sources': len(retrieved_docs)
        }
    
    def conversational_query(self, question: str) -> Dict[str, str]:
        """Answer with conversation memory.
        
        Maintains context across multiple turns.
        """
        # Retrieve context
        retrieved_docs = self._retrieve_context(question)
        kb_context = self._format_kb_context(retrieved_docs)
        
        # Build conversational prompt
        prompt_template = PromptTemplate(
            input_variables=["chat_history", "question", "context"],
            template=f"""
{self.system_prompt}

**Previous Conversation:**
{{chat_history}}

**Retrieved Context:**
{{context}}

**User Question:** {{question}}

**Your Answer:**
"""
        )
        
        # Create conversational chain
        chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            memory=self.memory,
            retriever=None,  # We handle retrieval manually
            combine_docs_chain_kwargs={"prompt": prompt_template}
        )
        
        # Generate response
        response = chain({
            "question": question,
            "context": kb_context
        })
        
        return {
            'answer': response['answer'],
            'num_sources': len(retrieved_docs)
        }
    
    def explain_method(self, method_id: str) -> str:
        """Explain a computational method in detail."""
        # Get full method details
        method = self.api.get_method_details(method_id)
        
        if not method:
            return f"Method '{method_id}' not found in knowledge base."
        
        # Get prerequisites
        prerequisites = self.api.get_method_prerequisites(method_id)
        
        # Build explanation query
        question = f"Explain the {method['name']} method in detail, including its theoretical basis, strengths, weaknesses, and when to use it."
        
        # Use query with method as context
        result = self.query(question, entity_types=['Method', 'Concept'])
        
        # Enhance with structured data
        answer = result['answer']
        answer += f"\n\n**Structured Information:**"
        answer += f"\n- **Computational Cost:** {method.get('computational_cost', 'N/A')}"
        answer += f"\n- **Accuracy Level:** {method.get('accuracy_level', 'N/A')}"
        
        if prerequisites:
            answer += f"\n- **Prerequisites to Understand:** {', '.join([p['name'] for p in prerequisites[:5]])}"
        
        if method.get('implemented_in'):
            tools = [t['name'] for t in method['implemented_in']]
            answer += f"\n- **Available in Software:** {', '.join(tools)}"
        
        return answer
    
    def suggest_workflow(self, task_description: str) -> str:
        """Suggest a workflow for a computational task."""
        # Retrieve workflow
        results = self.api.semantic_search(
            query=task_description,
            entity_types=['Workflow'],
            top_k=3
        )
        
        if not results:
            return "No suitable workflow found. Could you describe your task in more detail?"
        
        # Get full details for top match
        workflow_id = results[0]['id']
        
        with self.api.neo4j_driver.session() as session:
            result = session.run("""
                MATCH (w:Workflow {id: $id})
                OPTIONAL MATCH (w)-[:RELATED_TO]->(m:Method)
                OPTIONAL MATCH (w)-[:SUPPORTS]->(t:SoftwareTool)
                RETURN w, collect(DISTINCT m) AS methods, collect(DISTINCT t) AS tools
            """, id=workflow_id)
            
            record = result.single()
            if not record:
                return "Workflow details not available."
            
            workflow = dict(record['w'])
            methods = [dict(m) for m in record['methods']]
            tools = [dict(t) for t in record['tools']]
        
        # Format response
        response = f"**Recommended Workflow:** {workflow['name']}\n\n"
        response += f"{workflow.get('description', '')}\n\n"
        
        if 'steps' in workflow:
            response += "**Steps:**\n"
            for i, step in enumerate(workflow['steps'], 1):
                response += f"{i}. {step}\n"
            response += "\n"
        
        if methods:
            response += f"**Recommended Methods:** {', '.join([m['name'] for m in methods])}\n\n"
        
        if tools:
            response += f"**Supported Software:** {', '.join([t['name'] for t in tools])}\n\n"
        
        if 'pitfalls' in workflow:
            response += "**Common Pitfalls:**\n"
            for pitfall in workflow['pitfalls']:
                response += f"- {pitfall}\n"
        
        return response


# ==================== Convenience Functions ====================

def quick_ask(question: str) -> str:
    """Quick question-answer (no conversation memory)."""
    rag = QCExpertRAG()
    result = rag.query(question)
    return result['answer']


def start_conversation():
    """Start interactive conversation with the expert agent."""
    rag = QCExpertRAG()
    
    print("=" * 80)
    print("QC Expert Agent - Conversational Mode")
    print("=" * 80)
    print("Ask quantum chemistry questions. Type 'exit' to quit.\n")
    
    while True:
        question = input("You: ").strip()
        
        if question.lower() in ['exit', 'quit', 'q']:
            print("Goodbye!")
            break
        
        if not question:
            continue
        
        result = rag.conversational_query(question)
        print(f"\nAgent: {result['answer']}\n")
        print(f"[{result['num_sources']} sources consulted]\n")


if __name__ == "__main__":
    # Test RAG pipeline
    print("Testing RAG pipeline...\n")
    
    answer = quick_ask("What method should I use for geometry optimization of an organic molecule?")
    print(answer)
