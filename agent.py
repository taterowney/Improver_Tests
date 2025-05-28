import openai
from concurrent.futures import ThreadPoolExecutor

from prompts import *

MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"

client = openai.OpenAI(
    api_key="EMPTY",
    base_url="http://localhost:8000/v1"
)

def get_first_numeric_token(text):
    """
    Extracts the first numeric token from the given text.
    Returns 0 if no numeric token is found.
    """
    tokens = text.split()
    for token in tokens:
        try:
            return int(token)
        except ValueError:
            continue
    return 0

def score_proof(proof):
    """
    Scores a proof using a local model.
    Returns the score as an integer.
    """
    total_score = 0
    with ThreadPoolExecutor() as executor:
        futures = []

        for i in range(len(INDIVIDUAL_PROMPTS)):
            messages = [
                {
                    "role": "system",
                    "content": INDIVIDUAL_PROMPTS[i]["text"]
                },
                {
                    "role": "user",
                    "content": f"""The proof you will score is the following:
        ```lean
        {proof}
        ```
        
        Remember to output ONLY the final score, without anything else."""
                }
            ]
            futures.append(executor.submit(client.chat.completions.create,
                    model=MODEL_NAME,
                    messages=messages,
                    seed=42,
                    temperature=0.0,
                    extra_body={
                        "top_p": 1.0,
                    }
                )
            )
        for i in range(len(futures)):
            score = get_first_numeric_token(futures[i].result().choices[0].message.content)
            score = min(score, INDIVIDUAL_PROMPTS[i]["points"])
            total_score += score

    return total_score

def load_offline_model():
    from vllm import LLM
    llm = LLM(model=MODEL_NAME)
    return llm

def score_proof_online(proof, model):
    """
    Scores a proof using a local model.
    Returns the score as an integer.
    """
    from vllm import SamplineParams
    total_score = 0
    with ThreadPoolExecutor() as executor:
        futures = []

        for i in range(len(INDIVIDUAL_PROMPTS)):
            messages = [INDIVIDUAL_PROMPTS[i]["text"] + "\n< | User | >" + f"""The proof you will score is the following:
        ```lean
        {proof}
        ```

        Remember to output ONLY the final score, without anything else."""
            ]
            futures.append(
                executor.submit(
                    model.generate,
                    messages,
                    sampline_params=SamplingParams(
                        seed=42,
                        temperature=1.0,
                        top_p=1.0,
                    )
                )
            )
        for i in range(len(futures)):
            score = get_first_numeric_token(futures[i].result().choices[0].message.content)
            score = min(score, INDIVIDUAL_PROMPTS[i]["points"])
            total_score += score

    return total_score

if __name__ == '__main__':
    test_proof = """-- The kernel of a homomorphism forms a normal subgroup of its domain
theorem kernel_is_normal_subgroup (h : α → β) (is_hom : is_homomorphism h) : ∃ (N : Subgroup α), normal N ∧ (N.carrier = kernel h) := by
  let N : Subgroup α := kernel_subgroup h is_hom
  use N
  constructor
  · have conj_mem : ∀ x y, x ∈ N.carrier → y * x * y⁻¹ ∈ N.carrier := by
      intro x y hx
      have : h (y * x * y⁻¹) = 1 := by
        rw [is_hom, is_hom, hx, hom_pres_inv h is_hom, mul_one, mul_inv_cancel]
      exact this
    exact { conj_mem := conj_mem }
  rfl"""
    print(score_proof(test_proof), score_proof(test_proof), score_proof(test_proof))
    # model = load_offline_model()
    # print(score_proof_online(test_proof, model))
    # print(score_proof_online(test_proof, model))
    # print(score_proof_online(test_proof, model))