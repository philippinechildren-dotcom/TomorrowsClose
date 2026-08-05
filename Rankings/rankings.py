def build_rankings(
    strategy_results,
    rank_by="ulcer_performance_index",
    descending=True,
):
    """
    Rank completed strategy results by any metric.

    Parameters
    ----------
    strategy_results : list

        List of completed strategy dictionaries.

    rank_by : str

        Metric used for sorting.

    descending : bool

        True = highest value first.

    Returns
    -------
    list
    """

    rankings = sorted(

        strategy_results,

        key=lambda result: (

            result["metrics"].get(rank_by)

            if result["metrics"].get(rank_by) is not None

            else float("-inf")

        ),

        reverse=descending,

    )

    for rank, result in enumerate(

        rankings,

        start=1,

    ):

        result["rank"] = rank

    return rankings