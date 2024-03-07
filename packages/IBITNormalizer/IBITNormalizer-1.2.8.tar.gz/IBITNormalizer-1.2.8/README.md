# IBITNormalizer
Simple persian text-normalizer base on hazm lib

## install
```
pip install IBITNormalizer --upgrade
```

## import

```
from IBITNormalizer.normalizer import IBITNormalizer
```

## for lm task
```
text = """
سلام خوبی
از بیرون چخبر
چیکارا میکنی
تازگیا هوا  چقدر سرد شده نه ؟
"""

normalizer = IBITNormalizer.forLM()
print("forLM -> ", normalizer.normalize(text))

output:
forLM ->  سلام خوبی
از چخبر
چیکارا می‌کنی
تازگیا هوا سرد نه؟
```


## for llm task
```
text = """
سلام خوبی
از بیرون چخبر
چیکارا میکنی
تازگیا هوا  چقدر سرد شده نه ؟
"""

normalizer = IBITNormalizer.forLLM()
print("forLLM -> ", normalizer.normalize(text))

output:
forLLM ->  سلام خوبی
از بیرون چخبر
چیکارا می‌کنی
تازگیا هوا چقدر سرد‌شده‌نه؟
```