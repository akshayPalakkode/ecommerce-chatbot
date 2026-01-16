# 1.5 Hour RAG Demo with Data Ingestion & Chunking Strategies

## Enhanced Demo Flow

**Key Addition**: Show the **entire RAG pipeline** from raw documents to production chatbot

**Why This Is Better**:
- ✅ Audience sees the full data preparation process
- ✅ Understands why chunking matters (hands-on comparison)
- ✅ Learns production-grade ingestion patterns
- ✅ Can replicate for their own use cases

---

# Updated Session Structure (90 minutes)

## Part 1: Introduction (0-10 min)
- Problem: E-commerce support at scale
- Solution overview
- **Demo roadmap preview**: We'll build everything from scratch

## Part 2: Data Preparation & Ingestion (10-40 min) **← NEW!**

### 2A: Document Collection (10-15 min)
**Live Demo**: Show raw knowledge base files
- Display markdown files (policies, FAQs)
- Discuss document sources (Confluence, Google Docs, PDFs, etc.)
- Data cleaning considerations

### 2B: Chunking Strategies (15-30 min) **← CORE DEMO**
**Interactive Comparison**: Test different chunking approaches

#### Strategy 1: Fixed-Size Chunking (Naive)
```python
# Simple 500-character chunks
def fixed_size_chunk(text, size=500):
    return [text[i:i+size] for i in range(0, len(text), size)]
```

**Demo**:
- Show chunks created
- **Problem**: Cuts mid-sentence, loses context
- Retrieval quality: ⭐⭐ (Poor)

#### Strategy 2: Sentence-Based Chunking
```python
# Chunk by sentences, max size
import nltk
nltk.download('punkt')

def sentence_chunk(text, max_size=500):
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current = ""

    for sentence in sentences:
        if len(current + sentence) < max_size:
            current += sentence + " "
        else:
            chunks.append(current.strip())
            current = sentence + " "

    if current:
        chunks.append(current.strip())

    return chunks
```

**Demo**:
- Show improved chunks (respect sentence boundaries)
- **Better**: Maintains semantic units
- Retrieval quality: ⭐⭐⭐⭐ (Good)

#### Strategy 3: Semantic Chunking (Advanced)
```python
# Chunk by semantic similarity
from langchain.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

semantic_chunker = SemanticChunker(
    OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=90
)

chunks = semantic_chunker.split_text(text)
```

**Demo**:
- Show chunks based on topic shifts
- **Best**: Maintains semantic coherence
- Retrieval quality: ⭐⭐⭐⭐⭐ (Excellent)

#### Strategy 4: Recursive Character Splitting (LangChain)
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]
)

chunks = text_splitter.split_text(text)
```

**Demo**:
- Tries multiple separators hierarchically
- **Production-ready**: Good balance of quality and speed
- Retrieval quality: ⭐⭐⭐⭐ (Very Good)

### Live Comparison Table:
| Strategy | Chunk Count | Avg Size | Semantic Coherence | Speed | Best For |
|----------|-------------|----------|-------------------|-------|----------|
| Fixed Size | 15 | 500 | ⭐⭐ | ⚡⚡⚡ | Simple, fast |
| Sentence | 12 | 520 | ⭐⭐⭐⭐ | ⚡⚡ | Readable |
| Semantic | 8 | 750 | ⭐⭐⭐⭐⭐ | ⚡ | Best quality |
| Recursive | 10 | 510 | ⭐⭐⭐⭐ | ⚡⚡ | **Production** |

### 2C: Embedding Generation (30-35 min)
**Live Demo**: Generate embeddings for chunks

```python
from openai import OpenAI

client = OpenAI()

def embed_chunk(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-large"  # 3072 dimensions
    )
    return response.data[0].embedding

# Show embedding
chunk = chunks[0]
embedding = embed_chunk(chunk)

