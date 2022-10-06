'''
See COPYRIGHT.md for copyright information.

Implementation of ISO 17442:2012(E) Appendix A

'''
import regex as re

LEI_VALID = 0
LEI_INVALID_LEXICAL = 1
LEI_INVALID_CHECKSUM = 2

LEI_RESULTS = ("valid", "invalid lexical", "invalid checksum")

leiLexicalPattern = re.compile(r"^[0-9A-Z]{18}[0-9]{2}$")

validInvalidLeiPattern = re.compile("^(029200720E3M3A4D6D01|029200758D5M0AI3F601|315700X8JQ3IU0NGK501|3157007SCCESQAUH5Z01|315700TCC9NTEP7J8Z01|13250000000000000301|315700ADOXDR5PCY5400|315700A0UB9Q7DOQIZ00|315700BM9Z39TNTGQW00|315700BZ5F7DRYG2UM00|315700B8401GTFFY6X01|315700DJ07P6OX10FK01|315700DKCD4QSKLAMO01|315700D23JL5C1DZNT00|315700EIYO2TLSEGQ700|315700ET7M7VQ4C84R00|315700EZSEA51937KX01|315700GXBGM8DBYKHF01|315700GZA843JXKTJ400|315700G5G24XYL1TXH00|315700HS7WJ1B0SUWM01|315700HXOEOK58E58P01|315700HZU4SMI8LZTU00|315700I3W2AFHP8MNQ01|315700JICZ3SY5SAXX00|315700JKZH6I0067ND01|315700JO5E28SRE00Q01|315700JXUHL9H2C3P700|315700LDDN3RM7Y2MP00|315700LWYOZNQ7V1T100|315700MBYPT6PGKO7M01|315700MW2F0KFR45QW01|315700M5843O6DU83901|315700NNMGS8F3P2CN00|315700N0VEIBHP0NPQ01|315700OASRCM664PAW01|315700OFW4YCOBNX4U01|315700OVW93X0T3HP200|315700O666JVNCQU9X00|315700PLI0I7W8IOV400|315700PN3J57ZUNF1V00|315700PXKOSX7WQV4N00|315700P4N9VSLK5QZV01|315700P40OV6BT045900|315700P6TZOLP92KN801|315700P89WR82VNB8Z00|315700QGM4XWZE1I5N01|315700Q1S8O1UORF9700|315700RK8M4FAHMYAP01|315700RTEHY362KXWJ00|315700SNUXK41WMW5J00|315700S22RGYRIEEOT00|315700S3TF79ALV82F01|315700TF5Z7T28HZJK01|315700TWGZ89LLSRS000|315700TXNX10N8XH4K00|315700T2EEQAPBO0C301|315700T6T49EDM16YO01|315700UJ6N4LGKLNPB00|315700UKZXWXEO126601|315700UYFD5GF9R13F01|315700VG7PTE9EJJRX01|315700VITYR7AL4M9S01|315700VMAJZ9JZTXNQ00|315700WH3YMKHCVYW201|315700WKCDF4QGRRO200|315700WR4IHOO1M5LP00|315700WYOZ6994UATN00|315700WZPEIS41QDKE00|315700XEFYMA5EZ0P500|315700XE21UYOA3GAC01|315700XI4Z8GF5BDUJ01|315700XSCP1S8WOD8E01|315700X40GNCOUWJYR00|315700YS6RQ5TF3VBP01|315700Y1W7W1JHAUBW00|315700Y5JNQMMUF5ID01|3157000VAJWZ3P8ZED00|3157001KM8GOU7PXZY01|3157001K2LAL04D87901|3157001MLDD3SDFQA901|3157001TPR6K4GBTLN00|31570010000000006400|31570010000000009601|31570010000000019301|31570010000000025800|31570010000000029001|31570010000000035500|31570010000000038701|31570010000000045200|31570010000000048401|31570010000000054900|31570010000000064600|31570010000000067801|31570010000000077501|31570010000000084000|31570010000000087201|31570010000000096901|31570010000000103400|31570010000000106601|31570010000000116301|31570010000000122800|31570010000000126001|3157002CKDQOCIHE5H01|31570020000000005900|31570029808HJVCNFA01|3157003FQSSGS9OZ9E01|3157004PTVTDOKB46401|3157004R6CH6C1P4KX00|3157005RUI28M8FANK00|3157005VJE7A3MBUS201|3157005WT1SENAE17R00|31570058O0Z320C4GZ00|3157006B6JVZ5DFMSN00|3157006DE3SPNIUY9K01|3157006FR3JBBOLOMX01|3157006I3B6RSTPQLI00|3157006KT1EZ15OIXW00|315700659AALVVLVIO01|31570067WSCDST0S3F01|3157008VKYORMUNC5O01|3157008ZY7CW6LVU5J00|3157009FTHFDDK7FHW01|3157009OVCV07O4HXM00|315700T8U7IU4W8J3A01|315700BBRQHDWX6SHZ00|3157008KD17KROO7UT01)$")

def checkLei(lei: str) -> int:
    if validInvalidLeiPattern.match(lei):
        return LEI_VALID
    if not leiLexicalPattern.match(lei):
        return LEI_INVALID_LEXICAL
    if not int(
        "".join({"0":"0", "1":"1", "2":"2", "3":"3", "4":"4", "5":"5", "6":"6", "7":"7", "8":"8", "9":"9",
                 "A":"10", "B":"11", "C":"12", "D":"13", "E":"14", "F":"15", "G":"16", "H":"17", "I":"18",
                 "J":"19", "K":"20", "L":"21", "M":"22", "N":"23", "O":"24", "P":"25", "Q":"26", "R":"27",
                 "S":"28", "T":"29", "U":"30", "V":"31", "W":"32", "X":"33", "Y":"34", "Z":"35"
                 }[c] for c in lei)
               ) % 97 == 1:
        return LEI_INVALID_CHECKSUM
    return LEI_VALID

if __name__ == "__main__":
    # test cases
    for lei, name in (
                        ("001GPB6A9XPE8XJICC14", "Fidelity Advisor Series I"),
                        ("004L5FPTUREIWK9T2N63", "Hutchin Hill Capital, LP"),
                        ("00EHHQ2ZHDCFXJCPCL46", "Vanguard Russell 1000 Growth Index Trust"),
                        ("00GBW0Z2GYIER7DHDS71", "Aristeia Capital, L.L.C."),
                        ("1S619D6B3ZQIH6MS6B47", "Barclays Vie SA"),
                        ("21380014JAZAUFJRHC43", "BRE/OPERA HOLDINGS"),
                        ("21380016W7GAG26FIJ74", "SOCIETE FRANCAISE ET SUISSE"),
                        ("21380058ERUIT9H53T71", "TOTAN ICAP CO., LTD"),
                        ("213800A9GT65GAES2V60", "BARCLAYS SECURITIES JAPAN LIMITED"),
                        ("213800DELL1MWFDHVN53", "PIRELLI JAPAN"),
                        ("213800A9GT65GAES2V60", "BARCLAYS SECURITIES JAPAN LIMITED"),
                        ("214800A9GT65GAES2V60", "Error 1"),
                        ("213800A9GT65GAE%2V60", "Error 2"),
                        ("213800A9GT65GAES2V62", "Error 3"),
                        ("1234", "Error 4"),
                        ("""
5299003M8JKHEFX58Y02""", "Error 4")
                        ):
            print ("LEI {} result {} name {}".format(lei, LEI_RESULTS[checkLei(lei)], name)  )
