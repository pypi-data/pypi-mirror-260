// Copyright (c) 2024, The Endstone Project. (https://endstone.dev) All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#pragma once

#include <ostream>
#include <string>
#include <string_view>

namespace endstone::detail {

class CommandLexer {
public:
    enum class TokenType : uint8_t {
        Number,
        Identifier,
        LeftParen,
        RightParen,
        LeftSquare,
        RightSquare,
        LeftCurly,
        RightCurly,
        LessThan,
        GreaterThan,
        Equal,
        Plus,
        Minus,
        Asterisk,
        Slash,
        Hash,
        Dot,
        Comma,
        Colon,
        Semicolon,
        SingleQuote,
        DoubleQuote,
        Pipe,
        End,
        Unexpected,
    };

    struct Token {
        TokenType type;
        std::string_view value;

        [[nodiscard]] bool is(TokenType t) const
        {
            return type == t;
        }

        bool operator==(const Token &other) const
        {
            return type == other.type && value == other.value;
        }

        friend std::ostream &operator<<(std::ostream &os, const Token &token)
        {
            os << "{ Type: " << static_cast<int>(token.type) << ", Value: " << std::string(token.value) << " }";
            return os;
        }
    };

    explicit CommandLexer(std::string_view value) : value{value} {}
    Token next();

    void reset()
    {
        position = 0;
    }

    [[nodiscard]] char peek() const
    {
        if (position >= value.size()) {
            return '\0';
        }
        return value[position];
    }

    char get()
    {
        if (position >= value.size()) {
            return '\0';
        }
        return value[position++];
    }

    Token next(CommandLexer::TokenType type);
    Token nextIdentifier();
    Token nextNumber();

    static bool isSpace(char c)
    {
        return c == ' ' || c == '\t' || c == '\r' || c == '\n';
    }

    static bool isDigit(char c)
    {
        return c >= '0' && c <= '9';
    }

    static bool isIdentifierCharacter(char c)
    {
        return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || isDigit(c) || c == '_';
    }

    std::string_view value;
    size_t position = 0;
};
}  // namespace endstone::detail
