from base64 import b64decode
from pyparsing import (
    Forward,
    Suppress,
    Group,
    Word,
    ParseFatalException,
    Optional,
    OneOrMore,
    ZeroOrMore,
    nums,
    alphanums,
    srange,
    printables,
    dblQuotedString,
    python_style_comment,
    removeQuotes)


def grammar_to_list(grammar: str) -> list:
    # 解析s表达式
    def _bnf_sexp():
        LPAREN, RPAREN, LBRACK, RBRACK = map(Suppress, "()[]")

        base_64_char = alphanums + "+/="
        simple_punc = "-./_:*+="
        token_char = alphanums + simple_punc
        bytes = Word(printables)
        decimal = ("0" | Word(srange("[1-9]"), nums)).setParseAction(lambda t: int(t[0]))

        token = Word(token_char)
        # hexadecimal = "#" + ZeroOrMore(Word(hexnums)) + "#"

        dblQuotedString.setParseAction(removeQuotes)
        quoted_string = Optional(decimal.setResultsName("length")) + \
                        dblQuotedString.setResultsName("data")
        base_64_body = OneOrMore(Word(base_64_char))
        base_64_body.setParseAction(lambda t: b64decode(t[0]).decode('utf-8', 'ignore'))
        base_64 = Optional(decimal.setResultsName("length")) + \
                  "|" + base_64_body.setResultsName("data") + "|"

        raw = (decimal.setResultsName("length") + ":" +
               bytes.setResultsName("data"))
        simple_string = raw | token | base_64 | quoted_string  # | hexadecimal
        display = LBRACK + simple_string + RBRACK
        string_ = Optional(display) + simple_string

        sexp = Forward()
        list_ = Group(LPAREN + ZeroOrMore(sexp) + RPAREN)
        sexp << (string_ | list_)

        def validateDataLength(tokens):
            if tokens.length != "":
                if len(tokens.data) != int(tokens.length):
                    raise ParseFatalException \
                        ("invalid data length, %d specified, found %s (%d chars)" %
                         (int(tokens.length), tokens.data, len(tokens.data)))

        quoted_string.setParseAction(validateDataLength)
        base_64.setParseAction(validateDataLength)
        raw.setParseAction(validateDataLength)

        return sexp

    comment = python_style_comment.suppress()
    grammar = comment.transform_string(grammar)
    grammar_list = _bnf_sexp().parse_string(grammar.strip()).as_list()
    return grammar_list


def _test_1():
    tmp = """
(LINE_SINGLE 
  ( - (SERIE ID059345 (start_date 20180101))
    ( +
     (* 1.65 (/(SERIE ID001473) 0.92))
     (* 0.5(/(SERIE ID026017) 0.93))
     1050) 
     
     (name "热卷加工利润")   
     (unit "吨")
  )
)    
    """
    data = grammar_to_list(tmp)
    print(data)


if __name__ == "__main__":
    _test_1()