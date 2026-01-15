"""
FastAPI Server for QCDB
Provides REST API endpoints for querying the quantum chemistry knowledge base.
"""

from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import os
import sys
from pathlib import Path
import uvicorn

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent / "src" / "core" / "qc_agent"))

from unified_qc_api import UnifiedQCAPI
from rag_pipeline import QCExpertRAG


# Initialize FastAPI app
app = FastAPI(
    title="Quantum Chemistry Knowledge Base API",
    description="AI-powered API for quantum chemistry methods, software, and workflows",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key authentication
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)
VALID_API_KEYS = {
    "dev_key_12345": "developer",
    "public_key_67890": "public_user"
}


def verify_api_key(api_key: str = Security(API_KEY_HEADER)) -> str:
    """Verify API key and return user role."""
    if api_key is None:
        return "public_user"  # Allow public access with limited features
    
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return VALID_API_KEYS[api_key]


# Initialize API and RAG pipeline
api = UnifiedQCAPI()
rag = QCExpertRAG()


# ==================== Request/Response Models ====================

class QueryRequest(BaseModel):
    question: str = Field(..., description="Natural language question about quantum chemistry")
    entity_types: Optional[List[str]] = Field(None, description="Filter by entity types")
    include_citations: bool = Field(True, description="Include source citations")


class QueryResponse(BaseModel):
    answer: str
    citations: List[Dict[str, Any]]
    num_sources: int


class MethodSearchRequest(BaseModel):
    min_accuracy: str = Field("medium", description="Minimum accuracy: low, medium, high, very_high")
    max_cost: Optional[str] = Field(None, description="Maximum cost: low, medium, high, very_high")
    system_type: Optional[str] = Field(None, description="System type filter")


class SemanticSearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    entity_types: Optional[List[str]] = Field(None, description="Filter by entity types")
    top_k: int = Field(10, description="Number of results", ge=1, le=50)


class WorkflowSuggestionRequest(BaseModel):
    task_description: str = Field(..., description="Description of computational task")


# ==================== Health Check ====================

