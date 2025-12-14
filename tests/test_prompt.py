from src.app import build_prompt


def test_build_prompt_includes_context_and_question():
    context = "Doc snippet A\nDoc snippet B"
    question = "What is the summary?"
    prompt = build_prompt(context, question)

    assert "Context" in prompt
    assert context in prompt
    assert question in prompt
    assert prompt.strip().endswith("Assistant:")
