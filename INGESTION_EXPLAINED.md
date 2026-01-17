# Understanding Bedrock Knowledge Base Ingestion Jobs

## What is an Ingestion Job?

An **ingestion job** is the process that transforms your raw text files in S3 into searchable vector embeddings in your Knowledge Base.

### The Ingestion Pipeline

```
Step 1: READ           Step 2: CHUNK          Step 3: EMBED              Step 4: STORE
┌─────────┐           ┌──────────┐          ┌──────────────┐          ┌──────────────┐
│  S3     │  ──────>  │  Text    │  ─────>  │  Generate    │  ─────>  │  OpenSearch  │
│  Files  │           │  Chunks  │          │  Embeddings  │          │  Vector DB   │
└─────────┘           └──────────┘          └──────────────┘          └──────────────┘
   .txt                 500 char              [0.23, -0.45,             Indexed &
   files                chunks                ..., 0.12]                Searchable
                                              (1024 dims)
```

### What Happens During Ingestion?

1. **Read from S3**
   - Bedrock scans your S3 bucket/prefix
   - Identifies all `.txt`, `.pdf`, `.doc`, etc. files
   - Reads the content

2. **Parse & Chunk** (if enabled)
   - Splits documents into smaller chunks
   - In our case: We already chunked, so each file = 1 chunk
   - Applies your chunking strategy (fixed-size, semantic, etc.)

3. **Generate Embeddings**
   - Each chunk is sent to the embedding model (Titan v2)
   - Model converts text to a 1024-dimensional vector
   - Vector represents the semantic meaning
   - Example: "return policy" → [0.23, -0.45, 0.12, ..., 0.89]

4. **Store in Vector Database**
   - Embeddings stored in OpenSearch Serverless
   - Creates vector index for fast similarity search
   - Maintains metadata (source file, location, etc.)

5. **Build Search Index**
   - Creates data structures for fast retrieval
   - Enables approximate nearest neighbor (ANN) search
   - Ready for queries!

---

## Do I Need to Run Ingestion Again?

**YES**, in these scenarios:

### ✅ When to Trigger a New Ingestion Job

1. **Added New Files**
   ```
   Before: s3://bucket/knowledge-base/faqs/faq_1.txt
   After:  s3://bucket/knowledge-base/faqs/faq_1.txt
           s3://bucket/knowledge-base/faqs/faq_80.txt  ← NEW!

   Action: Run ingestion to index the new file
   ```

2. **Updated Existing Files**
   ```
   Before: faq_1.txt contains "Returns within 30 days"
   After:  faq_1.txt contains "Returns within 60 days"  ← UPDATED!

   Action: Run ingestion to update the embedding
   ```

3. **Deleted Files**
   ```
   Before: s3://bucket/knowledge-base/faqs/old_faq.txt
   After:  File deleted from S3

   Action: Run ingestion to remove from vector DB
   ```

4. **Changed Chunking Strategy**
   ```
   Before: 500 character chunks
   After:  400 character chunks with 20% overlap

   Action: Re-ingest with new chunking configuration
   ```

### ❌ When You DON'T Need to Re-ingest

1. **Just Querying** - Reading data doesn't change the index
2. **LLM Model Changes** - Embeddings stay the same
3. **Changing retrieval parameters** - Number of results, etc.

---

## How Bedrock Handles Changes

### Incremental Ingestion

Bedrock is smart about what it processes:

```
First Ingestion:
  - Scanned: 94 files
  - Indexed: 94 files (all new)
  - Modified: 0
  - Deleted: 0

Second Ingestion (after adding 5 files):
  - Scanned: 99 files
  - Indexed: 5 files (only new ones)
  - Modified: 0
  - Deleted: 0

Third Ingestion (after updating 2 files):
  - Scanned: 99 files
  - Indexed: 0
  - Modified: 2 files (re-embedded)
  - Deleted: 0
```

**Note**: Bedrock uses file checksums to detect changes, so it only re-processes what changed!

---

## Ingestion Job Lifecycle

```
START
  ↓
STARTING ─────> Reading metadata, preparing
  ↓
IN_PROGRESS ──> Scanning files, generating embeddings
  ↓
COMPLETE ─────> All done! Vector DB updated

  (or)

FAILED ───────> Check error logs
```

### Typical Duration

- **Small datasets** (< 100 docs): 30 seconds - 2 minutes
- **Medium datasets** (100-1000 docs): 2-10 minutes
- **Large datasets** (1000+ docs): 10+ minutes

Our dataset (94 chunks) took about 20-30 seconds.

---

## Cost Implications

### What You Pay For:

1. **Embedding Generation**
   - Charged per token processed
   - Titan v2: $0.00002 per 1K tokens
   - Our 94 chunks (~50K tokens) ≈ $0.001

2. **Vector Storage**
   - OpenSearch Serverless: ~$0.24/hour for OCU (compute)
   - ~$0.024/GB/month for storage

3. **Re-ingestion**
   - Only charged for NEW or MODIFIED documents
   - Not charged for unchanged files

**Best Practice**: Don't re-ingest unnecessarily. Only when data changes!

---

## How to Trigger Ingestion

### Option 1: AWS Console
1. Go to Bedrock > Knowledge Bases
2. Select your KB
3. Click "Sync" or "Start ingestion job"
4. Wait for completion

### Option 2: Programmatically (Notebook 02)
```python
# Start ingestion job
response = bedrock_agent.start_ingestion_job(
    knowledgeBaseId='XVIAYNVNB2',
    dataSourceId='REMI11JEYD'
)

# Monitor progress
job_id = response['ingestionJob']['ingestionJobId']
```

### Option 3: Automated (Lambda + S3 Event)
```
S3 Event (file uploaded)
    ↓
Lambda Function Triggered
    ↓
Calls start_ingestion_job()
    ↓
Automatic sync!
```

---

## Common Issues

### Issue 1: "No documents indexed"
**Cause**: S3 permissions, empty files, or unsupported format
**Fix**: Check IAM role has S3 read permissions

### Issue 2: "Failed documents"
**Cause**: File parsing errors, encoding issues
**Fix**: Check file format, ensure UTF-8 encoding

### Issue 3: "Ingestion takes too long"
**Cause**: Large files, many documents
**Fix**: Pre-chunk files, use smaller chunks, parallelize

---

## Best Practices

1. **Batch Updates**
   - Don't run ingestion for every single file
   - Collect changes and ingest in batches

2. **Monitor Statistics**
   - Check scanned/indexed/failed counts
   - Investigate failures promptly

3. **Version Control**
   - Keep track of ingestion job IDs
   - Document what changed in each ingestion

4. **Test Before Production**
   - Test ingestion on small dataset first
   - Verify retrieval works as expected

5. **Automate for Production**
   - Set up S3 event triggers for auto-sync
   - Use CloudWatch to monitor job status

---

## Summary

**Ingestion Job** = The process that converts your files into searchable vectors

**Key Points:**
- ✅ Run ingestion when you add/update/delete files in S3
- ✅ Bedrock only processes changed files (incremental)
- ✅ Takes a few seconds to minutes depending on size
- ❌ Don't run unnecessarily (costs money)
- ❌ Vector DB doesn't auto-sync with S3 changes

**Think of it like:**
- S3 = Your filing cabinet (source of truth)
- Ingestion = Photocopying and indexing for the library
- Vector DB = The searchable library catalog
- If you add new files to the cabinet, you need to photocopy and index them too!
