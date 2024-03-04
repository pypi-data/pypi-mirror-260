import pytest
import asyncio
from gptfree.core import question

@pytest.mark.asyncio
async def test_question():
    content = "This is a test question."

    response = await question(content)

    assert response is not None, "The response should not be None"