print(f"Chunk: {chunk[:100]}...")
print(f"Embedding dimensions: {len(embedding)}")
print(f"Sample values: {embedding[:5]}")
```

**Discussion**:
- Embedding model choices (OpenAI vs Cohere vs open-source)
- Dimension tradeoffs (384 vs 768 vs 3072)
- Cost implications (~$0.13/1M tokens for OpenAI)

### 2D: Vector Store Ingestion (35-40 min)
**Live Demo**: Upload to Bedrock Knowledge Base

#### Option A: Direct S3 Upload + Bedrock Sync
```python
import boto3

s3 = boto3.client('s3')

# Upload knowledge base files
for file_path in knowledge_base_files:
    s3.upload_file(
        file_path,
        'my-kb-bucket',
        f'policies/{os.path.basename(file_path)}'
    )

# Trigger Bedrock KB sync
bedrock_agent = boto3.client('bedrock-agent')

bedrock_agent.start_ingestion_job(
    knowledgeBaseId='KB123',
    dataSourceId='DS456'
)
```

#### Option B: Manual Vector Store (OpenSearch/Pinecone)
```python
from pinecone import Pinecone

pc = Pinecone(api_key="...")
index = pc.Index("ecommerce-kb")

# Upsert vectors
vectors_to_upsert = [
    {
        "id": f"chunk_{i}",
        "values": embedding,
        "metadata": {
            "text": chunk,
            "source": "return_policy.md",
            "chunk_id": i
        }
    }
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))
]

index.upsert(vectors=vectors_to_upsert)
```

**Show**:
- Upload progress
- Indexing status
- Verify ingestion (query test)

---

## Part 3: RAG Pipeline (40-60 min)

### 3A: Retrieval Testing (40-45 min)
**Live Demo**: Test retrieval with different queries

```python
# Query the knowledge base
query = "Can I return a damaged item?"

# Retrieve relevant chunks
results = retrieve_from_kb(query, top_k=3)

# Display results with scores
for i, result in enumerate(results):
    print(f"\n--- Result {i+1} (Score: {result['score']:.3f}) ---")
    print(f"Source: {result['source']}")
    print(f"Text: {result['text'][:200]}...")
```

**Compare**:
- How different chunking strategies affect retrieval
- Show relevance scores
- Discuss top-k selection (3 vs 5 vs 10)

### 3B: Agent Implementation (45-55 min)
- Quick overview of LangGraph agent
- Tool integration (order lookup, refund calc)
- Citation tracking

### 3C: End-to-End Demo (55-60 min)
**Live Demo**: Full chatbot interaction
- Simple query (retrieval only)
- Complex query (multi-tool + retrieval)
- Show sources and reasoning

---

## Part 4: Production Considerations (60-75 min)

### 4A: Chunking Best Practices (60-65 min)
- Chunk size optimization (test 256, 512, 1024)
- Overlap strategies (0%, 10%, 20%)
- Metadata enrichment (add source, section headers)
- Parent-child chunking (small chunks for retrieval, large for context)

### 4B: Ingestion Pipeline (65-70 min)
- Scheduled sync (cron job, EventBridge)
- Incremental updates (only changed docs)
- Version control for knowledge base
- A/B testing different chunking strategies

### 4C: Monitoring & Optimization (70-75 min)
- Retrieval quality metrics
- Latency tracking
- Cost per query

---

## Part 5: Deployment & Q&A (75-90 min)

### Docker + Streamlit (75-80 min)
- Quick overview of deployment
- Show Streamlit UI

### Q&A (80-90 min)

---

# Demo Artifacts to Create

## Jupyter Notebooks:

### 1. `0_data_ingestion.ipynb` **← MAIN DEMO NOTEBOOK**
**Sections**:
- Load raw documents
- Compare 4 chunking strategies side-by-side
- Generate embeddings
- Upload to S3
- Sync to Bedrock KB
- Test retrieval

### 2. `1_chunking_comparison.ipynb`
**Deep Dive**:
- Visual comparison of chunks
- Retrieval quality metrics
- Cost analysis
- Recommendations

### 3. `2_rag_pipeline.ipynb`
**Complete Pipeline**:
- Query → Retrieve → Generate
- Agent with tools
- Citation tracking

### 4. `3_production_deployment.ipynb`
**Deployment**:
- Docker build
- AWS deployment
- Monitoring setup

## Python Scripts:

### 1. `scripts/chunk_documents.py`
```python
"""
Chunking strategies implementation
"""

