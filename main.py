from fastapi import FastAPI, HTTPException
from guardrails import SecurityGuardrail
from pydantic import BaseModel

app = FastAPI(title="Agent Guardrail Lab", version="1.0.0")
guardrail = SecurityGuardrail()


class AgentRequest(BaseModel):
  prompt: str


class ToolExecutionRequest(BaseModel):
  tool_name: str
  arguments: dict


@app.post("/api/v1/agent/run")
def run_guarded_agent(req: AgentRequest):
  # 1. Validate Input via Guardrail Middleware
  verdict = guardrail.validate_input(req.prompt)

  if not verdict.allowed:
    return {
        "status": "blocked",
        "reason": verdict.reason,
        "matched_pattern": verdict.matched_pattern,
        "risk_score": verdict.risk_score,
    }

  # 2. Simulated Agent Execution (Input passed inspection)
  return {
      "status": "success",
      "output": f"Agent successfully processed: '{req.prompt}'",
  }


@app.post("/api/v1/agent/tool")
def execute_guarded_tool(req: ToolExecutionRequest):
  # Validate Tool Access
  verdict = guardrail.validate_tool_call(req.tool_name, req.arguments)

  if not verdict.allowed:
    return {
        "status": "blocked",
        "reason": verdict.reason,
        "risk_score": verdict.risk_score,
    }

  return {
      "status": "success",
      "output": f"Executed tool '{req.tool_name}' with args {req.arguments}",
  }