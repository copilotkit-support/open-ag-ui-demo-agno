import {
  CopilotRuntime,
  copilotRuntimeNextJSAppRouterEndpoint,
  OpenAIAdapter,
  GoogleGenerativeAIAdapter
} from '@copilotkit/runtime';
import { NextRequest } from 'next/server';
// import { HttpAgent } from "@ag-ui/client";
import { AgnoAgent } from "@ag-ui/agno"

// const langgraphAgent = new HttpAgent({
//   url: process.env.NEXT_PUBLIC_LANGGRAPH_URL || "http://0.0.0.0:8000/langgraph-agent",
// });
const serviceAdapter = new GoogleGenerativeAIAdapter()
const runtime = new CopilotRuntime({
  agents: {
    // Our FastAPI endpoint URL
    // @ts-ignore
    agno_agent: new AgnoAgent({ url: "http://localhost:8000/agui" }),
  }
});

// const runtime = new CopilotRuntime()
export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: '/api/copilotkit',
  });

  return handleRequest(req);
};