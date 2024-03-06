# IBITNormalizer
Simple persian text-normalizer base on hazm lib

## install
```
pip install IBITNormalizer
```

## import

```
from IBITNormalizer.normalizer import IBITNormalizer
```

## for lm task
```
normalizer = IBITNormalizer.forLM()
print("سلام خوبی", normalizer.normalize("سلام خوبی"))
```


## for llm task
```
normalizer = IBITNormalizer.forLLM()
print("سلام خوبی", normalizer.normalize("سلام خوبی"))
```