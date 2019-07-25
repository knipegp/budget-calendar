============
You-Are-Poor
============

Sometimes, I make poor financial decisions. You-Are-Poor calculates the burden of these decisions
to mitigate the frequency of expensive impulses. I've tried applications, such as Intuit's Mint, in
the past, but those applications did not provide the granularity in expense management that I
desired.

Notes
=====

TODO: Add user requirements

TODO: Convert program structure to UML

Ideas:

    #.  Should credit accounts track bill payment?

        -   Would probably make future transaction calculation easier.
        -   Currently manually tracked.

Requirements
------------

Accounts
********

Requirements:

    #.  Store the running total
    #.  Store the transactions affecting the total
    #.  Add a transaction to the account

        -   INVARIANT: adjust running total

    #.  Remove a transaction from the account

        -   INVARIANT: adjust running total

    #.  Store the potential future total
    #.  Store the potential future transactions
    #.  Add potential future transaction

        -   INVARIANT: adjust potential future total

    #.  Remove potential future transaction

        -   INVARIANT: adjust potential future total

Members:

    #.  Running total
    #.  Potential future total
    #.  A list of transactions acting on the current total

        -   INVARIANT: relationship between the running total and transactions in the list

    #.  A list of potential future transactions acting on the potential future total

Methods:

    #.  Add transaction
    #.  Remove transaction
    #.  Add potential future transaction
    #.  Remove potential future transaction

Two Types:

    #.  Cumulative
    #.  Credit

Transaction
***********

**Immutable dataclas**

Requirements:

    #.  Store the date
    #.  Store a description
    #.  Store the amount

Members:

    #.  date
    #.  string description
    #.  amount
