# 🚀 QUICK START GUIDE
## Proxi: The Context-Aware Cloud Guardian - ArmorIQ Hackathon

### ⚡ Get Running in 60 Seconds

```bash
# 1. Navigate to the project
cd proxi-armoriq

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the demo!
python main.py
```

That's it! The demo runs with a mock LLM, **no API keys required**.

---

## 🎯 What You'll See

The demo runs three scenarios:

### Scenario 1: NORMAL Mode Block
```
Agent tries: "Restart the web server"
Policy says: ❌ BLOCKED - Read-only mode
Result: Agent explains why it's blocked and suggests alternatives
```

### Scenario 2: EMERGENCY Mode Success  
```
Agent tries: "Fix the critical web server issue"
Policy says: ✅ ALLOWED - Emergency mode permits corrective actions
Result: Agent successfully restarts the service
```

### Scenario 3: Always Blocked
```
Agent tries: "Delete the database to clear space"
Policy says: ❌ BLOCKED - Destructive operations always forbidden
Result: Agent refuses and proposes safer alternatives
```

---

## 🎬 Expected Demo Output

```
================================================================================
                    PROXI: THE CONTEXT-AWARE CLOUD GUARDIAN
                         ArmorIQ Hackathon Demo
================================================================================

Starting MCP Server...
✓ MCP Server is ready

Initializing Proxi Agent...
✓ Agent initialized

┌──────────────────────────────────────────────────────────────────────────────┐
│ SCENARIO 1: NORMAL MODE - Corrective Action Blocked                         │
├──────────────────────────────────────────────────────────────────────────────┤
│ Agent attempts to restart a service but is blocked by policy                │
└──────────────────────────────────────────────────────────────────────────────┘

🤖 Agent reasoning process:
   → Thought: The task requires restarting a service
   → Action: Attempting to use restart_service tool
   → Observation: ❌ POLICY BLOCKED

💬 Agent response:
I attempted to restart the web-server, but the operation was blocked by policy.
This is because we are in NORMAL mode that only allows read-only operations...

[... continues with scenarios 2 and 3 ...]

================================================================================
                        DEMONSTRATION COMPLETE
================================================================================
```

---

## 🔍 Exploring the Code

### Core Components

1. **Policy Engine** (`src/guardrails/policy_engine.py`)
   - Validates every action against policies
   - Enforces mode-based constraints
   - Simple API: `engine.validate(tool_name)`

2. **MCP Server** (`src/mcp_server/server.py`)
   - FastAPI server exposing tools
   - **CRITICAL**: Every tool call goes through policy validation first
   - Try it: `http://localhost:8000/docs` while running

3. **AI Agent** (`src/agent/bot.py`)
   - LangChain-powered SRE agent
   - Respects policy blocks
   - Explains constraints to users

4. **Policy Definition** (`policies/ops_policy.json`)
   - Declarative security rules
   - Easy to modify and audit
   - Two modes: NORMAL (read-only) and EMERGENCY (corrective)

---

## 🧪 Test Individual Components

```bash
# Test just the policy engine
python -c "
from src.guardrails.policy_engine import PolicyEngine
engine = PolicyEngine('policies/ops_policy.json')
print(engine.get_policy_summary())
"

# Verify installation
python test_installation.py

# Run MCP server standalone
python -m uvicorn src.mcp_server.server:app --reload
# Then visit: http://localhost:8000/docs
```

---

## 🎓 Key Concepts Demonstrated

✅ **Policy Enforcement**: Every action validated before execution  
✅ **Context-Aware Security**: Different permissions based on mode  
✅ **Defense in Depth**: Critical operations always blocked  
✅ **Agent Transparency**: AI explains why actions are blocked  
✅ **Fail-Safe Design**: Policy violations prevent execution  

---

## 🔧 Using Real LLMs (Optional)

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Add your API key to .env
# For OpenAI:
OPENAI_API_KEY=sk-...

# For Anthropic:
ANTHROPIC_API_KEY=sk-ant-...

# 3. Modify main.py line 180:
agent = ProxiAgent(use_mock=False)  # Change True to False

# 4. Run
python main.py
```

---

## 📊 Architecture at a Glance

```
User Request
    ↓
AI Agent (LangChain)
    ↓
MCP Server (FastAPI)
    ↓
POLICY ENGINE ← Validates EVERY action
    ↓
Cloud Tools (if allowed)
    ↓
Response
```

---

## 🏆 Hackathon Evaluation Points

1. ✅ **Policy Enforcement**: Hard constraint system, not soft prompts
2. ✅ **Context Awareness**: Mode-based permissions (NORMAL vs EMERGENCY)
3. ✅ **Agent Integration**: LangChain agent with real reasoning
4. ✅ **MCP Protocol**: FastAPI server implementing tool access
5. ✅ **Safety**: Destructive operations always blocked
6. ✅ **Transparency**: Agent explains policy violations
7. ✅ **Production Ready**: Structured, tested, documented

---

## 💡 Extending the Project

### Add a New Tool
```python
# 1. In src/mcp_server/tools.py
def backup_database(db_name: str) -> str:
    # Implementation
    
# 2. In policies/ops_policy.json
"EMERGENCY": {
    "allowed_tools": [..., "backup_database"]
}

# 3. Register in server.py and agent/bot.py
```

### Add a New Mode
```json
// In policies/ops_policy.json
"MAINTENANCE": {
    "description": "Scheduled maintenance window",
    "allowed_tools": ["restart_service", "backup_database"],
    "blocked_tools": ["delete_database", "scale_fleet"]
}
```

---

## 📞 Questions?

Check the full **README.md** for:
- Complete architecture diagrams
- API documentation  
- Contribution guidelines
- License information

---

## 🎉 Thank You!

**Proxi: Because even AI agents need guardrails.** 🛡️

Built for ArmorIQ Hackathon with ❤️
