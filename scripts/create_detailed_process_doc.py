#!/usr/bin/env python3
"""Generate detailed Word document for RAG Masterclass with theory components."""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def add_colored_box(doc, text, color='blue'):
    """Add a colored callout box."""
    p = doc.add_paragraph()
    if color == 'blue':
        p.add_run('[THEORY] ').bold = True
    elif color == 'green':
        p.add_run('[SHOW UI] ').bold = True
    elif color == 'orange':
        p.add_run('[DEMO] ').bold = True
    elif color == 'purple':
        p.add_run('[RUN NOTEBOOK] ').bold = True
    p.add_run(text)
    return p

def create_detailed_document():
    doc = Document()

    # =========================================================================
    # TITLE PAGE
    # =========================================================================
    title = doc.add_heading('RAG & Agentic RAG Masterclass', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    subtitle = doc.add_paragraph('Building an E-commerce FAQ Chatbot with AWS Bedrock')
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()

    info = doc.add_paragraph()
    info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    info.add_run('Duration: 3 Hours (2 Sessions x 1.5 Hours)\n').bold = True
    info.add_run('Format: Hands-on Workshop with Theory & Practice')

    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    doc.add_heading('Table of Contents', level=1)

    toc_items = [
        'Part 1: Introduction to RAG',
        '  1.1 What is RAG?',
        '  1.2 Why RAG Matters',
        '  1.3 RAG Architecture Overview',
        '  1.4 Key Components',
        'Part 2: Environment Setup',
        '  2.1 AWS Configuration',
        '  2.2 S3 & Knowledge Base Setup',
        'Part 3: Data Preparation (Notebook 00-01)',
        '  3.1 Dataset Exploration',
        '  3.2 Chunking Strategies',
        'Part 4: Embeddings & Vector Search (Notebook 02)',
        '  4.1 What are Embeddings?',
        '  4.2 Vector Similarity',
        'Part 5: Retrieval Strategies (Notebook 03)',
        '  5.1 Vector Search',
        '  5.2 BM25 Keyword Search',
        '  5.3 Hybrid Search',
        'Part 6: RAG Pipeline',
        '  6.1 Conversational Memory',
        '  6.2 Source Attribution',
        'Part 7: Production Deployment',
        '  7.1 Streamlit Application',
        '  7.2 Docker & AWS Fargate',
    ]

    for item in toc_items:
        doc.add_paragraph(item)

    doc.add_page_break()

    # =========================================================================
    # PART 1: INTRODUCTION TO RAG
    # =========================================================================
    doc.add_heading('Part 1: Introduction to RAG', level=1)

    # ----- 1.1 What is RAG? -----
    doc.add_heading('1.1 What is RAG?', level=2)

    add_colored_box(doc, 'Start with this explanation before any notebooks', 'blue')

    doc.add_paragraph(
        'RAG (Retrieval-Augmented Generation) is a technique that enhances Large Language Models (LLMs) '
        'by giving them access to external knowledge sources. Instead of relying solely on what the model '
        'learned during training, RAG retrieves relevant information from a knowledge base and includes it '
        'in the prompt to generate more accurate, up-to-date, and contextual responses.'
    )

    doc.add_heading('The Problem RAG Solves', level=3)

    problems = [
        ('Knowledge Cutoff', 'LLMs are trained on data up to a certain date. They cannot know about events or information after their training cutoff.'),
        ('Hallucinations', 'LLMs can generate plausible-sounding but incorrect information when they do not have accurate knowledge.'),
        ('Domain-Specific Knowledge', 'General-purpose LLMs may lack specialized knowledge about your company, products, or industry.'),
        ('Verifiability', 'Without sources, users cannot verify if the LLM response is accurate.'),
    ]

    for title, desc in problems:
        p = doc.add_paragraph()
        p.add_run(f'{title}: ').bold = True
        p.add_run(desc)

    doc.add_heading('The RAG Solution', level=3)

    doc.add_paragraph(
        'RAG addresses these problems by:\n'
        '1. Storing your knowledge in a searchable vector database\n'
        '2. When a user asks a question, searching for relevant documents\n'
        '3. Including those documents in the LLM prompt as context\n'
        '4. Generating a response grounded in your actual data\n'
        '5. Citing sources so users can verify the information'
    )

    # ----- 1.2 Why RAG Matters -----
    doc.add_heading('1.2 Why RAG Matters', level=2)

    add_colored_box(doc, 'Explain the business value of RAG', 'blue')

    benefits = [
        ('Accuracy', 'Responses are grounded in your actual data, reducing hallucinations by up to 50-70%.'),
        ('Up-to-date', 'Knowledge base can be updated without retraining the LLM.'),
        ('Cost-effective', 'No need to fine-tune expensive models; just update your documents.'),
        ('Transparent', 'Source citations allow users to verify and trust the responses.'),
        ('Compliant', 'You control what data the model can access, important for regulated industries.'),
    ]

    for title, desc in benefits:
        p = doc.add_paragraph()
        p.add_run(f'{title}: ').bold = True
        p.add_run(desc)

    # ----- 1.3 RAG Architecture -----
    doc.add_heading('1.3 RAG Architecture Overview', level=2)

    add_colored_box(doc, 'Draw this diagram on whiteboard or show slide', 'blue')

    doc.add_paragraph('The RAG Pipeline consists of two main phases:')

    doc.add_heading('Indexing Phase (Offline)', level=3)

    steps = [
        'Load Documents: Gather your knowledge base (PDFs, FAQs, docs, etc.)',
        'Chunk Documents: Split into smaller, meaningful pieces',
        'Generate Embeddings: Convert text chunks into numerical vectors',
        'Store in Vector DB: Index vectors for fast similarity search',
    ]
    for i, step in enumerate(steps, 1):
        doc.add_paragraph(f'{i}. {step}')

    doc.add_heading('Query Phase (Online)', level=3)

    steps = [
        'User Query: User asks a question',
        'Query Embedding: Convert question to vector',
        'Retrieval: Find most similar document chunks',
        'Augmented Prompt: Combine query + retrieved context',
        'Generation: LLM generates response using context',
        'Response: Return answer with source citations',
    ]
    for i, step in enumerate(steps, 1):
        doc.add_paragraph(f'{i}. {step}')

    # ----- 1.4 Key Components -----
    doc.add_heading('1.4 Key Components', level=2)

    add_colored_box(doc, 'Explain each component we will use in this demo', 'blue')

    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'

    header = table.rows[0].cells
    header[0].text = 'Component'
    header[1].text = 'What We Use'
    header[2].text = 'Purpose'
    for cell in header:
        for p in cell.paragraphs:
            for r in p.runs:
                r.bold = True

    data = [
        ('Document Store', 'Amazon S3', 'Store raw FAQ documents'),
        ('Embeddings Model', 'Amazon Titan Embeddings v2', 'Convert text to 1024-dim vectors'),
        ('Vector Database', 'OpenSearch Serverless', 'Store and search vectors'),
        ('Knowledge Base', 'AWS Bedrock KB', 'Orchestrates indexing & retrieval'),
        ('LLM', 'OpenAI-compatible API (gpt-4o)', 'Generate natural language responses'),
        ('Application', 'Streamlit', 'User interface for the chatbot'),
        ('Deployment', 'AWS Fargate', 'Serverless container hosting'),
    ]

    for comp, tool, purpose in data:
        row = table.add_row().cells
        row[0].text = comp
        row[1].text = tool
        row[2].text = purpose

    doc.add_page_break()

    # =========================================================================
    # PART 2: ENVIRONMENT SETUP
    # =========================================================================
    doc.add_heading('Part 2: Environment Setup', level=1)

    doc.add_heading('2.1 AWS Configuration', level=2)

    add_colored_box(doc, 'AWS Console - IAM User creation', 'green')

    doc.add_paragraph('Prerequisites to explain:')
    items = [
        'AWS Account with billing enabled',
        'IAM permissions for: S3, Bedrock, ECR, ECS, CloudWatch',
        'Region: us-east-1 (Bedrock availability)',
    ]
    for item in items:
        doc.add_paragraph(item, style='List Bullet')

    doc.add_heading('.env File Configuration', level=3)

    doc.add_paragraph('Create .env file with these variables:')

    p = doc.add_paragraph()
    p.add_run('''AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=wJalr...
AWS_DEFAULT_REGION=us-east-1
KNOWLEDGE_BASE_ID=<will get after KB creation>
LLM_BASE_URL=<your LLM endpoint>
LLM_API_KEY=<your API key>
LLM_MODEL=gpt-4o''').italic = True

    doc.add_heading('2.2 S3 & Knowledge Base Setup', level=2)

    # S3
    doc.add_heading('Step 1: Create S3 Bucket', level=3)
    add_colored_box(doc, 'AWS Console > S3 > Create Bucket', 'green')

    steps = [
        'Bucket name: ecom-rag-bucket',
        'Region: us-east-1',
        'Block all public access: Yes (default)',
        'Versioning: Optional but recommended',
    ]
    for step in steps:
        doc.add_paragraph(step, style='List Bullet')

    add_colored_box(doc, 'Explain why S3 is the data source for Bedrock Knowledge Bases', 'blue')

    # Upload
    doc.add_heading('Step 2: Upload FAQ Data', level=3)
    add_colored_box(doc, 'Run notebooks/01.5_upload_to_s3.ipynb', 'purple')

    doc.add_paragraph(
        'The notebook creates a timestamped folder (e.g., knowledge-base-20260117_143521/) '
        'to prevent duplicate ingestion when syncing the Knowledge Base.'
    )

    add_colored_box(doc, 'Explain folder structure and why timestamps prevent duplicates', 'blue')

    # Knowledge Base
    doc.add_heading('Step 3: Create Bedrock Knowledge Base', level=3)
    add_colored_box(doc, 'AWS Console > Amazon Bedrock > Knowledge bases > Create', 'green')

    doc.add_paragraph('Configuration steps:')

    substeps = [
        ('Name', 'ecommerce-faq-kb'),
        ('Description', 'E-commerce FAQ Knowledge Base for RAG demo'),
        ('IAM Role', 'Create new role (let AWS handle permissions)'),
        ('Data Source', 'S3 - select your bucket and folder'),
        ('Embeddings', 'Titan Embeddings G1 - Text v2 (1024 dimensions)'),
        ('Vector Store', 'Quick create - OpenSearch Serverless'),
    ]

    for label, value in substeps:
        p = doc.add_paragraph()
        p.add_run(f'{label}: ').bold = True
        p.add_run(value)

    add_colored_box(doc, 'Explain what happens during KB creation: vector store provisioning, IAM roles, etc.', 'blue')

    # Sync
    doc.add_heading('Step 4: Sync Data', level=3)
    add_colored_box(doc, 'Knowledge Base > Data source > Sync', 'green')

    doc.add_paragraph(
        'The sync process:\n'
        '1. Reads documents from S3\n'
        '2. Chunks them using default strategy\n'
        '3. Generates embeddings with Titan\n'
        '4. Stores vectors in OpenSearch\n'
        '5. Creates metadata index for filtering'
    )

    add_colored_box(doc, 'Explain ingestion jobs and when to re-sync (new data added)', 'blue')

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('IMPORTANT: ').bold = True
    p.add_run('Copy the Knowledge Base ID and update your .env file!')

    doc.add_page_break()

    # =========================================================================
    # PART 3: DATA PREPARATION
    # =========================================================================
    doc.add_heading('Part 3: Data Preparation', level=1)

    doc.add_heading('Notebook 00: Setup & Connections', level=2)
    add_colored_box(doc, 'notebooks/00_setup_and_connections.ipynb', 'purple')

    doc.add_heading('Cell-by-Cell Guide', level=3)

    # Cell guide for notebook 00
    cells_00 = [
        ('Cell 1-3: Install & Import',
         'Quick setup - no theory needed',
         'Just run and verify imports succeed'),

        ('Cell 4-5: AWS Credentials',
         'Explain .env file and why we use environment variables for secrets',
         'Show that credentials are loaded from .env'),

        ('Cell 6-7: Test AWS Connection',
         'Explain boto3 and STS (Security Token Service)',
         'Verify Account ID matches expected'),

        ('Cell 8-9: List Bedrock Models',
         'Explain Bedrock model ecosystem: Foundation models vs Knowledge bases',
         'Show available embedding models'),

        ('Cell 10-11: Test LLM API',
         'Explain OpenAI-compatible APIs and why we use external LLM',
         'Verify LLM responds correctly'),

        ('Cell 12-13: Test Titan Embeddings',
         'Key theory: What are embeddings? Why 1024 dimensions?',
         'Show sample embedding vector'),

        ('Cell 14-21: Download Dataset',
         'Explain the HuggingFace dataset and what FAQ data looks like',
         'Preview Q&A pairs'),
    ]

    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    header = table.rows[0].cells
    header[0].text = 'Cell'
    header[1].text = 'Theory to Explain'
    header[2].text = 'Expected Output'
    for cell in header:
        for p in cell.paragraphs:
            for r in p.runs:
                r.bold = True

    for cell_name, theory, output in cells_00:
        row = table.add_row().cells
        row[0].text = cell_name
        row[1].text = theory
        row[2].text = output

    doc.add_heading('Notebook 01: Data Exploration & Chunking', level=2)
    add_colored_box(doc, 'notebooks/01_data_exploration_chunking.ipynb', 'purple')

    doc.add_heading('Theory: Chunking Strategies', level=3)
    add_colored_box(doc, 'Explain before running chunking cells', 'blue')

    doc.add_paragraph(
        'Chunking is how we split documents into smaller pieces for embedding. '
        'The chunk size affects retrieval quality:'
    )

    chunking = [
        ('Too Small', 'Loses context, may retrieve irrelevant fragments'),
        ('Too Large', 'May exceed token limits, dilutes relevance'),
        ('Just Right', 'Complete thoughts, fits model context, good retrieval'),
    ]

    for size, effect in chunking:
        p = doc.add_paragraph()
        p.add_run(f'{size}: ').bold = True
        p.add_run(effect)

    doc.add_heading('Common Chunking Methods', level=3)

    methods = [
        ('Fixed Size', 'Split every N characters/tokens. Simple but may break mid-sentence.'),
        ('Sentence-based', 'Split at sentence boundaries. Preserves meaning.'),
        ('Paragraph-based', 'Split at paragraph breaks. Good for structured docs.'),
        ('Semantic', 'Split based on topic changes. Most sophisticated.'),
        ('Recursive', 'Try multiple separators in order. Used by LangChain.'),
    ]

    for method, desc in methods:
        p = doc.add_paragraph()
        p.add_run(f'{method}: ').bold = True
        p.add_run(desc)

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('For FAQ data: ').bold = True
    p.add_run('Each Q&A pair is already a natural chunk! No splitting needed.')

    doc.add_page_break()

    # =========================================================================
    # PART 4: EMBEDDINGS
    # =========================================================================
    doc.add_heading('Part 4: Embeddings & Vector Search', level=1)

    doc.add_heading('Notebook 02: Embeddings and Indexing', level=2)
    add_colored_box(doc, 'notebooks/02_embeddings_and_indexing.ipynb', 'purple')

    doc.add_heading('4.1 What are Embeddings?', level=2)
    add_colored_box(doc, 'Core concept - spend time explaining this well', 'blue')

    doc.add_paragraph(
        'Embeddings are numerical representations of text in a high-dimensional vector space. '
        'Think of them as coordinates that capture the meaning of text.'
    )

    doc.add_heading('Key Concepts', level=3)

    concepts = [
        ('Vector', 'A list of numbers, e.g., [0.1, -0.3, 0.5, ...] with 1024 values'),
        ('Dimensions', 'Each number represents a different aspect of meaning'),
        ('Semantic Space', 'Similar meanings are close together in this space'),
        ('Distance', 'Measure how similar two texts are by their vector distance'),
    ]

    for concept, desc in concepts:
        p = doc.add_paragraph()
        p.add_run(f'{concept}: ').bold = True
        p.add_run(desc)

    doc.add_heading('Analogy for Embeddings', level=3)

    doc.add_paragraph(
        'Imagine a library where books are arranged not by author or title, but by meaning. '
        'Books about cooking are near each other. Books about space travel are in another area. '
        'A book about "cooking in space" would be between both areas. '
        'Embeddings work the same way but in 1024 dimensions!'
    )

    doc.add_heading('4.2 Vector Similarity', level=2)
    add_colored_box(doc, 'Explain before similarity search cells', 'blue')

    doc.add_paragraph('How do we measure if two texts are similar?')

    similarity = [
        ('Cosine Similarity', 'Measures angle between vectors. Range: -1 to 1. Most common.'),
        ('Euclidean Distance', 'Straight-line distance. Smaller = more similar.'),
        ('Dot Product', 'Related to cosine but not normalized. Fast to compute.'),
    ]

    for method, desc in similarity:
        p = doc.add_paragraph()
        p.add_run(f'{method}: ').bold = True
        p.add_run(desc)

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('We use Cosine Similarity: ').bold = True
    p.add_run('cos(A, B) = (A . B) / (||A|| * ||B||)')

    doc.add_heading('Visualization', level=3)
    add_colored_box(doc, 'Show the embedding visualization plot in notebook', 'orange')

    doc.add_paragraph(
        'The notebook uses PCA/t-SNE to reduce 1024 dimensions to 2D for visualization. '
        'You will see clusters of similar FAQs appearing together.'
    )

    doc.add_page_break()

    # =========================================================================
    # PART 5: RETRIEVAL STRATEGIES
    # =========================================================================
    doc.add_heading('Part 5: Retrieval Strategies', level=1)

    doc.add_heading('Notebook 03: Retrieval and RAG', level=2)
    add_colored_box(doc, 'notebooks/03_retrieval_and_rag.ipynb', 'purple')

    doc.add_heading('5.1 Vector Search (Semantic Search)', level=2)
    add_colored_box(doc, 'Explain before vector search cells', 'blue')

    doc.add_paragraph('Vector search finds documents based on meaning, not keywords.')

    doc.add_heading('How It Works', level=3)

    steps = [
        'Convert query to embedding using same model',
        'Compare query vector to all document vectors',
        'Return top-K most similar documents',
        'Similarity is based on cosine distance',
    ]
    for i, step in enumerate(steps, 1):
        doc.add_paragraph(f'{i}. {step}')

    doc.add_heading('Strengths & Weaknesses', level=3)

    p = doc.add_paragraph()
    p.add_run('Strengths: ').bold = True
    p.add_run('Understands synonyms, paraphrasing, conceptual similarity')

    p = doc.add_paragraph()
    p.add_run('Weaknesses: ').bold = True
    p.add_run('May miss exact keyword matches, computationally expensive')

    doc.add_heading('Example', level=3)
    doc.add_paragraph('Query: "How do I send back a product?"')
    doc.add_paragraph('Matches: "What is your return policy?" (semantic match)')

    doc.add_heading('5.2 BM25 Keyword Search', level=2)
    add_colored_box(doc, 'Explain before BM25 cells', 'blue')

    doc.add_paragraph(
        'BM25 (Best Match 25) is a traditional keyword-based ranking algorithm. '
        'It is the algorithm behind Elasticsearch and many search engines.'
    )

    doc.add_heading('How It Works', level=3)

    steps = [
        'Tokenize query and documents into words',
        'Count term frequency (TF) in each document',
        'Calculate inverse document frequency (IDF) - rare words score higher',
        'Combine TF and IDF with length normalization',
        'Rank documents by final score',
    ]
    for i, step in enumerate(steps, 1):
        doc.add_paragraph(f'{i}. {step}')

    doc.add_heading('Strengths & Weaknesses', level=3)

    p = doc.add_paragraph()
    p.add_run('Strengths: ').bold = True
    p.add_run('Exact keyword matching, fast, no embeddings needed, good for specific terms')

    p = doc.add_paragraph()
    p.add_run('Weaknesses: ').bold = True
    p.add_run('Misses synonyms and paraphrases, no semantic understanding')

    doc.add_heading('Example', level=3)
    doc.add_paragraph('Query: "PayPal payment"')
    doc.add_paragraph('Matches: Documents containing "PayPal" and "payment" exactly')

    doc.add_heading('5.3 Hybrid Search', level=2)
    add_colored_box(doc, 'Key concept - this is what production systems use', 'blue')

    doc.add_paragraph(
        'Hybrid search combines vector search and keyword search to get the best of both worlds.'
    )

    doc.add_heading('The Alpha Parameter', level=3)

    doc.add_paragraph('final_score = alpha * vector_score + (1 - alpha) * bm25_score')

    alpha_values = [
        ('alpha = 1.0', 'Pure vector search (semantic only)'),
        ('alpha = 0.0', 'Pure BM25 search (keywords only)'),
        ('alpha = 0.5', 'Balanced hybrid (recommended starting point)'),
        ('alpha = 0.7', 'Favor semantic, but consider keywords'),
    ]

    for val, desc in alpha_values:
        p = doc.add_paragraph()
        p.add_run(f'{val}: ').bold = True
        p.add_run(desc)

    doc.add_heading('Why Hybrid Works Best', level=3)

    doc.add_paragraph(
        'Consider the query: "PayPal refund process"\n\n'
        '- Vector search finds: documents about "returning money", "payment reversals"\n'
        '- BM25 finds: documents with exact word "PayPal"\n'
        '- Hybrid finds: documents about PayPal-specific refund policies (best match!)'
    )

    doc.add_page_break()

    # =========================================================================
    # PART 6: RAG PIPELINE
    # =========================================================================
    doc.add_heading('Part 6: RAG Pipeline', level=1)

    doc.add_heading('6.1 Conversational Memory', level=2)
    add_colored_box(doc, 'Explain before memory demo cells', 'blue')

    doc.add_paragraph(
        'A good chatbot remembers the conversation context. Without memory, each question '
        'is treated in isolation.'
    )

    doc.add_heading('Memory Strategies', level=3)

    strategies = [
        ('No Memory', 'Each turn is independent. Simple but poor UX.'),
        ('Full History', 'Include all previous messages. May exceed token limits.'),
        ('Sliding Window', 'Keep last N messages. Balance of context and tokens.'),
        ('Summary Memory', 'Summarize old messages. Preserves key info, saves tokens.'),
        ('Entity Memory', 'Extract and store key entities (names, preferences).'),
    ]

    for strategy, desc in strategies:
        p = doc.add_paragraph()
        p.add_run(f'{strategy}: ').bold = True
        p.add_run(desc)

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('Our Implementation: ').bold = True
    p.add_run('Sliding window (last 6 messages) + Entity extraction for user context (name, preferences)')

    doc.add_heading('6.2 Source Attribution', level=2)
    add_colored_box(doc, 'Important for trust and compliance', 'blue')

    doc.add_paragraph(
        'Source attribution tells users where the information came from. '
        'This is critical for:'
    )

    items = [
        'Trust: Users can verify the information',
        'Debugging: You can trace incorrect responses to source documents',
        'Compliance: Required in regulated industries (finance, healthcare)',
        'Improvement: Identify gaps in your knowledge base',
    ]
    for item in items:
        doc.add_paragraph(item, style='List Bullet')

    doc.add_heading('Implementation', level=3)

    doc.add_paragraph(
        'Our chatbot:\n'
        '1. Retrieves documents with metadata (source file, chunk ID)\n'
        '2. Includes sources in the LLM prompt\n'
        '3. Instructs LLM to cite sources inline [1], [2]\n'
        '4. Displays source documents below the response'
    )

    doc.add_page_break()

    # =========================================================================
    # PART 7: PRODUCTION DEPLOYMENT
    # =========================================================================
    doc.add_heading('Part 7: Production Deployment', level=1)

    doc.add_heading('7.1 Streamlit Application', level=2)

    doc.add_heading('Local Testing', level=3)
    add_colored_box(doc, 'Run: streamlit run app.py', 'purple')

    doc.add_paragraph('Demo the following features:')

    demos = [
        'Ask a product question and see the response',
        'Notice the source citations below the answer',
        'Tell the chatbot your name, then ask "what is my name?" later',
        'Switch between Vector, BM25, and Hybrid search modes',
        'Show the sidebar with user context memory',
    ]
    for demo in demos:
        doc.add_paragraph(demo, style='List Bullet')

    add_colored_box(doc, 'Live demo of chatbot features', 'orange')

    doc.add_heading('7.2 Docker & AWS Fargate Deployment', level=2)

    doc.add_heading('Step 1: Build Docker Image', level=3)

    doc.add_paragraph('docker build -t ecommerce-rag-chatbot .')

    add_colored_box(doc, 'Explain Dockerfile: base image, dependencies, .env inclusion', 'blue')

    doc.add_heading('Step 2: Create ECR Repository', level=3)
    add_colored_box(doc, 'AWS Console > ECR > Create Repository', 'green')

    doc.add_paragraph('Repository name: ecommerce-rag-chatbot')

    doc.add_heading('Step 3: Push to ECR', level=3)

    p = doc.add_paragraph()
    p.add_run('''aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com

docker tag ecommerce-rag-chatbot:latest <account>.dkr.ecr.us-east-1.amazonaws.com/ecommerce-rag-chatbot:latest

docker push <account>.dkr.ecr.us-east-1.amazonaws.com/ecommerce-rag-chatbot:latest''').italic = True

    doc.add_heading('Step 4: Create ECS Cluster', level=3)
    add_colored_box(doc, 'AWS Console > ECS > Create Cluster', 'green')

    items = [
        'Cluster name: ecommerce-rag-cluster',
        'Infrastructure: AWS Fargate (serverless)',
    ]
    for item in items:
        doc.add_paragraph(item, style='List Bullet')

    add_colored_box(doc, 'Explain Fargate: serverless containers, no server management', 'blue')

    doc.add_heading('Step 5: Create Task Definition', level=3)
    add_colored_box(doc, 'AWS Console > ECS > Task Definitions > Create', 'green')

    items = [
        'Family: ecommerce-rag-task',
        'CPU: 0.5 vCPU, Memory: 1 GB',
        'Container: ecommerce-rag-app',
        'Image: <ECR URI>:latest',
        'Port: 8501',
    ]
    for item in items:
        doc.add_paragraph(item, style='List Bullet')

    doc.add_heading('Step 6: Create Service', level=3)
    add_colored_box(doc, 'AWS Console > ECS > Cluster > Create Service', 'green')

    items = [
        'Launch type: FARGATE',
        'Task definition: ecommerce-rag-task',
        'Desired count: 1',
        'Security group: Allow port 8501',
        'Public IP: Enabled',
    ]
    for item in items:
        doc.add_paragraph(item, style='List Bullet')

    doc.add_heading('Step 7: Access Live Application', level=3)
    add_colored_box(doc, 'Get Public IP from ECS Task and open http://<ip>:8501', 'green')

    add_colored_box(doc, 'Final demo: Show the live deployed chatbot!', 'orange')

    doc.add_page_break()

    # =========================================================================
    # QUICK REFERENCE
    # =========================================================================
    doc.add_heading('Quick Reference: Presenter Checklist', level=1)

    doc.add_heading('UI Checkpoints', level=2)

    table = doc.add_table(rows=1, cols=4)
    table.style = 'Table Grid'

    header = table.rows[0].cells
    header[0].text = '#'
    header[1].text = 'Service'
    header[2].text = 'Action'
    header[3].text = 'When'
    for cell in header:
        for p in cell.paragraphs:
            for r in p.runs:
                r.bold = True

    checkpoints = [
        ('1', 'S3', 'Create bucket', 'Before notebooks'),
        ('2', 'Bedrock', 'Create Knowledge Base', 'Before notebooks'),
        ('3', 'Bedrock', 'Sync data source', 'After S3 upload'),
        ('4', 'Local', 'Run Streamlit app', 'After Notebook 03'),
        ('5', 'ECR', 'Create repository', 'Before Docker push'),
        ('6', 'ECS', 'Create cluster', 'After ECR push'),
        ('7', 'ECS', 'Create task definition', 'After cluster'),
        ('8', 'ECS', 'Create service', 'After task def'),
        ('9', 'Browser', 'Demo live app', 'Final step'),
    ]

    for num, service, action, when in checkpoints:
        row = table.add_row().cells
        row[0].text = num
        row[1].text = service
        row[2].text = action
        row[3].text = when

    doc.add_heading('Theory Topics by Notebook', level=2)

    table = doc.add_table(rows=1, cols=2)
    table.style = 'Table Grid'

    header = table.rows[0].cells
    header[0].text = 'Notebook'
    header[1].text = 'Key Theory Topics'
    for cell in header:
        for p in cell.paragraphs:
            for r in p.runs:
                r.bold = True

    theory = [
        ('00 Setup', 'AWS services, API authentication, Environment variables'),
        ('01 Data', 'Chunking strategies, Document preparation, Data quality'),
        ('02 Embeddings', 'What are embeddings, Vector similarity, Visualization'),
        ('03 Retrieval', 'Vector vs BM25 vs Hybrid, Alpha tuning, Trade-offs'),
        ('03 RAG', 'Prompt engineering, Memory strategies, Source attribution'),
        ('App Demo', 'Production considerations, User experience, Deployment'),
    ]

    for nb, topics in theory:
        row = table.add_row().cells
        row[0].text = nb
        row[1].text = topics

    # Save
    output_path = '/Users/apalakkode/Library/CloudStorage/OneDrive-PayPal/Agentic RAG/ecommerce-chatbot/docs/RAG_Masterclass_Detailed_Guide.docx'
    doc.save(output_path)
    print(f"Document saved to: {output_path}")
    return output_path

if __name__ == '__main__':
    create_detailed_document()
