from unittest.mock import Mock
import pytest
from app.services.chat_service import ChatService

class FakeGraph:
    def __init__(self, events, error=None):
        self.events, self.error = events, error

    async def astream(self, state, stream_mode):
        for event in self.events:
            yield event
        if self.error:
            raise self.error

@pytest.mark.asyncio
@pytest.mark.parametrize('events, expected', [
    ([('updates', {'router': {'route': 'RAG'}}),
      ('custom', {'type': 'token', 'node': 'rag', 'content': 'Reset '}),
      ('custom', {'type': 'token', 'node': 'rag', 'content': 'password'}),
      ('updates', {'rag': {'response': 'Reset password'}})], 'Reset password'),
    ([('updates', {'router': {'route': 'GENERAL'}}),
      ('updates', {'general': {'response': 'Washington, D.C.'}})], 'Washington, D.C.'),
    ([('custom', {'type': 'token', 'node': 'rag', 'content': 'No relevant information'}),
      ('updates', {'rag': {'response': 'No relevant information'}})], 'No relevant information'),
])
async def test_answer_text_only(events, expected):
    service = ChatService(Mock(), FakeGraph(events))
    answer = ''.join([chunk async for chunk in service.langgraph_stream('question', 'test')])
    assert answer == expected

@pytest.mark.asyncio
async def test_failure_is_visible_without_internal_details():
    service = ChatService(Mock(), FakeGraph([], RuntimeError('secret database error')))
    answer = ''.join([chunk async for chunk in service.langgraph_stream('question', 'test')])
    assert 'Unable to complete' in answer
    assert 'request test' in answer
    assert 'secret' not in answer
