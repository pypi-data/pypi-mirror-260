""" Unit Curious """


def cubit(n, to: str = "foot"):
    """Calculates the cubit based on forearm length.
    Calculates the conversion of a length measurement into cubits. The default
    output unit is feet, but can be changed using the 'to' parameter.

    Parameters
    ----------
    n : float
        The input value representing the length to be converted into cubits.
    to : str, optional
        The desired output unit for the calculation. Options include:
        "foot" (default), "meter", or "inches".

    Returns
    -------
    float
        The length measurement converted into the specified number of cubits.

    Examples
    --------
    >>> cubit(1.7, to="meter")
    0.9067799999999999

    Raises
    ------
    ValueError
        If the provided 'to' parameter is not one of the supported units.
    """

    if to == "foot":
        return n * 1.50
    elif to == "meter":
        return n * 0.5334
    elif to == "inches":
        return float(n * 1.7716535433071e1)
    elif to not in ["foot", "meter", "inches"]:
        raise ValueError("Invalid unit. Available options: foot, meter, or inches") # noqa


def barleycorn(n, to: str = "foot"):
    """Calculates conversions using the barleycorn, a historical English unit of length.

    Converts a length measurement into barleycorns. The default output unit is feet,
    but can be changed using the 'to' parameter.

    Parameters
    ----------
    n : float
        The input value representing the length to be converted into barleycorns.
    to : str, optional
        The desired output unit for the calculation. Options include:
        "foot" (default), "meter", or "inches".

    Returns
    -------
    float
        The length measurement converted into the specified number of barleycorns.

    Examples
    --------
    >>> barleycorn(3, to="meter")
    0.0833334

    Raises
    ------
    ValueError
        If the provided 'to' parameter is not one of the supported units.
    """ # noqa

    if to == "foot":
        return n * 0.0277778
    elif to == "meter":
        return n * 0.00846667344
    elif to == "inches":
        return n * 0.33333359999999984113
    elif to not in ["foot", "meter", "inches"]:
        raise ValueError("Invalid unit. Available options: foot, meter, or inches") # noqa


def smoot(n, to: str = "foot"):
    """Calculates lengths in smoots, a whimsical unit based on an MIT fraternity prank.

    Converts a length measurement into smoots. The default output unit is feet,
    but can be changed using the 'to' parameter.

    Parameters
    ----------
    n : float
        The input value representing the length to be converted into smoots.
    to : str, optional
        The desired output unit for the calculation. Options include:
        "foot" (default), "meter", or "inches".

    Returns
    -------
    float
        The length measurement converted into the specified number of smoots.

    Examples
    --------
    >>> smoot(1, to="inches")
    67.0
    """ # noqa

    if to == "foot":
        return n * 5.58333
    elif to == "meter":
        return n * 1.7018
    elif to == "inches":
        return float(n * 67)
    elif to not in ["foot", "meter", "inches"]:
        raise ValueError("Invalid unit. Available options: foot, meter, or inches") # noqa


def stone(n, to: str = "Kilogram"):
    """Calculates weight conversions using the stone, a British unit of mass.

    Converts a weight measurement into stones. The default output unit is kilograms,
    but can be changed using the 'to' parameter.

    Parameters
    ----------
    n : float
        The input value representing the weight to be converted into stones.
    to : str, optional
        The desired output unit for the calculation. Options include:
        "kilogram" (default), "pound", "gram", or "ounce".

    Returns
    -------
    float
        The weight measurement converted into the specified number of stones.

    Examples
    --------
    >>> stone(15, to="Ounces")
    3360

    """ # noqa

    if to == "Kilogram":
        return n * 6.35029
    elif to == "Pound":
        return n * 14
    elif to == "Gram":
        return n * 6350.29
    elif to == "Ounces":
        return n * 224
    elif to not in ["Kilogram", "Pound", "Gram", "Ounces"]:
        raise ValueError(
            "Invalid unit. Available options: Kilogram, Pound, Gram, or Ounces"
        )
