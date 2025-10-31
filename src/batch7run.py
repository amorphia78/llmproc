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
        individual_output_base_path="../coding_batches/batch7/batch7_individual_articles",
        human_coding_database_file="../coding_batches/batch7/batch7_human_coding.tsv",
        output_articles_individually=True,
        coding_output_filename="../coding_batches/batch7/batch7_quota_screening.tsv",
        html_output_filename="../coding_batches/batch7/batch7all.html",
        compilation_format="side-by-side",
        compilation_output_filename="../coding_batches/batch7/batch7_side_by_side.html",
        compilation_inclusion_criterion="passes_screening_specific",
        date_range_type="final",
        human_coding=True,
        check_human_coding="no",
    )

