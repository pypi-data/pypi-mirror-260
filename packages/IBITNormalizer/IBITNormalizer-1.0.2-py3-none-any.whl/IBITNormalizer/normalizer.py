from hazm import Normalizer
from re import sub


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
        )

    @classmethod
    def forLM(self):
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
        )

    def __init__(
        self: "Normalizer",
        *args, **kwargs
    ) -> None:
        self._replace_to_standard_chrs = kwargs["replace_to_standard_chrs"]
        del kwargs["replace_to_standard_chrs"]

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

        if self._replace_to_standard_chrs:
            text = self.replace_to_standard_chrs(text)

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


if __name__ == "__main__":

    # for lm task
    normalizer = IBITNormalizer.forLM()
    print("سلام خوبی", normalizer.normalize("سلام خوبی"))

    # for llm task
    normalizer = IBITNormalizer.forLLM()
    print("سلام خوبی", normalizer.normalize("سلام خوبی"))
