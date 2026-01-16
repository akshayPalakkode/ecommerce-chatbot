# E-commerce Data Strategy for RAG Demo

## Data Architecture

```
┌─────────────────────────────────────────────────────────┐
│              KNOWLEDGE BASE (Static)                     │
│  Bedrock KB ← S3 Bucket ← Local Markdown Files         │
│  - Policies, FAQs, Product Care, etc.                  │
└─────────────────────────────────────────────────────────┘
                         ↓ (RAG Retrieval)

┌─────────────────────────────────────────────────────────┐
│                  AGENT (LangGraph)                       │
│  - Decides: Retrieve KB or Call Tool                    │
└─────────────────────────────────────────────────────────┘
                         ↓
                ┌────────┴────────┐
                ↓                 ↓
┌───────────────────┐    ┌────────────────────┐
│ TRANSACTIONAL DB  │    │   PRODUCT DB       │
│  (DynamoDB/Mock)  │    │   (DynamoDB/Mock)  │
│  - Orders         │    │   - Products       │
│  - Customers      │    │   - Inventory      │
└───────────────────┘    └────────────────────┘
```

---

## Recommended Data Setup

### Phase 1: Quick Demo (Use Mock Data)
**Best for**: 1.5 hour session, local development

✅ **Mock Data in Python**:
- Hardcoded sample orders (3-5 examples)
- Hardcoded products (10-20 items)
- Knowledge base: Markdown files (existing)

**Pros**:
- ✅ No database setup needed
- ✅ Fast to demo
- ✅ Easy to understand
- ✅ Shows RAG + Agent pattern clearly

**Cons**:
- ❌ Not "real" production data
- ❌ Can't show scaling

### Phase 2: Production Demo (Real Database)
**Best for**: Production showcase, longer sessions

✅ **DynamoDB Tables**:
- Orders table (100-1000 sample orders)
- Products table (50-200 products)
- Customers table (optional)

**Pros**:
- ✅ Production-like
- ✅ Shows AWS integration
- ✅ Scalable

**Cons**:
- ❌ Requires setup time
- ❌ Small AWS costs

---

## Data Sources

### Option 1: Generate Synthetic Data (Recommended)
Use Python faker library to create realistic data:

```python
from faker import Faker
import random
import json

fake = Faker()

# Generate 100 orders
orders = []
for i in range(100):
    orders.append({
        "order_id": f"ORD{10000 + i}",
        "customer_name": fake.name(),
        "customer_email": fake.email(),
        "status": random.choice(["processing", "shipped", "delivered", "cancelled"]),
        "order_date": fake.date_between(start_date="-90d", end_date="today").isoformat(),
        "total": round(random.uniform(20, 500), 2),
        "items": [
            {
                "product_id": f"P{random.randint(1, 50):03d}",
                "name": fake.catch_phrase(),
                "quantity": random.randint(1, 3),
                "price": round(random.uniform(10, 100), 2)
            }
        ]
    })

# Save
with open('mock_orders.json', 'w') as f:
    json.dump(orders, f, indent=2)
```

### Option 2: Use Public E-commerce Datasets
- **Kaggle**: E-commerce datasets (Amazon, Shopify)
- **UCI ML Repository**: Online Retail dataset
- **Sample data from Stripe/Shopify docs**

### Option 3: Real Company Data (if available)
- Anonymize sensitive info
- Use subset for demo

---

## Recommended Setup for Your Demo

### Knowledge Base (Vector Store)
**Location**: Bedrock Knowledge Base (backed by S3)

**Files to Create**:
1. `return_policy.md` ✅ (already have)
2. `shipping_policy.md` ✅ (already have)
3. `product_info.md` ✅ (already have)
4. `faq.md` (NEW - add common questions)
5. `warranty_policy.md` (NEW - warranty info)

**Total**: ~5 documents, 10-20 KB total

### Transactional Data (Mock/DynamoDB)
**Location**: Start with mock Python dict, optionally migrate to DynamoDB

