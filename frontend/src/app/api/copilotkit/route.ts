import {
  CopilotRuntime,
  copilotRuntimeNextJSAppRouterEndpoint,
  OpenAIAdapter
} from '@copilotkit/runtime';
import { NextRequest } from 'next/server';
import { HttpAgent } from "@ag-ui/client";

const agnoAgent = new HttpAgent({
  url: process.env.NEXT_PUBLIC_AGNO_URL || "http://0.0.0.0:8000/agno-agent",
});
const serviceAdapter = new OpenAIAdapter()
const runtime = new CopilotRuntime({
  agents: {
    // Our FastAPI endpoint URL
    // @ts-ignore
    agnoAgent : agnoAgent
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