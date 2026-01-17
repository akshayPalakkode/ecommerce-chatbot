# E-commerce RAG Chatbot - Streamlit Application

Production-ready chatbot with multiple retrieval strategies, conversation memory, and source attribution.

## Features

- **Multiple Retrieval Strategies**
  - Vector Search: Semantic similarity using embeddings
  - BM25: Keyword-based search
  - Hybrid: Best of both worlds (recommended)

- **Conversation Memory**
  - Maintains chat history
  - Handles follow-up questions
  - Context-aware responses

- **Source Attribution**
  - Shows document sources for each answer
  - Relevance scores displayed
  - Transparent and verifiable

- **Interactive UI**
  - Clean, modern interface
  - Real-time chat experience
  - Export conversation history

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements-app.txt
```

### 2. Configure Environment

Ensure your `.env` file has:

```bash
# AWS Bedrock
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_DEFAULT_REGION=us-east-1
KNOWLEDGE_BASE_ID=XVIAYNVNB2

# LLM
LLM_BASE_URL=your_llm_endpoint
LLM_API_KEY=your_api_key
LLM_MODEL=gpt-4o
```

### 3. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

### Basic Chat

1. Type your question in the chat input
2. Press Enter to send
3. View the response and sources
4. Continue the conversation naturally

### Change Retrieval Method

1. Use the sidebar to select retrieval strategy
2. Click "Apply Settings"
3. Start a new conversation

### Export Conversation

1. Click "Export Conversation" in the sidebar
2. Download the JSON file with full conversation history

## Architecture

```
app.py (Streamlit UI)
    ↓
src/ecommerce_rag/
    ├── config.py         # Configuration management
    ├── retrieval.py      # Vector, BM25, Hybrid retrievers
    └── rag.py           # RAG pipeline & conversational system
    ↓
AWS Bedrock Knowledge Base (Vector DB)
Local BM25 Index (Keyword Search)
    ↓
LLM Generation (OpenAI-compatible API)
```

## Configuration Options

### Sidebar Settings

- **Retrieval Strategy**: Switch between vector, BM25, or hybrid
- **System Info**: View current model and configuration
- **Conversation Controls**: Clear history or export chat

### Code Configuration

Edit `src/ecommerce_rag/config.py` to adjust:

- `DEFAULT_NUM_RESULTS`: Number of documents to retrieve (default: 3)
- `HYBRID_ALPHA`: Balance between vector and BM25 (default: 0.5)
- `TEMPERATURE`: LLM creativity (default: 0.1 for consistency)
- `MAX_TOKENS`: Maximum response length (default: 500)
- `MAX_HISTORY_LENGTH`: Conversation turns to remember (default: 4)

## Deployment

### Local Development

```bash
streamlit run app.py
```

### Production (Streamlit Cloud)

1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Add secrets in Streamlit dashboard:
   - AWS credentials
   - LLM API keys
   - Knowledge Base ID

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements-app.txt .
RUN pip install -r requirements-app.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:

```bash
docker build -t ecommerce-chatbot .
docker run -p 8501:8501 --env-file .env ecommerce-chatbot
```

### AWS EC2 Deployment

1. Launch EC2 instance (t2.small or larger)
2. Install Python and dependencies
3. Clone repository
4. Set up environment variables
5. Run with systemd or supervisor

```bash
# Install
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements-app.txt

# Run
nohup streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &
```

## Troubleshooting

### Configuration Errors

**Error**: "Configuration incomplete"
**Solution**: Check `.env` file has all required variables

### Retrieval Errors

**Error**: "Error retrieving documents"
**Solutions**:
- Verify AWS credentials are valid
- Check Knowledge Base ID is correct
- Ensure ingestion job completed successfully

### LLM Errors

**Error**: "Error generating response"
**Solutions**:
- Verify LLM API key is valid
- Check LLM endpoint URL is correct
- Ensure network connectivity to LLM service

### Import Errors

**Error**: "Module not found"
**Solution**:
```bash
pip install -r requirements-app.txt
```

## Performance Tips

1. **Hybrid Search**: Use alpha=0.5 for balanced performance
2. **Num Results**: 3-5 documents provides best context
3. **Temperature**: Keep low (0.1) for consistent answers
4. **History Length**: 4 turns balances context and performance

## Security Notes

- Never commit `.env` file to version control
- Use environment variables for sensitive data
- Restrict AWS IAM permissions to minimum required
- Use HTTPS in production deployments
- Implement rate limiting for public deployments

## Monitoring

Add logging for production:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

Track metrics:
- Query latency
- Retrieval scores
- User satisfaction
- Error rates

## Next Steps

- Add authentication for user accounts
- Implement feedback collection
- Add analytics dashboard
- Create A/B testing for retrieval methods
- Build mobile-responsive design
- Add multilingual support
