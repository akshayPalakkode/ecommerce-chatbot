#!/usr/bin/env python3
"""Generate comprehensive cell-by-cell presenter's guide."""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def add_callout(doc, callout_type, text):
    """Add a styled callout box."""
    p = doc.add_paragraph()
    labels = {
        'theory': '[THEORY]',
        'say': '[SAY]',
        'show': '[SHOW OUTPUT]',
        'ui': '[SHOW UI]',
        'ask': '[ASK AUDIENCE]',
        'tip': '[TIP]',
        'demo': '[DEMO]',
        'transition': '[TRANSITION]'
    }
    p.add_run(f"{labels.get(callout_type, '[NOTE]')} ").bold = True
    p.add_run(text)
    return p

def create_guide():
    doc = Document()

    # Title
    title = doc.add_heading('RAG Masterclass - Cell-by-Cell Presenter Guide', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph('Detailed guide for what to say and explain at each notebook cell')
    doc.add_paragraph()

    # =========================================================================
    # INTRODUCTION
    # =========================================================================
    doc.add_heading('Pre-Session: Introduction (10-15 minutes)', level=1)

    add_callout(doc, 'say', 'Welcome everyone to this RAG masterclass. Today we will build a production-ready chatbot from scratch.')

    doc.add_heading('What is RAG?', level=2)

    add_callout(doc, 'theory', 'RAG = Retrieval-Augmented Generation')

    doc.add_paragraph(
        'Key points to explain:\n\n'
        '1. LLMs have a knowledge cutoff - they do not know recent events\n'
        '2. LLMs can hallucinate - make up plausible but wrong information\n'
        '3. LLMs do not know your company/product data\n\n'
        'RAG solves this by:\n'
        '- Storing your documents in a searchable database\n'
        '- When user asks a question, finding relevant documents\n'
        '- Including those documents in the LLM prompt\n'
        '- LLM generates answer based on YOUR data, not training data'
    )

    add_callout(doc, 'ask', 'Has anyone worked with RAG before? What challenges did you face?')

    doc.add_heading('What We Will Build Today', level=2)

    doc.add_paragraph(
        '1. Data preparation and chunking strategies\n'
        '2. AWS Bedrock Knowledge Base with vector search\n'
        '3. Multiple retrieval methods (Vector, BM25, Hybrid)\n'
        '4. Complete RAG pipeline with LLM generation\n'
        '5. Conversation memory and source citations\n'
        '6. Production Streamlit application\n'
        '7. AWS Fargate deployment'
    )

    doc.add_page_break()

    # =========================================================================
    # NOTEBOOK 00
    # =========================================================================
    doc.add_heading('Notebook 00: Setup & Connections', level=1)

    add_callout(doc, 'say', 'Let us start by setting up our environment and testing all connections.')

    # Cell 1-3
    doc.add_heading('Cells 1-3: Install & Import Libraries', level=2)

    doc.add_paragraph('Run: pip install and import statements')

    add_callout(doc, 'say', 'We are installing boto3 for AWS, datasets for HuggingFace, and other utilities. This should complete quickly.')

    add_callout(doc, 'tip', 'If anyone has import errors, make sure they activated the virtual environment.')

    # Cell 4-5
    doc.add_heading('Cells 4-5: AWS Credentials', level=2)

    add_callout(doc, 'theory', 'Environment Variables and Secrets Management')

    doc.add_paragraph(
        'Key points:\n'
        '- We use .env files to store sensitive credentials\n'
        '- NEVER commit .env files to git (check .gitignore)\n'
        '- python-dotenv loads these into environment variables\n'
        '- In production, use AWS Secrets Manager or SSM Parameter Store'
    )

    add_callout(doc, 'show', 'Show that credentials are loaded with masked output (AKIA...)')

    add_callout(doc, 'ask', 'Why do we use environment variables instead of hardcoding credentials?')

    # Cell 6-7
    doc.add_heading('Cells 6-7: Test AWS Connection', level=2)

    add_callout(doc, 'theory', 'AWS STS (Security Token Service)')

    doc.add_paragraph(
        'Explain:\n'
        '- STS get_caller_identity verifies our credentials work\n'
        '- Returns Account ID, User ARN, and User ID\n'
        '- This is always the first thing to test with AWS'
    )

    add_callout(doc, 'show', 'Highlight the Account ID and User ARN in output')

    # Cell 8-9
    doc.add_heading('Cells 8-9: List Bedrock Models', level=2)

    add_callout(doc, 'theory', 'AWS Bedrock Model Ecosystem')

    doc.add_paragraph(
        'Explain:\n'
        '- Bedrock provides access to foundation models from multiple providers\n'
        '- Embedding models: Convert text to vectors (Titan, Cohere)\n'
        '- LLM models: Generate text (Claude, Llama, etc.)\n'
        '- We will use Titan Embeddings v2 (1024 dimensions)'
    )

    add_callout(doc, 'show', 'Point out Titan embedding models in the list')

    add_callout(doc, 'tip', 'Models must be enabled in the Bedrock console before use')

    # Cell 10-11
    doc.add_heading('Cells 10-11: Test LLM API', level=2)

    add_callout(doc, 'theory', 'OpenAI-Compatible APIs')

    doc.add_paragraph(
        'Explain:\n'
        '- Many LLM providers offer OpenAI-compatible APIs\n'
        '- Same client library, just different base_url\n'
        '- Makes it easy to switch between providers\n'
        '- We use gpt-4o for generation'
    )

    add_callout(doc, 'show', 'Show the LLM response and token counts')

    add_callout(doc, 'say', 'Notice the input/output token counts - this is what you pay for with LLM APIs.')

    # Cell 12-13
    doc.add_heading('Cells 12-13: Test Titan Embeddings', level=2)

    add_callout(doc, 'theory', 'What Are Embeddings? (IMPORTANT - spend time here)')

    doc.add_paragraph(
        'Core concept to explain:\n\n'
        'Embeddings are numerical representations of text meaning.\n\n'
        '1. Text -> Model -> Vector of 1024 numbers\n'
        '2. Similar meanings = similar vectors\n'
        '3. "dog" and "puppy" have similar embeddings\n'
        '4. "dog" and "airplane" have different embeddings\n\n'
        'Analogy: Think of a map where cities close together are similar.\n'
        'Paris and Lyon are close. Paris and Tokyo are far.\n'
        'Embeddings work the same way but in 1024 dimensions!'
    )

    add_callout(doc, 'show', 'Show the embedding output: 1024 dimensions, sample values, range')

    add_callout(doc, 'ask', 'Why do you think we use 1024 dimensions instead of just 2 or 3?')

    doc.add_paragraph('Answer: More dimensions = more nuance in meaning. 2D would lose too much information.')

    # Cell 14-19
    doc.add_heading('Cells 14-19: Download Dataset', level=2)

    add_callout(doc, 'say', 'Now let us get some real data to work with.')

    doc.add_paragraph(
        'Explain the dataset:\n'
        '- HuggingFace Ecommerce FAQ dataset\n'
        '- 79 question-answer pairs\n'
        '- Real e-commerce scenarios: returns, shipping, payments, etc.\n'
        '- Perfect for demonstrating RAG'
    )

    add_callout(doc, 'show', 'Show sample Q&A pairs in the dataframe')

    add_callout(doc, 'transition', 'Now that everything is connected, let us explore the data and learn about chunking.')

    doc.add_page_break()

    # =========================================================================
    # NOTEBOOK 01
    # =========================================================================
    doc.add_heading('Notebook 01: Data Exploration & Chunking', level=1)

    add_callout(doc, 'say', 'Chunking is one of the most important decisions in RAG. Let me show you why.')

    # Cells 1-3
    doc.add_heading('Cells 1-3: Setup', level=2)
    add_callout(doc, 'say', 'Quick setup - we are importing NLTK for sentence tokenization and LangChain for text splitters.')

    # Cells 4-7
    doc.add_heading('Cells 4-7: Load and Explore Data', level=2)

    add_callout(doc, 'show', 'Show the dataset statistics: 79 Q&A pairs, average lengths')

    doc.add_paragraph(
        'Key observation to highlight:\n'
        '- Average Q&A pair is ~220 characters\n'
        '- This is small! Each Q&A is already a natural chunk\n'
        '- For FAQs, we may not need to chunk at all'
    )

    # Cells 8-9
    doc.add_heading('Cells 8-9: Visualize Length Distribution', level=2)

    add_callout(doc, 'show', 'Show the histogram plots')

    add_callout(doc, 'say', 'See how the data is distributed? Most answers are 150-200 characters. This will inform our chunk size choices.')

    # Cells 10-11
    doc.add_heading('Cells 10-11: Create Policy Documents', level=2)

    add_callout(doc, 'say', 'FAQs are too short to demonstrate chunking. Let me create some longer policy documents.')

    add_callout(doc, 'show', 'Show the policy lengths: Return (1651), Shipping (1520), Warranty (1307)')

    add_callout(doc, 'transition', 'Now we have longer documents. Let us see how different chunking strategies handle them.')

    # Cells 12-13
    doc.add_heading('Cells 12-13: Fixed-Size Chunking', level=2)

    add_callout(doc, 'theory', 'Fixed-Size Chunking (Naive Approach)')

    doc.add_paragraph(
        'How it works:\n'
        '- Split every N characters regardless of content\n'
        '- Example: Every 500 characters\n\n'
        'Problems:\n'
        '- Breaks words mid-word ("rece" | "ive")\n'
        '- Breaks sentences mid-thought\n'
        '- Loses context across chunks'
    )

    add_callout(doc, 'show', 'Point out the second chunk starting mid-sentence: "ive a return shipping label..."')

    add_callout(doc, 'ask', 'Would you want to search and find a chunk that starts with "ive a return"? What problems might this cause?')

    # Cells 14-15
    doc.add_heading('Cells 14-15: Sentence-Based Chunking', level=2)

    add_callout(doc, 'theory', 'Sentence-Based Chunking')

    doc.add_paragraph(
        'How it works:\n'
        '- Use NLP to detect sentence boundaries\n'
        '- Combine sentences until reaching size limit\n'
        '- Never break mid-sentence\n\n'
        'Better because:\n'
        '- Each chunk is readable\n'
        '- Complete thoughts preserved'
    )

    add_callout(doc, 'show', 'Show that chunks now start with complete sentences')

    add_callout(doc, 'say', 'Notice the second chunk starts with "Once approved..." - a complete sentence. Much better!')

    # Cells 16-17
    doc.add_heading('Cells 16-17: Recursive Character Splitting (PRODUCTION)', level=2)

    add_callout(doc, 'theory', 'Recursive Character Splitting - The Production Choice')

    doc.add_paragraph(
        'How it works:\n'
        '1. Try to split on paragraphs (\\n\\n) first\n'
        '2. If chunk too big, try sentences (.)\n'
        '3. If still too big, try words (space)\n'
        '4. Last resort: characters\n\n'
        'Key feature: OVERLAP\n'
        '- 50 character overlap between chunks\n'
        '- Prevents losing context at boundaries\n'
        '- If a sentence is split, the end of chunk 1 appears in chunk 2'
    )

    add_callout(doc, 'show', 'Point out: 5 chunks, consistent sizes (298-354), 50 char overlap')

    add_callout(doc, 'tip', 'This is what LangChain and most production systems use. Memorize these defaults: chunk_size=500, chunk_overlap=50')

    # Cells 18-19
    doc.add_heading('Cells 18-19: Semantic Chunking', level=2)

    add_callout(doc, 'theory', 'Semantic Chunking')

    doc.add_paragraph(
        'How it works:\n'
        '- Split based on meaning/topic, not size\n'
        '- Each section header = new chunk\n'
        '- Best semantic coherence\n\n'
        'Trade-offs:\n'
        '- Variable chunk sizes\n'
        '- May need embeddings (expensive)\n'
        '- Best for well-structured documents'
    )

    add_callout(doc, 'show', 'Show 6 topic-based chunks: Eligibility, Process, Timeline, Non-returnable, International')

    # Cells 20-23
    doc.add_heading('Cells 20-23: Compare All Strategies', level=2)

    add_callout(doc, 'show', 'Show the comparison table and histogram')

    doc.add_paragraph(
        'Key comparison points:\n'
        '- Fixed-Size: 4 chunks, high variance (breaks context)\n'
        '- Sentence: 4 chunks, better boundaries\n'
        '- Recursive: 5 chunks, most consistent sizes\n'
        '- Semantic: 6 chunks, highest variance but best coherence'
    )

    add_callout(doc, 'ask', 'Based on this comparison, which would you choose for a production system and why?')

    # Cells 24-25
    doc.add_heading('Cells 24-25: Impact on Retrieval', level=2)

    add_callout(doc, 'theory', 'Why Chunking Matters for RAG')

    doc.add_paragraph(
        'Key insight:\n'
        '- Query: "How long does it take to get a refund?"\n'
        '- Different chunking = different retrieval results\n'
        '- Bad chunking = incomplete or irrelevant answers\n'
        '- Good chunking = complete, relevant context for LLM'
    )

    add_callout(doc, 'show', 'Show how all strategies find "refund" but with different context amounts')

    # Cell 26-28
    doc.add_heading('Cells 26-28: Recommendations & Save', level=2)

    add_callout(doc, 'say', 'Here is my decision matrix for choosing chunking strategy...')

    doc.add_paragraph(
        'Recommendations:\n'
        '- Production RAG: Recursive (chunk_size=500, overlap=50)\n'
        '- FAQ/Q&A: Keep pairs intact (no chunking needed)\n'
        '- Long documents: Semantic if well-structured\n'
        '- Code: Use code-aware splitters'
    )

    add_callout(doc, 'transition', 'We have prepared our chunks. Now let us see how they get indexed in a vector database.')

    doc.add_page_break()

    # =========================================================================
    # NOTEBOOK 01.5 (S3 Upload)
    # =========================================================================
    doc.add_heading('Notebook 01.5: Upload to S3', level=1)

    add_callout(doc, 'say', 'Before we can use Bedrock Knowledge Base, we need our data in S3.')

    doc.add_heading('Key Cells', level=2)

    add_callout(doc, 'theory', 'Timestamped Folders for Data Versioning')

    doc.add_paragraph(
        'Why timestamped folders?\n'
        '- Each upload creates: knowledge-base-20260117_143521/\n'
        '- Prevents duplicate ingestion in Bedrock\n'
        '- Easy to track data versions\n'
        '- Can rollback by pointing to old folder'
    )

    add_callout(doc, 'show', 'Show the S3 upload progress and final folder structure')

    add_callout(doc, 'ui', 'Open AWS Console > S3 > ecom-rag-bucket to show uploaded files')

    add_callout(doc, 'transition', 'Data is in S3. Now we need to trigger ingestion to index it in the vector store.')

    doc.add_page_break()

    # =========================================================================
    # NOTEBOOK 02
    # =========================================================================
    doc.add_heading('Notebook 02: Bedrock Knowledge Base', level=1)

    add_callout(doc, 'say', 'Now we will explore how AWS Bedrock Knowledge Base works.')

    # Cells 1-2
    doc.add_heading('Cells 1-2: Setup', level=2)
    add_callout(doc, 'show', 'Verify Knowledge Base ID is loaded from .env')

    # Cells 3-4
    doc.add_heading('Cells 3-4: Knowledge Base Details', level=2)

    add_callout(doc, 'theory', 'Knowledge Base Architecture')

    doc.add_paragraph(
        'Components shown:\n'
        '- Knowledge Base ID: Unique identifier\n'
        '- Embedding Model: Titan Embeddings v2 (1024 dims)\n'
        '- Vector Store: OpenSearch Serverless (managed by AWS)\n'
        '- IAM Role: Permissions for Bedrock to access S3'
    )

    add_callout(doc, 'show', 'Highlight the embedding model ARN and OpenSearch collection ARN')

    add_callout(doc, 'say', 'AWS manages the vector database for us - no infrastructure to configure!')

    # Cells 5-6
    doc.add_heading('Cells 5-6: Data Sources', level=2)

    add_callout(doc, 'show', 'Show the data source pointing to our S3 bucket')

    add_callout(doc, 'say', 'A Knowledge Base can have multiple data sources - S3, Confluence, SharePoint, etc.')

    # Cells 7-8
    doc.add_heading('Cells 7-8: Ingestion Job History', level=2)

    add_callout(doc, 'theory', 'What is Ingestion?')

    doc.add_paragraph(
        'Ingestion process:\n'
        '1. Bedrock reads documents from S3\n'
        '2. Chunks them using default strategy\n'
        '3. Generates embeddings for each chunk\n'
        '4. Stores vectors in OpenSearch\n'
        '5. Creates metadata index\n\n'
        'When to re-ingest:\n'
        '- Added new files to S3\n'
        '- Modified existing files\n'
        '- Deleted files (need sync)'
    )

    add_callout(doc, 'show', 'Show job history: Scanned vs Indexed counts')

    # Cells 9-10
    doc.add_heading('Cells 9-10: Trigger Ingestion (Optional)', level=2)

    add_callout(doc, 'say', 'This code shows how to trigger ingestion programmatically. Useful for automation.')

    add_callout(doc, 'tip', 'For demo, we already ingested. Do not run unless you have new data.')

    # Cells 11-12
    doc.add_heading('Cells 11-12: Test Retrieval', level=2)

    add_callout(doc, 'theory', 'Vector Retrieval Process')

    doc.add_paragraph(
        'What happens when we retrieve:\n'
        '1. Query: "What is your return policy?"\n'
        '2. Query -> Titan Embeddings -> 1024-dim vector\n'
        '3. Compare query vector to all document vectors\n'
        '4. Return top K most similar (cosine similarity)\n'
        '5. Score indicates relevance (0-1 range)'
    )

    add_callout(doc, 'show', 'Show retrieval results: Score, Source file, Content preview')

    add_callout(doc, 'say', 'Notice the scores: 0.59 is the best match. Scores above 0.4 are usually relevant.')

    # Cells 13-14
    doc.add_heading('Cells 13-14: Document Structure', level=2)

    add_callout(doc, 'show', 'Show the full JSON structure of a retrieved document')

    doc.add_paragraph(
        'Key fields:\n'
        '- content.text: The actual chunk text\n'
        '- score: Relevance score (0-1)\n'
        '- location.s3Location.uri: Source file path\n'
        '- metadata: Chunk ID, source file, etc.'
    )

    # Cells 15-18
    doc.add_heading('Cells 15-18: Retrieval Analysis', level=2)

    add_callout(doc, 'show', 'Show the query comparison table and score visualizations')

    doc.add_paragraph(
        'Key observations:\n'
        '- Top result scores vary by query type\n'
        '- Score drops from rank 1 to rank 5 (expected)\n'
        '- FAQ source for direct questions, policy source for complex queries'
    )

    # Cells 19-20
    doc.add_heading('Cells 19-20: Semantic Similarity Demo', level=2)

    add_callout(doc, 'theory', 'The Power of Semantic Search')

    doc.add_paragraph(
        'Demo queries:\n'
        '- "What is your return policy?"\n'
        '- "Can I return items?"\n'
        '- "How do I send something back?"\n'
        '- "Return process"\n\n'
        'ALL find similar content despite different wording!\n'
        'This is why vector search beats keyword search for natural language.'
    )

    add_callout(doc, 'show', 'Show all 4 queries finding return-related content')

    add_callout(doc, 'ask', 'Would traditional keyword search find "return policy" for the query "send something back"?')

    add_callout(doc, 'transition', 'We understand vector search now. But is it always the best? Let us compare to other methods.')

    doc.add_page_break()

    # =========================================================================
    # NOTEBOOK 03
    # =========================================================================
    doc.add_heading('Notebook 03: RAG Pipeline & Retrieval Strategies', level=1)

    add_callout(doc, 'say', 'This is the main event - building a complete RAG system with multiple retrieval options.')

    # Cells 1-4
    doc.add_heading('Cells 1-4: Setup & Load Data', level=2)

    add_callout(doc, 'show', 'Show LLM client initialization and chunk loading (93 chunks)')

    # Cells 5-6
    doc.add_heading('Cells 5-6: Vector Search Implementation', level=2)

    add_callout(doc, 'theory', 'Vector Search Recap')

    doc.add_paragraph(
        'Strengths:\n'
        '- Understands synonyms and paraphrasing\n'
        '- Great for natural language questions\n'
        '- Handles typos reasonably well\n\n'
        'Weaknesses:\n'
        '- May miss exact keyword matches\n'
        '- Computationally expensive\n'
        '- Needs quality embeddings model'
    )

    add_callout(doc, 'show', 'Show vector search results with scores')

    # Cells 7-9
    doc.add_heading('Cells 7-9: BM25 Search Implementation', level=2)

    add_callout(doc, 'theory', 'BM25 - The Classic Keyword Search')

    doc.add_paragraph(
        'How BM25 works:\n'
        '1. Tokenize query into words\n'
        '2. For each document:\n'
        '   - Count term frequency (TF)\n'
        '   - Calculate inverse document frequency (IDF)\n'
        '   - Combine with length normalization\n'
        '3. Rank by final score\n\n'
        'Key insight: Rare words score higher (IDF)\n'
        '"PayPal" in a doc is more significant than "the"'
    )

    add_callout(doc, 'show', 'Show BM25 results - note different scoring scale (not 0-1)')

    add_callout(doc, 'say', 'Notice BM25 scores are higher numbers (8.18) - different scale than vector (0.59). We will normalize these.')

    # Cells 10-11
    doc.add_heading('Cells 10-11: Hybrid Search Implementation', level=2)

    add_callout(doc, 'theory', 'Hybrid Search - Best of Both Worlds (KEY CONCEPT)')

    doc.add_paragraph(
        'The Alpha Parameter:\n'
        'hybrid_score = alpha * vector_score + (1-alpha) * bm25_score\n\n'
        '- alpha = 1.0: Pure vector (semantic only)\n'
        '- alpha = 0.0: Pure BM25 (keywords only)\n'
        '- alpha = 0.5: Balanced (recommended start)\n'
        '- alpha = 0.7: Favor semantic, consider keywords\n\n'
        'Why it works:\n'
        'Query: "PayPal refund process"\n'
        '- Vector finds: documents about returning money\n'
        '- BM25 finds: documents with exact word "PayPal"\n'
        '- Hybrid: PayPal-specific refund info (best match!)'
    )

    add_callout(doc, 'show', 'Show hybrid results with vector_score, bm25_score, and combined score')

    add_callout(doc, 'tip', 'Start with alpha=0.5 and tune based on your query patterns. More natural language = higher alpha.')

    # Cells 12-15
    doc.add_heading('Cells 12-15: Compare All Strategies', level=2)

    add_callout(doc, 'show', 'Show the comparison table across all test queries')

    doc.add_paragraph(
        'Key observations from comparison:\n'
        '- "What is your return policy?" - All methods find faq_3\n'
        '- "free shipping" (keyword) - BM25 may do better\n'
        '- Natural language queries - Vector often wins\n'
        '- Hybrid provides consistent results across query types'
    )

    add_callout(doc, 'show', 'Show the bar chart visualization')

    add_callout(doc, 'ask', 'Looking at this chart, which method would you choose for a customer service chatbot?')

    # Cells 16-17
    doc.add_heading('Cells 16-17: Complete RAG with LLM Generation', level=2)

    add_callout(doc, 'theory', 'The RAG Pipeline')

    doc.add_paragraph(
        'Complete flow:\n'
        '1. User asks: "What is your return policy and refund timeline?"\n'
        '2. Retrieve: Get top 3 relevant chunks\n'
        '3. Augment: Build prompt with chunks as context\n'
        '4. Generate: LLM creates answer using context\n'
        '5. Return: Answer with source citations'
    )

    add_callout(doc, 'show', 'Show the complete RAG output: Question, Retrieved docs, Generated answer, Sources')

    add_callout(doc, 'say', 'Notice the answer combines information from multiple sources and cites them. This is the power of RAG!')

    # Cells 18-19
    doc.add_heading('Cells 18-19: Conversation Memory', level=2)

    add_callout(doc, 'theory', 'Why Memory Matters')

    doc.add_paragraph(
        'Without memory:\n'
        'User: "What is your return policy?"\n'
        'Bot: [answer about returns]\n'
        'User: "How long does IT take?"\n'
        'Bot: "What does IT refer to?" [BROKEN!]\n\n'
        'With memory:\n'
        'Bot understands "it" refers to returns from context.'
    )

    doc.add_paragraph(
        'Memory strategies:\n'
        '- Sliding window: Keep last N messages (we use 4)\n'
        '- Entity extraction: Remember names, preferences\n'
        '- Summary: Compress old context\n'
        '- Hybrid: Combine approaches'
    )

    add_callout(doc, 'show', 'Show the 3-turn conversation with follow-up questions')

    add_callout(doc, 'demo', 'Demonstrate asking "How long does IT take?" after return policy question')

    # Cells 20-21
    doc.add_heading('Cells 20-21: Source Attribution', level=2)

    add_callout(doc, 'theory', 'Why Citations Matter')

    doc.add_paragraph(
        'Benefits of source attribution:\n'
        '1. Trust: Users can verify information\n'
        '2. Debugging: Trace wrong answers to source\n'
        '3. Compliance: Required in regulated industries\n'
        '4. Improvement: Find knowledge gaps'
    )

    add_callout(doc, 'show', 'Show answer with inline [Source 1], [Source 2] citations')

    # Cells 22-23
    doc.add_heading('Cells 22-23: Evaluation', level=2)

    add_callout(doc, 'show', 'Show evaluation across 10 questions and 3 methods')

    add_callout(doc, 'say', 'This is how you would evaluate a RAG system before production. Compare methods, check answer quality.')

    add_callout(doc, 'transition', 'We have a working RAG system! Now let us package it as a web application.')

    doc.add_page_break()

    # =========================================================================
    # STREAMLIT & DEPLOYMENT
    # =========================================================================
    doc.add_heading('Streamlit Application & Deployment', level=1)

    doc.add_heading('Demo the Streamlit App', level=2)

    add_callout(doc, 'demo', 'Run: streamlit run app.py')

    doc.add_paragraph(
        'Features to demonstrate:\n'
        '1. Ask a question, show the response with citations\n'
        '2. Tell it your name, then ask "what is my name?" later\n'
        '3. Switch between Vector, BM25, Hybrid in sidebar\n'
        '4. Show the Sources section below each answer\n'
        '5. Show the sidebar with remembered user context'
    )

    add_callout(doc, 'ask', 'What features would you add to this chatbot for production?')

    doc.add_heading('Docker & AWS Fargate Deployment', level=2)

    add_callout(doc, 'ui', 'Walk through AWS Console for: ECR, ECS Cluster, Task Definition, Service')

    doc.add_paragraph(
        'Key deployment steps:\n'
        '1. Build Docker image with .env baked in\n'
        '2. Push to ECR (container registry)\n'
        '3. Create ECS cluster (Fargate = serverless)\n'
        '4. Define task (CPU, memory, container config)\n'
        '5. Create service (runs and maintains task)\n'
        '6. Get public IP and access app'
    )

    add_callout(doc, 'demo', 'Show the live deployed application!')

    doc.add_page_break()

    # =========================================================================
    # SUMMARY
    # =========================================================================
    doc.add_heading('Session Summary & Q&A', level=1)

    doc.add_heading('What We Covered', level=2)

    doc.add_paragraph(
        '1. What RAG is and why it matters\n'
        '2. Data preparation and chunking strategies\n'
        '3. AWS Bedrock Knowledge Base setup\n'
        '4. Three retrieval methods: Vector, BM25, Hybrid\n'
        '5. Complete RAG pipeline with LLM generation\n'
        '6. Conversation memory and source citations\n'
        '7. Production Streamlit application\n'
        '8. AWS Fargate deployment'
    )

    doc.add_heading('Key Takeaways', level=2)

    doc.add_paragraph(
        '- Chunking strategy matters: Use recursive with overlap\n'
        '- Hybrid search is usually best for production\n'
        '- Memory enables natural conversations\n'
        '- Citations build trust and enable debugging\n'
        '- AWS Bedrock simplifies vector database management'
    )

    doc.add_heading('Questions?', level=2)

    add_callout(doc, 'say', 'We have covered a lot! What questions do you have?')

    # Save
    output_path = '/Users/apalakkode/Library/CloudStorage/OneDrive-PayPal/Agentic RAG/ecommerce-chatbot/docs/RAG_Masterclass_Cell_by_Cell_Guide.docx'
    doc.save(output_path)
    print(f"Document saved to: {output_path}")
    return output_path

if __name__ == '__main__':
    create_guide()
