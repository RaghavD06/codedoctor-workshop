from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace
import json
from streamlit.testing.v1 import AppTest
from openai.types.chat import ChatCompletionMessage

APP=Path(__file__).resolve().parents[1]/'app/app.py'

def test_missing_secrets_help():
    at=AppTest.from_file(str(APP)).run()
    assert not at.exception
    assert 'GEMINI_API_KEY' in at.info[0].value
    assert not at.button

def test_diagnosis_ui_with_scripted_model():
    at=AppTest.from_file(str(APP),default_timeout=30)
    at.secrets.update({'GEMINI_API_KEY':'test-only','MODEL':'test-model','APP_PASSWORD':'workshop'})
    at.run()
    assert not at.button
    at.text_input[0].set_value('workshop').run()
    assert not at.exception
    def call(name,args,i):return {'id':str(i),'type':'function','function':{'name':name,'arguments':json.dumps(args)}}
    seq=[ChatCompletionMessage(role='assistant',tool_calls=[call('save_file',{'filename':'solution.py','content':'def add(a,b):\n    return a+b\n'},1),call('save_file',{'filename':'test_solution.py','content':'from solution import add\ndef test_add():\n    assert add(2,3)==5\n'},2)]),ChatCompletionMessage(role='assistant',tool_calls=[call('run_tests',{},3)]),ChatCompletionMessage(role='assistant',content='1. Scripted model report for UI testing.')]
    def fake(*args,**kwargs):return SimpleNamespace(choices=[SimpleNamespace(message=seq.pop(0))])
    with patch('openai.resources.chat.completions.Completions.create',side_effect=fake):
        at.button[0].click().run(timeout=30)
    assert not at.exception
    assert '1 passed' in at.code[2].value
    assert at.status[0].state=='complete'
    at.run()
    assert len(at.code)==3  # Result survives a Streamlit rerun.
