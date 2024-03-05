import json
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from time import time

from komodo.framework.komodo_tool import KomodoTool
from komodo.shared.utils.sentry_utils import sentry_trace
from komodo.shared.utils.timebox import time_print, time_limit, TimeoutException

TOOLS_TIMEOUT = 15


@sentry_trace
def process_actions_gpt40_1106_preview(run, tools) -> list:
    assert run.required_action.type == 'submit_tool_outputs'
    print("Processing actions. Run Id: " + run.id + " Thread Id: " + run.thread_id)
    tool_calls = run.required_action.submit_tool_outputs.tool_calls
    metadata = run.metadata or {}
    print("Metadata: ", json.dumps(metadata, default=vars))
    metadata['run_id'] = run.id
    outputs = get_tools_outputs(tools, metadata, tool_calls)
    for output in outputs:
        del output['name']

    print("Outputs: ", json.dumps(outputs, default=vars))
    return outputs


@sentry_trace
def process_actions_gpt_legacy_api(response, metadata, tools) -> list:
    assert len(response.choices) > 0
    print("Processing actions. Response Id: " + response.id)
    tool_calls = response.choices[0].message.tool_calls
    metadata = metadata or {}
    metadata['run_id'] = response.id
    outputs = get_tools_outputs(tools, metadata, tool_calls=tool_calls, timeout=TOOLS_TIMEOUT)
    for output in outputs:
        output['role'] = "tool"
        output['content'] = output['output']
        del output['output']

    print("Outputs: ", json.dumps(outputs, default=vars))
    return outputs


def get_tools_outputs(tools, metadata, tool_calls, timeout=TOOLS_TIMEOUT):
    parallel = len(tool_calls) > 1
    try:
        if parallel:
            return get_tools_outputs_parallel(tools, metadata, tool_calls, timeout)
        else:
            return get_tools_outputs_sequential(tools, metadata, tool_calls, timeout)
    except TimeoutError:
        if parallel:
            print("Timed out processing tool calls in parallel, trying sequential execution to collect outputs")
            return get_tools_outputs_sequential(tools, metadata, tool_calls, timeout)


@time_print
def get_tools_outputs_sequential(tools, metadata, tool_calls, timeout=TOOLS_TIMEOUT):
    outputs = []
    for call in tool_calls:
        output = process_tool_call(tools, call, metadata)
        outputs.append(output)
    return outputs


@time_print
def get_tools_outputs_parallel(tools, metadata, tool_calls, timeout=TOOLS_TIMEOUT):
    outputs = list()
    start = time()
    with ThreadPoolExecutor() as executor:
        for output in executor.map(process_tool_call, repeat(tools), tool_calls, repeat(metadata), timeout=timeout):
            outputs.append(output)
    finish = time()
    print(f'wall time to execute: {finish - start}')
    return outputs


def process_tool_call_with_time_limit(tools, call, metadata=None, timeout=TOOLS_TIMEOUT):
    # signal approach to timeouot only works in main thread
    if metadata is None:
        metadata = {'run_id': '123'}

    try:
        with time_limit(timeout):
            print("Processing tool call: " + call.id)
            result = process_tool_call(tools, call, metadata)
            print("Completed tool call: " + call.id)
            return result
    except TimeoutException:
        print("Timed out processing tool call: " + call.id)
        return json.dumps({"tool_call_id": call.id, "name": call.function.name,
                           "output": "Timed out processing tool call: " + call.id})


def process_tool_call(tools, call, metadata):
    f = call.function
    print("Call Id: " + call.id + " Type: " + call.type + " Function: " + f.name + " Description: " + f.arguments)
    args = json.loads(f.arguments)
    args['metadata'] = metadata
    args['run_id'] = metadata['run_id']
    args['f.name'] = f.name

    output = "Requested function not supported or available. Do not retry this action."

    for tool in tools:
        if isinstance(tool, KomodoTool):
            if tool.shortcode == f.name:
                output = tool.action(args)
                break

    return {"tool_call_id": call.id, "name": f.name, "output": output}
