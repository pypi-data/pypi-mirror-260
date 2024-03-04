from finter.framework_model.submission.config import (
    ModelTypeConfig,
    ModelUniverseConfig,
)
from finter.framework_model.submission.helper_notebook import (
    extract_and_convert_notebook,
)
from finter.framework_model.submission.helper_position import load_and_get_position
from finter.framework_model.submission.helper_simulation import run_simulation
from finter.framework_model.submission.helper_submission import submit_model
from finter.framework_model.validation import ValidationHelper
from finter.settings import log_section, logger


class NotebookSubmissionHelper:
    """
    A helper class to facilitate the submission process of financial models
    developed in Jupyter Notebooks. It supports extracting relevant cells from a
    notebook, running simulations, performing validations, and submitting the model
    for further use or evaluation.

    Attributes:
        cell_indices (list): Indices of the cells to extract from the notebook.
        notebook_name (str): The name of the notebook file (including path if necessary).
        model_name (str): The name of the model to be submitted.
        model_universe (str): The universe for the model (e.g. "kr_stock").
        model_type (str): The type of the model (e.g. "alpha" or "portfolio").
    """

    def __init__(
        self,
        cell_indices,
        notebook_name,
        model_name,
        model_universe,
        model_type="alpha",
    ):
        """
        Initializes the NotebookSubmissionHelper with necessary information.

        Parameters:
            cell_indices (list): Indices of the cells to extract from the notebook.
            notebook_name (str): The name of the notebook file (including path if necessary).
            model_name (str): The name of the model to be submitted.
            model_universe (str): The universe for the model (e.g. "kr_stock").
            model_type (str): The type of the model (e.g. "alpha" or "portfolio").
        """
        self.cell_indices = cell_indices
        self.notebook_name = notebook_name
        self.model_name = model_name
        try:
            self.model_type = ModelTypeConfig[model_type.upper()].name
        except KeyError:
            logger.error(
                f"Invalid model type: {model_type}. Available options: {ModelTypeConfig.available_options()}"
            )
            raise

        try:
            self.model_info = ModelUniverseConfig[model_universe.upper()].get_config(
                model_type=ModelTypeConfig[model_type.upper()]
            )
        except KeyError:
            logger.error(
                f"Invalid model universe: {model_universe}. Available options: {ModelUniverseConfig.available_options()}"
            )
            raise

    def process(
        self,
        start,
        end,
        position=False,
        simulation=False,
        validation=False,
        submit=False,
    ):
        """
        Processes the notebook by extracting specified cells, and optionally running position extraction,
        simulation, validation, and submission steps. Validation is automatically performed if submission is
        requested. Position extraction is mandatory for simulation.

        Parameters:
            start (str): The start date for the simulation and validation processes.
            end (str): The end date for the simulation and validation processes.
            position (bool): Flag to determine whether to extract positions from the model. Default is False.
            simulation (bool): Flag to determine whether to run a simulation based on the extracted positions. Default is False.
            validation (bool): Flag to determine whether to validate the model. Default is False.
            submit (bool): Flag to determine whether to submit the model. Default is False.
        """
        # Extract and convert the notebook
        log_section("Notebook Extraction")
        output_file_path = extract_and_convert_notebook(
            self.cell_indices,
            self.notebook_name,
            self.model_name,
            model_type=self.model_type,
        )

        if not output_file_path:
            logger.error("Error extracting notebook.")
            return
        logger.info(f"Notebook extracted to {output_file_path}")

        # Ensure position extraction if simulation is requested
        if simulation and not position:
            position = True
            logger.warning(
                "Position extraction is required for simulation. Setting position=True."
            )

        # Perform position extraction if required
        if position:
            log_section("Position Extraction")
            self.position = load_and_get_position(
                start, end, output_file_path, model_type=self.model_type
            )
            if self.position is None:
                logger.error("Error running notebook for position extraction.")
                return
            logger.info("Position extraction from notebook ran successfully.")

        # Run simulation with the extracted positions if requested
        if simulation:
            log_section("Simulation")
            self.model_stat = run_simulation(
                self.model_info, start, end, position=self.position
            )
            logger.info("Simulation run successfully based on the extracted positions.")

        # Validate the model if requested
        if validation:
            log_section("Validation")
            validator = ValidationHelper(
                model_path=self.model_name, model_info=self.model_info
            )
            validator.validate()
            logger.info("Model validated successfully.")

        # Submit the model if requested
        if submit:
            log_section("Model Submission")
            self.submit_result = submit_model(self.model_info, self.model_name)
            logger.info("Model submitted successfully.")
