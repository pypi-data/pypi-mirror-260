# escape-unk
Escape unknown symbols in SentecePiece vocabularies.
This is particulary useful for [MarianNMT](https://github.com/marian-nmt/marian) toolkit which does not support replacing unknown tokens with most attentive word in the source (see [here](https://github.com/marian-nmt/marian-dev/issues/732), thanks to @emjotde for the idea).

## Install
Just install it from PyPi
```
pip install escape-unk
```

## Background
There are some scenarios where your machine translation model has to translate sentencences containing characters unknown for the SentencePiece vocabulary.
Neural models usually start to hallucinate, throw out garbage or just don't know hot to translate when an unknown character comes to the input.
In the cases where those characters simply need to be copied, escaping them to their hexadecimal representation, can be useful if the model manages to copy the escaped symbols.

Escape Chinese characters in an English-German vocabulary is just like:
```bash
echo "Beijing (Chinese: 北京) is the capital of the People's Republic of China" | escape-unk -m vocab.deen.spm
```
```
Beijing (Chinese: [[e58c97e4baac]]) is the capital of the People's Republic of China
```

or escaping emojis
```bash
echo "I ❤️ you" | escape-unk -m vocab.deen.spm
```
```
I [[e29da4efb88f]] you
```

So instead of:
```bash
echo "Beijing (Chinese: 北京) is the capital of the People's Republic of China" | marian-decoder -c model.config.yml
```
```
Peking (chinesisch: ) ist die Hauptstadt der Volksrepublik China
```

we will have:
```bash
echo "Beijing (Chinese: 北京) is the capital of the People's Republic of China" | escape-unk -m vocab.deen.spm | marian-decoder -c model.config.yml
```
```
Beijing (chinesisch: [[e58c97e4baac]]) ist die Hauptstadt der Volksrepublik China
```

and the full pipeline with `unescape-unk`:
```bash
echo "Beijing ..." | escape-unk -m vocab.deen.spm | marian-decode -c config.yml | unescape-unk
```
```
Beijing (chinesisch: 北京) ist die Hauptstadt der Volksrepublik China
```

**WARNING**: if an escaped sequence is not correctly copied by the translator and generates an invalid sequence,
the character is omitted and substituted by an empty string.
If you want it to fail when this happens, use `--strict`/`-s` mode with `unescape-unk` command.

