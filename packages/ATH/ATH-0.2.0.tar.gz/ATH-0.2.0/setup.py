from setuptools import setup, find_packages

setup(
    name="ATH",
    version="0.2.0",
    description="For More Info: https://discord.com/channels/831614817458323537/1213477275232641044",
    packages=find_packages(),
    install_requires=["pyttsx3", "cryptography", "speechrecognition", "asyncio", "discord", "discord.py"]
)