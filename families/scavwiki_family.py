from pywikibot import family


class Family(family.Family):  # noqa: D101

    name = 'scavwiki'
    langs = {
        'en': 'scavprototype.wiki.gg',
    }

    def scriptpath(self, code):
        return {
            'en': '',
        }[code]

    def protocol(self, code):
        return {
            'en': 'https',
        }[code]