@app.get("/", tags=["Health"])
def root():
    """API health check."""
    return {
        "status": "online",
        "service": "QCDB API",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Detailed health check."""
    try:
        # Test Neo4j connection
        with api.neo4j_driver.session() as session:
            session.run("RETURN 1")
        neo4j_status = "connected"
    except:
        neo4j_status = "disconnected"
    
    try:
        # Test Redis connection
        api.redis_client.ping()
        redis_status = "connected"
    except:
        redis_status = "disconnected"
    
    return {
        "neo4j": neo4j_status,
        "redis": redis_status,
        "chromadb": "initialized",
        "status": "healthy" if neo4j_status == "connected" else "degraded"
    }


# ==================== AI Query Endpoints ====================

@app.post("/query", response_model=QueryResponse, tags=["AI Agent"])
def query_kb(
    request: QueryRequest,
    user_role: str = Depends(verify_api_key)
):
    """
    Ask the QC expert agent a question.
    
    Uses RAG (Retrieval-Augmented Generation) to answer questions grounded in the KB.
    """
    try:
        result = rag.query(
            question=request.question,
            entity_types=request.entity_types,
            include_citations=request.include_citations
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/explain_method/{method_id}", tags=["AI Agent"])
def explain_method(
    method_id: str,
    user_role: str = Depends(verify_api_key)
):
    """Explain a computational method in detail."""
    try:
        explanation = rag.explain_method(method_id)
        return {"method_id": method_id, "explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/suggest_workflow", tags=["AI Agent"])
def suggest_workflow(
    request: WorkflowSuggestionRequest,
    user_role: str = Depends(verify_api_key)
):
    """Suggest a workflow for a computational task."""
    try:
        suggestion = rag.suggest_workflow(request.task_description)
        return {"task": request.task_description, "suggestion": suggestion}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Method Endpoints ====================

@app.post("/methods/search", tags=["Methods"])
def search_methods(
    request: MethodSearchRequest,
    user_role: str = Depends(verify_api_key)
):
    """Find methods by accuracy and cost criteria."""
    try:
        methods = api.find_methods_by_accuracy(
            min_accuracy=request.min_accuracy,
            max_cost=request.max_cost,
            system_type=request.system_type
        )
        return {"methods": methods, "count": len(methods)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/methods/{method_id}", tags=["Methods"])
def get_method(
    method_id: str,
    user_role: str = Depends(verify_api_key)
):
    """Get full details for a method."""
    method = api.get_method_details(method_id)
    if not method:
        raise HTTPException(status_code=404, detail=f"Method '{method_id}' not found")
    return method


@app.get("/methods/{method_id}/prerequisites", tags=["Methods"])
def get_method_prerequisites(
    method_id: str,
    user_role: str = Depends(verify_api_key)
):
    """Get prerequisite concepts for understanding a method."""
    prerequisites = api.get_method_prerequisites(method_id)
    return {"method_id": method_id, "prerequisites": prerequisites}


# ==================== Tool Endpoints ====================

@app.get("/tools/{tool_id}/workflows", tags=["Tools"])
def get_tool_workflows(
    tool_id: str,
    user_role: str = Depends(verify_api_key)
):
    """Get workflows that use a specific tool."""
    workflows = api.get_workflows_for_tool(tool_id)
    return {"tool_id": tool_id, "workflows": workflows}


@app.get("/tools/capability/{capability}", tags=["Tools"])
def find_tools_by_capability(
    capability: str,
    user_role: str = Depends(verify_api_key)
):
    """Find tools with a specific capability."""
    tools = api.find_tools_with_capability(capability)
    return {"capability": capability, "tools": tools}


# ==================== Semantic Search ====================

@app.post("/semantic_search", tags=["Search"])
def semantic_search(
    request: SemanticSearchRequest,
    user_role: str = Depends(verify_api_key)
):
    """Semantic search across the knowledge base."""
    try:
        results = api.semantic_search(
            query=request.query,
            entity_types=request.entity_types,
            top_k=request.top_k
        )
        return {"query": request.query, "results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Benchmark Endpoints ====================

@app.get("/benchmarks/{benchmark_id}", tags=["Benchmarks"])
def get_benchmark(
    benchmark_id: str,
    methods: Optional[str] = None,
    user_role: str = Depends(verify_api_key)
):
    """Get benchmark performance data."""
    method_list = methods.split(',') if methods else None
    data = api.get_benchmark_performance(benchmark_id, method_list)
    
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])
    
    return data


# ==================== Graph Queries ====================

@app.get("/workflows/{workflow_id}/similar", tags=["Workflows"])
def find_similar_workflows(
    workflow_id: str,
    top_k: int = 5,
    user_role: str = Depends(verify_api_key)
):
    """Find workflows similar to a given workflow."""
    similar = api.find_similar_workflows(workflow_id, top_k)
    return {"workflow_id": workflow_id, "similar_workflows": similar}


# ==================== Statistics ====================

@app.get("/stats", tags=["Statistics"])
def get_statistics(user_role: str = Depends(verify_api_key)):
    """Get knowledge base statistics."""
    try:
        with api.neo4j_driver.session() as session:
            # Count nodes by type
            stats = {}
            for node_type in ['Concept', 'Method', 'SoftwareTool', 'Workflow', 'BenchmarkSet']:
                result = session.run(f"MATCH (n:{node_type}) RETURN count(n) AS count")
                stats[f"{node_type.lower()}_count"] = result.single()['count']
            
            # Count relationships
            result = session.run("MATCH ()-[r]->() RETURN count(r) AS count")
            stats['relationship_count'] = result.single()['count']
            
            return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats/relationships", tags=["Statistics"])
def get_relationship_stats(user_role: str = Depends(verify_api_key)):
    """Get detailed relationship statistics by type."""
    try:
        with api.neo4j_driver.session() as session:
            # Count each relationship type
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) AS rel_type, count(r) AS count
                ORDER BY count DESC
            """)
            
            relationships = [{"type": rec["rel_type"], "count": rec["count"]} for rec in result]
            total = sum(r["count"] for r in relationships)
            
            return {
                "total_relationships": total,
                "by_type": relationships,
                "types_count": len(relationships)
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Main ====================

if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
