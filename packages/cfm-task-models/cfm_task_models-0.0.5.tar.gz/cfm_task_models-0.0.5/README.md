# CFM-Task-Models

Popular CV models modified for various approaches of Compression for Machines (aka Coding for Machines)

### Installation

The easiest way to install CFM-Task-Models is through PyPI, to do this simply use `pip install cfm-task-models`
However, CFM-Task-Models has requirements that currently cannot be handled by pip, thus before using CFM-Task-Models for the first time please run `miminstaller.py` in your virutal environment. If using poetry consider:
`poetry run -m cfm_task_models.split_utils.miminstaller`

###### Requirements

CFM-Task-Models currently relies on several tools from OpenMMLab, which require custom installation using the openmim installer. Openmim is a tool provided by OpenMMLab which installs their libraries based on the user's pytorch and cuda versions.

See pyproject.toml for standard requirements and miminstaller.py for OpenMMLAB requirements

### Usage

To test Swin_Transformer, run the following command from the root directory:

```python models/Swin-Transformer/models/swin_transformer_v2.py```
