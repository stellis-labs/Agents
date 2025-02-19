from processing import BaseProcessor

class SummarizationProcessor(BaseProcessor):
    def process(self, insights):
        combined_text = " ".join(insights)
        return super().process(insights, combined_text, "Create a concise, actionable summary of the following business insights.")