class ChunkingStrategy:
    def chunk(self, text: str) -> List[str]:
        raise NotImplementedError

class FixedSizeChunker(ChunkingStrategy):
    def __init__(self, chunk_size: int = 500):
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> List[str]:
        return [text[i:i+self.chunk_size]
                for i in range(0, len(text), self.chunk_size)]

class SemanticChunker(ChunkingStrategy):
    # Implementation...

class RecursiveChunker(ChunkingStrategy):
    # Implementation...

# Comparison utility
def compare_strategies(text: str, strategies: List[ChunkingStrategy]):
    results = {}
    for strategy in strategies:
        chunks = strategy.chunk(text)
        results[strategy.__class__.__name__] = {
            "chunks": chunks,
            "count": len(chunks),
            "avg_size": sum(len(c) for c in chunks) / len(chunks),
            "sizes": [len(c) for c in chunks]
        }
    return results
```

### 2. `scripts/ingest_to_bedrock.py`
```python
"""
Upload documents to S3 and trigger Bedrock KB sync
"""

import boto3
import os
from pathlib import Path

def upload_knowledge_base(
    local_dir: str,
    s3_bucket: str,
    kb_id: str,
    data_source_id: str
):
    """Upload documents and sync to Bedrock KB."""

    s3 = boto3.client('s3')
    bedrock = boto3.client('bedrock-agent')

    # Upload files
    for file_path in Path(local_dir).glob('**/*.md'):
        key = f'knowledge-base/{file_path.name}'
        print(f"Uploading {file_path} to s3://{s3_bucket}/{key}")
        s3.upload_file(str(file_path), s3_bucket, key)

    # Start ingestion job
    print(f"Starting Bedrock KB ingestion...")
    response = bedrock.start_ingestion_job(
        knowledgeBaseId=kb_id,
        dataSourceId=data_source_id
    )

    job_id = response['ingestionJob']['ingestionJobId']
    print(f"Ingestion job started: {job_id}")

    return job_id

if __name__ == "__main__":
    upload_knowledge_base(
        local_dir="data/knowledge_base",
        s3_bucket=os.getenv("KB_S3_BUCKET"),
        kb_id=os.getenv("BEDROCK_KB_ID"),
        data_source_id=os.getenv("BEDROCK_DS_ID")
    )
```

### 3. `scripts/compare_retrieval.py`
```python
"""
Compare retrieval quality across chunking strategies
"""

def evaluate_retrieval(
    queries: List[str],
    ground_truth: Dict[str, List[str]],
    retriever: Callable
):
    """Evaluate retrieval quality."""

    metrics = {
        "precision": [],
        "recall": [],
        "mrr": []
    }

    for query in queries:
        results = retriever(query, top_k=5)
        relevant_docs = ground_truth[query]

        # Calculate metrics
        retrieved_ids = [r['id'] for r in results]

        # Precision@5
        relevant_retrieved = set(retrieved_ids) & set(relevant_docs)
        precision = len(relevant_retrieved) / len(retrieved_ids)

        # Recall@5
        recall = len(relevant_retrieved) / len(relevant_docs)

        # MRR
        mrr = 0
        for i, doc_id in enumerate(retrieved_ids):
            if doc_id in relevant_docs:
                mrr = 1 / (i + 1)
                break

        metrics["precision"].append(precision)
        metrics["recall"].append(recall)
        metrics["mrr"].append(mrr)

    return {
        "precision": sum(metrics["precision"]) / len(queries),
        "recall": sum(metrics["recall"]) / len(queries),
        "mrr": sum(metrics["mrr"]) / len(queries)
    }
