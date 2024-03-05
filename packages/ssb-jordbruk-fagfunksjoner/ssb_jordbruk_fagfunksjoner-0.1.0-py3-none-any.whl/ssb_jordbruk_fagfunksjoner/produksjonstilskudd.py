from typing import ClassVar


class Produksjonstilskudd:
    """A mapping class for produksjonstilskudd codes related to agricultural products.

    This class contains all such codes with associated labels for agricultural products, such as fruits, vegetables and livestock. This simplifies working with produksjonstilskudd data by making the codes easier to look up and subset.

    Attributes:
        codes (ClassVar[dict]): A dictionary mapping produksjonstilskudd codes to their corresponding agricultural product.
        code_groups (ClassVar[dict[list[str]]]): Organizes the codes into categorized groups to make it easier to refer to only relevant codes.
        combinations (ClassVar[dict[list[str]]]): Defines lists of code_groups that are related to eachother to simplify getting several codes that are related.

    Methods:
        _setup_dynamic_attributes: Dynamically assigns categorized code groups and combinations as attributes for direct access.
        _extract_from_codelist(numbers): Utility method to extract codes based on provided criteria.
        get_codes(attributes, prefix): Retrieves a list of codes, optionally filtered by attributes and/or prefixed.

    Example:
        >>> pt = Produksjonstilskudd()
        >>> print(pt.get_codes('frukt_avling', prefix=True))
        ['PK_001', 'PK_002', 'PK_003', 'PK_004', 'PK_005', 'PK_006']

    Note:
        The class is designed with immutability in mind for the 'codes' attribute to ensure consistent and error-free usage.
    """

    codes: ClassVar[dict[str, str]] = {
        "001": "Epler",
        "002": "Pærer",
        "003": "Plommer",
        "004": "Moreller",
        "005": "Kirsebær",
        "006": "Epler og pærer til press",
        "011": "Jordbær",
        "012": "Bringebær",
        "013": "Solbær",
        "014": "Rips",
        "016": "Hageblåbær",
        "021": "Stikkelsbær",
        "022": "Industribær",
        "031": "Tomat",
        "032": "Slangeagurk",
        "033": "Salat (også friland)",
        "060": "Matpoteter i Nord-Norge",
        "115": "Hester, under 3 år",
        "116": "Hester, 3 år og eldre",
        "118": "Ammekyr av minst 50% kjøttferase",
        "119": "Øvrige storfe",
        "120": "Melkekyr",
        "121": "Ammekyr",
        "139": "Melkesau",
        "140": "Melkegeiter",
        "142": "Ammegeiter",
        "144": "Bukker og ungdyr, medregnet kje",
        "145": "Søyer født i fjor eller tidligere",
        "146": "Værer født i fjor eller tidligere",
        "154": "Smågriser, levendevekt under 20kg eller alder inntil 8 uker",
        "155": "Avlspurker som har fått minst 1 kull",
        "156": "Råner som er satt inn i avl",
        "157": "Slaktegriser, levendevekt minst 20kg",
        "158": "Ungpurker bestemt for avl",
        "159": "Ungråner bestemt for avl",
        "161": "Verpehøner",
        "162": "Rugeegg levert til rugeri",
        "168": "Avlsdyr av ender, kalkuner og gjess",
        "170": "Minktisper",
        "171": "Revetisper",
        "174": "Ender, kalkuner og gjess for slakt",
        "175": "Livkyllinger",
        "176": "Slaktekyllinger",
        "178": "Hjort, 1 år og eldre",
        "179": "Hjort, under 1 år",
        "180": "Kaniner",
        "181": "Griser solgt som livdyr, vekt på minst 50 kg",
        "183": "Struts",
        "185": "Kyllinger og kalkuner solgt som livdyr",
        "192": "Esel",
        "193": "Hester i pensjon i beitesesongen",
        "194": "Bifolk",
        "196": "Lama",
        "197": "Alpakka",
        "210": "Fulldyrket eng",
        "211": "Overflatedyrket eng",
        "212": "Innmarksbeite",
        "213": "Andre grovforvekster til for",
        "223": "Grønngjødsling",
        "230": "Poteter",
        "231": "Annet korn og frø som er berettiget tilskudd",
        "235": "Engfør og annen såfrøproduksjon",
        "236": "Erter, bønner og andre belgvekster til modning",
        "237": "Oljevekster",
        "238": "Rug og rughvete",
        "239": "Korn til krossing",
        "240": "Vårhvete",
        "242": "Bygg",
        "243": "Havre",
        "245": "Erter og bønner til konservesindustri (høstet før modning)",
        "247": "Høsthvete",
        "264": "Grønnsaker på friland, inkl. matkålrot og urter",
        "271": "Moreller og kirsebær",
        "272": "Epler",
        "273": "Pærer",
        "274": "Plommer",
        "280": "Jordbær",
        "282": "Andre bærarter",
        "283": "Andre fruktarter",
        "285": "Planteskoleareal og blomsterdyrking på friland",
        "290": "Brakka areal",
        "292": "Fulldyrket og/eller overflatedyrket, ute av drift",
        "293": "Innmarksbeite, ute av drift",
        "294": "Areal i drift, men ikke berettiget produksjonstilskudd",
        "410": "Storfe på utmarksbeite - Melkekyr og ammekyr",
        "411": "Storfe på beite - Melkekyr og ammekyr",
        "420": "Storfe på utmarksbeite - Øvrige storfe",
        "422": "Storfe på beite - Øvrige storfe",
        "431": "Sauer, født i fjor eller tidligere, utmarksbeite",
        "432": "Lam, født i år, utmarksbeite",
        "440": "Geiter, voksne og kje, utmarksbeite",
        "445": "Geiter, voksne og kje, beitetilskudd",
        "450": "Hester på utmarksbeite",
        "455": "Hester på beite",
        "480": "Lama på beite",
        "481": "Alpakka på beite",
        "486": "Hjort på beite",
        "487": "Sauer, født i fjor eller tidligere, beitetilskudd",
        "488": "Lam, født i år, beitetilskudd",
        "521": "Høy",
        "522": "Surfor",
        "523": "Høyensilasje",
        "720": "Storfe på utmarksbeite - Kyr av bevaringsverdig rase",
        "721": "Storfe på utmarksbeite - Okser av bevaringsverdig rase",
        "722": "Søyer av bevaringsverdig rase",
        "723": "Værer av bevaringsverdig rase",
        "724": "Ammegeiter av bevaringsverdig rase",
        "725": "Unghester under 3 år av bevaringsverdig rase",
        "801": "Økologiske melkekyr",
        "802": "Økologiske ammekyr",
        "803": "Økologiske øvrige storfe",
        "810": "Økologiske melkegeiter",
        "811": "Økologiske ammegeiter",
        "821": "Økologiske sauer",
        "830": "Økologiske avlsgriser",
        "833": "Økologiske griser solgt som livdyr",
        "841": "Økologiske verpehøner",
        "852": "Grønngjødsling, 2. års karens",
        "855": "Korn til modning og krossing, økologisk samt 2.års karens",
        "861": "Poteter, økologisk areal samt 2.års karens",
        "863": "Frukt og bær, økologisk areal samt 2. og 3. års karens",
        "864": "Grønnsaker, økologisk areal samt 2. års karens",
        "870": "Annet areal (grovfôr), økologisk areal samt 2. års karens",
        "871": "Innmarksbeite, økologisk areal",
        "875": "Grønngjødsling, økologisk areal",
        "876": "Areal brakka for å bekjempe ugras, økologisk eller 2. års karens",
        "880": "Innmarksbeite i 1 års karens",
        "881": "Grovforareal i 1 års karens",
        "882": "Annet areal (enn grovfor) i 1 års karens",
    }

    code_groups: ClassVar[dict[str, list[str]]] = {
        "frukt_avling": ["001", "002", "003", "004", "005", "006"],
        "frukt_areal": ["271", "272", "273", "274", "283", "863"],
        "baer_avling": ["011", "012", "013", "014", "016", "021", "022"],
        "baer_areal": ["280", "282", "863"],
        "groennsaker": ["031", "032", "033", "060", "230", "264", "861", "864", "285"],
        "grovfor_areal": ["210", "211", "212", "213", "870", "871", "880", "881"],
        "grovfor_salg": ["521", "522", "523"],
        "korn": [
            "231",
            "235",
            "236",
            "237",
            "238",
            "239",
            "240",
            "242",
            "243",
            "245",
            "247",
            "855",
        ],
        "annet_areal": ["223", "290", "294", "876", "852", "875", "882"],
        "areal_ute_av_drift": ["292", "293"],
        "storfe": [
            "118",
            "119",
            "120",
            "121",
            "410",
            "411",
            "420",
            "422",
            "720",
            "721",
            "801",
            "802",
            "803",
        ],
        "hester": ["115", "116", "193", "455", "450", "725"],
        "småfe": [
            "145",
            "146",
            "139",
            "140",
            "142",
            "144",
            "821",
            "811",
            "810",
            "487",
            "488",
            "445",
            "440",
            "431",
            "432",
            "722",
            "723",
            "724",
        ],
        "griser": ["155", "156", "158", "159", "154", "157", "830", "181", "833"],
        "fjørfe_og_rugeegg": ["161", "162", "168", "175", "176", "174", "841", "185"],
        "pelsdyr": ["170", "171"],
        "andre_husdyr": [
            "178",
            "179",
            "180",
            "183",
            "192",
            "194",
            "196",
            "197",
            "480",
            "481",
            "486",
        ],
    }

    combinations: ClassVar[dict[str, list[str]]] = {
        "frukt": ["frukt_avling", "frukt_areal"],
        "baer": ["baer_avling", "baer_areal"],
        "grovfor": ["grovfor_areal", "grovfor_salg"],
        "areal": ["grovfor", "korn", "annet_areal", "areal_ute_av_drift"],
        "dyr": [
            "hester",
            "storfe",
            "småfe",
            "griser",
            "fjørfe_og_rugeegg",
            "pelsdyr",
            "andre_husdyr",
        ],
        "frukt_baer_groennsaker": ["frukt", "baer", "groennsaker"],
    }

    def __init__(self) -> None:
        """Initializes an instance of the Produksjonstilskudd class.

        This constructor method dynamically sets up class attributes based on predefined code groups and combinations. It organizes various agricultural product codes, including fruits, vegetables, and livestock, into easily accessible class attributes for further processing or querying.
        Upon instantiation, it calls the _setup_dynamic_attributes method to dynamically assign attributes to the instance based on the `code_groups` and `combinations` class variables. This setup allows for flexible manipulation and access to specific subsets of product codes.
        Attributes are set up to facilitate extraction of codes with the option to prefix them with 'PK_', indicating a primary key or unique identifier, which can be used for database operations or internal logic.

        Example usage:
            pt = Produksjonstilskudd()
            print(pt.get_codes('frukt_avling', prefix=True))

        The example above will print all fruit harvesting codes, prefixed with 'PK_', indicating that these codes are treated as unique identifiers.
        """
        self._setup_dynamic_attributes()

    def _setup_dynamic_attributes(self) -> None:
        # Set attributes for each code group
        for group_name, codes in self.code_groups.items():
            setattr(self, group_name, self._extract_from_codelist(codes))

        for combo_name, groups in self.combinations.items():
            combined_dict: dict[str, str] = {}
            for group in groups:
                combined_dict.update(getattr(self, group, {}))
            setattr(self, combo_name, combined_dict)

    def _extract_from_codelist(self, numbers: list[str]) -> dict[str, str]:
        result = {}
        for code in numbers:
            if code not in self.codes:
                raise ValueError(f"Code {code} not found in codes dictionary.")
            result[code] = self.codes[code]
        return result

    def get_codes(
        self, attributes: str | list[str] | None = None, prefix: bool | None = False
    ) -> list[str]:
        """Returns a list of 3-digit codes from the specified attributes.

        If no attributes are specified, this method returns all 3-digit codes available. Optionally, a 'PK_' prefix can be added to each code.

        Parameters
        ----------
        attributes : None, str, or list of str, optional
            The attribute or list of attributes for which codes are to be retrieved. If `None`, codes for all attributes are returned.
        prefix : bool, optional
            Indicates whether to add a 'PK_' prefix to each code. Default is `False`.

        Returns:
        -------
        list of str
            A list containing the requested 3-digit codes, optionally prefixed with 'PK_'.

        Examples:
        --------
        >>> pt = Produksjonstilskudd()
        >>> pt.get_codes('frukt_avling', prefix=True)
        ['PK_001', 'PK_002', 'PK_003', 'PK_004', 'PK_005', 'PK_006']

        >>> pt.get_codes()
        ['001', '002', '003', '004', '005', '006', '011', '012', '013', '014', '016', '021', '022', '031', '032', '033', '060', '115', '116', '118', '119', '120', '121', '139', '140', '142', '144', '145', '146', '154', '155', '156', '157', '158', '159', '161', '162', '168', '170', '171', '174', '175', '176', '178', '179', '180', '181', '183', '185', '192', '193', '194', '196', '197', '210', '211', '212', '213', '223', '230', '231', '235', '236', '237', '238', '239', '240', '242', '243', '245', '247', '264', '271', '272', '273', '274', '280', '282', '283', '285', '290', '292', '293', '294', '410', '411', '420', '422', '431', '432', '440', '445', '450', '455', '480', '481', '486', '487', '488', '521', '522', '523', '720', '721', '722', '723', '724', '725', '801', '802', '803', '810', '811', '821', '830', '833', '841', '852', '855', '861', '863', '864', '870', '871', '875', '876', '880', '881', '882']
        """
        if attributes:
            if isinstance(attributes, str):  # Single attribute name
                attributes = [attributes]  # Convert to list for consistency
            codes = []
            for attribute_name in attributes:
                attribute_dict = getattr(self, attribute_name, {})
                codes.extend(list(attribute_dict.keys()))
        else:
            # No specific attributes provided, return all 3-digit codes
            codes = list(self.codes.keys())

        if prefix:
            return ["PK_" + code for code in codes]
        else:
            return codes
