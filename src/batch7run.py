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
    "BBC": 2,
    "The-Guardian": 1,
    "Daily-Mail": 1,
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
        check_summary=True,
        very_short_summary=False,
        do_summary_corrections=True,
        corrections_instructions_file="../coding_batches/batch7/batch7_corrections_instructions.tsv",
        output_article_full=True,
        output_article_summarised=True,
        individual_output_base_path="../coding_batches/batch7/batch7_individual_articles",
        human_coding_database_file="../coding_batches/batch7/batch7_human_coding.tsv",
        output_articles_individually=True,
        coding_output_filename="../coding_batches/batch7/batch7_quota_screening_summarising.tsv",
        html_output_filename="../coding_batches/batch7/batch7all.html",
        compilation_format="side-by-side",
        compilation_output_filename="../coding_batches/batch7/batch7_side_by_side.html",
        compilation_inclusion_criterion="passes_screening_specific",
        date_range_type="final",
        human_coding=True,
        check_human_coding="no",
        make_text_descriptions_for_images=True
    )

def dont_run():
    import llmproc_core as llm
    image_url = "https://ichef.bbci.co.uk/news/1536/cpsprodpb/3a81/live/863d06a0-d4cb-11ee-9614-4f148ae4c766.jpg.webp"
    llm.describe_image_from_url(image_url, "Please describe this image in detail.")
    llm.describe_image_from_url(image_url, "Please describe this image in detail in at most 100 words.")
    llm.describe_image_from_url(image_url, "Please describe this image in detail in at most 50 words.")
    llm.describe_image_from_url(image_url, "Please describe this image in detail in roughly 20 words.")

    image_url = "https://ichef.bbci.co.uk/news/1536/cpsprodpb/fa58/live/ab688f30-d4cb-11ee-9614-4f148ae4c766.jpg.webp"
    llm.describe_image_from_url(image_url, "Please describe this image in detail.")
    llm.describe_image_from_url(image_url, "Please describe this image in detail in at most 100 words.")
    llm.describe_image_from_url(image_url, "Please describe this image in detail in at most 50 words.")
    llm.describe_image_from_url(image_url, "Please describe this image in detail in roughly 20 words.")

    image_url = "https://www.thetimes.com/imageserver/image/%2Fmethode%2Ftimes%2Fprod%2Fweb%2Fbin%2Fa0ff0276-f0a1-413b-950d-477bcbf051fc.jpg?crop=1049%2C590%2C227%2C130&resize=1500"
    llm.describe_image_from_url(image_url, "Please describe this image in detail.")
    llm.describe_image_from_url(image_url, "Please describe this image in detail in at most 100 words.")
    llm.describe_image_from_url(image_url, "Please describe this image in detail in at most 50 words.")
    llm.describe_image_from_url(image_url, "Please describe this image in detail in roughly 20 words.")

    image_url = "https://www.thetimes.com/imageserver/image/%2Fmethode%2Ftimes%2Fprod%2Fweb%2Fbin%2Faa0dd352-5da6-4657-ad4a-e1d667c9cab6.jpg?crop=5000%2C3333%2C0%2C0"
    llm.describe_image_from_url(image_url, "Please describe this image in detail.")
    llm.describe_image_from_url(image_url, "Please describe this image in detail in at most 100 words.")
    llm.describe_image_from_url(image_url, "Please describe this image in detail in at most 50 words.")
    llm.describe_image_from_url(image_url, "Please describe this image in detail in roughly 20 words.")

    image_url = "https://www.thetimes.com/imageserver/image/%2Fmethode%2Ftimes%2Fprod%2Fweb%2Fbin%2Fcc4fbeac-d161-4f62-a7b7-98888e9e0dca.jpg?crop=999%2C562%2C12%2C0"
    llm.describe_image_from_url(image_url, "Please describe this image in detail.")
    llm.describe_image_from_url(image_url, "Please describe this image in detail in at most 100 words.")
    llm.describe_image_from_url(image_url, "Please describe this image in detail in at most 50 words.")
    llm.describe_image_from_url(image_url, "Please describe this image in detail in roughly 20 words.")
