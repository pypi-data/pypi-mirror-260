from modeltranslation.translator import translator, TranslationOptions
from .models import MenuItem


class MenuItemTranslationOptions(TranslationOptions):
    fields = ('label',)

translator.register(MenuItem, MenuItemTranslationOptions)