```

---

# Visual Aids for Demo

## 1. Chunking Comparison Visualization
```python
import matplotlib.pyplot as plt

def visualize_chunks(chunks_dict: Dict[str, List[str]]):
    """Visualize chunk size distribution."""

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    for idx, (strategy, chunks) in enumerate(chunks_dict.items()):
        ax = axes[idx // 2, idx % 2]

        sizes = [len(c) for c in chunks]
        ax.hist(sizes, bins=20, alpha=0.7)
        ax.set_title(f"{strategy}\n{len(chunks)} chunks")
        ax.set_xlabel("Chunk Size (characters)")
        ax.set_ylabel("Frequency")
        ax.axvline(sum(sizes)/len(sizes), color='red',
                   linestyle='--', label=f'Avg: {sum(sizes)/len(sizes):.0f}')
        ax.legend()

    plt.tight_layout()
    plt.show()
```

## 2. Retrieval Quality Heatmap
```python
def plot_retrieval_quality(results: Dict[str, Dict[str, float]]):
    """Show retrieval metrics across strategies."""

    import seaborn as sns

    strategies = list(results.keys())
    metrics = ['Precision@5', 'Recall@5', 'MRR']

    data = [[results[s][m] for m in metrics] for s in strategies]

    sns.heatmap(
        data,
        annot=True,
        xticklabels=metrics,
        yticklabels=strategies,
        cmap='YlGnBu',
        vmin=0,
        vmax=1
    )
    plt.title("Retrieval Quality by Chunking Strategy")
    plt.show()
```

---

# Session Materials Checklist

## Pre-Demo Setup:
- [ ] Create 5 knowledge base markdown files
- [ ] Prepare 10 sample e-commerce orders (mock data)
- [ ] Set up AWS account with Bedrock access
- [ ] Create S3 bucket for knowledge base
- [ ] Create Bedrock Knowledge Base (or have template ready)
- [ ] Install required Python packages

## During Demo:
- [ ] Show raw markdown files
- [ ] Run chunking comparison live
- [ ] Generate embeddings live
- [ ] Upload to S3 (or show pre-uploaded)
- [ ] Sync to Bedrock KB (or show status)
- [ ] Test retrieval with queries
- [ ] Show full chatbot interaction
- [ ] Display metrics and visualizations

## Post-Demo:
- [ ] Share GitHub repo with all notebooks
- [ ] Provide AWS setup guide
- [ ] Share cost calculator
- [ ] Offer to help with custom implementations

---

# Estimated Timing Breakdown

| Section | Time | Activities |
|---------|------|-----------|
| Intro | 10 min | Problem, solution, roadmap |
| **Data Prep** | **30 min** | **Documents, chunking demo, embeddings** |
| RAG Pipeline | 20 min | Retrieval, agent, demo |
| Production | 15 min | Best practices, optimization |
| Deployment | 5 min | Quick overview |
| Q&A | 10 min | Questions |
| **Total** | **90 min** | |

---

# Key Takeaways for Audience

After this demo, attendees will:
1. ✅ Understand **why chunking matters** (saw live comparison)
2. ✅ Know **how to chunk** (4 different strategies)
3. ✅ Can **implement ingestion** (saw code + live demo)
4. ✅ Understand **Bedrock Knowledge Bases** (AWS-native RAG)
5. ✅ Can **evaluate retrieval quality** (metrics + visualization)
6. ✅ Have **production-ready code** (notebooks + scripts)

---

Would you like me to create:
1. ✅ The main `0_data_ingestion.ipynb` notebook?
2. ✅ The chunking comparison scripts?
3. ✅ The S3 upload and Bedrock sync scripts?
4. ✅ Visual comparison utilities?
5. ✅ All of the above?

Let me know and I'll build it!
