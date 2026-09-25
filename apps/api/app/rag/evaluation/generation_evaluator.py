# from groq import Groq

# from ragas.llms import llm_factory
# from ragas.metrics.collections import Faithfulness
# from app.core.config import get_settings

# settings = get_settings()

# # Evaluator client
# groq_client = Groq(
#     api_key=settings.groq_api_key,
# )

# # RAGAS-compatible evaluator LLM
# evaluator_llm = llm_factory(
#     settings.llm_model,
#     provider="groq",
#     client=groq_client,
#     temperature=0,
#     max_tokens=settings.llm_max_tokens,
# )

# # RAGAS Faithfulness evaluator
# faithfulness_evaluator = Faithfulness(
#     llm=evaluator_llm,
#     max_output_tokens=settings.llm_max_tokens,
#     temperature=settings.llm_temperature,
# )

# async def evaluate_faithfulness(
#     query: str,
#     generated_answer: str,
#     retrieved_contexts: list[str],
# ) -> float:

#     result = await faithfulness_evaluator.ascore(
#         query=query,
#         answer=generated_answer,
#         contexts=retrieved_contexts,
#     )

#     return result.value


#     if __name__ == "__main__":
#         import asyncio

#         query = "What is the capital of France?"
#         generated_answer = "The capital of France is Paris."
#         retrieved_contexts = [
#             "France is a country in Europe. Its capital is Paris.",
#             "The Eiffel Tower is located in Paris, the capital of France.",
#         ]

#         score = asyncio.run(
#             evaluate_faithfulness(query, generated_answer, retrieved_contexts)
#         )
#         print(f"Faithfulness score: {score}")



import json

from app.core.config import get_settings
from app.dependencies.llm import GroqClient

settings = get_settings()

evaluator_llm = GroqClient(
    api_key=settings.groq_api_key,
    model=settings.llm_model,
)


async def evaluate_faithfulness(
    query: str,
    generated_answer: str,
    retrieved_contexts: list[str],
) -> float:
    """
    Measures whether factual claims in the generated answer
    are supported by the retrieved context.

    Score:
        supported factual claims / total factual claims

    EKA convention:
        If there are no factual claims, return 0.0.
    """

    if not generated_answer.strip():
        return 0.0

    if not retrieved_contexts:
        return 0.0

    context = "\n\n".join(retrieved_contexts)

    system_prompt = """
You are an evaluator for a Retrieval-Augmented Generation (RAG) system.

Evaluate the FAITHFULNESS of the generated answer.

Faithfulness means:
Are the factual claims in the generated answer supported by the
retrieved context?

Instructions:
1. Identify the factual claims in the generated answer.
2. Evaluate each factual claim using ONLY the retrieved context.
3. Do not use external knowledge.
4. A claim is supported only when the retrieved context provides
   sufficient evidence for it.
5. Calculate:

   score = supported_claims / total_claims

6. If the answer contains no factual claims, return score 0.0.
7. The score must be between 0.0 and 1.0.

Return ONLY valid JSON.

Required format:
{
    "total_claims": 0,
    "supported_claims": 0,
    "score": 0.0
}
"""

    user_prompt = f"""
USER QUESTION:
{query}

RETRIEVED CONTEXT:
{context}

GENERATED ANSWER:
{generated_answer}
"""

    response = await evaluator_llm.generate(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        max_tokens=300,
        temperature=0,
    )

    try:
        result = json.loads(response)

        total_claims = int(result["total_claims"])
        supported_claims = int(result["supported_claims"])
        score = float(result["score"])

        # Validate evaluator output
        if total_claims < 0:
            raise ValueError("total_claims cannot be negative")

        if supported_claims < 0:
            raise ValueError("supported_claims cannot be negative")

        if supported_claims > total_claims:
            raise ValueError(
                "supported_claims cannot exceed total_claims"
            )

        # EKA convention
        if total_claims == 0:
            return 0.0

        # Recalculate ourselves instead of blindly trusting
        # the LLM-generated score.
        calculated_score = supported_claims / total_claims

        return round(calculated_score, 4)

    except (
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError,
    ) as exc:
        raise ValueError(
            f"Invalid faithfulness evaluator response: {response}"
        ) from exc



