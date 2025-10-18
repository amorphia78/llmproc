#This wouldn't actually run because you'd need an anthropic key specified
#This was run again a second time but with output_only_articles_passing_screening=True

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

# Uses articles now hard-coded instead of randomly selected (see below for original random selection)
# Also, outputting non-summarised HTML
if __name__ == "__main__":
    multitool.process_articles(
        key = anthropic_key,
        articles_path="../../new_article_content/",
        count_type="any",
        stop_after=999999,  # Process all articles
        article_selection="random",
        article_order_random_seed=7,
        source_quotas=real_quotas,
        quota_pad=0.2,
        use_owe_focussed=False,
        use_owe_specific=True,
        do_screening=True,
        do_coding=False,
        do_summarising=False,
        output_article_full=False,
        output_article_summarised=False,
        output_only_articles_passing_screening=False,
        output_articles_individually=False,
        coding_output_filename="quota_screening.tsv",
        html_output_filename="test_parse.html",
        date_range_type="final"
    )

