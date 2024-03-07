# pip install IBITNormalizer
from IBITNormalizer.normalizer import IBITNormalizer

text = """
سلام خوبی
از بیرون چخبر
چیکارا میکنی
تازگیا هوا  چقدر سرد شده نه ؟
"""

# for lm task
normalizer = IBITNormalizer.forLM()
print("forLM -> ", normalizer.normalize(text))

# for llm task
normalizer = IBITNormalizer.forLLM()
print("forLLM -> ", normalizer.normalize(text))
