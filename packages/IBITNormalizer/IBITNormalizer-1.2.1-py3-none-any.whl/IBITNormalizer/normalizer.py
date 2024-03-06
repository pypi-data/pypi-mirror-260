from hazm import Normalizer
import os
import glob
from re import sub
from pathlib import Path


class IBITNormalizer(Normalizer):
    """این کلاس شامل توابعی برای نرمال‌سازی متن است.

    Args:
        hazm:
            correct_spacing: اگر `True` فاصله‌گذاری‌ها را در متن، نشانه‌های سجاوندی و پیشوندها و پسوندها اصلاح می‌کند.
            remove_diacritics: اگر `True` باشد اعرابِ حروف را حذف می‌کند.
            remove_specials_chars: اگر `True` باشد برخی از کاراکترها و نشانه‌های خاص را که کاربردی در پردازش متن ندارند حذف می‌کند.
            decrease_repeated_chars: اگر `True` باشد تکرارهای بیش از ۲ بار را به ۲ بار کاهش می‌دهد. مثلاً «سلاممم» را به «سلامم» تبدیل می‌کند.
            persian_style: اگر `True` باشد اصلاحات مخصوص زبان فارسی را انجام می‌دهد؛ مثلاً جایگزین‌کردن کوتیشن با گیومه.
            persian_numbers: اگر `True` باشد ارقام انگلیسی را با فارسی جایگزین می‌کند.
            unicodes_replacement: اگر `True` باشد برخی از کاراکترهای یونیکد را با معادل نرمال‌شدهٔ آن جایگزین می‌کند.
            seperate_mi: اگر `True` باشد پیشوند «می» و «نمی» را در افعال جدا می‌کند.

        personal:
            replace_to_standard_chrs: اگر `True` کاراکتر هارو استاندارد میکنه
            space_correction: اگر `True` تحصیح فاصله و نیم فاصله ها
            remove_stop_words :  اگر `True` حذف استاپ ورد ها

    """

    @classmethod
    def forLLM(self):
        return IBITNormalizer(
            correct_spacing=True,
            remove_diacritics=True,
            remove_specials_chars=True,
            decrease_repeated_chars=True,
            persian_style=False,
            persian_numbers=False,
            unicodes_replacement=True,
            seperate_mi=True,
            replace_to_standard_chrs=True,
            space_correction=True,
            remove_stop_words=False
        )

    @classmethod
    def forLM(self):
        return IBITNormalizer(
            correct_spacing=True,
            remove_diacritics=True,
            remove_specials_chars=True,
            decrease_repeated_chars=True,
            persian_style=True,
            persian_numbers=True,
            unicodes_replacement=True,
            seperate_mi=True,
            replace_to_standard_chrs=True,
            space_correction=True,
            remove_stop_words=True
        )

    def __init__(
        self: "Normalizer",
        *args, **kwargs
    ) -> None:
        self._replace_to_standard_chrs = kwargs["replace_to_standard_chrs"]
        del kwargs["replace_to_standard_chrs"]

        self._space_correction = kwargs["space_correction"]
        del kwargs["space_correction"]

        self._remove_stop_words = kwargs["remove_stop_words"]
        del kwargs["remove_stop_words"]

        self.dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

        if self._remove_stop_words:

            self.stop_words_paths = glob.glob(
                str(self.dir_path / 'resource' / 'Stopwords' / '**/*.txt'), recursive=True)

            self.__read_stop_words()

        if self._space_correction:

            self.dic1_path = self.dir_path / 'resource' / 'Normalizer' / 'Dic1_new.txt'
            self.dic2_path = self.dir_path / 'resource' / 'Normalizer' / 'Dic2_new.txt'
            self.dic3_path = self.dir_path / 'resource' / 'Normalizer' / 'Dic3_new.txt'

            self.__read_normalizer_word()

        super(IBITNormalizer, self).__init__(*args, **kwargs)

    def normalize(self: "Normalizer", text: str) -> str:
        """متن را نرمال‌سازی می‌کند.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.normalize('اِعلاممممم کَرد : « زمین لرزه ای به بُزرگیِ 6 دهم ریشتر ...»')
            'اعلام کرد: «زمین‌لرزه‌ای به بزرگی ۶ دهم ریشتر …»'
            >>> normalizer.normalize('')
            ''

        Args:
            text: متنی که باید نرمال‌سازی شود.

        Returns:
            متنِ نرمال‌سازی‌شده.

        """

        text = super(IBITNormalizer, self).normalize(text)

        if self._remove_stop_words:
            text = self.remove_stop_words(text)

        if self._replace_to_standard_chrs:
            text = self.replace_to_standard_chrs(text)

        if self._space_correction:
            text = self.space_correction(self.space_correction_plus1(
                self.space_correction_plus2(self.space_correction_plus3(text)))).strip()

        return text

    def replace_to_standard_chrs(self, doc_string):
        """ کاراکتر های غیر استاندارد فارسی رو با استاندارد هاش عوض میکنه
        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.replace_to_standard_chrs('ي')
            'ی'

        Args:
            text: متن ورودی

        Returns:
            متنی با کاراکتر های استاندارد

        """

        replaces = {
            r"ٲ|ٱ|إ|ﺍ|أ": r"ا",
            r"ﺁ|آ":  r"آ",
            r"ﺐ|ﺏ|ﺑ": r"ب",
            r"ﭖ|ﭗ|ﭙ|ﺒ|ﭘ": r"پ",
            r"ﭡ|ٺ|ٹ|ﭞ|ٿ|ټ|ﺕ|ﺗ|ﺖ|ﺘ": r"ت",
            r"ﺙ|ﺛ": r"ث",
            r"ﺝ|ڃ|ﺠ|ﺟ": r"ج",
            r"ڃ|ﭽ|ﭼ":  r"چ",
            r"ﺢ|ﺤ|څ|ځ|ﺣ": r"ح",
            r"ﺥ|ﺦ|ﺨ|ﺧ": r"خ",
            r"ڏ|ډ|ﺪ|ﺩ":  r"د",
            r"ﺫ|ﺬ|ﻧ":  r"ذ",
            r"ڙ|ڗ|ڒ|ڑ|ڕ|ﺭ|ﺮ": r"ر",
            r"ﺰ|ﺯ": r"ز",
            r"ﮊ":  r"ژ",
            r"ݭ|ݜ|ﺱ|ﺲ|ښ|ﺴ|ﺳ": r"س",
            r"ﺵ|ﺶ|ﺸ|ﺷ": r"ش",
            r"ﺺ|ﺼ|ﺻ": r"ص",
            r"ﺽ|ﺾ|ﺿ|ﻀ":  r"ض",
            r"ﻁ|ﻂ|ﻃ|ﻄ": r"ط",
            r"ﻆ|ﻇ|ﻈ":  r"ظ",
            r"ڠ|ﻉ|ﻊ|ﻋ": r"ع",
            r"ﻎ|ۼ|ﻍ|ﻐ|ﻏ": r"غ",
            r"ﻒ|ﻑ|ﻔ|ﻓ": r"ف",
            r"ﻕ|ڤ|ﻖ|ﻗ": r"ق",
            r"ڭ|ﻚ|ﮎ|ﻜ|ﮏ|ګ|ﻛ|ﮑ|ﮐ|ڪ|ك": r"ک",
            r"ﮚ|ﮒ|ﮓ|ﮕ|ﮔ": r"گ",
            r"ﻝ|ﻞ|ﻠ|ڵ":  r"ل",
            r"ﻡ|ﻤ|ﻢ|ﻣ": r"م",
            r"ڼ|ﻦ|ﻥ|ﻨ": r"ن",
            r"ވ|ﯙ|ۈ|ۋ|ﺆ|ۊ|ۇ|ۏ|ۅ|ۉ|ﻭ|ﻮ|ؤ":  r"و",
            r"ﺔ|ﻬ|ھ|ﻩ|ﻫ|ﻪ|ۀ|ە|ة|ہ":  r"ه",
            r"ﭛ|ﻯ|ۍ|ﻰ|ﻱ|ﻲ|ں|ﻳ|ﻴ|ﯼ|ې|ﯽ|ﯾ|ﯿ|ێ|ے|ى|ي": r"ی",
            r'¬': r'‌',
            r'•|·|●|·|・|∙|｡|ⴰ': r'.',
            r',|٬|٫|‚|，': r'،',
            r'ʕ': r'؟',
            r'ـ|ِ|ُ|َ|ٍ|ٌ|ً|': r'',
            r'( )+': r' ',
            r'(\n)+': r'\n'
        }

        for _from, _to in replaces.items():
            doc_string = sub(_from, _to, doc_string)

        return doc_string

    def space_correction(self, doc_string):
        """ فاصله و نیم فاصله هارو درست میکنه
        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.space_correction('سیب هایشان')
            'سیب[  نیم فاصله ]هایشان'

        Args:
            text: متن ورودی

        Returns:
            متنی با فاصله های استاندارد

        """

        a00 = r'^(بی|می|نمی)( )'
        b00 = r'\1‌'
        c00 = sub(a00, b00, doc_string)
        a0 = r'( )(می|نمی|بی)( )'
        b0 = r'\1\2‌'
        c0 = sub(a0, b0, c00)
        a1 = r'( )(هایی|ها|های|ایی|هایم|هایت|هایش|هایمان|هایتان|هایشان|ات|ان|ین' \
            r'|انی|بان|ام|ای|یم|ید|اید|اند|بودم|بودی|بود|بودیم|بودید|بودند|ست)( )'
        b1 = r'‌\2\3'
        c1 = sub(a1, b1, c0)
        a2 = r'( )(شده|نشده)( )'
        b2 = r'‌\2‌'
        c2 = sub(a2, b2, c1)
        a3 = r'( )(طلبان|طلب|گرایی|گرایان|شناس|شناسی|گذاری|گذار|گذاران|شناسان|گیری|پذیری|بندی|آوری|سازی|' \
            r'بندی|کننده|کنندگان|گیری|پرداز|پردازی|پردازان|آمیز|سنجی|ریزی|داری|دهنده|آمیز|پذیری' \
            r'|پذیر|پذیران|گر|ریز|ریزی|رسانی|یاب|یابی|گانه|گانه‌ای|انگاری|گا|بند|رسانی|دهندگان|دار)( )'
        b3 = r'‌\2\3'
        c3 = sub(a3, b3, c2)
        return c3

    def space_correction_plus1(self, doc_string):
        out_sentences = ''
        for wrd in doc_string.split(' '):
            try:
                out_sentences = out_sentences + ' ' + self.dic1[wrd]
            except KeyError:
                out_sentences = out_sentences + ' ' + wrd
        return out_sentences

    def space_correction_plus2(self, doc_string):
        out_sentences = ''
        wrds = doc_string.split(' ')
        L = wrds.__len__()
        if L < 2:
            return doc_string
        cnt = 1
        for i in range(0, L - 1):
            w = wrds[i] + wrds[i + 1]
            try:
                out_sentences = out_sentences + ' ' + self.dic2[w]
                cnt = 0
            except KeyError:
                if cnt == 1:
                    out_sentences = out_sentences + ' ' + wrds[i]
                cnt = 1
        if cnt == 1:
            out_sentences = out_sentences + ' ' + wrds[i + 1]
        return out_sentences

    def space_correction_plus3(self, doc_string):

        # Dict = {'گفتوگو': 'گفت‌وگو'}
        out_sentences = ''
        wrds = doc_string.split(' ')
        L = wrds.__len__()
        if L < 3:
            return doc_string
        cnt = 1
        cnt2 = 0
        for i in range(0, L - 2):
            w = wrds[i] + wrds[i + 1] + wrds[i + 2]
            try:
                out_sentences = out_sentences + ' ' + self.dic3[w]
                cnt = 0
                cnt2 = 2
            except KeyError:
                if cnt == 1 and cnt2 == 0:
                    out_sentences = out_sentences + ' ' + wrds[i]
                else:
                    cnt2 -= 1
                cnt = 1
        if cnt == 1 and cnt2 == 0:
            out_sentences = out_sentences + ' ' + \
                wrds[i + 1] + ' ' + wrds[i + 2]
        elif cnt == 1 and cnt2 == 1:
            out_sentences = out_sentences + ' ' + wrds[i + 2]
        return out_sentences

    def remove_stop_words(self, text):
        """
        Examples:
        >>> normalizer = Normalizer()
        >>> normalizer.remove_stop_words('از سیب')
        'سیب'

        Args:
            text: متن ورودی

        Returns:
            متنی که استاپ ورد های ان حذف شده
        """

        words = text.split(" ")
        new_words = []

        for word in words:
            if word in self.stop_words:
                continue

            new_words.append(word)

        new_text = " ".join(new_words)
        return new_text

    def __load_dictionary(self, file_path):
        dict = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            g = f.readlines()
            for Wrds in g:
                wrd = Wrds.split(' ')
                dict[wrd[0].strip()] = sub('\n', '', wrd[1].strip())
        return dict

    def __read_normalizer_word(self):
        self.dic1 = self.__load_dictionary(self.dic1_path)
        self.dic2 = self.__load_dictionary(self.dic2_path)
        self.dic3 = self.__load_dictionary(self.dic3_path)

    def __read_stop_words(self):

        self.stop_words = set()

        for stop_word_file_path in self.stop_words_paths:
            with open(stop_word_file_path, "r", encoding="utf-8") as stop_word_file:
                self.stop_words.update([line.strip("\n")
                                       for line in stop_word_file.readlines()])


if __name__ == "__main__":
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
