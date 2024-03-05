from src.raga_llm_eval import RagaLLMEval

evaluator = RagaLLMEval(
    api_keys={"OPENAI_API_KEY": "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"}
)

evaluator.list_available_tests()

# evaluator.add_test(
#     name=["answer_relevancy_test", "summarisation_test"],
#     prompt=["How are you?", "How do you do?"],
#     context=["You are a student, answering your teacher."],
#     response=["I am fine. Thank you", "Doooo do do do doooo..."],
#     test_arguments={"model": "gpt-3.5-turbo-1106", "threshold": 0.6},
# ).run().print_results().save_results("test_results.json")

evaluator.add_test(
    test_names=["relevancy_test", "summarisation_test"],
    data={
        "prompt": ["How are you?", "How do you do?"],
        "response": ["I am fine. Thank you", "Doooo do do do doooo..."],
        "context": ["You are a student, answering your teacher."],
    },
    arguments={"model": "gpt-3.5-turbo-1106", "threshold": 0.6},
).run().print_results().save_results("test_results.json")

# evaluator.add_test(
#     test_names=["refusal_test", "refusal_test"],
#     data={"response": ["I am fine. Thank you", "Doooo do do do doooo..."]},
# ).run().print_results().save_results("test_results.json")
