from concurrent.futures import ThreadPoolExecutor, as_completed

class ParallelReasoningPipeline:
    def __init__(self):
        self.steps = []

    def add_step(self, description, data_source, processor, data_type, color):
        self.steps.append({
            "description": description,
            "data_source": data_source,
            "processor": processor,
            "data_type": data_type,
            "color": color
        })

    def run(self):
        results = []
        with ThreadPoolExecutor() as executor:
            future_to_step = {executor.submit(self.process_step, step): step for step in self.steps}
            for future in as_completed(future_to_step):
                results.append(future.result())
        return results

    def process_step(self, step):
        data = step["data_source"].fetch_data()
        return step["processor"].process(data)