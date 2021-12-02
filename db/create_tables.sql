CREATE TABLE Symbol (
    Symbol  VARCHAR(10) PRIMARY KEY
)

CREATE TABLE Price (
    Symbol          VARCHAR(10) REFERENCES Symbol(Symbol),
    Date            Date,
    AdjustedClose   DECIMAL(19,3)
    PRIMARY KEY (Symbol, Date)
)

CREATE TABLE AdditionalData (
    Symbol  VARCHAR(10) REFERENCES Symbol(Symbol),
    [Key]    VARCHAR(255),
    Value   VARCHAR(5000) NOT NULL,
    PRIMARY KEY (Symbol, [Key])
)
