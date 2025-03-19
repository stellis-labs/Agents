# fractal_reasoning_agent/fra_system.py
import logging
import time
import json
from concurrent.futures import ThreadPoolExecutor
from ollama_client import OllamaClient
from layers.input_layer import ProblemInputProcessor
from layers.decomposition_layer import PrimaryDecomposer
from layers.processing_layer import SolverUnit, Evaluator, Optimizer
from layers.integration_layer import SolutionIntegrator, QualityController

class FRAgent:
    """Main class for the Fractal Reasoning Agent system."""
    
    def __init__(self, config):
        """Initialize the FRA system with the provided configuration."""
        self.logger = logging.getLogger("FRA.System")
        self.config = config
        self.logger.info("Initializing Fractal Reasoning Agent")
        
        # Initialize the Ollama client
        self.ollama_client = OllamaClient(
            model=config['ollama']['model'],
            host=config['ollama']['host'],
            port=config['ollama']['port']
        )
        
        # Initialize all system layers
        self._init_layers()
        
        self.logger.info("Fractal Reasoning Agent initialized successfully")
    
    def _init_layers(self):
        """Initialize all layers of the FRA system."""
        # Initialize input layer
        self.input_processor = ProblemInputProcessor(self.ollama_client, self.config['input_layer'])
        
        # Initialize decomposition layer
        self.primary_decomposer = PrimaryDecomposer(self.ollama_client, self.config['decomposition_layer'])
        
        # Processing layer components will be created dynamically based on sub-problems
        
        # Initialize integration layer
        self.solution_integrator = SolutionIntegrator(self.ollama_client, self.config['integration_layer'])
        self.quality_controller = QualityController(self.ollama_client, self.config['integration_layer'])
    
    def solve(self, problem_statement):
        """Process the problem statement and generate a solution."""
        self.logger.info(f"Starting to solve problem: {problem_statement}")
        start_time = time.time()
        
        # Step 1: Process the input problem
        processed_problem = self.input_processor.process(problem_statement)
        self.logger.info("Problem processed")
        
        # Step 2: Decompose the problem into sub-problems
        all_subproblems = self.primary_decomposer.decompose(processed_problem)
        self.logger.info(f"Problem decomposed into {len(all_subproblems)} sub-problems")
        
        # Step 3: Process all sub-problems in parallel
        sub_solutions = self._process_subproblems(all_subproblems)
        self.logger.info("All sub-problems processed")
        
        # Step 4: Integrate sub-solutions
        integrated_solution = self.solution_integrator.integrate(sub_solutions, processed_problem)
        self.logger.info("Sub-solutions integrated")
        
        # Step 5: Quality control
        final_solution = self.quality_controller.validate(integrated_solution, processed_problem)
        self.logger.info("Quality control completed")
        
        # Add metadata
        final_solution['metadata'] = {
            'problem_statement': problem_statement,
            'processed_problem': processed_problem,
            'subproblems_count': len(all_subproblems),
            'processing_time': time.time() - start_time
        }
        
        return final_solution
    
    def _process_subproblems(self, subproblems):
        """Process all sub-problems in parallel using the processing layer."""
        sub_solutions = []
        
        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=self.config.get('max_workers', 5)) as executor:
            future_to_subproblem = {
                executor.submit(self._process_single_subproblem, subproblem): subproblem
                for subproblem in subproblems
            }
            
            for future in future_to_subproblem:
                try:
                    sub_solution = future.result()
                    sub_solutions.append(sub_solution)
                except Exception as e:
                    subproblem = future_to_subproblem[future]
                    self.logger.error(f"Error processing sub-problem '{subproblem['id']}': {e}")
        
        return sub_solutions
    
    def _process_single_subproblem(self, subproblem):
        """Process a single sub-problem through solver, evaluator, and optimizer."""
        # Create processing layer components for this sub-problem
        solver = SolverUnit(self.ollama_client, self.config['processing_layer'])
        evaluator = Evaluator(self.ollama_client, self.config['processing_layer'])
        optimizer = Optimizer(self.ollama_client, self.config['processing_layer'])
        
        # Solve the sub-problem
        solution = solver.solve(subproblem)
        
        # Evaluate the solution
        evaluation = evaluator.evaluate(solution, subproblem)
        
        # Optimize the solution based on evaluation
        optimized_solution = optimizer.optimize(solution, evaluation)
        
        # Return the processed sub-solution with metadata
        return {
            'subproblem': subproblem,
            'solution': optimized_solution,
            'evaluation': evaluation
        }