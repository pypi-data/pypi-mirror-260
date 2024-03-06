# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vision_llama']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'swarms', 'torch', 'torchvision', 'zetascale']

setup_kwargs = {
    'name': 'vision-llama',
    'version': '0.0.8',
    'description': 'Vision Llama - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Vision LLama\nImplementation of VisionLLaMA from the paper: "VisionLLaMA: A Unified LLaMA Interface for Vision Tasks" in PyTorch and Zeta. [PAPER LINK](https://arxiv.org/abs/2403.00522)\n\n\n## install\n`$ pip install vision-llama`\n\n\n## usage\n```python\n\nimport torch\nfrom vision_llama.main import VisionLlama\n\n# Forward Tensor\nx = torch.randn(1, 3, 224, 224)\n\n# Create an instance of the VisionLlamaBlock model with the specified parameters\nmodel = VisionLlama(\n    dim=768, depth=12, channels=3, heads=12, num_classes=1000\n)\n\n\n# Print the shape of the output tensor when x is passed through the model\nprint(model(x))\n\n```\n\n\n\n# License\nMIT\n\n## Citation\n```bibtex\n@misc{chu2024visionllama,\n    title={VisionLLaMA: A Unified LLaMA Interface for Vision Tasks}, \n    author={Xiangxiang Chu and Jianlin Su and Bo Zhang and Chunhua Shen},\n    year={2024},\n    eprint={2403.00522},\n    archivePrefix={arXiv},\n    primaryClass={cs.CV}\n}\n```\n\n## todo\n- [ ] Implement the AS2DRoPE rope, might just use axial rotary embeddings instead, my implementation is really bad\n- [x] Implement the GSA attention, i implemented it but\'s bad\n- [ ] Add imagenet training script with distributed',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/VisionLLaMA',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
