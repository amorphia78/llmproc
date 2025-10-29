import llm_activism_article_multitool as multitool

with open('anthropic_key.txt', 'r') as f:
    anthropic_key = f.read().strip()

real_quotas = {
    "BBC": 32,
    "The-Guardian": 13,
    "Daily-Mail": 13,
    "Sky": 10,
    "Metro": 6,
    "Sun": 6,
    "Telegraph": 6,
    "The-Times": 6,
    "Mirror": 5,
    "ITV": 3
}

test_quotas = {
    "BBC": 1,
    "The-Guardian": 1,
    "Daily-Mail": 0,
    "Sky": 0,
    "Metro": 0,
    "Sun": 0,
    "Telegraph": 0,
    "The-Times": 0,
    "Mirror": 0,
    "ITV": 0
}

multitool.process_articles(
        key = anthropic_key,
        articles_path="../../disruption/content_scraping/article_contents",
        count_type="any",
        stop_after=999999,
        article_selection="random",
        article_order_random_seed=7,
        source_quotas=real_quotas,
        quota_pad=0,
        get_owe_focussed_llm_coding=True,
        use_owe_focussed=True,
        use_owe_specific=True,
        do_screening=True,
        do_coding=False,
        do_summarising=True,
        very_short_summary=False,
        output_article_full=True,
        output_article_summarised=True,
        output_only_articles_passing_screening=False,
        output_only_articles_passing_screening_specific=True,
        output_articles_individually=True,
        coding_output_filename="batch7_quota_screening_focussed_screening.tsv",
        html_output_filename="batch7all_test.html",
        compilation_format="side-by-side",
        side_by_side_output_filename="batch7_side_by_side.html",
        date_range_type="final",
        human_coding=True,
        check_human_coding="no",
    )

