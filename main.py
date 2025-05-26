import os, re
# import vllm
from prompts import *
from agent_boilerplate import Client
from concurrent.futures import ThreadPoolExecutor

def load_examples():
#     return ["""-- The kernel of a homomorphism forms a normal subgroup of its domain
# theorem kernel_is_normal_subgroup (h : α → β) (is_hom : is_homomorphism h) : ∃ (N : Subgroup α), normal N ∧ (N.carrier = kernel h) := by
#   let N : Subgroup α := kernel_subgroup h is_hom
#   use N
#   constructor
#   · have conj_mem : ∀ x y, x ∈ N.carrier → y * x * y⁻¹ ∈ N.carrier := by
#       intro x y hx
#       have : h (y * x * y⁻¹) = 1 := by
#         rw [is_hom, is_hom, hx, hom_pres_inv h is_hom, mul_one, mul_inv_cancel]
#       exact this
#     exact { conj_mem := conj_mem }
#   rfl"""]
    from examples import EXAMPLES
    return EXAMPLES

def get_first_numeric_token(text):
    # find first numeric token
    pattern = r'\d+'
    match = re.search(pattern, text)
    if match:
        return int(match.group()[0])
    return -1

def get_local_model_completions(multi_agent=False):
    # client = openai.OpenAI(
    #     api_key="EMPTY",
    #     base_url="http://localhost:8000/v1"
    # )
    #
    # def get_response(messages):
    #     res = client.chat.completions.create(
    #         model="deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    #         messages=messages,
    #         # extra_body={"guided_json": Response.model_json_schema()},
    #     )
    #     return res.choices
    client = Client(
        model_source="local",
        model_name="deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    )

    proofs = load_examples()
    scores = []
    if not multi_agent:
        for proof in proofs:
            #TODO: few-shot examples
            messages = [
                {
                    "role": "system",
                    "content": FULL_PROMPT
                },
                {
                    "role": "user",
                    "content": f"""
The proof you will score is the following:
```lean
{proof}
```

Remember to output ONLY the final score and a short explanation, without anything else."""
                }
            ]
            choices = client.get_response(messages, raw=True).choices
            found_choice = False
            for c in choices:
                print(c)
                match = get_first_numeric_token(c.message.content)
                if match != -1:
                    scores.append(match)
                    found_choice = True
                    break
            if not found_choice:
                print(f"Failed to find a score for proof: {proof}")
                scores.append(-1)
    else:
        for proof in proofs:
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
                    futures.append(executor.submit(client.get_response, messages, raw=True))
            score_sum = 0
            for i in range(len(futures)):
                choices = futures[i].result().choices
                found_choice = False
                for c in choices:
                    match = get_first_numeric_token(c.message.content)
                    if match != -1:
                        score_sum += match
                        found_choice = True
                        break
                if not found_choice:
                    print(f"Failed to find a score for proof: {proof}")
                    scores.append(-1)
                    score_sum = -1
                    break
            if score_sum != -1:
                scores.append(score_sum)
    return scores

def get_gemini_completions():
    client = Client(
        model_source="google",
        model_name="gemini-2.0-flash"
    )

    proofs = load_examples()
    scores = []

    for proof in proofs:
        messages = [
            {
                "role": "system",
                "content": FULL_PROMPT
            },
            {
                "role": "user",
                "content": f"""The proof you will score is the following:
```lean
{proof}
```

Remember to output the final score at the TOP of your explanation. """
                }
            ]
        response = client.get_response(
            messages,
            config={"temperature": 0.0}
        )

        pattern = r'\d+'
        match = re.search(pattern, response)
        if match:
            scores.append(int(match.group()[0]))
        else:
            print(f"Failed to find a score for proof: {proof}")
            scores.append(-1)

    return scores

if __name__ == "__main__":
    # scores = get_local_model_completions()
    # print(scores)

    # Evaluate a few times using API model
    # for i in range(12):
    #     scores = get_gemini_completions()
    #     print(scores)
    #     with open(f"scores/scores_gemini_{i}.txt", "w") as f:
    #         for score in scores:
    #             f.write(f"{score}\n")

    # Evaluate a few times using local model
    # for i in range(12):
    #     scores = get_local_model_completions()
    #     print(scores)
    #     with open(f"scores/scores_local_{i}.txt", "w") as f:
    #         for score in scores:
    #             f.write(f"{score}\n")

    # Evaluate with work divided between agents
    for i in range(4):
        scores = get_local_model_completions(multi_agent=True)
        print(scores)
        with open(f"scores/scores_local_multi_{i+8}.txt", "w") as f:
            for score in scores:
                f.write(f"{score}\n")

    # TODO: experiment with temperature