**Mock Data**:
```python
# app/data/mock_data.py

MOCK_ORDERS = {
    "12345": {
        "order_id": "12345",
        "customer_name": "John Doe",
        "status": "delivered",
        "order_date": "2025-01-10",
        "delivery_date": "2025-01-15",
        "items": [
            {
                "product_id": "P001",
                "name": "Blue Cotton T-Shirt",
                "quantity": 2,
                "price": 29.99
            }
        ],
        "total": 59.98,
        "tracking_number": "1Z999AA10123456784"
    },
    "12346": {
        "order_id": "12346",
        "customer_name": "Jane Smith",
        "status": "shipped",
        "order_date": "2025-01-14",
        "expected_delivery": "2025-01-18",
        "items": [
            {
                "product_id": "P002",
                "name": "Black Jeans",
                "quantity": 1,
                "price": 79.99
            }
        ],
        "total": 79.99,
        "tracking_number": "1Z999AA10987654321"
    },
    "12347": {
        "order_id": "12347",
        "customer_name": "Bob Johnson",
        "status": "processing",
        "order_date": "2025-01-16",
        "items": [
            {
                "product_id": "P003",
                "name": "White Sneakers",
                "quantity": 1,
                "price": 89.99
            }
        ],
        "total": 89.99
    }
}

MOCK_PRODUCTS = {
    "P001": {
        "product_id": "P001",
        "name": "Blue Cotton T-Shirt",
        "category": "Apparel",
        "price": 29.99,
        "in_stock": True,
        "stock_quantity": 150,
        "description": "100% organic cotton, machine washable",
        "sizes": ["S", "M", "L", "XL"]
    },
    "P002": {
        "product_id": "P002",
        "name": "Black Jeans",
        "category": "Apparel",
        "price": 79.99,
        "in_stock": True,
        "stock_quantity": 75,
        "description": "Premium denim, slim fit",
        "sizes": ["28", "30", "32", "34", "36"]
    },
    "P003": {
        "product_id": "P003",
        "name": "White Sneakers",
        "category": "Footwear",
        "price": 89.99,
        "in_stock": True,
        "stock_quantity": 50,
        "description": "Comfortable everyday sneakers",
        "sizes": ["7", "8", "9", "10", "11", "12"]
    }
}
```

---

## Data Volume Recommendations

### For 1.5 Hour Demo:
- **Knowledge Base**: 5-10 documents (~20-50 KB)
- **Orders**: 5-10 mock orders
- **Products**: 10-20 products
- **Customers**: Optional (can derive from orders)

### For Production Showcase:
- **Knowledge Base**: 20-50 documents (~100-500 KB)
- **Orders**: 1,000-10,000 orders
- **Products**: 100-1,000 products
- **Customers**: 500-5,000 customers

---

## Implementation Steps

### Step 1: Create Knowledge Base Files (5 min)
Use existing + add 2 more:
- ✅ return_policy.md (have)
- ✅ shipping_policy.md (have)
- ✅ product_info.md (have)
- ⭕ faq.md (create)
- ⭕ warranty_policy.md (create)

### Step 2: Create Mock Data (10 min)
Create `app/data/mock_data.py` with:
- 5 sample orders
- 10 sample products
- Helper functions to query

### Step 3: Upload to S3 (5 min)
Upload markdown files to S3 bucket for Bedrock KB

### Step 4: Create Bedrock Knowledge Base (10 min)
Via AWS Console, point to S3 bucket

### Step 5: Test Integration (10 min)
Query knowledge base, test mock data access

---

## Alternative: Use Real E-commerce Dataset

If you want realistic data without manual creation:

### Kaggle Datasets (Free):
1. **"E-Commerce Data"** by CarAdvice
   - 500K+ transactions
   - Product info, prices, categories

2. **"Brazilian E-Commerce Public Dataset by Olist"**
   - 100K orders
   - Products, reviews, customers

3. **"Online Retail Dataset"** (UCI)
   - 500K transactions
   - UK-based retailer

**How to use**:
1. Download CSV from Kaggle
2. Convert to JSON
3. Load into DynamoDB or use as mock data
4. Clean/anonymize if needed

---

## My Recommendation for Your 1.5 Hour Session:

### Use This Setup:
1. **Knowledge Base**: 5 markdown files (3 existing + 2 new) → Upload to S3 → Bedrock KB
2. **Orders**: 5-10 mock orders in Python dict (no database needed)
3. **Products**: 10-15 mock products in Python dict

### Why This Works:
- ✅ Fast to set up (30 min total)
- ✅ Shows both RAG (policies) and Tools (orders)
- ✅ Easy to demo and explain
- ✅ Can scale to real DB later
- ✅ No database costs during dev

### Demo Flow:
1. **Query 1**: "What is your return policy?" → Retrieves from Bedrock KB
2. **Query 2**: "Where is order 12345?" → Uses tool to query mock data
3. **Query 3**: "Return order 12345, damaged item" → Multi-step: Check order + Calculate refund + Cite policy
4. **Shows**: RAG + Agentic behavior + Citations

---

## Next Steps

Would you like me to:
1. ✅ Create the 2 additional knowledge base markdown files (faq.md, warranty_policy.md)?
2. ✅ Create the mock data Python file with realistic e-commerce data?
3. ✅ Create a data generator script using Faker for more data?
4. ✅ All of the above?

Let me know and I'll create the files!
