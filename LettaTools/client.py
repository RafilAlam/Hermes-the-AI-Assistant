from letta import create_client
from letta import LLMConfig

client = create_client(base_url='http://localhost:8283')

'''updated_agent_state = client.update_agent(
    agent_id="agent-dc2321b8-f92a-4f11-9209-dada9010d38d",
    tools=["image_generate", "screen_view", "app_write", "app_close", "app_open", "archival_memory_insert", "archival_memory_search", "conversation_search", "conversation_search_date", "pause_heartbeats", "send_message", "core_memory_append", "core_memory_replace"],
)'''

Hermes_agentID = 'agent-dc2321b8-f92a-4f11-9209-dada9010d38d'

def UserChat(Msg):
    response = client.user_message(
        agent_id=Hermes_agentID, 
        message=Msg,
    )

    Response = response.messages

    InternalMonologue = None
    Message = None

    for value in Response:
        InternalMonologue = value.internal_monologue if hasattr(value, 'internal_monologue') else InternalMonologue
        Message = eval(value.function_call.arguments)['message'] if hasattr(value, 'function_call') and value.function_call.arguments != 'true' and value.function_call.arguments != 'false' and 'message' in value.function_call.arguments else Message
    #print('INTERNAL MONOLOGUE:', InternalMonologue.internal_monologue, 'FUNCTIONCALLRETURN:', eval(FunctionCallMessage.function_call.arguments)['message'])
    return InternalMonologue, Message