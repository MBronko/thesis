from sqlparse.sql import Identifier, TokenList, Values, Parenthesis, IdentifierList, Token


def get_identifier_name(token: Identifier):
    tokens = TokenList(token.tokens)

    token = tokens.token_first()
    name_token = token

    idx = 0
    while token is not None and not isinstance(token, Identifier):
        idx, token = tokens.token_next(idx)

    if token is None:
        return name_token.value, name_token.value

    return name_token.value, token.value


def parse_insert_values(values_token: Values):
    idx, token = values_token.token_next(0)

    result = []

    while token is not None:
        if isinstance(token, Parenthesis):
            identifierlist_token = token.token_first()
            identifierlist_idx = 0

            while identifierlist_token is not None:
                if isinstance(identifierlist_token, IdentifierList):
                    values = []
                    for parenthesis_token in identifierlist_token.tokens:
                        value = parenthesis_token.value

                        match str(parenthesis_token.ttype):
                            case "Token.Punctuation" | "Token.Text.Whitespace":
                                continue
                            case "Token.Literal.String.Single":
                                value = value[1:-1]

                        values.append(value)

                    result.append(values)
                identifierlist_idx, identifierlist_token = token.token_next(identifierlist_idx)

        idx, token = values_token.token_next(idx)

    return result
