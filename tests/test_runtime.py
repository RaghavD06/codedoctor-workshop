from types import SimpleNamespace
import json
import sys
from openai.types.chat import ChatCompletionMessage
from agent.loop import run_agent
from tools.python_tools import Workspace
from examples.patient import BUGGY_CODE

def test_tools_and_isolation():
    with Workspace() as first, Workspace() as second:
        assert first.workdir != second.workdir
        assert 'NameError' in first.run_code(BUGGY_CODE)
        first.save_file('hello.py', 'def add(a, b):\n    return a + b\n')
        first.save_file('test_hello.py', 'from hello import add\ndef test_add():\n    assert add(2, 3) == 5\n')
        assert '1 passed' in first.run_tests()
        first.save_file('unicode.txt', 'Hello 🩺')
        assert first.read_file('unicode.txt') == 'Hello 🩺'
        assert second.read_file('hello.py') == ''
        assert first._run([sys.executable, '-c', 'import time; time.sleep(2)'], .1).startswith('FAILED: timed out')
        folder = first.workdir
    assert not folder.exists()

def test_loop_returns_tool_results_and_preserves_metadata():
    message = ChatCompletionMessage.model_validate({'role':'assistant', 'content':None, 'tool_calls':[{'id':'one','type':'function','function':{'name':'run_code','arguments':json.dumps({'code':'print(42)'})},'extra_content':{'google':{'thought_signature':'test-signature'}}}]})
    seen=[]
    def chat(**kwargs):
        seen.append(list(kwargs['messages']))
        return SimpleNamespace(choices=[SimpleNamespace(message=message if len(seen)==1 else ChatCompletionMessage(role='assistant',content='Finished'))])
    with Workspace() as workspace:
        assert run_agent('task','system',chat_fn=chat,tools=workspace.tools,log=lambda _:None)=='Finished'
    assert '42' in seen[-1][-1]['content']
    assert seen[-1][-2]['tool_calls'][0]['extra_content']['google']['thought_signature']=='test-signature'

def test_step_limit():
    msg=ChatCompletionMessage(role='assistant',tool_calls=[{'id':'one','type':'function','function':{'name':'run_code','arguments':'{"code":"pass"}'}}])
    with Workspace() as workspace:
        result=run_agent('task','system',max_steps=1,chat_fn=lambda **_:SimpleNamespace(choices=[SimpleNamespace(message=msg)]),tools=workspace.tools,log=lambda _:None)
    assert result.startswith('Stopped:')
