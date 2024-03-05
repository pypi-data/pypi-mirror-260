import glob
import json
import os
import sqlite3
import xml.etree.ElementTree as ET
from typing import Any, Dict, Optional, Union

import pandas as pd
import torch
import yaml  # type: ignore
from datasets import Dataset, load_dataset, load_from_disk, load_metric
from geniusrise import BatchInput, BatchOutput, State
from pyarrow import feather
from pyarrow import parquet as pq

from geniusrise_text.base import TextBulk


class InstructionEval(TextBulk):
    r"""
    InstructionEval extends TextBulk to support evaluation of instruction-based models on large datasets.
    It enables processing of datasets, model inference, and computation of evaluation metrics such as BLEU score.

    Args:
        input (BatchInput): Configuration and data inputs for the batch process.
        output (BatchOutput): Configurations for output data handling.
        state (State): State management for the instruction task.
        **kwargs: Arbitrary keyword arguments for extended configurations.
    """

    def __init__(self, input: BatchInput, output: BatchOutput, state: State, **kwargs) -> None:
        """
        Initializes the InstructionEval class with configurations for input, output, state, and evaluation settings.

        Args:
            input (BatchInput): Configuration for the input data.
            output (BatchOutput): Configuration for the output data.
            state (State): State management for the instruction task.
            **kwargs: Additional keyword arguments for extended functionality.
        """
        super().__init__(input, output, state, **kwargs)

    def load_dataset(self, dataset_path: str, max_length: int = 1024, **kwargs) -> Optional[Dataset]:
        r"""
        Loads a dataset from the specified path. This method supports various data formats including JSON, CSV, Parquet,
        and others. It's designed to facilitate the bulk processing of text data for generation tasks.

        Args:
            dataset_path (str): Path to the directory containing the dataset files.
            max_length (int): Maximum token length for text processing (default is 1024).
            **kwargs: Additional keyword arguments for dataset loading.

        Returns:
            Optional[Dataset]: A Dataset object if loading is successful; otherwise, None.

        Raises:
            Exception: If an error occurs during dataset loading.

        ## Supported Data Formats and Structures:

        ### JSONL
        Each line is a JSON object representing an example.
        ```json
        {"instruction": "The instruction", "output": "The output"}
        ```

        ### CSV
        Should contain 'instruction' and 'output' columns.
        ```csv
        instruction,output
        "The instruction","The output"
        ```

        ### Parquet
        Should contain 'instruction' and 'output' columns.

        ### JSON
        An array of dictionaries with 'instruction' and 'output' keys.
        ```json
        [{"instruction": "The instruction", "output": "The output"}]
        ```

        ### XML
        Each 'record' element should contain 'instruction' and 'output' child elements.
        ```xml
        <record>
            <instruction>The instruction</instruction>
            <output>The output</output>
        </record>
        ```

        ### YAML
        Each document should be a dictionary with 'instruction' and 'output' keys.
        ```yaml
        - instruction: "The instruction"
          output: "The output"
        ```

        ### TSV
        Should contain 'instruction' and 'output' columns separated by tabs.

        ### Excel (.xls, .xlsx)
        Should contain 'instruction' and 'output' columns.

        ### SQLite (.db)
        Should contain a table with 'instruction' and 'output' columns.

        ### Feather
        Should contain 'instruction' and 'output' columns.
        """
        try:
            self.log.info(f"Loading dataset from {dataset_path}")
            self.max_length = max_length

            if self.use_huggingface_dataset:
                dataset = load_dataset(self.huggingface_dataset)
            elif os.path.isfile(os.path.join(dataset_path, "dataset_info.json")):

                dataset = load_from_disk(dataset_path)
            else:
                data = []
                for filename in glob.glob(f"{dataset_path}/*"):
                    filepath = os.path.join(dataset_path, filename)
                    if filename.endswith(".jsonl"):
                        with open(filepath, "r") as f:
                            for line in f:
                                example = json.loads(line)
                                data.append(example)

                    elif filename.endswith(".csv"):
                        df = pd.read_csv(filepath)
                        data.extend(df.to_dict("records"))

                    elif filename.endswith(".parquet"):
                        df = pq.read_table(filepath).to_pandas()
                        data.extend(df.to_dict("records"))

                    elif filename.endswith(".json"):
                        with open(filepath, "r") as f:
                            json_data = json.load(f)
                            data.extend(json_data)

                    elif filename.endswith(".xml"):
                        tree = ET.parse(filepath)
                        root = tree.getroot()
                        for record in root.findall("record"):
                            instruction = record.find("instruction").text  # type: ignore
                            output = record.find("output").text  # type: ignore
                            data.append({"instruction": instruction, "output": output})

                    elif filename.endswith(".yaml") or filename.endswith(".yml"):
                        with open(filepath, "r") as f:
                            yaml_data = yaml.safe_load(f)
                            data.extend(yaml_data)

                    elif filename.endswith(".tsv"):
                        df = pd.read_csv(filepath, sep="\t")
                        data.extend(df.to_dict("records"))

                    elif filename.endswith((".xls", ".xlsx")):
                        df = pd.read_excel(filepath)
                        data.extend(df.to_dict("records"))

                    elif filename.endswith(".db"):
                        conn = sqlite3.connect(filepath)
                        query = "SELECT instruction, output FROM dataset_table;"
                        df = pd.read_sql_query(query, conn)
                        data.extend(df.to_dict("records"))

                    elif filename.endswith(".feather"):
                        df = feather.read_feather(filepath)
                        data.extend(df.to_dict("records"))

                dataset = Dataset.from_pandas(pd.DataFrame(data))

            if hasattr(self, "map_data") and self.map_data:
                fn = eval(self.map_data)  # type: ignore
                dataset = dataset.map(fn)
            else:
                dataset = dataset

            return dataset
        except Exception as e:
            self.log.error(f"Error occurred when loading dataset from {dataset_path}. Error: {e}")
            raise

    def evaluate(
        self,
        model_name: str,
        model_class: str = "AutoModelForSeq2SeqLM",
        tokenizer_class: str = "AutoTokenizer",
        use_cuda: bool = False,
        precision: str = "float16",
        quantization: int = 0,
        device_map: Union[str, Dict, None] = "auto",
        max_memory: Dict[int, str] = {0: "24GB"},
        torchscript: bool = False,
        compile: bool = False,
        awq_enabled: bool = False,
        flash_attention: bool = False,
        batch_size: int = 32,
        notification_email: Optional[str] = None,
        use_huggingface_dataset: bool = False,
        huggingface_dataset: str = "",
        **kwargs: Any,
    ) -> None:
        """
        Evaluates the model on the loaded dataset, calculates evaluation metrics, and saves both predictions and metrics.

        Args:
            model_name (str): Name or path of the model.
            model_class (str): Class name of the model (default "AutoModelForSeq2SeqLM").
            tokenizer_class (str): Class name of the tokenizer (default "AutoTokenizer").
            use_cuda (bool): Whether to use CUDA for model inference (default False).
            precision (str): Precision for model computation (default "float16").
            quantization (int): Level of quantization for optimizing model size and speed (default 0).
            device_map (Union[str, Dict, None]): Specific device to use for computation (default "auto").
            max_memory (Dict[int, str]): Maximum memory configuration for devices (default {0: "24GB"}).
            torchscript (bool): Whether to use a TorchScript-optimized version of the model (default False).
            compile (bool): Whether to compile the model before evaluation (default True).
            awq_enabled (bool): Whether to enable AWQ optimization (default False).
            flash_attention (bool): Whether to use flash attention optimization (default False).
            batch_size (int): Number of evaluations to process simultaneously (default 32).
            notification_email (Optional[str]): Email to notify upon completion (default None).
            use_huggingface_dataset (bool, optional): Whether to load a dataset from huggingface hub.
            huggingface_dataset (str, optional): The huggingface dataset to use.
            **kwargs: Configuration and additional arguments for text generation and model loading.

        Note:
            Additional arguments are passed directly to the model and tokenizer initialization and the evaluation method.
        """
        if ":" in model_name:
            model_revision = model_name.split(":")[1]
            tokenizer_revision = model_name.split(":")[1]
            model_name = model_name.split(":")[0]
            tokenizer_name = model_name
        else:
            model_revision = None
            tokenizer_revision = None
            tokenizer_name = model_name

        self.model_name = model_name
        self.tokenizer_name = tokenizer_name
        self.model_revision = model_revision
        self.tokenizer_revision = tokenizer_revision
        self.model_class = model_class
        self.tokenizer_class = tokenizer_class
        self.use_cuda = use_cuda
        self.precision = precision
        self.quantization = quantization
        self.device_map = device_map
        self.max_memory = max_memory
        self.torchscript = torchscript
        self.compile = compile
        self.awq_enabled = awq_enabled
        self.flash_attention = flash_attention
        self.batch_size = batch_size
        self.notification_email = notification_email
        self.use_huggingface_dataset = use_huggingface_dataset
        self.huggingface_dataset = huggingface_dataset

        model_args = {k.replace("model_", ""): v for k, v in kwargs.items() if "model_" in k}
        self.model_args = model_args

        generation_args = {k.replace("generation_", ""): v for k, v in kwargs.items() if "generation_" in k}
        self.generation_args = generation_args

        self.model, self.tokenizer = self.load_models(
            model_name=self.model_name,
            tokenizer_name=self.tokenizer_name,
            model_revision=self.model_revision,
            tokenizer_revision=self.tokenizer_revision,
            model_class=self.model_class,
            tokenizer_class=self.tokenizer_class,
            use_cuda=self.use_cuda,
            precision=self.precision,
            quantization=self.quantization,
            device_map=self.device_map,
            max_memory=self.max_memory,
            torchscript=self.torchscript,
            awq_enabled=self.awq_enabled,
            flash_attention=self.flash_attention,
            compile=self.compile,
            **self.model_args,
        )

        dataset_path = self.input.input_folder
        output_path = self.output.output_folder

        # Load dataset
        dataset = self.load_dataset(dataset_path)
        if dataset is None:
            self.log.error("Failed to load dataset.")
            return

        bleu_metric = load_metric("bleu")

        all_predictions = []
        all_references = []

        # Process data in batches
        for i in range(0, len(dataset), batch_size):
            batch = dataset[i : i + batch_size]
            inputs = self.tokenizer(
                batch["instruction"], return_tensors="pt", padding=True, truncation=True, max_length=self.max_length
            )
            references = batch["output"]

            if use_cuda:
                inputs = {k: v.cuda() for k, v in inputs.items()}

            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"], max_length=self.max_length
                )

            predictions = [self.tokenizer.decode(g, skip_special_tokens=True) for g in outputs]
            all_predictions.extend(predictions)
            all_references.extend([[ref] for ref in references])

        # Compute BLEU score
        result = bleu_metric.compute(predictions=all_predictions, references=all_references)
        bleu_score = result["bleu"]

        # Save evaluation metrics
        metrics = {"bleu_score": bleu_score}
        self._save_metrics(metrics, output_path)

        self.done()

    def _save_metrics(self, metrics: Dict[str, float], output_path: str) -> None:
        """
        Saves the evaluation metrics to a specified output path.

        Args:
            metrics (Dict[str, float]): The evaluation metrics to save.
            output_path (str): The directory path to save the metrics.
        """
        with open(os.path.join(output_path, "evaluation_metrics.json"), "w") as f:
            json.dump(metrics, f, indent=4)
