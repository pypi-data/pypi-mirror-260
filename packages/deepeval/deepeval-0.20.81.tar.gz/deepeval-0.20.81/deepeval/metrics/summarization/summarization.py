from typing import List, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field
from concurrent.futures import ThreadPoolExecutor

from deepeval.test_case import LLMTestCase
from deepeval.metrics import BaseMetric
from deepeval.models import GPTModel, DeepEvalBaseLLM
from deepeval.utils import trimAndLoadJson
from deepeval.metrics.summarization.template import SummarizationTemplate
from deepeval.metrics.faithfulness.template import FaithfulnessTemplate
from deepeval.progress_context import metrics_progress_context
from deepeval.telemetry import capture_metric_type


class SummarizationAlignmentVerdict(BaseModel):
    # yes, no, or idk
    verdict: str
    reason: str = Field(default=None)


class SummarizationCoverageVerdict(BaseModel):
    summary_verdict: str
    original_verdict: str
    question: str = Field(default=None)


class ScoreType(Enum):
    ALIGNMENT = "Alignment"
    COVERAGE = "Coverage"


class SummarizationMetric(BaseMetric):
    def __init__(
        self,
        threshold: float = 0.5,
        n: int = 5,
        model: Optional[Union[str, DeepEvalBaseLLM]] = None,
        assessment_questions: Optional[List[str]] = None,
        include_reason: bool = True,
        multithreading=True,
    ):
        self.threshold = threshold
        if isinstance(model, DeepEvalBaseLLM):
            self.model = model
        else:
            self.model = GPTModel(model=model)
        self.evaluation_model = self.model.get_model_name()

        if assessment_questions is not None and len(assessment_questions) == 0:
            self.assessment_questions = None
        else:
            self.assessment_questions = assessment_questions

        self.multithreading = multithreading
        self.include_reason = include_reason
        self.n = n

    def measure(self, test_case: LLMTestCase):
        if test_case.input is None or test_case.actual_output is None:
            raise ValueError("Input or actual output cannot be None")

        with metrics_progress_context(self.__name__, self.evaluation_model):
            if test_case.input is None or test_case.actual_output is None:
                raise ValueError("Input and actual output cannot be None")

            if self.multithreading:
                # Use multithreading to generate truths and claims in parallel
                with ThreadPoolExecutor() as executor:
                    future_truths = executor.submit(
                        # Claims made in the original text === truths
                        self._generate_claims,
                        test_case.input,
                    )
                    future_claims = executor.submit(
                        self._generate_claims, test_case.actual_output
                    )
                    future_coverage_verdicts = executor.submit(
                        self._generate_coverage_verdicts, test_case
                    )

                    self.truths: List[str] = future_truths.result()
                    self.claims: List[str] = future_claims.result()
                    self.coverage_verdicts: List[
                        SummarizationCoverageVerdict
                    ] = future_coverage_verdicts.result()
            else:
                # Sequential execution
                self.truths: List[str] = self._generate_claims(test_case.input)
                self.claims: List[str] = self._generate_claims(
                    test_case.actual_output
                )
                self.coverage_verdicts: List[SummarizationCoverageVerdict] = (
                    self._generate_coverage_verdicts(test_case)
                )

            self.alignment_verdicts: List[SummarizationAlignmentVerdict] = (
                self._generate_alignment_verdicts()
            )
            alignment_score = self._generate_score(ScoreType.ALIGNMENT)
            coverage_score = self._generate_score(ScoreType.COVERAGE)

            self.score_breakdown = {
                ScoreType.ALIGNMENT.value: alignment_score,
                ScoreType.COVERAGE.value: coverage_score,
            }
            summarization_score = min(alignment_score, coverage_score)
            self.reason = self._generate_reason(summarization_score)
            self.success = summarization_score >= self.threshold
            self.score = summarization_score
            capture_metric_type(self.__name__)
            return self.score

    def _generate_reason(self, score: float) -> str:
        if self.include_reason is False:
            return None

        contradictions = []
        redundancies = []
        for verdict in self.alignment_verdicts:
            if verdict.verdict.strip().lower() == "no":
                contradictions.append(verdict.reason)
            elif verdict.verdict.strip().lower() == "idk":
                redundancies.append(verdict.reason)

        questions = []
        if self.coverage_verdicts:
            for verdict in self.coverage_verdicts:
                if (
                    verdict.original_verdict.strip().lower() == "yes"
                    and verdict.summary_verdict.strip().lower() == "no"
                ):
                    questions.append(verdict.question)

        prompt: dict = SummarizationTemplate.generate_reason(
            contradictions=contradictions,
            redundancies=redundancies,
            questions=questions,
            score=format(score, ".2f"),
        )

        if len(questions) > 0:
            prompt += f"""Questions the original text can answer but not the summary:
{questions}

"""
        prompt += """Reason:"""

        res = self.model(prompt)
        return res

    def _generate_score(self, score_type: ScoreType) -> float:
        if score_type == ScoreType.ALIGNMENT:
            total = len(self.alignment_verdicts)
            if total == 0:
                return 0
            faithfulness_count = 0
            for verdict in self.alignment_verdicts:
                # Different from the faithfulness score, this
                # penalizes 'idk' (full of fluff) summaries
                if verdict.verdict.strip().lower() == "yes":
                    faithfulness_count += 1

            return faithfulness_count / total

        else:
            if self.assessment_questions is None:
                return 1
            total = 0
            coverage_count = 0
            for verdict in self.coverage_verdicts:
                if verdict.original_verdict.strip().lower() == "yes":
                    total += 1
                    if verdict.summary_verdict.strip().lower() == "yes":
                        coverage_count += 1

            if total == 0:
                return 0

            return coverage_count / total

    def _generate_answers(self, text: str) -> List[str]:
        prompt = SummarizationTemplate.generate_answers(
            questions=self.assessment_questions, text=text
        )
        res = self.model(prompt)
        data = trimAndLoadJson(res)
        return data["answers"]

    def _generate_assessment_questions(self, text: str):
        prompt = SummarizationTemplate.generate_questions(text=text, n=self.n)
        res = self.model(prompt)
        data = trimAndLoadJson(res)
        return data["questions"]

    def _generate_coverage_verdicts(
        self, test_case: LLMTestCase
    ) -> List[SummarizationCoverageVerdict]:
        if self.assessment_questions is None:
            self.assessment_questions = self._generate_assessment_questions(
                test_case.input
            )

        if self.multithreading:
            with ThreadPoolExecutor() as executor:
                future_original_answers: List[str] = executor.submit(
                    self._generate_answers, test_case.input
                )
                future_summary_answers: List[str] = executor.submit(
                    self._generate_answers, test_case.actual_output
                )
                original_answers = future_original_answers.result()
                summary_answers = future_summary_answers.result()

        else:
            original_answers = self._generate_answers(test_case.input)
            summary_answers = self._generate_answers(test_case.actual_output)

        if len(original_answers) != len(summary_answers):
            raise ValueError("Number of verdicts generated does not equal.")

        coverage_veridcts: List[SummarizationCoverageVerdict] = []
        for i in range(len(original_answers)):
            coverage_veridcts.append(
                SummarizationCoverageVerdict(
                    summary_verdict=summary_answers[i],
                    original_verdict=original_answers[i],
                    question=self.assessment_questions[i],
                )
            )

        return coverage_veridcts

    def _generate_alignment_verdicts(
        self,
    ) -> List[SummarizationAlignmentVerdict]:
        verdicts: List[SummarizationAlignmentVerdict] = []
        prompt = SummarizationTemplate.generate_alignment_verdicts(
            summary_claims=self.claims, orignal_text="\n\n".join(self.truths)
        )
        res = self.model(prompt)
        data = trimAndLoadJson(res)
        verdicts = [
            SummarizationAlignmentVerdict(**item) for item in data["verdicts"]
        ]

        return verdicts

    def _generate_claims(self, text: str) -> List[str]:
        # Borrow faithfulness template
        prompt = FaithfulnessTemplate.generate_claims(text=text)
        res = self.model(prompt)
        data = trimAndLoadJson(res)

        return data["claims"]

    def is_successful(self) -> bool:
        self.success = self.score >= self.threshold
        return self.success

    @property
    def __name__(self):
        return "Summarization"
