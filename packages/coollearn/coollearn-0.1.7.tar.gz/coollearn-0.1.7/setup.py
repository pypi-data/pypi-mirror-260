#!/usr/bin/env python3

from setuptools import setup, find_packages

readme = """
# CoolLearn - 你的个性化学习助手 📘✨

欢迎来到CoolLearn，这里你的学习之旅将变得更加引人入胜、高效且贴合你的偏好。我们的前沿平台提供了一种变革性的知识吸收方式，为你提供选择学习深度、风格、语调和框架的灵活性。潜入一个教育遇见个性化的世界，开启一场与众不同的学习探险！

## 特点

- **个性化学习计划**：根据你选择的主题和偏好生成学习大纲，确保你深入探索对你来说最重要的科目。
- **互动对话**：与一个对你的提示做出响应的智能AI进行交流，鼓励你深入思考并提出问题。
- **流畅的用户体验**：享受一个无杂乱环境的易导航，提供一个无压力的学习空间。
- **历史跟踪**：通过历史记录跟踪你的学习进度，同步你的计划，并随时回顾过去的对话。
- **即时评估**：通过测验测试你的知识，并从你的AI伙伴那里接收反馈来指导你的学习旅程。
- **可定制偏好**：设置你的学习参数，如风格、语调和框架，以适应你的学习需求。
"""

setup(
    name="coollearn",
    version="0.1.7",
    author="boyjiangboyu",
    author_email="boyjiangboyu@outlook.com",
    description="Personalized Learning Assistant",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "zhipuai>=2.0.1",
        "streamlit>=1.31.1",
        "python-dotenv>=1.0.1"
    ],
    python_requires='>=3.10',
    entry_points={
        "console_scripts": [
            "coollearn = coollearn:run_app"
        ]
    },
)