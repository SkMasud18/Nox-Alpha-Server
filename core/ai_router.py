import time
from typing import AsyncGenerator, Dict, Any, List

class Nox3TierRouter:
    """
    Production 3-Tier Multi-LLM Routing Engine.
    Dynamically balances latency, inference cost, and cognitive depth
    based on task complexity heuristics and user intent scores.
    """

    def __init__(self, primary_api_key: str):
        self.api_key = primary_api_key

    def calculate_complexity(self, prompt: str, has_images: bool = False) -> int:
        """Computes complexity score between 1 and 100."""
        score = 25  # Base casual score
        prompt_lower = prompt.lower()

        # Heuristics for analytical/technical tasks
        code_keywords = ["function", "class", "def ", "docker", "algorithm", "async", "bug", "traceback"]
        math_keywords = ["integrate", "matrix", "derivative", "solve", "proof", "latex", "theorem"]
        deep_keywords = ["research", "system architecture", "benchmark", "quantum", "comprehensive analysis"]

        if any(k in prompt_lower for k in code_keywords):
            score += 35
        if any(k in prompt_lower for k in math_keywords):
            score += 45
        if any(k in prompt_lower for k in deep_keywords):
            score += 40
        if has_images:
            score += 25

        return min(score, 100)

    def route_tier(self, complexity_score: int) -> Dict[str, Any]:
        """Maps complexity score to optimal hardware and inference budget."""
        if complexity_score <= 50:
            # Tier 1: Casual & Conversational (Sub-second target: ~700ms)
            return {
                "tier": 1,
                "name": "Casual Stream",
                "max_tokens": 2048,
                "temperature": 0.3,
                "reasoning_effort": "none"
            }
        elif 51 <= complexity_score < 95:
            # Tier 2: Analytical & Multimodal Coding
            return {
                "tier": 2,
                "name": "Analytical Engine",
                "max_tokens": 8192,
                "temperature": 0.1,
                "reasoning_effort": "low"
            }
        else:
            # Tier 3: Deep Autonomous Reasoning & Formal Math
            return {
                "tier": 3,
                "name": "Autonomous Deep Reasoning",
                "max_tokens": 16384,
                "temperature": 0.1,
                "reasoning_effort": "high"
            }

    async def stream_completion(
        self,
        messages: List[Dict[str, str]],
        has_images: bool = False
    ) -> AsyncGenerator[str, None]:
        """
        Simulated generation illustrating the streaming pipeline contract.
        In production, executes async HTTP chunk streaming via the Nox Sovereign Neural Engine.
        """
        last_prompt = messages[-1]["content"] if messages else ""
        complexity = self.calculate_complexity(last_prompt, has_images)
        tier_cfg = self.route_tier(complexity)

        yield f"data: {{\"meta\": {{\"tier\": {tier_cfg['tier']}, \"name\": \"{tier_cfg['name']}\"}}}}\n\n"
        
        # Production tokens yield progressively
        yield f"data: {{\"text\": \"Evaluating query under Tier {tier_cfg['tier']} ({tier_cfg['name']})... \"}}\n\n"
        yield f"data: {{\"status\": \"complete\"}}\n\n"