async def evaluate_answer_relevancy(
    query: str,
    generated_answer: str,
) -> float:
    """
    Measures how well the generated answer addresses
    the user's question.

    Score:
        0.0 = completely irrelevant
        1.0 = directly and fully relevant
    """

    if not query.strip():
        return 0.0

    if not generated_answer.strip():
        return 0.0

    system_prompt = """
You are an evaluator for a Retrieval-Augmented Generation (RAG) system.

Evaluate the ANSWER RELEVANCY of the generated answer.

Answer Relevancy means:
How well does the generated answer address the user's question?

Instructions:
1. Compare the generated answer with the user's question.
2. Evaluate whether the answer directly addresses what was asked.
3. Penalize answers that are unrelated, off-topic, or mostly irrelevant.
4. Do NOT evaluate whether the answer is factually correct.
5. Do NOT use retrieved context or external knowledge.
6. Return a relevancy score between 0.0 and 1.0.

Scoring guidance:
1.0 = directly and fully addresses the question
0.7 = mostly relevant but misses some aspects
0.5 = partially relevant
0.2 = mostly irrelevant
0.0 = completely irrelevant or does not answer the question

Return ONLY valid JSON.

Required format:
{
    "score": 0.0
}
"""

    user_prompt = f"""
USER QUESTION:
{query}

GENERATED ANSWER:
{generated_answer}
"""

    response = await evaluator_llm.generate(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        max_tokens=100,
        temperature=0,
    )

    try:
        result = json.loads(response)

        score = float(result["score"])

        if not 0.0 <= score <= 1.0:
            raise ValueError(
                f"Answer relevancy score must be between 0 and 1: {score}"
            )

        return round(score, 4)

    except (
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError,
    ) as exc:
        raise ValueError(
            f"Invalid answer relevancy evaluator response: {response}"
        ) from exc


if __name__ == "__main__":
    import asyncio

    query = "What causes NAT exhaustion?"

    # The retrieved context should contain information that can be used to verify the factual claims in the generated answer. In this case, the context mentions that NAT exhaustion can occur due to high concurrent outbound connections and that NAT gateway metrics and SNAT port usage should be monitored. The generated answer states that NAT exhaustion can occur when SNAT ports are exhausted because of high concurrent outbound traffic. The evaluator will check if the claims in the generated answer are supported by the retrieved context.
    retrieved_contexts = [
        """
        NAT exhaustion can occur when SNAT ports are exhausted
        due to high concurrent outbound connections.
        NAT gateway metrics and SNAT port usage should be monitored.
        """
    ]

    generated_answer = """
    NAT exhaustion can occur when SNAT ports are exhausted
    because of high concurrent outbound traffic.
    """
    # The generated answer is relevant to the query used for relevant_score
    relevant_answer = """
    NAT exhaustion can occur when available SNAT ports
    are exhausted due to high concurrent outbound connections.
    """
    # The generated answer is not relevant to the queryused for irrelevant_score
    irrelevant_answer = """
    PostgreSQL supports indexes that can improve database
    query performance.
    """

    score = asyncio.run(
        evaluate_faithfulness(
            query=query,
            generated_answer=generated_answer,
            retrieved_contexts=retrieved_contexts,
        )
    )

relevant_score = asyncio.run(
        evaluate_answer_relevancy(
            query=query,
            generated_answer=relevant_answer,
        )
    )

irrelevant_score = asyncio.run(
     evaluate_answer_relevancy(
          query=query,
          generated_answer=irrelevant_answer,
     ))


print(f"Relevant answer score: {relevant_score}")
print(f"Irrelevant answer score: {irrelevant_score}")
print(f"Faithfulness: {score}")